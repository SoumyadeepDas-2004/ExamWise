def format_unit_response(rows, slots):
    if not rows:
        return "No sufficient MAKAUT data available for this query."

    # -----------------------------
    # DOMINANCE / MOST IMPORTANT
    # -----------------------------
    if slots["metric"] == "importance":
        top = rows[0]
        return (
            f"📊 **Most Important Unit (MAKAUT CN)**\n\n"
            f"**Unit {top[0]} – {top[1]}** dominates.\n\n"
            f"- {top[2]} weighted marks\n"
            f"- {top[3]} questions\n"
        )

    # -----------------------------
    # WEIGHTAGE DISTRIBUTION
    # -----------------------------
    if slots["metric"] == "weightage":
        total = sum(r[2] for r in rows)
        lines = ["📊 **Weightage Distribution Across Units**\n"]
        for u, title, marks, _ in rows:
            pct = round((marks / total) * 100)
            lines.append(f"- Unit {u} – {title}: ~{pct}%")
        return "\n".join(lines)

    # -----------------------------
    # FREQUENCY (DEFAULT)
    # -----------------------------
    lines = ["📊 **Unit-wise Question Frequency**\n"]
    for u, title, _, q in rows:
        lines.append(f"- Unit {u} – {title}: {q} questions")
    return "\n".join(lines)
