import json
import os
from uuid import uuid4
from typing import List
from schemas.academic_schema import AcademicChunk


# -------------------------------------------------
# Config
# -------------------------------------------------
PYQ_DIR = "data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/raw"
OUT_DIR = "data/makaut/btech/cse/semester/semester_6/computer_networks/pyqs/intermediate"
TOPIC_INDEX_PATH = "data/makaut/btech/cse/semester/semester_6/computer_networks/syllabus/cleaned/syllabus_topic_index.json"

os.makedirs(OUT_DIR, exist_ok=True)


# -------------------------------------------------
# Load syllabus topic → unit index
# -------------------------------------------------
def load_topic_index(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------------------------
# Infer unit from keyword index
# -------------------------------------------------
def infer_unit(question_text: str, topic_index: dict):
    text = question_text.lower()
    matches = []

    for topic, units in topic_index.items():
        if topic in text:
            matches.extend(units)

    if not matches:
        return None, None

    freq = {}
    for u in matches:
        freq[u["unit_number"]] = freq.get(u["unit_number"], 0) + 1

    best_unit = max(freq, key=freq.get)
    for u in matches:
        if u["unit_number"] == best_unit:
            return u["unit_number"], u["unit_title"]

    return None, None


# -------------------------------------------------
# Normalize one PYQ file
# -------------------------------------------------
def normalize_pyq(pyq_path: str, topic_index: dict) -> List[AcademicChunk]:
    with open(pyq_path, "r", encoding="utf-8") as f:
        pyq = json.load(f)

    chunks: List[AcademicChunk] = []

    base_meta = {
        "university": pyq["university"],
        "programme": pyq["programme"],
        "semester": pyq["semester"],
        "subject": pyq["subject"],
        "subject_code": pyq["subject_code"],
        "year": pyq["year"],
    }

    # -------------------------
    # GROUP A (1 mark each)
    # -------------------------
    for q in pyq["groups"]["A"]:
        unit_no, unit_title = infer_unit(q["text"], topic_index)

        chunks.append({
            "id": uuid4(),
            "text": q["text"],
            "clean_text": q["text"],
            **base_meta,
            "doc_type": "pyq",
            "exam_group": "A",
            "marks": 1,
            "question_type": "theory",
            "unit_number": unit_no,
            "unit_title": unit_title,
            "difficulty": "easy",
            "keywords": [],
            "frequency_label": None,
        })

    # -------------------------
    # GROUP B & C
    # -------------------------
    for group in ["B", "C"]:
        for q in pyq["groups"][group]:
            parts = q["parts"]
            marks_per_part = q["marks"] // len(parts)

            for part in parts:
                clean_text = part["text"]
                unit_no, unit_title = infer_unit(clean_text, topic_index)

                chunks.append({
                    "id": uuid4(),
                    "text": clean_text,
                    "clean_text": clean_text,
                    **base_meta,
                    "doc_type": "pyq",
                    "exam_group": group,
                    "marks": marks_per_part,
                    "question_type": "theory",
                    "unit_number": unit_no,
                    "unit_title": unit_title,
                    "difficulty": None,
                    "keywords": [],
                    "frequency_label": None,
                })

    return chunks


# -------------------------------------------------
# MAIN — Loop all years
# -------------------------------------------------
if __name__ == "__main__":
    topic_index = load_topic_index(TOPIC_INDEX_PATH)

    for file in sorted(os.listdir(PYQ_DIR)):
        if not file.endswith(".json"):
            continue

        year = file.replace(".json", "")
        pyq_path = os.path.join(PYQ_DIR, file)

        rows = normalize_pyq(pyq_path, topic_index)

        out_path = os.path.join(OUT_DIR, f"{year}_normalized.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, default=str)

        print(f"✅ {year}: {len(rows)} questions normalized & saved")
