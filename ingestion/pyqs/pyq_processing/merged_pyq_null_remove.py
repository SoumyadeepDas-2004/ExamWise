import json
from typing import List, Dict
from schemas.academic_schema import AcademicChunk
import re

def contains_whole_word(text: str, phrase: str) -> bool:
    """
    Checks if `phrase` appears in `text` as a whole word or phrase.
    Safe against 'ip' in 'ship'.
    """
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text) is not None

def infer_unit_advanced(text: str, topic_index: dict, alias_map: dict):
    t = text.lower()

    # 1️⃣ Direct canonical topic match
    for topic, units in topic_index.items():
        if contains_whole_word(t, topic):
            return units[0]["unit_number"], units[0]["unit_title"]

    # 2️⃣ Alias → canonical → topic_index
    for canonical, aliases in alias_map.items():
        for a in aliases:
            if contains_whole_word(t, a):
                for units in topic_index.values():
                    if units[0]["unit_title"].lower() == canonical.lower():
                        return units[0]["unit_number"], units[0]["unit_title"]

    # 3️⃣ Fail → LLM fallback later
    return None, None




def backfill_units(
    pyq_path: str,
    topic_index_path: str,
    alias_map_path: str,
    output_path: str,
):
    # Load files
    with open(pyq_path, "r", encoding="utf-8") as f:
        rows: List[AcademicChunk] = json.load(f)

    with open(topic_index_path, "r", encoding="utf-8") as f:
        topic_index = json.load(f)

    with open(alias_map_path, "r", encoding="utf-8") as f:
        alias_map = json.load(f)

    updated = 0
    skipped = 0

    for row in rows:
        # 🚫 DO NOT touch already-filled units
        if row.get("unit_number") is not None:
            skipped += 1
            continue

        unit_no, unit_title = infer_unit_advanced(
            row["clean_text"], topic_index, alias_map
        )

        if unit_no is not None:
            row["unit_number"] = unit_no
            row["unit_title"] = unit_title
            updated += 1

    # Save new version
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, default=str)

    print("✅ Unit backfill complete")
    print(f"Updated rows: {updated}")
    print(f"Skipped (already had unit): {skipped}")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    backfill_units(
        pyq_path="data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/intermediate/merged_pyq.json",
        topic_index_path="data/makaut/btech/cse/semester/semester_6/computer_networks/syllabus/cleaned/syllabus_topic_index.json",
        alias_map_path="data/makaut/btech/cse/semester/semester_6/computer_networks/syllabus/cleaned/alias_map.json",
        output_path="data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/cleaned/null_removed_merged.json",
    )
