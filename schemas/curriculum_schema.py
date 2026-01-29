# schemas/curriculum_schema.py

from enum import Enum
from typing import List
from pydantic import BaseModel, Field, validator


class ConceptType(str, Enum):
    theory = "theory"
    algorithm = "algorithm"
    protocol = "protocol"
    technology = "technology"
    tool = "tool"
    modeling_notation = "modeling_notation"
    cryptographic_mechanism = "cryptographic_mechanism"


class CurriculumConcept(BaseModel):
    # ---- Identity ----
    concept_id: str = Field(..., description="Globally unique concept ID")

    # ---- Semantic ----
    concept: str
    aliases: List[str] = Field(default_factory=list)
    domain: str

    # ---- Academic hierarchy ----
    university: str
    program: str
    department: str
    semester: int = Field(..., ge=1, le=8)
    course_code: str
    course_title: str
    unit: int = Field(..., ge=1)

    # ---- Knowledge graph ----
    topic_path: List[str] = Field(..., min_items=2)

    # ---- Meta ----
    concept_type: ConceptType
    is_exam_relevant: bool = True

    # ---------------- Validators ----------------

    @validator("concept_id")
    def concept_id_no_spaces(cls, v):
        if " " in v:
            raise ValueError("concept_id must not contain spaces")
        return v

    @validator("topic_path")
    def topic_path_min_depth(cls, v):
        if len(v) < 2:
            raise ValueError("topic_path must have at least 2 levels")
        return v

    @validator("aliases", each_item=True)
    def strip_aliases(cls, v):
        return v.strip()
