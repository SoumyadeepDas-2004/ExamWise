import subprocess
import sys
import shutil
from pathlib import Path

# -------------------------------------------------
# PROJECT PATHS (ADJUSTED TO YOUR TREE)
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_ROOT = BASE_DIR / "data" / "makaut" / "btech" / "cse" / "semester" / "semester_6" / "computer_networks"

CHROMA_DB = DATA_ROOT / "chroma_db"
DUCKDB_FILE = DATA_ROOT / "duckdb" / "analytics.duckdb"

ANALYTICS_DIR = DATA_ROOT / "analytics"
PYQ_INTERMEDIATE = DATA_ROOT / "pyqs" / "intermediate"
PYQ_CLEANED = DATA_ROOT / "pyqs" / "cleaned"
SYLLABUS_CLEANED = DATA_ROOT / "syllabus" / "cleaned"

# -------------------------------------------------
# UTILS
# -------------------------------------------------
def run(step_name, command):
    print(f"\n▶ {step_name}")
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"❌ Failed at step: {step_name}")
        sys.exit(1)
    print(f"✅ Completed: {step_name}")

def safe_delete(path: Path):
    if path.exists():
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)
        print(f"🧹 Deleted: {path}")

# -------------------------------------------------
# RESET STAGE (CRITICAL)
# -------------------------------------------------
def reset_pipeline_state():
    print("\n🧹 RESETTING PIPELINE STATE")

    safe_delete(CHROMA_DB)
    safe_delete(DUCKDB_FILE)
    safe_delete(ANALYTICS_DIR)
    safe_delete(PYQ_INTERMEDIATE)
    safe_delete(PYQ_CLEANED)
    safe_delete(SYLLABUS_CLEANED)

    print("✅ Reset complete")

# -------------------------------------------------
# PIPELINE
# -------------------------------------------------
def main():
    reset_pipeline_state()

    run(
        "Normalize PYQs",
        ["python", "-m", "ingestion.pyqs.pyq_processing.normalize_pyq"]
    )

    run(
        "Merge Normalized PYQs",
        ["python", "-m", "ingestion.pyqs.pyq_processing.merge_normalized_pyqs"]
    )

    run(
        "Remove NULL / Invalid PYQs",
        ["python", "-m", "ingestion.pyqs.pyq_processing.merged_pyq_null_remove"]
    )

    run(
        "Topic-wise Question Frequency",
        ["python", "-m", "ingestion.enrichment.topic_wise_question_count"]
    )

    run(
        "Unit-wise Marks Weightage",
        ["python", "-m", "ingestion.enrichment.unit_wise_marks_weightage"]
    )

    run(
        "Build Vector Store (Embeddings)",
        ["python", "-m", "vectorstore.build_vector_store"]
    )

    run(
        "Initialize DuckDB",
        ["python", "-m", "databases.init_duckdb"]
    )

    run(
        "Load Analytics into DuckDB",
        ["python", "-m", "databases.load_analytics"]
    )

    print("\n🎉 FULL PIPELINE COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()
