# backend/rag/knowledge_base.py

import chromadb
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder

VECTOR_DIR = "Backend/Rag/vectorstore"

def load_rag_kb():
    """Load the persistent vector store and return KnowledgeBase."""
    
    # Use sentence-transformers for local embeddings (no API key needed)
    embedder = SentenceTransformerEmbedder(
        id="sentence-transformers/all-MiniLM-L6-v2",  # Fast, lightweight model
    )
    
    # Initialize ChromaDb with persistent path
    vector_db = ChromaDb(
        collection="restaurant_menu",
        path=VECTOR_DIR,
        persistent_client=True,
        embedder=embedder,
    )

    kb = Knowledge(
        vector_db=vector_db,
    )

    return kb
