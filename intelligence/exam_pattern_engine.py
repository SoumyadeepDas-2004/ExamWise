def generate_exam_strategy(topic_rows, unit_rows, slots):
    """
    topic_rows: data from DuckDB (topic_analytics)
    unit_rows: data from DuckDB (unit_analytics)
    slots: extracted intent (group, unit, topic)
    """

    insights = []

    if topic_rows:
        top_topic, freq = topic_rows[0]
        insights.append(
            f"🔥 **High Probability Topic**: '{top_topic.title()}' "
            f"(appeared {freq} times historically)."
        )

    if unit_rows:
        u, title, marks, q = unit_rows[0]
        insights.append(
            f"⚖️ **Unit Strategy**: Unit {u} ({title}) "
            f"is a strong contributor with {marks} marks."
        )

    if not insights:
        insights.append(
            "ℹ️ No dominant historical pattern detected. Prepare conceptually."
        )

    return insights
