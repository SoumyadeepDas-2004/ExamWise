import chromadb

DB_PATH = "../data/chroma_db"
COLLECTION_NAME = "makaut_cn"

client = chromadb.PersistentClient(path=DB_PATH)

try:
    client.delete_collection(COLLECTION_NAME)
    print("🗑️ Vector DB reset")
except Exception:
    print("🆕 No existing collection")

client.get_or_create_collection(COLLECTION_NAME)
print("✅ Empty collection ready")
