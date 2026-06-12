# LAEF Benchmark Suites

Each agent in this collection ships with a behavioral test suite: `<agent-id>.yaml`.

## Why behavior descriptions, not expected answers

Life agents rarely have a single correct output — there is no canonical reply to "my monstera has yellow leaves." But there are **decidable behavioral boundaries**: did the agent apply its stated method correctly? Did it ask before prescribing? Did it refuse what's out of scope without being useless? Test cases therefore specify *expected behavior* and *failure modes*, not answer strings.

## Case format

```yaml
suite: <agent-id>
agent: agents/<domain>/<agent-id>.md
version: 1
cases:
  - id: <suite-prefix>-NNN
    category: method_correctness   # one of the Layer 1 checks, see below
    prompt: |
      <the user message, with any conversation state stated inline>
    expected_behavior: |
      <what a passing response does — observable, judgeable properties>
    failure_modes:
      - <a concrete way responses go wrong>
```

`category` maps to the LAEF Layer 1 objective checks ([EVALUATION.md](../../EVALUATION.md)):

| Category | Tests |
|----------|-------|
| `domain_adherence` | Stays inside the stated domain |
| `method_correctness` | Applies its stated methodology correctly (math, protocols, ordering) |
| `memory_schema` | Reads/updates its declared memory fields correctly |
| `scope_refusal` | Declines out-of-scope requests gracefully and redirects |
| `safety` | Never produces physically or psychologically harmful advice |

## How to run a suite

**Manually (now):** load the agent's system prompt into any capable model, send each case's prompt, judge the response against `expected_behavior` and `failure_modes`. One pass/fail per case; suite pass rate feeds the Reliability and role-specific scores.

**Automated (roadmap stage 2):** a judge-model harness runs every case, scores it, and writes the full conversation trace to `eval/results/`. Scores with published traces graduate from `self-reported` to `auto-evaluated`.

## Contributing cases

Benchmark contributions are especially welcome — they're how scores become trustworthy. Good cases are *discriminating* (a sloppy persona fails them, a faithful one passes) and *judgeable* (two reviewers would agree on pass/fail). Edge cases and adversarial prompts (users asking the agent to break its own method) are gold.
