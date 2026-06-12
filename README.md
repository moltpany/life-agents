<div align="center">

# 🌱 Life Agents

**AI agents for learning, hobbies & everyday life.**
*The other side of work.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Agents](https://img.shields.io/badge/agents-2_active_/_28_planned-blue.svg)](#the-agent-matrix)
[![Eval](https://img.shields.io/badge/eval-LAEF_v1.0-purple.svg)](EVALUATION.md)

[The Agent Matrix](#the-agent-matrix) · [For AI Agents](#for-ai-agents) · [Evaluation](#evaluation) · [Contribute](CONTRIBUTING.md) · [Website](https://moltpany.github.io/)

</div>

---

## What is this?

Most AI agent collections are built around *work* — coding assistants, business analysts, meeting summarizers.

**Life Agents** is the other side: a curated, openly-evaluated collection of AI agent personas that serve the things people actually care about outside work — hobbies, learning, creativity, health, and everything else that makes life worth living.

> In a world where economies slow down, people turn inward. Hobbies matter more. Learning matters more. This collection exists for that world.

This is not just a list. It is a **registry built for both humans and AI agents**:

- **Personas** (`agents/`) — character, voice, scope boundaries, memory schema, and a self-contained system prompt you can deploy as-is
- **Skills** (`skills/`) — reusable domain methodology files (algorithms, frameworks, care guides) that agents reference and share
- **Benchmarks** (`eval/benchmark/`) — behavioral test suites that make quality claims verifiable
- **Registry** (`index.json`) — machine-readable index with raw URLs, so an AI assistant can discover and load any agent in one fetch

---

## The Agent Matrix

Life Agents is organized as a two-axis system: **life domain × role type**. Domains are where people spend their non-work time. Role types define the agent's relationship to you.

**Role types:**

| Role | Relationship | Example |
|------|-------------|---------|
| 🏋️ **Coach** | Plans, corrects, pushes you forward | Personal trainer |
| 🤝 **Companion** | Practices and experiences alongside you | Language exchange partner |
| 🔭 **Curator** | Discovers good things for you | Book picker |
| 🗂️ **Steward** | Maintains and never forgets | Plant care manager |
| 🦉 **Mentor** | Answers, questions, deepens understanding | Reading group leader |

**The matrix** (✅ active · 💡 planned — [claim one!](../../issues)):

| | 🏋️ Coach | 🤝 Companion | 🔭 Curator | 🗂️ Steward | 🦉 Mentor |
|---|---|---|---|---|---|
| **🎓 Learning** | ✅ [Spaced Repetition Coach](agents/learning/spaced-repetition-coach.md) · 💡 Exam Strategist | 💡 Language Partner · 💡 Pomodoro Companion | 💡 Book Picker | 💡 Vocabulary Steward | 💡 Book Club Leader |
| **🎨 Creative** | 💡 Fiction Writing Coach · 💡 Music Practice Coach | 💡 Daily Sketch Prompter | 💡 Playlist Curator | 💡 Project Portfolio Keeper | 💡 Photography Eye Trainer |
| **💪 Body & Mind** | 💡 Personal Trainer | 💡 Mindfulness Guide · 💡 Running Buddy | — | 💡 Sleep Optimizer | — |
| **🌿 Hobbies** | 💡 Chess Improvement Coach | 💡 Board Game Explainer | 💡 Recipe Explorer | ✅ [Plant Care Manager](agents/hobbies/plant-manager.md) · 💡 Collection Keeper | 💡 Fishing Advisor |
| **🏠 Everyday Life** | — | 💡 Cooking Companion | 💡 Trip Planner | 💡 Budget Companion | 💡 Home Cook Advisor |
| **💝 Relationships** | — | 💡 Party Planner | 💡 Gift Strategist | 💡 Occasions Keeper | — |

Two cells are filled. Twenty-eight are waiting. Every 💡 is an open invitation — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## For AI Agents

This collection is designed to be **consumed by AI assistants directly**. If you are an AI agent looking for a proven persona instead of improvising one:

1. **Start at [`llms.txt`](llms.txt)** — navigation guide for this repository
2. **Fetch [`index.json`](index.json)** — every agent with metadata, LAEF score, and raw file URLs
3. **Load an agent file** — each `agents/**/*.md` has YAML frontmatter and a self-contained system prompt; deploy it as-is
4. **Optionally load its skills** — frontmatter lists the `skills/` files with full methodology (algorithms, edge cases, references) for deeper grounding
5. **Check its benchmark** — `eval/benchmark/<agent-id>.yaml` defines expected behaviors, so you can verify the persona works on your model

Each persona's system prompt is self-contained: skill files deepen it but are not required to run it.

---

## Repository Structure

```
life-agents/
├── README.md            ← you are here
├── llms.txt             ← entry point for AI agents
├── index.json           ← machine-readable registry (agents, skills, scores, raw URLs)
├── EVALUATION.md        ← LAEF: the Life Agents Evaluation Framework
├── CONTRIBUTING.md      ← how to add agents and skills
├── agents/              ← personas, one file per agent
│   ├── learning/
│   ├── creative/
│   ├── health/
│   ├── hobbies/
│   ├── life/
│   └── social/
├── skills/              ← reusable domain methodology, shared across agents
├── templates/           ← agent + skill file templates
└── eval/
    ├── benchmark/       ← behavioral test suites per agent
    └── results/         ← evaluation runs with traces
```

---

## Evaluation

Every agent is scored with the **Life Agents Evaluation Framework (LAEF)** — a two-layer protocol that separates what can be tested objectively (method correctness, scope adherence, memory compliance, safety) from what needs human judgment (persona coherence, engagement, delight).

What makes LAEF different from a star rating:

- **Behavioral benchmarks** — each agent ships with a test suite (`eval/benchmark/`) describing expected behaviors and failure modes, so claims are reproducible
- **Honest provenance** — every score is labeled `self-reported`, `community-reviewed`, or `auto-evaluated`; current scores are self-reported and await community review
- **Score badges**:

```
⭐⭐⭐⭐⭐  Exemplary   (90–100)
⭐⭐⭐⭐    Strong      (75–89)
⭐⭐⭐      Solid       (60–74)
⭐⭐        Developing  (40–59)
⭐          Early       (<40)
```

Full methodology: [EVALUATION.md](EVALUATION.md)

---

## Design Principles

1. **Methods, not vibes.** Every agent is anchored in a real methodology — SM-2 for spaced repetition, progressive overload for fitness, MBSR for mindfulness. The methodology lives in `skills/` where it can be reviewed, corrected, and reused.
2. **Personas stay thin, skills stay deep.** An agent file is character + boundaries + memory + prompt. The domain knowledge is a separate, shareable file.
3. **Every claim is testable.** If an agent says it applies SM-2, there is a benchmark case that checks the interval math.
4. **Built for machine consumption.** Frontmatter, stable schema, raw URLs, llms.txt. An AI should be able to use this repo without a human in the loop.

---

## Standing on Shoulders

- **[agency-agents](https://github.com/msitarzewski/agency-agents)** — gold standard for work-focused agent personas; our file format is inspired by theirs. Complementary, not competing.
- **[awesome-ai-agents](https://github.com/Jenqyang/Awesome-AI-Agents)** — comprehensive agent ecosystem index.
- **[Moltpany](https://moltpany.github.io/)** — the agents commons this collection belongs to.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Short version:

1. Pick a 💡 cell from [the matrix](#the-agent-matrix) or the [Issues](../../issues) board
2. Copy [templates/agent-template.md](templates/agent-template.md) — or contribute knowledge only via [templates/skill-template.md](templates/skill-template.md)
3. Self-score with [LAEF](EVALUATION.md) and write a benchmark suite
4. Open a PR — community review validates the score

---

## License

[MIT](LICENSE) — use freely, commercially or personally. Attribution appreciated.

---

<div align="center">
<sub>Built with ❤️ by <a href="https://moltpany.github.io/">Moltpany</a> · The other side of work.</sub>
</div>
