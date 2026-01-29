from enum import Enum

STRATEGY_KEYWORDS = [
    "focus", "prioritize", "priority",
    "revise", "revision",
    "safe", "safest",
    "tough",
    "prepare", "preparation",
    "score", "scoring",
    "less time", "last minute"
]
class QueryRoute(Enum):
    RAG = "rag"
    ANALYTICS = "analytics"
    PREDICTION = "prediction"
    UNKNOWN = "unknown"
import re

def classify_query(query: str) -> QueryRoute:
    q = query.lower().strip()

    # -----------------------------
    # ANALYTICS QUERIES
    # -----------------------------
    if re.search(
        r"(important questions|important topics|high yield|scoring|"
        r"which questions|what questions|priority questions|"
        r"from .* layer|from unit|unit wise important)",
        q
    ):
        return QueryRoute.ANALYTICS


    if re.search(r"(how many times|frequency|trend|asked)", q):
        return QueryRoute.ANALYTICS

    # -----------------------------
    # PREDICTION / PATTERN
    # -----------------------------
    if re.search(r"(predict|chances|expected|likely)", q):
        return QueryRoute.PREDICTION
     # -----------------------------
    # 🔥 STRATEGY INTENT → ANALYTICS (NEW)
    # -----------------------------
    if any(k in q for k in STRATEGY_KEYWORDS):
        return QueryRoute.ANALYTICS
    # -----------------------------
    # RAG (EXPLANATORY)
    # -----------------------------
    # -----------------------------
    # RAG (EXPLANATORY / COMPARATIVE)
    # -----------------------------
    if re.search(
        r"(explain|define|describe|what is|how does|compare|differentiate|difference)",
        q
    ):
        return QueryRoute.RAG


    return QueryRoute.ANALYTICS
