from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from intelligence.embedding_model import get_embedding_model
STRATEGY_KEYWORDS = [
    "focus", "prioritize", "priority",
    "revise", "revision",
    "safe", "safest",
    "prepare", "preparation",
    "score", "scoring",
    "less time", "last minute"
]

# -------------------------------------------------
# Load embedding model (same family as retriever)
# -------------------------------------------------
MODEL = get_embedding_model()
# -------------------------------------------------
# Define intent space (natural language descriptions)
# -------------------------------------------------
INTENT_DESCRIPTIONS = {
    "importance_query": (
        "questions asking which topics are important, most asked, "
        "frequently repeated, or high priority for exams"
    ),
    "pattern_query": (
        "questions about exam trends, patterns, historical analysis, "
        "or how questions usually appear"
    ),
    "explanation_query": (
        "questions asking to explain, describe, define, derive, "
        "or elaborate a concept in detail"
    ),
    "unit_analysis": (
        "questions focusing on a specific syllabus unit, "
        "unit-wise analysis, or unit-based preparation"
    ),
    "general": (
        "general academic questions that do not clearly fall into "
        "importance, pattern, explanation, or unit-based analysis"
    )
}

# -------------------------------------------------
# Precompute intent embeddings (done once)
# -------------------------------------------------
INTENT_LABELS = list(INTENT_DESCRIPTIONS.keys())
INTENT_TEXTS = list(INTENT_DESCRIPTIONS.values())
INTENT_EMBEDDINGS = MODEL.encode(INTENT_TEXTS)


# -------------------------------------------------
# Main intent detection function
# -------------------------------------------------
def detect_intent(query: str, confidence_threshold: float = 0.35) -> str:
    """
    Detects the semantic intent of a query using embeddings.

    Args:
        query (str): User query
        confidence_threshold (float): Minimum similarity required
                                      to accept a specific intent

    Returns:
        str: intent label
    """
    q = query.lower()
    if any(k in q for k in STRATEGY_KEYWORDS):
        return "importance_query"
    query_embedding = MODEL.encode([query])

    similarities = cosine_similarity(query_embedding, INTENT_EMBEDDINGS)[0]
    best_idx = int(np.argmax(similarities))
    best_score = similarities[best_idx]

    if best_score < confidence_threshold:
        return "general"

    return INTENT_LABELS[best_idx]


# -------------------------------------------------
# Quick manual test
# -------------------------------------------------
if __name__ == "__main__":
    tests = [
        "Most important topics in computer networks",
        "Explain routing algorithms",
        "What is the exam pattern for Unit 4?",
        "Unit 3 important questions",
        "Tell me about TCP"
    ]

    for t in tests:
        print(f"{t}  →  {detect_intent(t)}")
