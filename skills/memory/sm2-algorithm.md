---
id: sm2-algorithm
name: SM-2 Spaced Repetition Algorithm
domain: memory
type: method
used_by:
  - agents/learning/spaced-repetition-coach.md
references:
  - https://www.supermemo.com/en/blog/application-of-a-computer-to-improve-the-results-obtained-in-working-with-the-supermemo-method
---

# SM-2 Spaced Repetition Algorithm

The SM-2 algorithm (Piotr Woźniak, 1987, SuperMemo) schedules card reviews at expanding intervals based on self-rated recall quality. It is the basis of Anki and most modern spaced repetition systems.

## Core state per card

| Field | Initial value | Meaning |
|-------|--------------|---------|
| `interval_days` | — | Days until next review |
| `ease_factor` (EF) | 2.5 | Multiplier controlling interval growth |
| `repetition` | 0 | Count of consecutive successful reviews |

## Recall quality scale

After each review, the user rates recall quality `q` from 0 to 5:

| q | Meaning |
|---|---------|
| 0 | Complete blank |
| 1 | Wrong, but the answer felt familiar |
| 2 | Wrong, but close |
| 3 | Correct, with serious difficulty |
| 4 | Correct, after hesitation |
| 5 | Perfect, instant recall |

## Update rules

**If q < 3 (failed recall):**
- `repetition` resets to 0
- `interval_days` resets to 1
- `ease_factor` is **not** changed on failure (per original SM-2)

**If q ≥ 3 (successful recall):**
- `repetition` increments
- Interval:
  - 1st success: `interval_days = 1`
  - 2nd success: `interval_days = 6`
  - thereafter: `interval_days = round(previous_interval × ease_factor)`
- Ease factor update (applies on every rated review, success or not, in many implementations; original SM-2 applies it after each response — this collection follows the original):

```
EF' = EF + (0.1 − (5 − q) × (0.08 + (5 − q) × 0.02))
```

- **Floor:** if `EF' < 1.3`, set `EF' = 1.3`. There is no defined ceiling, but q=5 adds at most +0.1 per review.

### Worked examples

| q | EF before | Δ | EF after |
|---|-----------|-----|----------|
| 5 | 2.50 | +0.10 | 2.60 |
| 4 | 2.50 | 0.00 | 2.50 |
| 3 | 2.50 | −0.14 | 2.36 |
| 2 | 2.50 | −0.32 | 2.18 (and interval resets to 1 day) |
| 3 | 1.35 | −0.14 | 1.30 (floored) |

Interval sequence at constant q=4, EF=2.5: **1 → 6 → 15 → 38 → 94 → 234 days.**

## Edge cases and practical rules

- **Overdue reviews:** if a card is reviewed late, schedule from the actual review date, not the originally due date.
- **Same-day relearning:** after a failed card resets to 1 day, it should reappear the next day; do not re-test it repeatedly within the same session beyond one relearn pass.
- **Minimum EF 1.3 exists to prevent "ease hell":** cards that would otherwise repeat near-daily forever.
- **New card limits:** introducing more than ~20 new cards/day typically creates an unsustainable review backlog (rule of thumb: daily reviews ≈ 10× daily new cards at steady state).

## Relationship to the Ebbinghaus forgetting curve

Ebbinghaus (1885) measured exponential memory decay and the spacing effect. Fixed-interval schedules derived from it (1, 3, 7, 14, 30, 90 days) are a reasonable default for list-based review without per-item tracking. SM-2 improves on fixed intervals by adapting per card: easy cards grow intervals faster, hard cards slower. When a user has no per-card state (e.g., reviewing a chapter, not flashcards), fall back to the fixed Ebbinghaus sequence.

## Known limitations

- Depends on honest self-grading; users systematically over-rate recall.
- Treats cards as independent; ignores interference between similar cards (mitigate with card design — see [active-recall.md](active-recall.md)).
- Modern successors (FSRS) fit individual forgetting curves and outperform SM-2 by ~20–30% review efficiency; SM-2 remains the best simplicity/effectiveness trade-off for prompt-based agents because it is fully specified in a dozen lines.
