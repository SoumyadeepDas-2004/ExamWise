# intelligence/curriculum_resolver.py

import json
from typing import List, Dict
import numpy as np

from schemas.curriculum_schema import CurriculumConcept

# -------------------------------------------------
# EMBEDDING PROVIDER (plug your model here)
# -------------------------------------------------

def embed_text(text: str) -> np.ndarray:
    """
    Replace with:
    - OpenAI embeddings
    - Instructor embeddings
    - SentenceTransformers
    """
    raise NotImplementedError("embed_text() not implemented")


# -------------------------------------------------
# SIMILARITY
# -------------------------------------------------

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# -------------------------------------------------
# CURRICULUM RESOLVER
# -------------------------------------------------

class CurriculumResolver:
    def __init__(self, curriculum_json_path: str):
        self.concepts: List[CurriculumConcept] = []
        self.concept_embeddings: Dict[str, np.ndarray] = {}

        self._load_concepts(curriculum_json_path)
        self._build_embeddings()

    # ---------------- Load ----------------

    def _load_concepts(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.concepts = [CurriculumConcept(**item) for item in data]

    # ---------------- Embeddings ----------------

    def _build_embeddings(self):
        for concept in self.concepts:
            text = self._concept_to_text(concept)
            self.concept_embeddings[concept.concept_id] = embed_text(text)

    # ---------------- Public API ----------------

    def resolve(
        self,
        query: str,
        top_k: int = 3,
        threshold: float = 0.55
    ) -> List[Dict]:
        query_vec = embed_text(query)

        matches = []

        for concept in self.concepts:
            concept_vec = self.concept_embeddings[concept.concept_id]
            score = cosine_similarity(query_vec, concept_vec)

            if score >= threshold:
                matches.append((score, concept))

        matches.sort(key=lambda x: x[0], reverse=True)

        return [
            self._format(concept, score)
            for score, concept in matches[:top_k]
        ]

    # ---------------- Helpers ----------------

    def _concept_to_text(self, concept: CurriculumConcept) -> str:
        """
        This defines semantic grounding.
        """
        return " | ".join([
            concept.concept,
            ", ".join(concept.aliases),
            concept.domain,
            " > ".join(concept.topic_path),
            concept.course_title,
            f"Semester {concept.semester}",
        ])

    def _format(self, concept: CurriculumConcept, score: float) -> Dict:
        return {
            "concept_id": concept.concept_id,
            "subject": concept.course_title,
            "semester": concept.semester,
            "confidence": round(score, 3),
        }
