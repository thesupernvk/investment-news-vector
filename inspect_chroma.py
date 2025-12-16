import chromadb
from config import CHROMA_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_collection(COLLECTION_NAME)

print("Total vectors:", collection.count())

data = collection.get(include=["documents", "metadatas"])

for i in range(min(3, len(data["documents"]))):
    print("\n---")
    print("Document (chunk):")
    print(data["documents"][i][:500], "...")
    print("Metadata:")
    print(data["metadatas"][i])
