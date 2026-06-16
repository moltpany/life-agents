# Evaluation Results

This directory holds evaluation run artifacts: reproducible scores, with the data behind them.

## Objective outcome benchmarks (live)

Simulation benchmarks from [`eval/sim/`](../sim/) write their committed results here. These are `auto-evaluated`: standard-library, seeded, and reproducible with one command — no judge model, no human in the loop.

```
eval/results/
└── spaced-repetition/
    ├── results.json    # machine-readable scores for every scheduling policy
    └── scorecard.md    # human-readable comparative table
```

- **[spaced-repetition/](spaced-repetition/)** — scores SM-2 and alternative schedulers against a hidden ground-truth memory model. Reproduce: `python3 eval/sim/spaced-repetition/benchmark.py`. Methodology: [eval/sim/spaced-repetition/README.md](../sim/spaced-repetition/README.md).

## Behavioral judge runs (roadmap stage 2)

The behavioral suites in [`eval/benchmark/`](../benchmark/) are still scored manually today; current persona scores in [`index.json`](../../index.json) are `self-reported`. When the automated judge harness lands, its runs will be committed here as:

```
eval/results/
└── <agent-id>/
    └── <date>-<model>/
        ├── run.json        # per-case pass/fail + dimension scores
        └── traces/         # full conversation per benchmark case
```

A score with a published trace — or a reproducible simulation — is worth more than any badge.
