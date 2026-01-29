import json
import glob

all_rows = []

for path in glob.glob("data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/intermediate/*_normalized.json"):
    with open(path, "r", encoding="utf-8") as f:
        all_rows.extend(json.load(f))

with open("data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/intermediate/merged_pyq.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, indent=2, default=str)

print("✅ Total questions:", len(all_rows))
