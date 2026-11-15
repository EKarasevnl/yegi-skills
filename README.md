# yegi-skills

**A growing collection of practical AI-agent skills for learning, coding, research, and everyday workflows.**

This repository is where I develop and refine reusable instructions that help AI assistants become better collaborators — not just better answer generators. Each skill is built around a real need, tested in practice, and iterated as shortcomings become clear.

The goal is to keep skills **useful, portable, and opinionated**, without making everyday tasks unnecessarily complicated.

## Skills

| Skill | What it does | Status |
| --- | --- | --- |
| [General Learning Coach](./general-learning-coach/) | Helps you learn without outsourcing the thinking: diagnoses your reasoning, asks focused questions, protects important discoveries, escalates hints, and extracts transferable lessons after a breakthrough. | v0.1 · POC |

This is the first skill in the collection. More will be added as real workflows justify them.

## Philosophy

- **Build independence.** Good assistance should strengthen judgment and capability, not create dependence.
- **Prefer the smallest useful intervention.** Sometimes that means a question, sometimes a hint, sometimes a direct answer.
- **Design for actual workflows.** Improve instructions from real sessions rather than theoretical perfection.
- **Keep skills modular.** Each lives in its own directory and can evolve independently.

## Structure

```text
yegi-skills/
├── general-learning-coach/
│   ├── SKILL.md
│   └── README.md
├── LICENSE
└── README.md
```

## Using a skill

Each skill has a `SKILL.md` with its behavioral instructions and a local `README.md` explaining the intended use.

For **Codex**, install a skill directory under `~/.agents/skills/` for personal use, or `.agents/skills/` inside a repository. For **ChatGPT Projects** and other assistants, use the skill instructions as project/custom instructions where supported.

Different assistants may support different skill-discovery mechanisms. See the skill's own README for details.

## Development

Skills in this repository are experiments, not finished products. Feedback from real usage — especially when the assistant overhelps, underhelps, or misunderstands intent — should drive revisions.

## License

See [LICENSE](./LICENSE).
