import json
from collections import defaultdict
import unicodedata
import os

def normalize(text: str) -> str:
    # Handles OCR + unicode issues like ’ vs '
    return unicodedata.normalize("NFKD", text).lower().strip()


def build_topic_unit_index(syllabus_json_path: str) -> dict:
    with open(syllabus_json_path, "r", encoding="utf-8") as f:
        syllabus = json.load(f)

    # key -> list of unit mappings
    index = defaultdict(list)

    for unit in syllabus["units"]:
        unit_no = unit["unit"]
        unit_title = unit["title"]

        for topic_block in unit["topics"]:
            for item in topic_block["items"]:
                key = normalize(item)

                entry = {
                    "unit_number": unit_no,
                    "unit_title": unit_title,
                }

                # avoid duplicate entries
                if entry not in index[key]:
                    index[key].append(entry)

    return dict(index)


if __name__ == "__main__":
    syllabus_path = "data/makaut/btech/cse/semester/semester_6/computer_networks/syllabus/raw/syllabus.json"

    index = build_topic_unit_index(syllabus_path)

    out_path = "data/makaut/btech/cse/semester/semester_6/computer_networks/syllabus/cleaned/syllabus_topic_index.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"✅ Topic index built: {len(index)} unique topics")

    # preview
    preview = list(index.items())[:5]
    print(json.dumps(preview, indent=2))
