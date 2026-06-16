# Spaced-Repetition Outcome Benchmark

**The objective track of LAEF for the Spaced Repetition Coach agent.**

The [behavioral suite](../../benchmark/spaced-repetition-coach.yaml) checks whether
the agent *computes SM-2 correctly*. This benchmark checks something the behavioral
suite structurally cannot: **whether the scheduling policy actually produces good
learning, and how it compares to the alternatives** — against a hidden ground-truth
memory, with hard, reproducible numbers.

That distinction is the whole reason this directory claims to be more than a
persona dump. "Uses SM-2" is a feature. "SM-2 scores 73/100 on retention-efficiency,
18 points behind a target-retention scheduler" is *evidence*. Evidence is the thing
an AI agent — or a human — can't cheaply regenerate, and the thing worth coming here for.

---

## What it measures

A spaced-repetition coach makes one consequential decision over and over: **when
should this card be reviewed next?** Schedule too early and you waste the user's
time on cards they already know. Schedule too late and they forget, and the card
resets. The benchmark scores policies on the two outcomes that follow from that
decision, over a simulated study career:

| Metric | Meaning | Better |
|--------|---------|:------:|
| `retention` | Mean true retrievability across all cards at the horizon (0–1) | higher |
| `reviews_per_card` | Total reviews spent per card — the user's time cost | lower |
| `lapses_per_card` | Times a card was forgotten and had to be relearned | lower |
| `efficiency` | `retention / reviews_per_card` | higher |
| `laef_outcome` | Efficiency as a % of the cheating Oracle's efficiency (0–100) | higher |

Retention and review-count are in tension — you can always buy more retention with
more reviews (see `fixed-1d`). The benchmark rewards getting retention *cheaply*.

---

## The ground-truth memory model

Each simulated learner ([`model.py`](model.py)) holds a hidden state per card,
following the **DSR** framing (Difficulty / Stability / Retrievability) that
underlies modern schedulers like FSRS, with the classic Ebbinghaus exponential
forgetting curve:

```
Retrievability t days after the last review:   R = exp(-t / S)
```

`S` is the card's **stability** (roughly its current half-life in days). Two
mechanics give scheduling real consequences:

1. **Recall is probabilistic.** At a review, success is a Bernoulli draw on the
   true `R`. Wait until `R` is low and the draw probably fails.

2. **Spacing effect.** A *successful* review multiplies stability. Every success
   compounds it (`base_growth`), and reviewing at lower `R` — closer to the edge of
   forgetting — banks an extra bonus (`spacing_bonus`). Harder cards earn less of
   both. A **lapse** resets stability to a small relearning value.

So there is a genuine optimum: review late enough to bank the spacing bonus, early
enough to keep the lapse risk low. Rigid policies miss it; adaptive ones find it.

### The fairness barrier

This is what makes it a fair test of *policy* rather than of who read the simulator.
A scheduler **never sees `S`**. After each review it receives only a self-grade
(0–5), exactly as a real user would report one:

| Outcome | Grade reported |
|---------|----------------|
| Recalled, felt easy (`R ≥ 0.9`) | 5 |
| Recalled, felt solid (`0.7 ≤ R < 0.9`) | 4 |
| Recalled, felt hard (`R < 0.7`) | 3 |
| Forgot (close) / (blank) | 2 / 1 |

The grade is the only channel between the hidden memory and the policy — the same
information bottleneck a human coach works through. The lone exception is the
`oracle`, which reads `S` directly to mark the efficiency ceiling; it is labelled a
cheat everywhere and is not a deployable policy.

---

## The policies under test

([`schedulers.py`](schedulers.py) — adding your own is a few lines; see below.)

| Policy | Idea |
|--------|------|
| `fixed-1d` | Review everything every day. The naive floor: buys retention with brute force. |
| `leitner` | Boxes: interval doubles on a pass, resets to 1 on a lapse. |
| `sm2` | **SuperMemo-2** — the algorithm the Coach agent advertises. Faithful (EF floor 1.3, reps 1/2 fixed at 1/6 days, lapse resets). |
| `target-r90` | Tracks an *estimate* of each card's stability from grades alone and schedules for a target retrievability. FSRS in spirit. |
| `oracle` | Cheats — schedules from the true `S`. The 100-point reference ceiling. |

---

## Results

See [the scorecard](../../results/spaced-repetition/scorecard.md) for the current
table and [`results.json`](../../results/spaced-repetition/results.json) for the
machine-readable run. Headline as committed:

| Policy | LAEF outcome | Retention | Reviews/card |
|--------|-------------:|----------:|-------------:|
| `oracle` (ceiling) | 100 | 0.93 | 42.0 |
| `target-r90` | **91** | 0.86 | 43.1 |
| `leitner` | 73 | 0.69 | 42.7 |
| `sm2` | **73** | 0.73 | 44.9 |
| `fixed-1d` | 26 | 0.99 | 170.5 |

The story the numbers tell: **a correct SM-2 implementation is not the same as a
good scheduler.** SM-2 retains 73% of cards at roughly the same review cost a
target-retention policy uses to retain 86% — an 18-point efficiency gap, reproducible
to the third decimal. `fixed-1d` shows the trap of optimizing retention alone: near-perfect
recall at four times the work. This is precisely the kind of objective, comparative
signal the LAEF score is meant to carry.

---

## Running it

```bash
cd eval/sim/spaced-repetition
python3 benchmark.py                # writes results.json + scorecard.md
python3 benchmark.py --regen-deck   # regenerate the card deck from deck_seed
python3 benchmark.py --quiet        # no stdout table
```

Standard library only — no dependencies, no network, Python 3.9+. Every input is
seeded ([`config.json`](config.json), [`deck.json`](deck.json)), so the same commit
produces the same numbers on any machine. That reproducibility is what lets a score
graduate from `self-reported` to `auto-evaluated`.

## Adding a scheduler

Implement `schedule_new` and `update` in [`schedulers.py`](schedulers.py) (look only
at the grades and intervals you're handed — not at `hidden`), add it to the list in
[`benchmark.py`](benchmark.py), and rerun. If your policy beats `target-r90` on
efficiency, open a PR — a better baseline makes every score on this benchmark sharper.

---

## Honest caveats

- **This is a model of memory, not memory.** The DSR equations and the constants in
  `config.json` are a defensible, literature-shaped abstraction, not ground truth
  about any real learner. The constants were calibrated so the scheduling tension
  actually bites (early versions lapse-stormed and separated nothing); calibration
  notes live in the git history of this file.
- **Absolute numbers are model-dependent; the ranking is the product.** Don't read
  "44 reviews/card" as a real-world prediction. Read "target-retention dominates SM-2
  on this memory model" — that ordering is robust across seeds, deck, and a range of
  `target_r` (swept 0.85–0.92), which is the claim the benchmark is entitled to make.
- **One model can't crown a universal winner.** A real learner is not exactly DSR.
  The right next step is a second, differently-shaped memory model: a policy that wins
  under both earns far more trust than one tuned to this one. Contributions of
  alternative learner models are especially welcome.
