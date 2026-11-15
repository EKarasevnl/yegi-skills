# General Learning Coach — POC v0.1

This is a **standalone, domain-agnostic** learning-coach instruction set, built from a competitive-programming tutoring workflow but usable in ML, mathematics, reading papers, statistics, languages, and other study settings.

## Files
- `SKILL.md`: the reusable instruction set, with skill metadata and behavioral rules.

## How to use
- **Codex (globally):** put this directory at `~/.agents/skills/general-learning-coach/`.
- **Codex (per repository):** put this directory at `.agents/skills/general-learning-coach/` in the repository.
- **ChatGPT Projects or custom assistants:** add the contents of `SKILL.md` to the assistant instructions, or attach it as context if supported.
- **In conversation:** say “Use General Learning Coach for this session. I want to learn, not outsource the thinking.”

Example prompts:
- **“Coach me; no spoilers. Here's what I've tried: ...”**
- **“Teach me from scratch, then make me apply it.”**
- **“Just explain the answer.”**

Native skill discovery and installation depend on the environment. Adding this directory does not configure every ChatGPT conversation automatically.

## What to test
1. Start a new ML concept with zero background: teach a prerequisite and check application, rather than interrogating.
2. Bring a partially solved math/programming problem: ask one targeted, non-leading question without revealing the trick.
3. Get stuck for two turns: adapt or increase specificity, instead of looping.
4. Finish a task: elicit a transferable lesson and offer an optional variation.
5. Say “just explain”: immediately stop withholding.

## Evolution
After 5–10 sessions, revise against real friction: hints that reveal too much, questions that stall, weak postmortems, or poor transfer tests. Keep the skill lean and practical.
