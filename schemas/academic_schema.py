# =========================
# academic_chunk.py
# =========================
from typing import TypedDict, List, Literal, Optional
from uuid import UUID

class AcademicChunk(TypedDict, total=False):
    # DB identity
    id: Optional[UUID]

    # Core content
    text: str
    clean_text: Optional[str]

    # Academic hierarchy
    university: str
    programme: str
    department: Optional[str]
    semester: int
    subject: str
    subject_code: str

    # Document traceability
    doc_type: Literal["pyq", "syllabus", "notes", "metadata"]
    source_filename: Optional[str]
    page_number: Optional[int]

    # Exam / analytics metadata
    year: Optional[int]
    exam_session: Optional[Literal["odd", "even"]]
    exam_group: Optional[str]
    normalized_group: Optional[Literal["group_a", "group_b", "group_c"]]
    question_type: Optional[
        Literal["theory", "numerical", "derivation", "code"]
    ]
    marks: Optional[int]

    # Syllabus structure
    unit_number: Optional[int]
    unit_title: Optional[str]

    # Intelligence / computed fields
    difficulty: Optional[Literal["easy", "medium", "hard"]]
    keywords: Optional[List[str]]
    frequency_label: Optional[
        Literal["high_yield", "medium_yield", "low_yield"]
    ]
