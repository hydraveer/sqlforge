# SQLForge

End-to-end LLMOps platform for Text-to-SQL.

**Pipeline:** QLoRA fine-tune → MLflow registry → vLLM on EKS → CI eval gate → Prometheus/Grafana

## Status
- [ ] Week 1: Baseline evaluation on Spider
- [ ] Week 2: QLoRA fine-tuning
- [ ] Week 3: MLflow tracking & registry
- [ ] Week 4: vLLM serving on EKS
- [ ] Week 5: CI eval gate + monitoring
- [ ] Week 6: Demo + design doc

## Results
## Baseline results (Spider dev, 1,034 examples)

| Model | Exec Accuracy (strict) | Error Rate |
|---|---|---|
| Qwen2.5-Coder-1.5B (base) | 60.4% | 18.0% |
| Qwen2.5-Coder-3B (base) | 65.0% | 11.2% |

### Failure analysis (1.5B, 407 wrong)
| Category | Count |
|---|---|
| Ran but wrong result | 224 |
| Column from wrong table (schema linking) | 138 |
| Hallucinated column | 34 |
| Hallucinated table | 7 |
| Other / degenerate | 4 |

**Main weakness:** schema linking — 75% of SQL errors use a real column from the wrong table.

**Evaluator audit:** 29 of the 224 silent failures differ only in column order,
so strict accuracy understates the model by up to ~2.8 points. All models are
scored with the same strict evaluator (v1) for fair comparison.

## How to run

```bash
pip install -r requirements.txt

# Baseline evaluation on the first 20 Spider dev examples
python -m src.run_baseline --model Qwen/Qwen2.5-Coder-1.5B-Instruct --limit 20

# Full dev set, custom output path
python -m src.run_baseline --model Qwen/Qwen2.5-Coder-3B-Instruct --out results/qwen3b.json

# Tests
pytest tests/
```

Results are written to `results/{model_short_name}.json` by default. Spider must be at `data/spider/`.
