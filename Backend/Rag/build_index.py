# backend/rag/build_index.py
import json
import os
from pathlib import Path
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.document.base import Document
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder


# Define paths relative to this script
CURRENT_DIR = Path(__file__).parent
MENU_JSON_PATH = CURRENT_DIR / "menu.json"
VECTOR_DIR = CURRENT_DIR / "vectorstore"

from dotenv import load_dotenv
load_dotenv(CURRENT_DIR.parent / ".env")

# ensure vectorstore directory exists
os.makedirs(VECTOR_DIR, exist_ok=True)

def load_menu_as_documents():
    """Load menu.json and convert it into Agno Document objects."""
    with open(MENU_JSON_PATH, "r") as f:
        menu = json.load(f)

    docs = []
    for item in menu:
        text = f"""
        Name: {item['name']}
        Category: {item['category']}
        Price: {item['price']}
        Tags: {', '.join(item['tags'])}
        Description: {item['description']}
        """

        docs.append(Document(
            id=item["name"],    # unique ID for vector DB
            content=text
        ))

    return docs


def main():
    # print("📌 Loading menu.json ...")

    # Convert menu items → SimpleDocument list
    documents = load_menu_as_documents()

    # print(f"📚 Loaded {len(documents)} menu items.")

    # Create ChromaDb instance with local embedder
    embedder = SentenceTransformerEmbedder(
        id="sentence-transformers/all-MiniLM-L6-v2",  # Fast, lightweight model
    )
    
    vector_db = ChromaDb(
        collection="restaurant_menu",
        path=str(VECTOR_DIR),
        persistent_client=True,
        embedder=embedder,
    )

    # Create Knowledge Base
    kb = Knowledge(
        vector_db=vector_db,
    )

    print("🧠 Adding documents to VectorStore...")
    vector_db.create()
    vector_db.upsert("menu_v1", documents)

    print("✅ RAG index built successfully!")
    # print("📍 Stored at:", str(VECTOR_DIR))


if __name__ == "__main__":
    main()
