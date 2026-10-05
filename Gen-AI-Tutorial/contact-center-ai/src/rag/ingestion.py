"""
Document Ingestion Pipeline for Contact-Center AI

This module handles:
1. Loading documents from various sources (PDF, TXT, JSON)
2. Parsing and metadata extraction
3. Chunking with multiple strategies
4. Storing chunks with metadata

KEY CONCEPTS FOR INTERVIEW:
- Chunking strategy affects retrieval quality
- Metadata (source, section, date) enables filtering and citations
- Chunk overlap prevents context loss at boundaries
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
from datetime import datetime


@dataclass
class Chunk:
    """Represents a document chunk with metadata."""
    content: str
    metadata: Dict[str, Any]
    chunk_id: str
    source: str
    section: Optional[str] = None
    position: Optional[int] = None  # Position in original document


class ChunkingStrategy(Enum):
    """Chunking strategies and when to use each."""
    FIXED_SIZE = "fixed"  # Naive but deterministic
    RECURSIVE = "recursive"  # Smart default, preserves context
    SEMANTIC = "semantic"  # Requires embedding model, best quality


class DocumentIngestionPipeline:
    """
    Handles document loading, parsing, and chunking.
    
    Interview Question: "Why recursive chunking over fixed-size?"
    Answer: Recursive chunking splits on logical boundaries (paragraphs, sentences)
    before falling back to fixed size. This preserves context better, improving
    retrieval precision by ~15-20% in empirical tests.
    """
    
    def __init__(self, chunk_size: int = 1024, chunk_overlap: int = 128, strategy: str = "recursive"):
        """
        Args:
            chunk_size: Target chunk size in tokens (approximate)
            chunk_overlap: Overlap between chunks to preserve context
            strategy: Chunking strategy ("fixed", "recursive", "semantic")
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = ChunkingStrategy(strategy)
        self.chunks: List[Chunk] = []
    
    def load_documents(self, doc_path: str) -> List[Dict[str, Any]]:
        """
        Load documents from a file or directory.
        
        Supported formats: .txt, .json, .md
        
        Args:
            doc_path: Path to document file or directory
            
        Returns:
            List of document dicts with 'content' and 'metadata'
        """
        documents = []
        path = Path(doc_path)
        
        if path.is_file():
            doc = self._load_single_file(path)
            if doc:
                documents.append(doc)
        elif path.is_dir():
            for file_path in path.rglob("*.txt"):
                doc = self._load_single_file(file_path)
                if doc:
                    documents.append(doc)
            for file_path in path.rglob("*.md"):
                doc = self._load_single_file(file_path)
                if doc:
                    documents.append(doc)
        
        return documents
    
    def _load_single_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load a single document file."""
        try:
            if file_path.suffix == ".txt" or file_path.suffix == ".md":
                content = file_path.read_text(encoding="utf-8")
                return {
                    "content": content,
                    "metadata": {
                        "source": str(file_path),
                        "file_name": file_path.name,
                        "timestamp": datetime.now().isoformat()
                    }
                }
            elif file_path.suffix == ".json":
                data = json.loads(file_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    # Array of documents
                    return data
                else:
                    # Single document
                    return data
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
        return None
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Chunk]:
        """
        Apply chunking strategy to documents.
        
        INTERVIEW PREP:
        Strategy Selection:
        - FIXED: Simple, deterministic, but may cut mid-sentence
        - RECURSIVE: Smart, preserves paragraphs/sentences, best for general docs
        - SEMANTIC: Requires embeddings upfront, slowest, best for heterogeneous content
        
        Impact on Retrieval:
        Good chunks → tighter retrieval candidates → better reranking → accurate answers
        Bad chunks → noise → reranker struggles → hallucinations or misses
        """
        all_chunks = []
        
        for doc_idx, doc in enumerate(documents):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            if self.strategy == ChunkingStrategy.FIXED_SIZE:
                chunks = self._chunk_fixed_size(content, metadata, doc_idx)
            elif self.strategy == ChunkingStrategy.RECURSIVE:
                chunks = self._chunk_recursive(content, metadata, doc_idx)
            elif self.strategy == ChunkingStrategy.SEMANTIC:
                # For now, fall back to recursive; semantic needs embedding model
                chunks = self._chunk_recursive(content, metadata, doc_idx)
            
            all_chunks.extend(chunks)
        
        self.chunks = all_chunks
        return all_chunks
    
    def _chunk_fixed_size(self, content: str, metadata: Dict, doc_idx: int) -> List[Chunk]:
        """
        Split into fixed-size chunks (naive approach).
        
        PROS: Simple, fast, deterministic
        CONS: May cut mid-sentence, loses context
        USE WHEN: Speed matters more than quality (e.g., preprocessing large corpora)
        """
        # Approximate: split by words, ~4 chars per token average
        words = content.split()
        chunk_size_words = self.chunk_size // 4
        overlap_words = self.chunk_overlap // 4
        
        chunks_list = []
        for i in range(0, len(words), chunk_size_words - overlap_words):
            chunk_words = words[i:i + chunk_size_words]
            if chunk_words:  # Skip empty chunks
                chunk_text = " ".join(chunk_words)
                chunk = Chunk(
                    content=chunk_text,
                    metadata={**metadata, "chunk_strategy": "fixed_size"},
                    chunk_id=f"{doc_idx}_{len(chunks_list)}",
                    source=metadata.get("source", "unknown"),
                    position=i
                )
                chunks_list.append(chunk)
        
        return chunks_list
    
    def _chunk_recursive(self, content: str, metadata: Dict, doc_idx: int) -> List[Chunk]:
        """
        Recursive chunking: split by paragraph, then sentence, then fixed size.
        
        PROS: Preserves context, respects document structure
        CONS: Chunks may vary in size
        USE WHEN: Most general use cases (docs, wikis, FAQs)
        
        RECOMMENDED FOR CONTACT-CENTER because:
        - Support docs have clear structure (sections, FAQs)
        - Preserves coherence of troubleshooting steps
        - Improves reranker confidence
        """
        # Step 1: Split by double newline (paragraph boundary)
        paragraphs = content.split("\n\n")
        
        chunks_list = []
        char_position = 0
        chunk_counter = 0
        
        for para_idx, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                char_position += len(paragraph) + 2
                continue
            
            # Step 2: If paragraph is too long, split by sentence
            sentences = paragraph.split(". ")
            current_chunk = ""
            
            for sent_idx, sentence in enumerate(sentences):
                if not sentence.endswith("."):
                    sentence += "."
                
                # Check if adding this sentence exceeds chunk_size
                test_chunk = current_chunk + " " + sentence if current_chunk else sentence
                test_tokens = len(test_chunk.split())
                
                if test_tokens > self.chunk_size and current_chunk:
                    # Save current chunk
                    chunk = Chunk(
                        content=current_chunk.strip(),
                        metadata={
                            **metadata,
                            "chunk_strategy": "recursive",
                            "paragraph": para_idx,
                            "sentence": sent_idx
                        },
                        chunk_id=f"{doc_idx}_{chunk_counter}",
                        source=metadata.get("source", "unknown"),
                        position=char_position
                    )
                    chunks_list.append(chunk)
                    chunk_counter += 1
                    
                    # Start new chunk with overlap
                    overlap_sentences = current_chunk.split(". ")[-1:]  # Keep last sentence for overlap
                    current_chunk = " ".join(overlap_sentences) + " " + sentence
                    char_position += len(current_chunk)
                else:
                    if current_chunk:
                        current_chunk += " " + sentence
                    else:
                        current_chunk = sentence
            
            # Add final chunk for this paragraph
            if current_chunk.strip():
                chunk = Chunk(
                    content=current_chunk.strip(),
                    metadata={
                        **metadata,
                        "chunk_strategy": "recursive",
                        "paragraph": para_idx,
                        "sentence": -1
                    },
                    chunk_id=f"{doc_idx}_{chunk_counter}",
                    source=metadata.get("source", "unknown"),
                    position=char_position
                )
                chunks_list.append(chunk)
                chunk_counter += 1
            
            char_position += len(paragraph) + 2
        
        return chunks_list
    
    def export_chunks_jsonl(self, output_path: str) -> None:
        """
        Export chunks to JSONL format for indexing.
        
        Format: One JSON per line
        {
            "chunk_id": "...",
            "content": "...",
            "metadata": {...},
            "source": "..."
        }
        """
        with open(output_path, "w") as f:
            for chunk in self.chunks:
                record = {
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "metadata": chunk.metadata,
                    "source": chunk.source,
                    "section": chunk.section,
                    "position": chunk.position
                }
                f.write(json.dumps(record) + "\n")
        
        print(f"Exported {len(self.chunks)} chunks to {output_path}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Return ingestion statistics for debugging."""
        if not self.chunks:
            return {"total_chunks": 0}
        
        total_chars = sum(len(c.content) for c in self.chunks)
        avg_chunk_size = total_chars / len(self.chunks) if self.chunks else 0
        
        return {
            "total_chunks": len(self.chunks),
            "total_chars": total_chars,
            "avg_chunk_size": avg_chunk_size,
            "chunk_strategy": self.strategy.value,
            "chunk_size_config": self.chunk_size,
            "chunk_overlap_config": self.chunk_overlap
        }


# Example usage
if __name__ == "__main__":
    # Initialize pipeline with recursive chunking (recommended)
    pipeline = DocumentIngestionPipeline(
        chunk_size=1024,
        chunk_overlap=128,
        strategy="recursive"
    )
    
    # Example: Load and chunk a sample doc
    sample_doc = {
        "content": """
        How to reset your network.
        
        Network issues can be frustrating. Here are the steps to reset your network connection.
        
        Step 1: Restart your router.
        Turn off your router for 30 seconds. Then turn it back on.
        
        Step 2: Check your cables.
        Ensure all cables are connected properly. Look for loose connections.
        
        Step 3: Run network diagnostics.
        On your device, open Settings > Network > Diagnostics. This will help identify issues.
        """,
        "metadata": {
            "source": "docs/network_troubleshooting.txt",
            "category": "support",
            "intent": "Network Issue"
        }
    }
    
    chunks = pipeline.chunk_documents([sample_doc])
    print(f"\nChunking Results:")
    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} ---")
        print(f"Content: {chunk.content[:100]}...")
        print(f"Metadata: {chunk.metadata}")
