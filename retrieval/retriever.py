from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Tuple
from intelligence.embedding_model import get_embedding_model
# -------------------------------------------------
# VECTOR STORE (FROZEN)
# -------------------------------------------------
DB_PATH = (
    "data/makaut/btech/cse/semester/semester_6/"
    "computer_networks/chroma_db"
)

COLLECTION_NAME = "makaut_cn"

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

MODEL = get_embedding_model()

# -------------------------------------------------
# RETRIEVER (STRICT)
# -------------------------------------------------
def retrieve(
    query: str,
    unit_number: int | None = None,
    exam_group: str | None = None,
    top_k: int = 5
) -> Tuple[List[str], List[dict]]:
    """
    Returns:
        documents, metadatas

    IMPORTANT:
    - May return empty lists
    - Caller MUST enforce refusal if empty
    """

    query_embedding = MODEL.encode(query).tolist()

    # Build active filters
    active_filters = {}

    if unit_number is not None:
        active_filters["unit_number"] = unit_number

    if exam_group is not None:
        active_filters["exam_group"] = exam_group.upper()

    # Convert to ChromaDB where clause
    if len(active_filters) > 1:
        where_clause = {
            "$and": [{k: v} for k, v in active_filters.items()]
        }
    else:
        where_clause = active_filters or None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_clause
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return documents, metadatas


# -------------------------------------------------
# LOCAL TEST (SAFE)
# -------------------------------------------------
if __name__ == "__main__":
    docs, metas = retrieve(
        "Explain routing",
        unit_number=3,
        exam_group="C"
    )

    print(f"Found {len(docs)} results")

    if not docs:
        print("⚠️ Retrieval empty — answer must be refused")
    else:
        print("Sample doc:", docs[0])
