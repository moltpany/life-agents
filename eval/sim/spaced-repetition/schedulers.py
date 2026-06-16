"""
Scheduling policies under test.

A scheduler decides *when* a card should next be reviewed. It is given only what
a real coach would have: the interval it last chose and the learner's self-grade
(0-5). It must never read the hidden CardState.stability — with one deliberate
exception, the Oracle, which cheats in order to mark the efficiency ceiling.

Each scheduler implements:

    schedule_new(card_id, hidden=None) -> int        # first interval after learning
    update(card_id, interval_used, grade, hidden=None) -> int   # next interval

`interval_used` is the interval that elapsed before the review now being graded.
`hidden` is the ground-truth CardState; it is passed to every scheduler but only
the Oracle is permitted to look at it (and the README says so out loud).
"""

from __future__ import annotations

import math


class Scheduler:
    name = "base"

    def reset(self) -> None:
        self.state = {}

    def schedule_new(self, card_id, hidden=None) -> int:
        raise NotImplementedError

    def update(self, card_id, interval_used, grade, hidden=None) -> int:
        raise NotImplementedError


class FixedInterval(Scheduler):
    """Review everything on a constant cadence. The naive floor: maximal burden."""

    def __init__(self, days: int = 1):
        self.days = days
        self.name = f"fixed-{days}d"
        self.reset()

    def schedule_new(self, card_id, hidden=None) -> int:
        return self.days

    def update(self, card_id, interval_used, grade, hidden=None) -> int:
        return self.days


class Leitner(Scheduler):
    """Classic boxes: interval doubles on a pass, resets to 1 on a lapse."""

    name = "leitner"

    def __init__(self, cap: int = 365):
        self.cap = cap
        self.reset()

    def schedule_new(self, card_id, hidden=None) -> int:
        self.state[card_id] = 1
        return 1

    def update(self, card_id, interval_used, grade, hidden=None) -> int:
        cur = self.state.get(card_id, 1)
        nxt = 1 if grade < 3 else min(self.cap, cur * 2)
        self.state[card_id] = nxt
        return nxt


class SM2(Scheduler):
    """
    SuperMemo-2 — the algorithm the Spaced Repetition Coach agent claims to use.
    Faithful to the canonical formulation (EF floor 1.3; reps 1 and 2 fixed at
    1 and 6 days; thereafter interval = round(prev * EF); lapse resets reps).
    """

    name = "sm2"

    def __init__(self):
        self.reset()

    def schedule_new(self, card_id, hidden=None) -> int:
        self.state[card_id] = {"ef": 2.5, "reps": 1, "interval": 1}
        return 1

    def update(self, card_id, interval_used, grade, hidden=None) -> int:
        s = self.state.setdefault(card_id, {"ef": 2.5, "reps": 1, "interval": 1})
        q = grade
        # Ease factor update (applied on every review, then floored).
        s["ef"] = max(1.3, s["ef"] + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
        if q < 3:
            s["reps"] = 0
            s["interval"] = 1
        else:
            if s["reps"] == 0:
                s["interval"] = 1
            elif s["reps"] == 1:
                s["interval"] = 6
            else:
                s["interval"] = max(1, round(s["interval"] * s["ef"]))
            s["reps"] += 1
        return s["interval"]


class TargetRetention(Scheduler):
    """
    A stability-tracking policy in the spirit of FSRS. It keeps a running
    *estimate* of each card's stability (from grades only — never the truth) and
    schedules the next review for the interval at which estimated retrievability
    hits a target. Adapts interval length to each card instead of using fixed
    multipliers, which is the whole hypothesis being tested.
    """

    PASS_GAIN = {3: 1.25, 4: 1.7, 5: 2.3}   # grade -> stability-estimate multiplier
    S_INIT = 1.0
    S_FAIL = 0.5

    def __init__(self, target_r: float = 0.85):
        self.target_r = target_r
        self.k = -math.log(target_r)         # interval = k * S_hat
        self.name = f"target-r{int(round(target_r * 100))}"
        self.reset()

    def _interval(self, s_hat: float) -> int:
        return max(1, round(self.k * s_hat))

    def schedule_new(self, card_id, hidden=None) -> int:
        self.state[card_id] = self.S_INIT
        return self._interval(self.S_INIT)

    def update(self, card_id, interval_used, grade, hidden=None) -> int:
        s_hat = self.state.get(card_id, self.S_INIT)
        if grade < 3:
            s_hat = self.S_FAIL
        else:
            s_hat *= self.PASS_GAIN[grade]
        self.state[card_id] = s_hat
        return self._interval(s_hat)


class Oracle(Scheduler):
    """
    Reference ceiling — NOT a real policy. It reads the hidden true stability and
    schedules exactly at the target retrievability. No deployable scheduler can
    beat it on efficiency, so it anchors the 0-100 LAEF outcome scale.
    """

    def __init__(self, target_r: float = 0.85):
        self.target_r = target_r
        self.k = -math.log(target_r)
        self.name = "oracle"
        self.reset()

    def _interval(self, hidden) -> int:
        s = getattr(hidden, "stability", 0.0) or self.k
        return max(1, round(self.k * s))

    def schedule_new(self, card_id, hidden=None) -> int:
        return self._interval(hidden)

    def update(self, card_id, interval_used, grade, hidden=None) -> int:
        return self._interval(hidden)
