# Data Science Thinking & Research Coach — Codex Skill

A reusable learning-first partner for **professional Data Science**, applied ML research, competitions and hackathons. Helps frame problems, understand data, build hypotheses, design discriminating tests and turn evidence into decisions. It does not default to a list of architectures or ensembles.

## Install globally (all projects)

Clone the repository, then:

```bash
mkdir -p ~/.agents/skills
cp -R ds-research-coach ~/.agents/skills/
```

Or install in a single project at `.agents/skills/ds-research-coach/`.

## Kickoff (works in any DS repository)

```text
$ds-research-coach Help me approach this Data Science problem systematically. Inspect relevant project context, distinguish facts from assumptions, and help me frame the objective and identify the most consequential unknown. Coach my reasoning, one question at a time; don't jump straight to modeling tricks.
```

## Specific examples

**Work:**
```text
$ds-research-coach work: We need to improve a promotions targeting process. Start with the business decision and causal vs predictive objective, then help me decide which evidence and experiments we need.
```

**Competition:**
```text
$ds-research-coach competition: Inspect our experiment history. Pick one unexplained result and guide me through hypotheses and a discriminating experiment, rather than immediately proposing an ensemble.
```

**Research:**
```text
$ds-research-coach research: Help me evaluate whether this result supports a new scientific claim. Challenge the assumptions and help design strong baselines and falsification tests.
```

**Shortcuts:** `frame`, `diagnose`, `brainstorm`, `design`, `critique`, `execute`, `teach`. Direct requests for brainstorming and implementation are honored rather than blocked by coaching.
