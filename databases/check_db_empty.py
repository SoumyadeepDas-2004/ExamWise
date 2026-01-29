import duckdb

con = duckdb.connect(
    "data/makaut/btech/cse/semester/semester_6/"
    "computer_networks/duckdb/analytics.duckdb"
)

print("Topic rows:", con.execute("SELECT COUNT(*) FROM topic_analytics").fetchone())
print("Unit rows:", con.execute("SELECT COUNT(*) FROM unit_analytics").fetchone())

print(
    con.execute(
        """
        SELECT unit_number, unit_title, exam_group, total_marks, question_count
        FROM unit_analytics
        ORDER BY total_marks DESC
        """
    ).fetchall()
)

con.close()
