---
id: active-recall
name: Active Recall & Card Design
domain: memory
type: method
used_by:
  - agents/learning/spaced-repetition-coach.md
references:
  - https://andymatuschak.org/prompts/
  - Roediger & Karpicke (2006), "Test-Enhanced Learning"
---

# Active Recall & Card Design

Active recall — retrieving information from memory rather than re-reading it — is the single most robust finding in learning science (the "testing effect"). A spaced repetition system is only as good as its cards; this file defines what a good card is.

## Principles of effective cards

1. **One concept per card (minimum information principle).** A card that asks two things will be graded on the weaker one and scheduled wrong for both. Split it.
2. **Question–answer format, retrieval first.** The front must force a retrieval attempt before the answer is visible. "Cloze deletion" (fill-in-the-blank) counts; "read this paragraph" does not.
3. **Concrete over abstract.** "What does the SM-2 ease factor floor prevent?" beats "Explain ease factors."
4. **Answerable in one breath.** If the honest answer takes more than ~10 seconds to produce, the card is too big.
5. **Cue discrimination.** If two cards have similar fronts ("Spanish for *dog*" / "Spanish for *cat*"), recall of one interferes with the other. Make fronts distinctive, or merge into a contrast card.
6. **Two-way when meaningful.** Vocabulary usually deserves both recognition (L2→L1) and production (L1→L2) cards; production is harder and more valuable for speaking goals.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|--------------|-------------|-----|
| List cards ("name all 7 …") | All-or-nothing grading, painful reviews | One card per item + one card for "how many" |
| Orphan facts with no context | Recall without understanding decays into noise | Add a "why does this matter" sibling card |
| Yes/no questions | 50% guess rate masks forgetting | Rephrase as wh-question |
| Copied sentences as answers | Recognizing a sentence ≠ recalling the idea | Rewrite the answer in the user's own words |

## Mnemonics

Offer a mnemonic when a card fails twice consecutively, not preemptively — self-generated associations stick better than supplied ones. Prefer: vivid imagery, absurdity, personal connection, sound-alike bridges for vocabulary.

## Interleaving

Mix topics within a review session rather than blocking by subject. Interleaving feels harder and produces more errors during practice — and measurably better retention. Practical rule for an agent: shuffle due cards across decks by default; only block by topic when the user is cramming for an imminent narrow exam.
