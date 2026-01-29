import re

def extract_analytics_slots(query: str) -> dict:
    q = query.lower()

    slots = {
        "scope": None,        # unit | topic
        "group": None,        # A | B | C | None
        "metric": None,      # importance | frequency | weightage
        "filter_unit": None  # 1–6 | None
    }

    # -----------------------------
    # GROUP EXTRACTION
    # -----------------------------
    if "group a" in q:
        slots["group"] = "A"
    elif "group b" in q:
        slots["group"] = "B"
    elif "group c" in q:
        slots["group"] = "C"

    # -----------------------------
    # UNIT FILTER
    # -----------------------------
    match = re.search(r"unit\s*(\d)", q)
    if match:
        slots["filter_unit"] = int(match.group(1))

    # -----------------------------
    # SCOPE
    # -----------------------------
    if "topic" in q:
        slots["scope"] = "topic"
    else:
        slots["scope"] = "unit"

    # -----------------------------
    # METRIC
    # -----------------------------
    if any(x in q for x in ["important", "priority", "dominate", "focus"]):
        slots["metric"] = "importance"
    elif any(x in q for x in ["weightage", "marks", "distribution"]):
        slots["metric"] = "weightage"
    else:
        slots["metric"] = "frequency"

    return slots
