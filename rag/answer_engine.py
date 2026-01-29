from retrieval.retriever import retrieve
from intelligence.exam_pattern_engine import generate_exam_strategy
from intelligence.exam_analytics_engine import get_unit_stats, get_expected_marks
from intelligence.semantic_intent_engine import detect_intent
from openai import OpenAI

# -------------------------------------------------
# LLM (LOCAL)
# -------------------------------------------------
llm = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# -------------------------------------------------
# Helpers (PURE FORMATTERS)
# -------------------------------------------------
def build_context(docs, metas):
    blocks = []
    for d, m in zip(docs, metas):
        blocks.append(
            f"- {d} (Year: {m['year']}, Marks: {m['marks']})"
        )
    return "\n".join(blocks)


def infer_answer_depth(metas):
    marks = [m.get("marks", 5) for m in metas]
    avg = sum(marks) / len(marks)

    if avg <= 3:
        return "SHORT (2–3 marks, ~6–8 lines)"
    elif avg <= 6:
        return "MEDIUM (5 marks, ~1–1.5 pages)"
    else:
        return "LONG (10 marks, ~2–3 pages)"


# -------------------------------------------------
# MAIN ANSWER ENGINE (STRICT)
# -------------------------------------------------
def answer_question(
    query: str,
    unit_number: int | None = None,
    exam_group: str | None = None
):
    print(f"🤔 Analyzing Query: '{query}'")

    if len(query.strip().split()) < 2:
        return "⚠️ Please provide a complete exam-style question."

    # 1️⃣ INTENT CLASSIFICATION
    query_type = detect_intent(query)
    if query_type == "explanation_query":
        tone = "theoretical and descriptive"
    elif query_type == "importance_query":
        tone = "exam-oriented and concise"
    else:
        tone = "standard exam tone"


    # 2️⃣ RETRIEVAL (FROZEN VECTOR STORE)
    docs, metas = retrieve(
        query=query,
        unit_number=unit_number,
        exam_group=exam_group,
        top_k=5
    )

    # 🛑 STEP 3 — HARD ENFORCEMENT
    if not docs:
        return (
            "⚠️ This question cannot be answered strictly using "
            "MAKAUT syllabus / PYQs.\n"
            "No relevant context was found."
        )

    # 3️⃣ ANALYTICS (DUCKDB ONLY)
    dominant_unit = unit_number or metas[0].get("unit_number")
    dominant_group = exam_group or metas[0].get("exam_group")

    unit_rows = get_unit_stats(
    group=dominant_group,
    unit_number=dominant_unit
    )

    strategy_lines = generate_exam_strategy(
        topic_rows=None,   # optional for now
        unit_rows=unit_rows,
        slots={
            "group": dominant_group,
            "filter_unit": dominant_unit
        }
    )

    exam_stats = "\n".join(strategy_lines)


    expected_marks = get_expected_marks(
        unit_number=dominant_unit,
        exam_group=dominant_group
    )

    # 4️⃣ USER-FACING STATS BLOCK (DETERMINISTIC)
    stats_display = (
        "### 📊 MAKAUT Exam Statistics & Strategy\n"
        f"{exam_stats}\n"
        "---\n"
        f"⚖️ **Typical Weightage**: {expected_marks}\n"
        "---\n\n"
    )

    # 5️⃣ PROMPT CONDITIONING (ANALYTICS → PROMPT)
    expected_depth = infer_answer_depth(metas)
    context = build_context(docs, metas)

    prompt = f"""
You are a MAKAUT B.Tech Computer Networks **exam answer writer**.
You must write answers exactly as expected in a university examination.

==================================================
QUESTION
==================================================
{query}

QUERY INTENT (for guidance only):
{query_type}

ANSWER TONE:
{tone}

EXPECTED ANSWER DEPTH:
{expected_depth}

RELEVANT PREVIOUS YEAR QUESTIONS (for context only):
{context}

EXAM PATTERN CONTEXT (DO NOT MENTION OR REFER):
{exam_stats}

==================================================
STRICT RULES (NON-NEGOTIABLE)
==================================================
- Stay strictly within the MAKAUT Computer Networks syllabus
- Write like a **student in the exam hall**, not like a textbook or teacher
- Use **clear academic language**, no casual tone
- Match the answer length to EXPECTED ANSWER DEPTH
- Do NOT mention:
  • analytics
  • trends
  • statistics
  • unit weightage
  • marks distribution
- Do NOT shorten explanations unnaturally
- Do NOT add information outside syllabus
- Do NOT invent new sections

==================================================
MANDATORY OUTPUT FORMAT (STRICT — FOLLOW EXACTLY)
==================================================

- Use Markdown headings EXACTLY as specified
- Do NOT write headings as plain text
- Do NOT change heading order
- Every section MUST be present
- If formatting is violated, the answer is INVALID

FORMAT TO FOLLOW:

## 1. Definition / Introduction
- Write **4–6 complete sentences**
- Must clearly cover:
  • what the concept is  
  • OSI layer (if applicable)  
  • why it is used  
  • where it is practically applied  

## 2. Core Explanation

### 2.1 Working Principle
- Write **5–7 descriptive lines**
- Explain step-by-step operation

### 2.2 Architecture / Components
- Write **5–7 descriptive lines**
- Explain components or structure clearly

### 2.3 Data Flow / Operation Steps
- Write **5–7 descriptive lines**
- Explain how data moves or how the protocol operates

## 3. ASCII Diagram
- Diagram is **MANDATORY**
- Must be clean, aligned, and readable
- Diagram must be **referred to in Section 2**

## 4. Advantages and Limitations

### Advantages
- Minimum **3 advantages**
- Each advantage: **1–2 full sentences**

### Limitations
- Minimum **3 limitations**
- Each limitation: **1–2 full sentences**
- Include security, performance, or practical issues where relevant

## 5. Conclusion
- Write **3–4 summarizing sentences**
- Mention modern relevance or alternatives (if applicable)

==================================================
DEPTH CONTROL
==================================================
- SHORT answers: concise but complete
- MEDIUM answers: moderately descriptive
- LONG answers (8–10 marks):
  • Highly descriptive
  • No shallow explanations
  • Should comfortably fill **1.5–2 handwritten pages**

==================================================
FINAL INSTRUCTION
==================================================
Write the final answer now.
Follow the structure strictly.
"""



    response = llm.chat.completions.create(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": "You are a strict MAKAUT university examiner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    final_answer = response.choices[0].message.content.strip()
    return (
    stats_display
    + "\n\n---\n\n"
    + final_answer
)
