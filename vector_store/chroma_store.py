import os
import chromadb
from openai import OpenAI
from config import CHROMA_PATH, COLLECTION_NAME

client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

def embed_text(text: str):
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def url_exists(url: str) -> bool:
    collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    results = collection.get(where={"url": url}, include=[])
    return len(results["ids"]) > 0


def content_hash_exists(content_hash: str) -> bool:
    collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    results = collection.get(where={"content_hash": content_hash}, include=[])
    return len(results["ids"]) > 0
