import json
from collections import defaultdict

# -----------------------------
# Paths
# -----------------------------
TOPIC_FREQ_PATH = "data/makaut/btech/cse/semester/semester_6/computer_networks/analytics/topic_frequency.json"
OUTPUT_PATH = "data/makaut/btech/cse/semester/semester_6/computer_networks/analytics/unit_yield_summary.json"

# -----------------------------
# Load topic stats
# -----------------------------
with open(TOPIC_FREQ_PATH, "r", encoding="utf-8") as f:
    topic_stats = json.load(f)

# -----------------------------
# Aggregate per unit
# -----------------------------
units = defaultdict(lambda: {
    "unit_title": None,
    "high_yield": [],
    "medium_yield": [],
    "low_yield": []
})

for topic, data in topic_stats.items():
    unit_no = data["unit_number"]
    unit_title = data["unit_title"]
    yield_label = data["yield"]

    if unit_no is None:
        continue

    unit_key = f"Unit {unit_no}"
    units[unit_key]["unit_title"] = unit_title
    units[unit_key][f"{yield_label}_yield"].append(topic)

# -----------------------------
# Sort topics alphabetically
# -----------------------------
for unit in units.values():
    for k in ["high_yield", "medium_yield", "low_yield"]:
        unit[k].sort()

# -----------------------------
# Save
# -----------------------------
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(units, f, indent=2)

print("✅ Unit-wise yield summary generated")
print(f"Units covered: {len(units)}")
