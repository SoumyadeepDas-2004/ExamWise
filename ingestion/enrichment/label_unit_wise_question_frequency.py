import json
from collections import Counter

INPUT = "../data/computer_networks/pyqs/pyq_normalized/pyq_ALL_backfilled.json"
OUTPUT = "../data/computer_networks/pyqs/pyq_normalized/pyq_ALL_enriched.json"

with open(INPUT, "r", encoding="utf-8") as f:
    rows = json.load(f)

# Count (unit_number, exam_group)
counter = Counter()
for r in rows:
    if r["unit_number"] is not None:
        key = (r["unit_number"], r["exam_group"])
        counter[key] += 1

# Assign frequency label
for r in rows:
    if r["unit_number"] is None:
        r["frequency_label"] = "low_yield"
        continue

    freq = counter[(r["unit_number"], r["exam_group"])]

    if freq >= 25:
        r["frequency_label"] = "high_yield"
    elif freq >= 10:
        r["frequency_label"] = "medium_yield"
    else:
        r["frequency_label"] = "low_yield"

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, default=str)

print("✅ Unit-level frequency labeling done")

for k, v in counter.most_common(10):
    print(f"Unit {k[0]} | Group {k[1]} → {v} questions")