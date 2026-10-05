"""Extract table schemas from Spider SQLite databases."""

import sqlite3
from contextlib import closing
from functools import lru_cache
from pathlib import Path

DEFAULT_DB_DIR = Path("data/spider/database")

@lru_cache(maxsize=None)
def get_schema(db_id: str, db_dir: Path = DEFAULT_DB_DIR) -> str:
    """Return all CREATE TABLE statements for a Spider database.

    Args:
        db_id: Database name, e.g. "concert_singer".
        db_dir: Folder containing one subfolder per database.

    Returns:
        CREATE TABLE statements separated by blank lines.

    Raises:
        FileNotFoundError: If the database file does not exist.
        ValueError: If the database contains no user tables.
    """
    db_path = db_dir / db_id / f"{db_id}.sqlite"

    if not Path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    query = """
    SELECT sql
    FROM sqlite_master
    WHERE type = 'table'
      AND name NOT LIKE 'sqlite_%'
      AND sql IS NOT NULL
    ORDER BY name
    """

    with closing(sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)) as conn:
        rows = conn.execute(query).fetchall()

    if len(rows) == 0:
        raise ValueError(f"No tables found in {db_id}")

    # Step 6: join the statements
    return "\n\n".join(row[0] for row in rows)

    