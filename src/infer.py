"""vLLM batch inference for Text-to-SQL."""

from vllm import LLM, SamplingParams

def load_model(model_id: str)-> LLM:
    """Load a Hugging Face model into vLLM.

    Args:
        model_id: e.g. "Qwen/Qwen2.5-Coder-1.5B-Instruct".
    """
    return LLM(model=model_id, dtype="half", max_model_len=4096)

def generate(llm: LLM, messages_batch: list[list[dict[str, str]]])->list[str]:
    """Generate one response per conversation.

    Args:
        llm: Loaded vLLM model.
        messages_batch: List of conversations (each from build_messages()).

    Returns:
        Raw generated text, same order as input.
    """

    params = SamplingParams(temperature=0, max_tokens=256)
    outputs = llm.chat(messages_batch, params)
    return [out.outputs[0].text for out in outputs]

def clean_sql(text: str) -> str:
    """Extract a single SQL query from raw model output."""
    sql = text.strip()
    sql = sql.replace("```sql", "")   # remove opening fence with "sql" tag
    sql = sql.replace("```", "")      # remove any remaining fences
    sql = sql.split(";")[0]           # keep only text before the first ';'
    return sql.strip()
