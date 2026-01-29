import json
from uuid import uuid4
from typing import List

from academic_schema import AcademicChunk


def ingest_syllabus(syllabus_json_path: str) -> List[AcademicChunk]:
    with open(syllabus_json_path, "r", encoding="utf-8") as f:
        syllabus = json.load(f)

    chunks: List[AcademicChunk] = []

    base_meta = {
        "university": syllabus["university"],
        "programme": syllabus["programme"],
        "semester": syllabus["semester"],
        "subject": syllabus["subject"],
        "subject_code": syllabus["subject_code"],
    }

    for unit in syllabus["units"]:
        unit_no = unit["unit"]
        unit_title = unit["title"]

        for topic_block in unit["topics"]:
            category = topic_block["category"]

            for item in topic_block["items"]:
                chunk: AcademicChunk = {
                    "id": uuid4(),
                    "text": item,
                    "clean_text": item,

                    # hierarchy
                    **base_meta,

                    # document identity
                    "doc_type": "syllabus",

                    # syllabus structure
                    "unit_number": unit_no,
                    "unit_title": unit_title,

                    # intelligence (empty by design)
                    "marks": None,
                    "question_type": None,
                    "difficulty": None,
                    "keywords": [item, category],

                    "frequency_label": None,
                }

                chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    syllabus_path = "../data/computer_networks/syllabus/syllabus.json"  # adjust if needed
    rows = ingest_syllabus(syllabus_path)

    print(f"✅ Syllabus rows generated: {len(rows)}")
    print(json.dumps(rows[:5], indent=2, default=str))
