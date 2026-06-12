# Evaluation Results

This directory holds evaluation run artifacts: per-agent scores **with full conversation traces**.

It is currently empty by design. All scores in [`index.json`](../../index.json) are `self-reported` (see [EVALUATION.md](../../EVALUATION.md) for provenance levels). When the automated judge harness lands (LAEF roadmap stage 2), runs will be committed here as:

```
eval/results/
└── <agent-id>/
    └── <date>-<model>/
        ├── run.json        # per-case pass/fail + dimension scores
        └── traces/         # full conversation per benchmark case
```

A score with a published trace is worth more than any badge. Until then, the benchmark suites in [`eval/benchmark/`](../benchmark/) let anyone re-run the cases manually.
