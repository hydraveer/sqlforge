"""Execution-accuracy evaluation for Text-to-SQL."""

import sqlite3
import time
from collections import Counter
from contextlib import closing
from pathlib import Path

def execute_sql(db_path: Path, sql: str, timeout_s: float = 5.0)-> list[tuple]:
    """Run SQL on a read-only connection; abort if it exceeds timeout_s.

    Args:
        db_path: Path to the .sqlite file.
        sql: Query to run.
        timeout_s: Max seconds before the query is aborted.

    Returns:
        All result rows.

    Raises:
        sqlite3.Error: If the SQL is invalid or times out.
    """
    deadline = time.monotonic() + timeout_s
    def _check_timeout() -> int:
        return int(time.monotonic() > deadline)

    with closing(sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)) as conn:
        conn.set_progress_handler(_check_timeout, 10_000)
        return conn.execute(sql).fetchall()

def is_correct(db_path: Path, gold: str, pred: str) -> tuple[bool, str | None]:
    """Compare gold vs predicted SQL by execution results.

    Args:
        db_path: Path to the .sqlite file.
        gold: Reference SQL (assumed valid).
        pred: Model-generated SQL.

    Returns:
        (correct, error_message). error_message is None when pred ran successfully.
    """

    if not pred.strip():
        return False, "empty prediction"

    gold_rows = execute_sql(db_path, gold)

    try:
        pred_rows = execute_sql(db_path, pred)
    except sqlite3.Error as e:
        return False, str(e)

    if "order by" in gold.lower():
        return gold_rows == pred_rows, None
    return Counter(gold_rows)==Counter(pred_rows), None


    

    
