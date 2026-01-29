from typing import Dict
from schemas.academic_schema import AcademicChunk

def chunk_to_rag_doc(chunk: AcademicChunk) -> Dict:
    return {
        "id": str(chunk["id"]),
        "text": chunk["clean_text"],
        "metadata": {
            "doc_type": chunk["doc_type"],
            "unit_number": chunk.get("unit_number"),
            "unit_title": chunk.get("unit_title"),
            "exam_group": chunk.get("exam_group"),
            "marks": chunk.get("marks"),
            "difficulty": chunk.get("difficulty"),
            "frequency_label": chunk.get("frequency_label"),
            "year": chunk.get("year"),
            "subject_code": chunk["subject_code"]
        }
    }
