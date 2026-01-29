import duckdb
import os
# -------------------------------------------------
# DuckDB connection (AUTHORITATIVE)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "makaut",
    "btech",
    "cse",
    "semester",
    "semester_6",
    "computer_networks",
    "duckdb",
    "analytics.duckdb",
)

def _connect():
    return duckdb.connect(DB_PATH, read_only=True)

def get_unit_stats(group=None, unit_number=None):
    con = duckdb.connect(DB_PATH)

    conditions = []
    params = []

    if group:
        conditions.append("exam_group = ?")
        params.append(group)

    if unit_number:
        conditions.append("unit_number = ?")
        params.append(unit_number)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    rows = con.execute(
        f"""
        SELECT unit_number, unit_title,
               SUM(total_marks) AS marks,
               SUM(question_count) AS questions
        FROM unit_analytics
        {where}
        GROUP BY unit_number, unit_title
        ORDER BY marks DESC
        """
    , params).fetchall()

    con.close()
    return rows
# -------------------------------------------------
# ANALYTICS API
# -------------------------------------------------

def get_expected_marks(
    unit_number: int | None,
    exam_group: str | None
) -> str:
    con = _connect()
    conditions = []
    params = []

    if unit_number is not None:
        conditions.append("unit_number = ?")
        params.append(unit_number)

    if exam_group is not None:
        conditions.append("exam_group = ?")
        params.append(exam_group)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT AVG(total_marks)
        FROM unit_analytics
        {where_clause}
    """

    result = con.execute(query, params).fetchone()
    con.close()

    if not result or result[0] is None:
        return "Unknown"

    avg = round(result[0])

    if avg <= 3:
        return "2–3 marks (short)"
    elif avg <= 6:
        return "5 marks (standard)"
    else:
        return "8–10 marks (long)"
def predict_questions(
    unit_number: int | None = None,
    exam_group: str | None = None,
    limit: int = 10
) -> str:
    """
    Predict likely questions using historical frequency.
    PURE DuckDB logic. No LLM guessing.
    """

    con = _connect()
    conditions = []
    params = []

    if unit_number is not None:
        conditions.append("unit_number = ?")
        params.append(unit_number)

    if exam_group is not None:
        conditions.append("exam_group = ?")
        params.append(exam_group)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT
            topic,
            SUM(question_count) AS freq
        FROM topic_analytics
        {where_clause}
        GROUP BY topic
        ORDER BY freq DESC
        LIMIT ?
    """

    params.append(limit)

    rows = con.execute(query, params).fetchall()
    con.close()

    if not rows:
        return "No sufficient historical data to predict likely questions."

    lines = [
        "🔮 **Likely Questions (Based on MAKAUT Trends)**",
        "Focus revision on these topics:"
    ]

    for i, (topic, freq) in enumerate(rows, start=1):
        lines.append(f"{i}. **{topic.title()}** (asked {freq} times)")

    return "\n".join(lines)
