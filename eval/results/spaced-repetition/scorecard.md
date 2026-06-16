# Spaced-Repetition Outcome Scorecard

_Generated 2026-06-16 by `eval/sim/spaced-repetition/benchmark.py` — fully reproducible (`python3 benchmark.py`)._

Each policy schedules the **same 120-card deck** for the **same 180-day horizon**, averaged over **24 seeded simulated learners**. Schedulers see only the intervals they chose and the learner's self-grades — never the hidden memory state. Target retrievability: 0.9.

| Rank | Policy | LAEF outcome | Retention @180d | Reviews/card | Lapses/card | Pareto |
|-----:|--------|-------------:|----------------:|-------------:|------------:|:------:|
| 1 | `oracle` ⭐ | **100** | 0.929 ± 0.006 | 42.01 | 7.58 | — |
| 2 | `target-r90` | **91** | 0.864 ± 0.007 | 43.07 | 9.03 | ✅ |
| 3 | `leitner` | **73** | 0.692 ± 0.012 | 42.74 | 16.74 | ✅ |
| 4 | `sm2` | **73** | 0.725 ± 0.015 | 44.89 | 17.02 | — |
| 5 | `fixed-1d` | **26** | 0.995 ± 0.003 | 170.50 | 3.58 | ✅ |

`oracle` cheats (reads the true memory state) and defines the 100-point efficiency ceiling; it is not a deployable policy. Everything else is.

## What this says about the agent's claim

The Spaced Repetition Coach agent advertises **SM-2**. On this benchmark SM-2 scores **73/100** (0.72 retention at 44.9 reviews/card), while a target-retention policy scores **91/100** (0.86 at 43.1 reviews/card). 
The objective gap is the kind of evidence the directory exists to surface: a faithful SM-2 implementation is *correct* yet leaves measurable efficiency on the table versus a stability-tracking scheduler.

See [eval/sim/spaced-repetition/README.md](../../sim/spaced-repetition/README.md) for the memory model, fairness barrier, and calibration notes.
