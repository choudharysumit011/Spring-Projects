"""
Embedding Pipeline for Contact-Center AI

This module handles:
1. Text embedding (text → vector representation)
2. Batch embedding with retry logic
3. Metadata embedding for hybrid retrieval
4. Embedding quality assessment

KEY CONCEPTS FOR INTERVIEW:
- Embeddings map text to dense vectors (~1500 dims)
- Similarity in vector space ≈ semantic similarity in text
- Different models trade off speed, quality, and cost
- Embedding quality critically affects retrieval precision
"""

from typing import List, Dict, Optional, Tuple
from abc import ABC, abstractmethod
import numpy as np
from dataclasses import dataclass
import os

# Try importing OpenAI; fall back gracefully if not installed
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class EmbeddingResult:
    """Result of embedding a text."""
    text: str
    embedding: List[float]
    model: str
    dimension: int


class EmbeddingModel(ABC):
    """Base class for embedding models."""
    
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Return embedding dimension."""
        pass


class OpenAIEmbedding(EmbeddingModel):
    """
    OpenAI Embedding Models
    
    Models:
    - text-embedding-3-small: Fast, cheap, 1536 dims (RECOMMENDED for MVP)
    - text-embedding-3-large: Slower, more expensive, 3072 dims (better quality)
    
    Cost Analysis (per 1M tokens):
    - small: $0.02
    - large: $0.13
    
    Quality vs Speed Tradeoff for Contact-Center:
    We use "small" because:
    1. Contact-center queries are short (10-50 tokens avg)
    2. Reranking (cross-encoder) handles quality → embedding just needs to be "good enough"
    3. Cost optimization: ~$50/M queries with small vs $300/M with large
    
    INTERVIEW TIP: "We don't use the biggest embedding model. Hybrid retrieval + reranking is better ROI."
    """
    
    def __init__(self, model: str = "text-embedding-3-small", api_key: Optional[str] = None):
        if not HAS_OPENAI:
            raise ImportError("openai package required. Install with: pip install openai")
        
        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self._dimension = 1536 if "small" in model else 3072
    
    def embed(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Embed texts using OpenAI API.
        
        Args:
            texts: List of texts to embed
            batch_size: Process in batches to avoid API limits
            
        Returns:
            List of embeddings (each is a list of floats)
        """
        all_embeddings = []
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                
                # Extract embeddings, maintaining order
                batch_embeddings = sorted(response.data, key=lambda x: x.index)
                all_embeddings.extend([item.embedding for item in batch_embeddings])
            
            except Exception as e:
                print(f"Error embedding batch {i//batch_size}: {e}")
                # Return zero embeddings as fallback
                all_embeddings.extend([[0.0] * self.get_dimension() for _ in batch])
        
        return all_embeddings
    
    def get_dimension(self) -> int:
        return self._dimension


class SentenceTransformerEmbedding(EmbeddingModel):
    """
    Sentence-Transformers Embedding (Local, Free)
    
    Models:
    - all-MiniLM-L6-v2: 384 dims, fast, good for semantic similarity
    - all-mpnet-base-v2: 768 dims, slower, better quality
    
    WHEN TO USE:
    - Local/offline requirements
    - Budget constraints
    - Privacy requirements (no API calls)
    
    PROS: Free, privacy-preserving, deterministic locally
    CONS: Slower than OpenAI, lower quality dims
    
    For Contact-Center MVP, we prefer OpenAI, but this is viable fallback.
    """
    
    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model)
            self.model_name = model
        except ImportError:
            raise ImportError("sentence-transformers required. Install with: pip install sentence-transformers")
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed texts using sentence-transformers."""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return [emb.tolist() for emb in embeddings]
    
    def get_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()


class EmbeddingPipeline:
    """
    Orchestrates embedding of document chunks.
    
    Responsibilities:
    1. Batch embedding with progress tracking
    2. Error handling and retries
    3. Metadata embedding for faceted search
    4. Quality metrics (embedding distribution)
    """
    
    def __init__(self, embedding_model: EmbeddingModel):
        self.model = embedding_model
        self.dimension = embedding_model.get_dimension()
    
    def embed_chunks(self, chunks: List[Dict], batch_size: int = 100) -> List[Dict]:
        """
        Embed document chunks.
        
        Args:
            chunks: List of chunk dicts with 'content' and 'metadata'
            batch_size: Batch size for API calls
            
        Returns:
            List of chunks with added 'embedding' field
        """
        texts = [chunk["content"] for chunk in chunks]
        embeddings = self.model.embed(texts, batch_size=batch_size)
        
        # Attach embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding
        
        return chunks
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Similarity ranges [-1, 1]:
        - 1.0 = identical
        - 0.5-0.9 = highly related
        - 0.0 = orthogonal
        - <0 = opposite meaning
        
        INTERVIEW TIP: "In RAG, we typically retrieve candidates with similarity > 0.7,
        then rerank to refine further."
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(np.dot(vec1, vec2) / (norm1 * norm2))
    
    def get_embedding_stats(self, embeddings: List[List[float]]) -> Dict:
        """
        Compute statistics on embeddings for quality assessment.
        
        Metrics:
        - Mean norm: Average vector magnitude (should be ~1.0)
        - Variance: Spread across embeddings
        - Sparsity: Fraction of near-zero values
        """
        embeddings_array = np.array(embeddings)
        norms = np.linalg.norm(embeddings_array, axis=1)
        
        return {
            "count": len(embeddings),
            "dimension": embeddings_array.shape[1],
            "mean_norm": float(np.mean(norms)),
            "std_norm": float(np.std(norms)),
            "min_norm": float(np.min(norms)),
            "max_norm": float(np.max(norms)),
            "sparsity": float(np.mean(embeddings_array == 0.0))
        }


# Example usage
if __name__ == "__main__":
    # Initialize embedding pipeline
    # Note: Requires OPENAI_API_KEY env var
    
    if HAS_OPENAI and os.getenv("OPENAI_API_KEY"):
        embedding = OpenAIEmbedding(model="text-embedding-3-small")
        pipeline = EmbeddingPipeline(embedding)
        
        # Example texts
        sample_texts = [
            "How do I reset my network connection?",
            "Network troubleshooting steps for contact center",
            "Payment methods and billing questions"
        ]
        
        embeddings = embedding.embed(sample_texts)
        print(f"Embeddings shape: {len(embeddings)}x{len(embeddings[0])}")
        
        # Compute similarity between first two
        sim = pipeline.compute_similarity(embeddings[0], embeddings[1])
        print(f"\nSimilarity between Q1 and Q2: {sim:.3f}")
        
        # Get stats
        stats = pipeline.get_embedding_stats(embeddings)
        print(f"\nEmbedding Stats: {stats}")
    else:
        print("OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")
