from intelligence.query_classifier import classify_query, QueryRoute

# RAG (explanations)
from rag.answer_engine import answer_question

# NEW analytics pipeline
from intelligence.analytics_query_planner import extract_analytics_slots
from intelligence.exam_analytics_engine import get_unit_stats
from intelligence.analytics_response_formatter import format_unit_response

# Prediction (unchanged)
from intelligence.exam_analytics_engine import predict_questions



def route_query(
    query: str,
    unit_number: int | None = None,
    exam_group: str | None = None
):
    route = classify_query(query)

    # -----------------------------
    # 1. RAG PATH — Explanations
    # -----------------------------
    if route == QueryRoute.RAG:
        return answer_question(
            query=query,
            unit_number=unit_number,
            exam_group=exam_group
        )

    # -----------------------------
    # 2. ANALYTICS PATH — FACTS
    # -----------------------------
    if route == QueryRoute.ANALYTICS:
        # 🔑 Extract analytics parameters from natural language
        slots = extract_analytics_slots(query)

        # Explicit args override inferred ones (if user passed them)
        if exam_group:
            slots["group"] = exam_group
        if unit_number:
            slots["filter_unit"] = unit_number

        # 🔍 Fetch raw stats from DuckDB
        rows = get_unit_stats(
            group=slots["group"],
            unit_number=slots["filter_unit"]
        )

        # 🧾 Format response (NO SQL, NO LOGIC HERE)
        return format_unit_response(rows, slots)

    # -----------------------------
    # 3. PREDICTION PATH — Trends
    # -----------------------------
    if route == QueryRoute.PREDICTION:
    # 🔑 Reuse the SAME slot extractor
        slots = extract_analytics_slots(query)

        # Explicit args override inferred ones
        if exam_group:
            slots["group"] = exam_group
        if unit_number:
            slots["filter_unit"] = unit_number

        return predict_questions(
            unit_number=slots["filter_unit"],
            exam_group=slots["group"]
        )


    # -----------------------------
    # 4. FALLBACK — Reject
    # -----------------------------
    return (
        "⚠️ Unable to classify this query clearly.\n"
        "Please rephrase using MAKAUT exam-oriented language."
    )
