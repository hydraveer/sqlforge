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
| Model | Execution Accuracy |
|---|---|
| Qwen2.5-Coder-1.5B (base) | TBD |
| Qwen2.5-Coder-3B (base) | TBD |# sqlforge
End-to-end LLMOps platform for Text-to-SQL: QLoRA fine-tuning, MLflow model registry, vLLM serving on EKS, CI eval gates, and Prometheus/Grafana monitoring.

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
