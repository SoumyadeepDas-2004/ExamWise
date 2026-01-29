# import json
# import chromadb
# from sentence_transformers import SentenceTransformer
# from rag_documents import chunk_to_rag_doc

# DB_PATH = "data/makaut/btech/cse/semester/semester_6/computer_networks/chroma_db"
# client = chromadb.PersistentClient(path=DB_PATH)
# COLLECTION_NAME = "makaut_cn"
# collection = client.get_or_create_collection("makaut_cn")

# MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# with open("data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/cleaned/null_removed_merged.json", "r", encoding="utf-8") as f:
#     rows = json.load(f)

# documents, metadatas, ids = [], [], []

# print(f"Processing {len(rows)} rows...")

# for row in rows:
#     doc = chunk_to_rag_doc(row)
#     raw_meta = doc["metadata"]
#     safe_meta = {}

#     for k, v in raw_meta.items():
#         if k in ["year", "marks", "unit_number"]:
#             safe_meta[k] = int(v or 0)

#         elif k == "exam_group":
#             safe_meta[k] = v.upper() if v else "Unknown"

#         elif isinstance(v, list):
#             safe_meta[k] = ", ".join(map(str, v))

#         else:
#             safe_meta[k] = str(v) if v is not None else "Unknown"

#     documents.append(doc["text"])
#     metadatas.append(safe_meta)
#     ids.append(str(doc["id"]))

# print("Generating embeddings...")
# embeddings = MODEL.encode(documents, batch_size=64, show_progress_bar=True).tolist()

# print("Adding to ChromaDB...")
# collection.add(
#     documents=documents,
#     embeddings=embeddings,
#     metadatas=metadatas,
#     ids=ids
# )

# print("✅ Vector store built")
# print("Total docs:", collection.count())
# print(collection.peek(3))
import json
import chromadb
from sentence_transformers import SentenceTransformer
from vectorstore.rag_documents import chunk_to_rag_doc

# -----------------------------
# VECTOR STORE (FROZEN)
# -----------------------------
DB_PATH = "data/makaut/btech/cse/semester/semester_6/computer_networks/chroma_db"
COLLECTION_NAME = "makaut_cn"

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(COLLECTION_NAME)

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# LOAD CLEAN PYQs (NO ANALYTICS)
# -----------------------------
with open(
    "data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/cleaned/null_removed_merged.json",
    "r",
    encoding="utf-8"
) as f:
    rows = json.load(f)

documents, metadatas, ids = [], [], []

ALLOWED_META_KEYS = {
    "unit_number",
    "unit_title",
    "exam_group",
    "marks",
    "year",
    "difficulty"
}

print(f"Processing {len(rows)} rows...")

for row in rows:
    doc = chunk_to_rag_doc(row)
    raw_meta = doc["metadata"]
    safe_meta = {}

    for k, v in raw_meta.items():
        if k not in ALLOWED_META_KEYS:
            continue

        if k in ["year", "marks", "unit_number"]:
            safe_meta[k] = int(v or 0)

        elif k == "exam_group":
            safe_meta[k] = v.upper() if v else "UNKNOWN"

        else:
            safe_meta[k] = str(v) if v is not None else "UNKNOWN"

    # 🔒 EMBED ONLY CLEAN TEXT
    documents.append(row["clean_text"])
    metadatas.append(safe_meta)
    ids.append(str(doc["id"]))

print("Generating embeddings...")
embeddings = MODEL.encode(
    documents,
    batch_size=64,
    show_progress_bar=True
).tolist()

print("Adding to ChromaDB...")
collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print("✅ Vector store built and FROZEN")
print("Total docs:", collection.count())
print(collection.peek(3))

# ⚠️ DO NOT RE-RUN THIS SCRIPT
# Vector store is frozen unless schema changes
