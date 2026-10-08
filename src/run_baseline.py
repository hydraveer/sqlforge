"""Run baseline Text-to-SQL evaluation on the Spider dev set."""

import argparse
import json
import time
from pathlib import Path

from src.evaluate import is_correct
from src.infer import clean_sql, generate, load_model
from src.prompts import build_messages
from src.schema import DEFAULT_DB_DIR, get_schema

DEV_PATH = Path("data/spider/dev.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Spider baseline evaluation")
    parser.add_argument("--model", required=True, help="HF model id")
    parser.add_argument("--limit", type=int, default=None, help="Only run first N examples")
    parser.add_argument("--out", type=Path, default=None, help="Output JSON path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    examples = json.loads(DEV_PATH.read_text())
    if args.limit:
        examples = examples[: args.limit]

    messages_batch = [
        build_messages(get_schema(ex["db_id"]), ex["question"]) for ex in examples
    ]

    start = time.monotonic()
    llm = load_model(args.model)
    raw_outputs = generate(llm, messages_batch)
    preds = [clean_sql(r) for r in raw_outputs]

    rows = []
    for ex, pred in zip(examples, preds):
        db_path = DEFAULT_DB_DIR / ex["db_id"] / f"{ex['db_id']}.sqlite"
        correct, error = is_correct(db_path, ex["query"], pred)
        rows.append({
            "db_id": ex["db_id"],
            "question": ex["question"],
            "gold": ex["query"],
            "pred": pred,
            "correct": correct,
            "error": error,
        })

    n = len(rows)
    summary = {
        "model": args.model,
        "n": n,
        "exec_accuracy": round(sum(r["correct"] for r in rows) / n, 4),
        "error_rate": round(sum(r["error"] is not None for r in rows) / n, 4),
        "total_seconds": round(time.monotonic() - start, 1),
    }

    preds_path = Path("results") / f"{args.model.split('/')[-1]}_preds.json"
    preds_path.parent.mkdir(parents=True, exist_ok=True)
    preds_path.write_text(json.dumps(preds, indent=2))

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()