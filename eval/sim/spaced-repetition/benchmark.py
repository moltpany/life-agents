#!/usr/bin/env python3
"""
Spaced-repetition OUTCOME benchmark — the objective track of LAEF.

The behavioral suite in eval/benchmark/spaced-repetition-coach.yaml asks "does
the agent compute SM-2 correctly?". This asks the deeper question a directory of
agents actually needs answered: "is the scheduling policy any good, and how does
it compare to the alternatives?" — measured against a hidden ground-truth memory
with hard, reproducible numbers.

Run:
    python3 benchmark.py                 # uses config.json, writes results
    python3 benchmark.py --quiet         # no stdout table
    python3 benchmark.py --regen-deck    # regenerate deck.json from deck_seed

Everything is standard-library and fully seeded: same inputs, same numbers.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import statistics
from datetime import date

from model import CardState, LearnerModel, ModelParams
from schedulers import FixedInterval, Leitner, SM2, TargetRetention, Oracle

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "results", "spaced-repetition"))


def load_config() -> dict:
    with open(os.path.join(HERE, "config.json")) as f:
        return json.load(f)


def build_deck(cfg: dict) -> list[dict]:
    """Reproducibly generate a deck of cards with a spread of difficulties."""
    rng = random.Random(cfg["deck_seed"])
    deck = []
    for i in range(cfg["deck_size"]):
        # Triangular over [1, 10] peaked at 5: most cards are middling, a few are
        # very easy and a few genuinely hard — the hard tail is where policies diverge.
        d = round(rng.triangular(1, 10, 5), 1)
        deck.append({"id": f"c{i:03d}", "difficulty": d})
    return deck


def load_deck(cfg: dict, regen: bool) -> list[dict]:
    path = os.path.join(HERE, "deck.json")
    if regen or not os.path.exists(path):
        deck = build_deck(cfg)
        with open(path, "w") as f:
            json.dump({"deck_seed": cfg["deck_seed"], "cards": deck}, f, indent=2)
    with open(path) as f:
        return json.load(f)["cards"]


def run_once(scheduler, deck, params: ModelParams, cfg: dict, seed: int) -> dict:
    """Simulate one learner over the full horizon under one scheduling policy."""
    learner = LearnerModel(params, seed)
    cards = {c["id"]: CardState(c["id"], c["difficulty"]) for c in deck}
    scheduler.reset()

    order = [c["id"] for c in deck]
    due_day: dict[str, int] = {}
    next_new = 0
    horizon = cfg["horizon_days"]

    for day in range(horizon):
        # Introduce the day's new cards (first study session).
        for _ in range(cfg["new_per_day"]):
            if next_new >= len(order):
                break
            cid = order[next_new]
            next_new += 1
            card = cards[cid]
            learner.introduce(card, day)
            due_day[cid] = day + scheduler.schedule_new(cid, hidden=card)

        # Review everything due today.
        for cid, card in cards.items():
            if card.introduced and due_day.get(cid, horizon + 1) <= day:
                prev = card.last_review_day
                grade = learner.review(card, day)
                interval = scheduler.update(cid, day - prev, grade, hidden=card)
                due_day[cid] = day + interval

    introduced = [c for c in cards.values() if c.introduced]
    n = len(introduced)
    retention = statistics.fmean(learner.retrievability(c, horizon) for c in introduced)
    total_reviews = sum(c.reviews for c in introduced)
    total_lapses = sum(c.lapses for c in introduced)
    return {
        "retention": retention,
        "reviews_per_card": total_reviews / n,
        "lapses_per_card": total_lapses / n,
    }


def aggregate(scheduler, deck, params, cfg) -> dict:
    runs = [run_once(scheduler, deck, params, cfg, s) for s in cfg["seeds"]]
    out = {"scheduler": scheduler.name}
    for k in ("retention", "reviews_per_card", "lapses_per_card"):
        vals = [r[k] for r in runs]
        out[k] = statistics.fmean(vals)
        out[k + "_std"] = statistics.pstdev(vals)
    out["efficiency"] = out["retention"] / out["reviews_per_card"]
    return out


def pareto_front(rows: list[dict]) -> set[str]:
    """Names of schedulers not dominated on (higher retention, fewer reviews)."""
    front = set()
    for a in rows:
        dominated = any(
            b["retention"] >= a["retention"]
            and b["reviews_per_card"] <= a["reviews_per_card"]
            and (b["retention"] > a["retention"] or b["reviews_per_card"] < a["reviews_per_card"])
            for b in rows
        )
        if not dominated:
            front.add(a["scheduler"])
    return front


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--regen-deck", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    params = ModelParams.from_dict(cfg["model"])
    deck = load_deck(cfg, args.regen_deck)
    tr = cfg["target_r"]

    schedulers = [
        FixedInterval(1),
        Leitner(),
        SM2(),
        TargetRetention(tr),
        Oracle(tr),
    ]

    rows = [aggregate(s, deck, params, cfg) for s in schedulers]
    oracle_eff = next(r["efficiency"] for r in rows if r["scheduler"] == "oracle")
    for r in rows:
        r["laef_outcome"] = max(0, min(100, round(100 * r["efficiency"] / oracle_eff)))

    real = [r for r in rows if r["scheduler"] != "oracle"]
    front = pareto_front(real)
    for r in rows:
        r["pareto_optimal"] = r["scheduler"] in front

    rows.sort(key=lambda r: r["laef_outcome"], reverse=True)

    results = {
        "benchmark": "spaced-repetition-outcome",
        "version": 1,
        "generated": date.today().isoformat(),
        "harness": "eval/sim/spaced-repetition/benchmark.py",
        "config": {
            "horizon_days": cfg["horizon_days"],
            "deck_size": cfg["deck_size"],
            "new_per_day": cfg["new_per_day"],
            "seeds": len(cfg["seeds"]),
            "target_r": tr,
            "model": cfg["model"],
            "deck_seed": cfg["deck_seed"],
        },
        "metrics_glossary": {
            "retention": "mean true retrievability across all cards at the horizon (0-1); higher is better",
            "reviews_per_card": "total reviews performed per card over the horizon; lower is less work",
            "lapses_per_card": "times a card was forgotten and had to be relearned; lower is better",
            "efficiency": "retention / reviews_per_card",
            "laef_outcome": "efficiency as a percentage of the cheating Oracle's efficiency (0-100)",
            "pareto_optimal": "true if no other real policy gets higher retention for equal-or-fewer reviews",
        },
        "results": rows,
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    write_scorecard(results)

    if not args.quiet:
        print_table(rows)


def print_table(rows):
    hdr = f"{'scheduler':<12}{'LAEF':>6}{'retention':>12}{'rev/card':>11}{'lapse/card':>12}{'pareto':>8}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(
            f"{r['scheduler']:<12}{r['laef_outcome']:>6}"
            f"{r['retention']:>11.3f} {r['reviews_per_card']:>10.2f} "
            f"{r['lapses_per_card']:>11.2f} {'  yes' if r['pareto_optimal'] else '   - ':>8}"
        )


def write_scorecard(results):
    rows = results["results"]
    cfg = results["config"]
    lines = []
    lines.append("# Spaced-Repetition Outcome Scorecard")
    lines.append("")
    lines.append(f"_Generated {results['generated']} by `{results['harness']}` — "
                 "fully reproducible (`python3 benchmark.py`)._")
    lines.append("")
    lines.append(
        f"Each policy schedules the **same {cfg['deck_size']}-card deck** for the "
        f"**same {cfg['horizon_days']}-day horizon**, averaged over "
        f"**{cfg['seeds']} seeded simulated learners**. Schedulers see only the intervals "
        f"they chose and the learner's self-grades — never the hidden memory state. "
        f"Target retrievability: {cfg['target_r']}."
    )
    lines.append("")
    lines.append("| Rank | Policy | LAEF outcome | Retention @180d | Reviews/card | Lapses/card | Pareto |")
    lines.append("|-----:|--------|-------------:|----------------:|-------------:|------------:|:------:|")
    for i, r in enumerate(rows, 1):
        star = " ⭐" if r["scheduler"] == "oracle" else ""
        pareto = "✅" if r["pareto_optimal"] else "—"
        lines.append(
            f"| {i} | `{r['scheduler']}`{star} | **{r['laef_outcome']}** | "
            f"{r['retention']:.3f} ± {r['retention_std']:.3f} | "
            f"{r['reviews_per_card']:.2f} | {r['lapses_per_card']:.2f} | {pareto} |"
        )
    lines.append("")
    lines.append("`oracle` cheats (reads the true memory state) and defines the 100-point "
                 "efficiency ceiling; it is not a deployable policy. Everything else is.")
    lines.append("")
    sm2 = next((r for r in rows if r["scheduler"] == "sm2"), None)
    tr = next((r for r in rows if r["scheduler"].startswith("target-r")), None)
    if sm2 and tr:
        lines.append("## What this says about the agent's claim")
        lines.append("")
        lines.append(
            f"The Spaced Repetition Coach agent advertises **SM-2**. On this benchmark SM-2 "
            f"scores **{sm2['laef_outcome']}/100** ({sm2['retention']:.2f} retention at "
            f"{sm2['reviews_per_card']:.1f} reviews/card), while a target-retention policy "
            f"scores **{tr['laef_outcome']}/100** ({tr['retention']:.2f} at "
            f"{tr['reviews_per_card']:.1f} reviews/card). "
        )
        if tr["laef_outcome"] > sm2["laef_outcome"]:
            lines.append(
                "The objective gap is the kind of evidence the directory exists to surface: "
                "a faithful SM-2 implementation is *correct* yet leaves measurable efficiency "
                "on the table versus a stability-tracking scheduler."
            )
        else:
            lines.append(
                "SM-2 holds up well here — useful evidence in the other direction: the agent's "
                "advertised method is objectively competitive, not just popular."
            )
    lines.append("")
    lines.append("See [eval/sim/spaced-repetition/README.md](../../sim/spaced-repetition/README.md) "
                 "for the memory model, fairness barrier, and calibration notes.")
    lines.append("")
    with open(os.path.join(RESULTS_DIR, "scorecard.md"), "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
