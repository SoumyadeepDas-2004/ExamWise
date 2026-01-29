def build_prompt(query, context, exam_group):
    marks = {
        "A": "1 mark (very short answer)",
        "B": "5 marks (medium answer)",
        "C": "15 marks (detailed answer with diagram)"
    }

    return f"""
You are a MAKAUT Computer Networks exam assistant.

Exam Group: {exam_group} → {marks[exam_group]}

Answer the question strictly in MAKAUT exam style.

Context:
{chr(10).join(context)}

Question:
{query}

Answer:
"""
