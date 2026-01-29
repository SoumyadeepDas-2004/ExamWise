import duckdb
import os

DB_PATH = (
    "data/makaut/btech/cse/semester/semester_6/"
    "computer_networks/duckdb/analytics.duckdb"
)

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

con = duckdb.connect(DB_PATH)

# -----------------------------------
# Topic-level analytics (AGGREGATED)
# -----------------------------------
con.execute("""
CREATE TABLE IF NOT EXISTS topic_analytics (
    topic TEXT,
    unit_number INTEGER,
    exam_group TEXT,
    question_count INTEGER,
    year INTEGER
);
""")

# -----------------------------------
# Unit-level analytics (AGGREGATED)
# -----------------------------------
con.execute("""
CREATE TABLE IF NOT EXISTS unit_analytics (
    unit_number INTEGER,
    unit_title TEXT,
    exam_group TEXT,
    total_marks INTEGER,
    question_count INTEGER
);
""")

# Helpful indexes
con.execute("""
CREATE INDEX IF NOT EXISTS idx_topic_analytics
ON topic_analytics (unit_number, exam_group, year);
""")

con.execute("""
CREATE INDEX IF NOT EXISTS idx_unit_analytics
ON unit_analytics (exam_group, total_marks);
""")

con.close()

print("✅ Analytics DuckDB schema initialized")
