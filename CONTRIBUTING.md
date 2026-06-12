# Contributing to Life Agents

Thanks for wanting to contribute! Life Agents grows through community — every hobby, skill, and corner of human life deserves a great agent.

There are **three ways to contribute**, in increasing order of effort:

1. **A skill** — you know a domain deeply (fishing seasons, watercolor technique, marathon training) but don't want to design a persona. Write the methodology file; someone else can build the agent on it.
2. **An agent** — a full persona built on one or more skills.
3. **Benchmark cases** — test cases that make existing agents' scores trustworthy. The most undervalued contribution.

---

## Adding a skill

1. Copy [`templates/skill-template.md`](templates/skill-template.md) to `skills/<domain>/<id>.md`
2. Write the full methodology: core rules, worked examples, edge cases, **honest limitations**
3. Cite upstream sources — methods, not vibes
4. Add the skill to the `skills` array in `index.json`
5. Open a PR titled `[New Skill] Your Skill Name`

## Adding an agent

1. Pick a 💡 cell from the [README matrix](README.md#the-agent-matrix) or the [Issues](../../issues) board
2. Copy [`templates/agent-template.md`](templates/agent-template.md) to the right domain folder:
   - `agents/learning/` — study, languages, exams, reading
   - `agents/creative/` — writing, music, art, photography
   - `agents/health/` — fitness, sleep, mindfulness
   - `agents/hobbies/` — gardening, games, collecting, sports
   - `agents/life/` — cooking, budgeting, travel, home
   - `agents/social/` — gifts, gatherings, family occasions
3. **Write the methodology as a skill file first** (or reference an existing one) — personas stay thin, skills stay deep
4. Fill in all sections. The System Prompt must be self-contained and deployable as-is
5. **Write a benchmark suite** at `eval/benchmark/<id>.yaml` — at least 8 cases covering method correctness, memory schema, scope refusal, and safety (see [eval/benchmark/README.md](eval/benchmark/README.md))
6. Self-score with [LAEF](EVALUATION.md), provenance `self-reported`
7. **Update `index.json`** — add your agent (and any new skills) with raw URLs. PRs that don't update the registry will be asked to
8. Open a PR titled `[New Agent] Your Agent Name`

## Adding benchmark cases

Open a PR adding cases to any `eval/benchmark/*.yaml`. Good cases are *discriminating* (a sloppy persona fails, a faithful one passes) and *judgeable* (two reviewers would agree on pass/fail). Adversarial prompts — users asking the agent to break its own method — are gold.

---

## Review process

- Community reviewers validate scores within 7 days; validated scores graduate from `self-reported` to `community-reviewed`
- Agents scoring below ⭐⭐ are moved to `agents/incubating/`
- Evaluation scores can be challenged via issue — re-running the benchmark suite settles it

## What we're looking for

✅ Clear persona with defined scope boundaries
✅ Domain knowledge backed by real methods (not vibes), written into `skills/`
✅ Non-work focus — the more unusual the hobby, the better
✅ Honest evaluation, including known limitations
✅ A benchmark suite that would catch a broken implementation

## What we're not looking for

❌ Work / productivity / coding agents (many great repos for those already)
❌ Generic "helpful assistant" prompts without a specific domain
❌ Agents that ignore scope boundaries
❌ Agents without a completed LAEF scorecard and benchmark suite
❌ Skills without sources

---

## Improving existing agents

Open an issue tagged `[Improvement]`, or submit a PR directly if the change is small. If you change an agent's method, update its skill file and benchmark cases in the same PR.

## Code of Conduct

Be kind. This is a space for people who care about the non-work parts of life. Keep discussions on-topic and constructive.
