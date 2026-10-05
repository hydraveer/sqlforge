"""Build chat prompts for Text-to-SQL."""

SYSTEM_PROMPT = (
    "You are a SQLite Expert. Given a database schema and question, "
    "return only one valid Sqlite query that answer it. "
    "No explanation, no markdown, no code fences."
)

def build_messages(schema: str, question: str) -> list[dict[str, str]]:
    """Build chat messages for a Text-to-SQL request.

    Args:
        schema: CREATE TABLE statements from get_schema().
        question: Natural-language question.

    Returns:
        A list of chat messages (system + user).

    Raises:
        ValueError: If schema or question is empty.
    """

    if not schema.strip() or not question.strip():
        raise ValueError("schema and question must be non-empty")
    
    user_content = f"Schema:\n{schema}\n\nQuestion: {question.strip()}"

    return[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
