"""
Ground-truth learner model for the spaced-repetition outcome benchmark.

This module simulates a *hidden* human memory. Schedulers under test never see
anything in here directly — they only ever receive the observable signals a real
coach gets: the interval they themselves chose, and a self-grade (0-5) the
"learner" reports after each review. That information barrier is what makes the
benchmark a fair, objective test of scheduling *policy* rather than of who has
read the simulator's source.

The model follows the well-documented DSR framing (Difficulty / Stability /
Retrievability) that underlies modern schedulers such as FSRS, combined with the
classic Ebbinghaus exponential forgetting curve.

    Retrievability after t days since last review:   R = exp(-t / S)

where S is the card's memory *stability* (roughly, its current half-life in
days, scaled). Two mechanics give scheduling its teeth:

  * Spacing effect / desirable difficulty. A successful review strengthens
    memory *more* when it happens at lower R (closer to the edge of forgetting).
    Reviewing a card you can already recall easily (R ~= 1) is nearly wasted.

  * Lapse risk. Recall is a Bernoulli draw on the true R. Wait too long and R
    falls, the draw fails, and stability resets — you have to relearn the card.

So there is a genuine optimum: review late enough to bank the spacing bonus, but
early enough to keep the lapse probability low. A good policy finds it; a rigid
one does not. The constants below are calibrated (see README) so that this
tension actually separates the policies instead of washing out.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field


@dataclass
class ModelParams:
    s0_base: float = 10.0         # initial stability (days) for an easiest (D=1) card
    s0_floor: float = 2.0         # minimum initial stability for the hardest card
    base_growth: float = 1.5      # baseline stability multiplier on any successful review
    spacing_bonus: float = 1.6    # extra multiplier earned by reviewing at low R (spacing effect)
    s_fail_base: float = 4.0      # stability a card relearns to on a lapse (D=1)
    s_fail_floor: float = 1.0     # minimum post-lapse stability (hardest card)

    @staticmethod
    def from_dict(d: dict) -> "ModelParams":
        return ModelParams(**{k: d[k] for k in d if k in ModelParams().__dict__})


@dataclass
class CardState:
    """Hidden ground-truth state for one card. Schedulers must never read this."""
    card_id: str
    difficulty: float             # intrinsic, in [1, 10], fixed for the card's life
    stability: float = 0.0        # current S (days); 0 means not yet learned
    last_review_day: int = 0      # simulation day of the most recent review
    introduced: bool = False
    reviews: int = 0
    lapses: int = 0
    history: list = field(default_factory=list)  # observable (interval, grade) pairs


def _scale_by_difficulty(value_easy: float, floor: float, difficulty: float) -> float:
    """Linearly scale an easiest-card value down toward `floor` as difficulty rises."""
    frac = (11.0 - difficulty) / 10.0          # 1.0 at D=1, 0.1 at D=10
    return floor + (value_easy - floor) * frac


class LearnerModel:
    """A seeded, deterministic simulated learner. One instance per simulated run."""

    def __init__(self, params: ModelParams, seed: int):
        self.p = params
        self.rng = random.Random(seed)

    def retrievability(self, card: CardState, day: int) -> float:
        if not card.introduced or card.stability <= 0:
            return 0.0
        t = max(0, day - card.last_review_day)
        return math.exp(-t / card.stability)

    def introduce(self, card: CardState, day: int) -> None:
        """First exposure: the learner studies the card and learns it this day."""
        card.introduced = True
        card.stability = _scale_by_difficulty(
            self.p.s0_base, self.p.s0_floor, card.difficulty
        )
        card.last_review_day = day
        card.reviews += 1

    def review(self, card: CardState, day: int) -> int:
        """
        Perform a scheduled review. Returns the self-grade (0-5) the learner
        reports — the only outcome signal a scheduler is allowed to observe.
        Mutates the hidden stability according to the DSR update rules.
        """
        R = self.retrievability(card, day)
        success = self.rng.random() < R
        card.reviews += 1

        if success:
            # Every success compounds stability (base_growth), and reviewing at
            # lower R banks an extra spacing bonus. Harder cards earn less of both.
            diff_factor = (11.0 - card.difficulty) / 10.0
            gain = 1.0 + diff_factor * (
                (self.p.base_growth - 1.0) + self.p.spacing_bonus * (1.0 - R)
            )
            card.stability *= gain
            grade = 5 if R >= 0.9 else (4 if R >= 0.7 else 3)
        else:
            card.lapses += 1
            card.stability = _scale_by_difficulty(
                self.p.s_fail_base, self.p.s_fail_floor, card.difficulty
            )
            grade = 2 if R >= 0.5 else 1

        card.last_review_day = day
        return grade
