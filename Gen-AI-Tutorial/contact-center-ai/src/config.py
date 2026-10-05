"""
Config Management for Contact-Center AI

This module centrally manages environment variables, API keys, and system settings.
Using Pydantic BaseSettings ensures type safety and validation.
"""

import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

class Settings(BaseSettings):
    """Central configuration for the contact-center-ai system."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    
    # Embedding Configuration
    embedding_model: str = Field(default="text-embedding-3-small", env="EMBEDDING_MODEL")
    embedding_dim: int = 1536  # text-embedding-3-small outputs 1536 dims
    
    # Reranker Configuration
    reranker_model: str = Field(default="BAAI/bge-reranker-large", env="RERANKER_MODEL")
    
    # Pinecone Configuration
    pinecone_api_key: str = Field(default="", env="PINECONE_API_KEY")
    pinecone_index_name: str = Field(default="contact-center-docs", env="PINECONE_INDEX_NAME")
    pinecone_environment: str = Field(default="gcp-starter", env="PINECONE_ENVIRONMENT")
    
    # MongoDB Configuration
    mongodb_uri: str = Field(..., env="MONGODB_URI")
    mongodb_db_name: str = Field(default="contact_center", env="MONGODB_DB_NAME")
    
    # Chunking Strategy Configuration
    chunk_strategy: str = Field(default="recursive", env="CHUNK_STRATEGY")  # Options: "fixed", "recursive", "semantic"
    chunk_size: int = Field(default=1024, env="CHUNK_SIZE")  # tokens
    chunk_overlap: int = Field(default=128, env="CHUNK_OVERLAP")  # tokens
    
    # Retrieval Configuration
    retrieval_mode: str = Field(default="hybrid", env="RETRIEVAL_MODE")  # Options: "similarity", "mmr", "hybrid"
    retrieval_top_k: int = Field(default=50, env="RETRIEVAL_TOP_K")  # Before reranking
    rerank_top_k: int = Field(default=5, env="RERANK_TOP_K")  # After reranking
    
    # LangSmith (optional, for debugging)
    langsmith_api_key: str = Field(default="", env="LANGSMITH_API_KEY")
    langsmith_project: str = Field(default="contact-center-ai", env="LANGSMITH_PROJECT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global config instance
settings = Settings()


if __name__ == "__main__":
    print("Contact-Center AI Configuration:")
    print(f"  LLM: {settings.openai_model}")
    print(f"  Embedding Model: {settings.embedding_model}")
    print(f"  Chunking Strategy: {settings.chunk_strategy}")
    print(f"  Chunk Size: {settings.chunk_size} tokens")
    print(f"  Retrieval Mode: {settings.retrieval_mode}")
    print(f"  Rerank Top-K: {settings.rerank_top_k}")
