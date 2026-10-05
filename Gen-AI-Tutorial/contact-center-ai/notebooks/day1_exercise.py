"""
DAY 1 EXERCISE: Document Ingestion → Embedding → Retrieval

This script walks you through the RAG pipeline foundation:
1. Load documents
2. Chunk with recursive strategy (smart, context-preserving)
3. Embed chunks using OpenAI embeddings
4. Store in vector DB (FAISS for local testing)
5. Run basic similarity search

LEARNING OUTCOMES:
- Understand chunking impact on retrieval quality
- Learn why reranking is critical
- Build intuition for embedding-based search
- See how retrieval errors propagate to hallucination

INTERVIEW PREP:
- "Walk me through your RAG pipeline" → This is your answer
- "Why recursive chunking?" → Because it preserves context at paragraph/sentence boundaries
- "Why do you embed?" → To find semantically similar chunks in vector space
- "What happens if retrieval fails?" → Wrong chunks, LLM hallucinates, confidence drops
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import settings
from rag.ingestion import DocumentIngestionPipeline, Chunk
from rag.embeddings import OpenAIEmbedding, EmbeddingPipeline, HAS_OPENAI

# Try to import FAISS for local vector storage
try:
    import faiss
    import numpy as np
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False
    print("⚠️  FAISS not installed. Install with: pip install faiss-cpu")


class LocalVectorStore:
    """
    Simple local vector store using FAISS.
    
    FAISS = Facebook AI Similarity Search
    - Fast similarity search on CPU
    - No setup required (unlike Pinecone)
    - Good for prototyping and testing
    - Can handle millions of vectors
    
    Why FAISS for experiments:
    - Fast iteration (no cloud latency)
    - No API key management
    - Reproducible (same results every time)
    """
    
    def __init__(self, dimension: int = 1536):
        if not HAS_FAISS:
            raise ImportError("FAISS required. Install with: pip install faiss-cpu")
        
        # Create FAISS index for cosine similarity
        # Dimension must match embedding model output (1536 for OpenAI small)
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance
        self.dimension = dimension
        self.chunks = []
        self.metadata = []
    
    def add_vectors(self, embeddings: List[List[float]], chunks: List[Dict], metadata: List[Dict] = None) -> None:
        """
        Add embeddings and associated chunks to the index.
        
        Args:
            embeddings: List of embedding vectors (each 1536-dim for OpenAI small)
            chunks: List of chunk dicts with content and metadata
            metadata: Optional additional metadata per embedding
        """
        embeddings_array = np.array(embeddings, dtype=np.float32)
        
        # Normalize embeddings for cosine similarity
        # (FAISS L2 distance on normalized vectors = cosine distance)
        faiss.normalize_L2(embeddings_array)
        
        self.index.add(embeddings_array)
        self.chunks.extend(chunks)
        
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{"index": i} for i in range(len(chunks))])
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for most similar chunks.
        
        Args:
            query_embedding: Query embedding vector (1536-dim)
            top_k: Number of results to return
            
        Returns:
            List of (chunk_dict, similarity_score) tuples
        """
        query_array = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_array)
        
        distances, indices = self.index.search(query_array, top_k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx >= 0:  # Valid index
                # Convert L2 distance to similarity score (lower distance = higher similarity)
                similarity = 1.0 / (1.0 + distance)
                results.append((self.chunks[int(idx)], similarity))
        
        return results


def exercise_1_load_documents():
    """
    EXERCISE 1: Load documents from disk.
    
    Demonstrates:
    - Flexible document loading
    - Metadata extraction
    - Support for multiple formats
    """
    print("\n" + "="*70)
    print("EXERCISE 1: Load Documents")
    print("="*70)
    
    doc_path = Path(__file__).parent / "data" / "docs"
    pipeline = DocumentIngestionPipeline()
    
    documents = pipeline.load_documents(str(doc_path))
    
    print(f"\n✓ Loaded {len(documents)} documents from {doc_path}")
    for i, doc in enumerate(documents):
        content_preview = doc["content"][:100].replace("\n", " ")
        print(f"  [{i}] {doc['metadata'].get('file_name', 'unknown')} ({len(doc['content'])} chars)")
    
    return documents


def exercise_2_chunk_documents(documents: List[Dict], strategy: str = "recursive"):
    """
    EXERCISE 2: Chunk documents with different strategies.
    
    KEY INSIGHT:
    - FIXED: Fast but may break mid-sentence → retrieval noise
    - RECURSIVE: Smart, respects structure → better precision
    - SEMANTIC: Requires embeddings, slowest → best quality
    
    For Contact-Center: RECURSIVE is sweet spot (fast + good quality)
    """
    print("\n" + "="*70)
    print(f"EXERCISE 2: Chunk Documents ({strategy} strategy)")
    print("="*70)
    
    pipeline = DocumentIngestionPipeline(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        strategy=strategy
    )
    
    chunks = pipeline.chunk_documents(documents)
    stats = pipeline.get_stats()
    
    print(f"\n✓ Chunking complete:")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Total characters: {stats['total_chars']:,}")
    print(f"  Average chunk size: {stats['avg_chunk_size']:.0f} chars")
    
    # Show sample chunks
    print(f"\nFirst 3 chunks:")
    for i, chunk in enumerate(chunks[:3]):
        source = chunk.metadata.get("file_name", "unknown")
        content = chunk.content[:80].replace("\n", " ")
        print(f"  [{i}] {source}: {content}...")
    
    return chunks


def exercise_3_embed_chunks(chunks: List[Chunk]) -> List[Dict]:
    """
    EXERCISE 3: Embed chunks using OpenAI embeddings.
    
    KEY INSIGHT:
    - Each chunk → 1536-dimensional vector
    - Vectors capture semantic meaning
    - Similarity in vector space ≈ semantic similarity
    
    Cost: $0.02 per 1M tokens (text-embedding-3-small)
    """
    print("\n" + "="*70)
    print("EXERCISE 3: Embed Chunks with OpenAI")
    print("="*70)
    
    if not HAS_OPENAI or not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OpenAI API key not configured!")
        print("   Set OPENAI_API_KEY in .env file")
        return []
    
    # Convert chunks to dicts for embedding pipeline
    chunk_dicts = [
        {
            "content": chunk.content,
            "metadata": chunk.metadata,
            "chunk_id": chunk.chunk_id,
            "source": chunk.source
        }
        for chunk in chunks
    ]
    
    # Initialize embedding model
    embedding_model = OpenAIEmbedding(model=settings.embedding_model)
    pipeline = EmbeddingPipeline(embedding_model)
    
    # Embed all chunks
    print(f"\nEmbedding {len(chunk_dicts)} chunks...")
    embedded_chunks = pipeline.embed_chunks(chunk_dicts, batch_size=50)
    
    # Compute embedding statistics
    embeddings = [chunk["embedding"] for chunk in embedded_chunks]
    stats = pipeline.get_embedding_stats(embeddings)
    
    print(f"\n✓ Embedding complete:")
    print(f"  Total chunks: {stats['count']}")
    print(f"  Embedding dimension: {stats['dimension']}")
    print(f"  Mean norm: {stats['mean_norm']:.3f}")
    print(f"  Std dev: {stats['std_norm']:.3f}")
    print(f"  Sparsity: {stats['sparsity']:.1%}")
    
    return embedded_chunks


def exercise_4_build_vector_store(embedded_chunks: List[Dict]) -> LocalVectorStore:
    """
    EXERCISE 4: Build a local vector store with FAISS.
    
    KEY INSIGHT:
    - Store chunks + embeddings for fast retrieval
    - FAISS enables nearest-neighbor search in O(log n) time
    - In production: Pinecone for scalability
    """
    print("\n" + "="*70)
    print("EXERCISE 4: Build Local Vector Store (FAISS)")
    print("="*70)
    
    if not HAS_FAISS:
        print("\n⚠️  FAISS not available. Skipping vector store.")
        return None
    
    embeddings = [chunk["embedding"] for chunk in embedded_chunks]
    
    vector_store = LocalVectorStore(dimension=len(embeddings[0]))
    vector_store.add_vectors(embeddings, embedded_chunks)
    
    print(f"\n✓ Vector store created:")
    print(f"  Indexed vectors: {vector_store.index.ntotal}")
    print(f"  Dimension: {vector_store.dimension}")
    print(f"  Ready for search!")
    
    return vector_store


def exercise_5_retrieval_and_ranking(
    vector_store: LocalVectorStore,
    embedding_model: OpenAIEmbedding,
    pipeline: EmbeddingPipeline
) -> None:
    """
    EXERCISE 5: Run retrieval queries and observe ranking.
    
    INTERVIEW SCENARIO:
    Q: "A customer asks: 'How do I check my balance?'"
    A: "I embed the query → search vector DB → get top-50 candidates
       → rerank with BGE cross-encoder → return top-5 with confidence"
    
    This exercise runs steps 1-3. Reranking comes in Day 2.
    """
    print("\n" + "="*70)
    print("EXERCISE 5: Similarity Search & Retrieval")
    print("="*70)
    
    # Sample queries representing our 5 intents
    queries = [
        "How do I check my account details?",
        "What's my remaining data balance?",
        "Network is not working, how to troubleshoot?",
        "How to pay my bill online?",
        "Do you have FAQs about common issues?"
    ]
    
    for query in queries:
        print(f"\n📍 Query: \"{query}\"")
        
        # Step 1: Embed the query
        query_embedding = embedding_model.embed([query])[0]
        
        # Step 2: Search in vector store
        results = vector_store.search(query_embedding, top_k=5)
        
        # Step 3: Show results with rankings
        print(f"   Top 5 retrieved chunks:")
        for rank, (chunk, similarity) in enumerate(results, 1):
            source = chunk.get("metadata", {}).get("file_name", "unknown")
            content = chunk["content"][:60].replace("\n", " ")
            confidence = "🟢" if similarity > 0.75 else "🟡" if similarity > 0.60 else "🔴"
            print(f"   {rank}. [{confidence} {similarity:.2f}] {source}: {content}...")


def main():
    """Run all Day 1 exercises."""
    print("\n" + "#"*70)
    print("# DAY 1 EXERCISE: RAG FOUNDATION")
    print("# Document Ingestion → Embedding → Retrieval")
    print("#"*70)
    
    # Exercise 1: Load documents
    documents = exercise_1_load_documents()
    
    # Exercise 2: Chunk with recursive strategy
    chunks = exercise_2_chunk_documents(documents, strategy="recursive")
    
    # Exercise 3: Embed chunks
    if HAS_OPENAI and os.getenv("OPENAI_API_KEY"):
        embedded_chunks = exercise_3_embed_chunks(chunks)
        
        # Exercise 4: Build vector store
        if HAS_FAISS and embedded_chunks:
            vector_store = exercise_4_build_vector_store(embedded_chunks)
            
            # Exercise 5: Test retrieval
            embedding_model = OpenAIEmbedding(model=settings.embedding_model)
            pipeline = EmbeddingPipeline(embedding_model)
            
            exercise_5_retrieval_and_ranking(vector_store, embedding_model, pipeline)
            
            # Save results for Day 2
            print("\n" + "="*70)
            print("CHECKPOINT: Ready for Day 2!")
            print("="*70)
            print("\nYou've built:")
            print("✓ Recursive chunking pipeline (context-preserving)")
            print("✓ OpenAI embedding integration (1536 dims)")
            print("✓ FAISS vector store (local similarity search)")
            print("✓ Retrieval and ranking (similarity scores)")
            print("\nNext steps (Day 2):")
            print("- Add BGE reranker (cross-encoder) to refine results")
            print("- Implement hybrid retrieval (vector + BM25 sparse)")
            print("- Build intent router agent")
            print("- Connect MCP tools for actions")
    else:
        print("\n⚠️  Skipping embedding exercises (OpenAI API key required)")
        print("   Set OPENAI_API_KEY=sk-... in .env file")


if __name__ == "__main__":
    main()
