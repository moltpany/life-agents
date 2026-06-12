---
id: # kebab-case, unique, matches filename
name: # Display name
domain: # learning | creative | health | hobbies | life | social
role: # coach | companion | curator | steward | mentor
status: active
version: 0.1.0
skills: [] # paths to skills/ files this agent uses, e.g. skills/memory/sm2-algorithm.md
benchmark: # eval/benchmark/<id>.yaml
laef:
  score: # 0–100
  badge: # exemplary | strong | solid | developing | early
  provenance: self-reported
  scored_by: # your GitHub handle
  date: # YYYY-MM-DD
tags: [] # 3–6 lowercase keywords
---

# [Agent Name]

> One-sentence description of what this agent does and who it's for.

## Identity

- **Role type**: <!-- Coach / Companion / Curator / Steward / Mentor -->
- **Domain**: <!-- e.g., Language Learning, Home Gardening -->
- **Persona**: <!-- 2–3 sentences. Who is this agent? What's their character? -->
- **Voice**: <!-- e.g., warm and encouraging, precise and concise, playful but knowledgeable -->
- **Scope boundaries**: This agent does NOT...
  - <!-- e.g., give medical diagnoses -->
  - <!-- e.g., recommend specific financial products -->

## Skills

<!-- Link the skills/ files this agent depends on. If the methodology doesn't
     exist in skills/ yet, write it there first (templates/skill-template.md) —
     that's the reusable, reviewable part. -->

| Skill | What it provides |
|-------|-----------------|
| [Skill name](../../skills/...) | |

## Tools

<!-- External tools, APIs, or utilities this agent uses or recommends -->

-

## Memory Schema

<!-- What this agent needs to remember across sessions -->

- `user.goal` —
- `user.level` —
- `user.history[]` —
- `user.preferences` —

## System Prompt

<!-- MUST be self-contained: deployable as-is without fetching the skill files.
     Embed the operative rules of your methodology here; the skills/ files
     carry the full version (derivations, edge cases, references). -->

```
[Complete system prompt: persona, method rules, session structure, constraints, scope refusals.]
```

## Example Interaction

**User:** <!-- Sample first message -->

**Agent:** <!-- Sample response that demonstrates the persona and method -->

## LAEF Evaluation Scorecard

<!-- Score against EVALUATION.md. Role-specific dimensions depend on your role type. -->

| Dimension | Score (0–100) | Notes |
|-----------|--------------|-------|
| Reliability | | |
| Safety | | |
| Clarity | | |
| Memory | | |
| *(Role-specific 1)* | | |
| *(Role-specific 2)* | | |
| *(Role-specific 3)* | | |
| **Overall** | | |

**Badge**: <!-- ⭐ / ⭐⭐ / ⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐ -->

*Provenance: self-reported — scored by <!-- handle --> on <!-- date -->. Community review: pending.*
*Benchmark suite: [eval/benchmark/<id>.yaml](../../eval/benchmark/)*

## References

- Method: <!-- links to your skills/ files -->
- Upstream sources:
- Related agents in this collection:
