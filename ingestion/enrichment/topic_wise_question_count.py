import json
from collections import defaultdict


# ----------------------------
# Config
# ----------------------------
PYQ_PATH = "data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/cleaned/null_removed_merged.json"
TOPIC_INDEX_PATH = "data/makaut/btech/cse/semester/semester_6/computer_networks/syllabus/cleaned/syllabus_topic_index.json"
OUTPUT_PATH = "data/makaut/btech/cse/semester/semester_6/computer_networks/analytics/topic_frequency.json"

GROUP_WEIGHT = {
    "A": 1,
    "B": 3,
    "C": 5
}

# ----------------------------
# Load files
# ----------------------------
with open(PYQ_PATH, "r", encoding="utf-8") as f:
    pyqs = json.load(f)

with open(TOPIC_INDEX_PATH, "r", encoding="utf-8") as f:
    topic_index = json.load(f)

# ----------------------------
# Aggregation store
# ----------------------------
topic_stats = defaultdict(lambda: {
    "unit_number": None,
    "unit_title": None,
    "group_a": 0,
    "group_b": 0,
    "group_c": 0,
    "weighted_score": 0
})

# ----------------------------
# Aggregate
# ----------------------------
import re

def contains_whole_word(text: str, phrase: str) -> bool:
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text) is not None


for q in pyqs:
    if q.get("unit_number") is None:
        continue  # 🚫 skip ambiguous questions

    text = q["clean_text"].lower()
    group = q["exam_group"]

    for topic, units in topic_index.items():
        if contains_whole_word(text, topic):
            stat = topic_stats[topic]
            stat["unit_number"] = units[0]["unit_number"]
            stat["unit_title"] = units[0]["unit_title"]

            if group == "A":
                stat["group_a"] += 1
            elif group == "B":
                stat["group_b"] += 1
            elif group == "C":
                stat["group_c"] += 1

            stat["weighted_score"] += GROUP_WEIGHT[group]
            break  # ✅ critical


# ----------------------------
# Yield labeling
# ----------------------------
for topic, stat in topic_stats.items():
    score = stat["weighted_score"]

    if score >= 15:
        stat["yield"] = "high"
    elif score >= 6:
        stat["yield"] = "medium"
    else:
        stat["yield"] = "low"

# ----------------------------
# Save
# ----------------------------
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(topic_stats, f, indent=2)

print("✅ Topic-level frequency analysis complete")
print(f"Total topics analyzed: {len(topic_stats)}")
