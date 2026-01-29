import json
import duckdb
import os
from collections import defaultdict

# -------------------------------------------------
# PATHS
# -------------------------------------------------
DB_PATH = (
    "data/makaut/btech/cse/semester/semester_6/"
    "computer_networks/duckdb/analytics.duckdb"
)

ANALYTICS_DIR = (
    "data/makaut/btech/cse/semester/semester_6/"
    "computer_networks/analytics"
)

# -------------------------------------------------
# CONNECT
# -------------------------------------------------
con = duckdb.connect(DB_PATH)

# -------------------------------------------------
# CLEAR TABLES (IDEMPOTENT)
# -------------------------------------------------
con.execute("DELETE FROM topic_analytics;")
con.execute("DELETE FROM unit_analytics;")

# =================================================
# 1️⃣ LOAD topic_analytics (FROM topic_frequency.json)
# =================================================
with open(
    os.path.join(ANALYTICS_DIR, "topic_frequency.json"),
    "r",
    encoding="utf-8"
) as f:
    topic_freq = json.load(f)

for topic, data in topic_freq.items():
    unit_number = int(data.get("unit_number", 0))

    for group_key, exam_group in [
        ("group_a", "A"),
        ("group_b", "B"),
        ("group_c", "C"),
    ]:
        count = int(data.get(group_key, 0))

        if count > 0:
            con.execute(
                """
                INSERT INTO topic_analytics
                (topic, unit_number, exam_group, question_count, year)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    topic,
                    unit_number,
                    exam_group,
                    count,
                    0,  # year not available
                )
            )

# =================================================
# 2️⃣ DERIVE unit_analytics (AGGREGATED FROM TOPICS)
# =================================================
unit_agg = defaultdict(lambda: {
    "unit_title": "UNKNOWN",
    "total_marks": 0,
    "group_a": 0,
    "group_b": 0,
    "group_c": 0,
})

for topic, data in topic_freq.items():
    u = int(data.get("unit_number", 0))
    unit_agg[u]["unit_title"] = data.get("unit_title", "UNKNOWN")

    unit_agg[u]["total_marks"] += int(data.get("weighted_score", 0))
    unit_agg[u]["group_a"] += int(data.get("group_a", 0))
    unit_agg[u]["group_b"] += int(data.get("group_b", 0))
    unit_agg[u]["group_c"] += int(data.get("group_c", 0))

# Insert one row per (unit × exam_group)
for unit_number, stats in unit_agg.items():
    for exam_group, count in [
        ("A", stats["group_a"]),
        ("B", stats["group_b"]),
        ("C", stats["group_c"]),
    ]:
        con.execute(
            """
            INSERT INTO unit_analytics
            (unit_number, unit_title, exam_group, total_marks, question_count)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                unit_number,
                stats["unit_title"],
                exam_group,
                stats["total_marks"],
                count,
            )
        )

# -------------------------------------------------
# CLOSE
# -------------------------------------------------
con.close()

print("✅ Completed: Duck db data loading")
