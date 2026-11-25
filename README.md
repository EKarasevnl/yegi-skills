# yegi-skills

My personal collection of reusable agent skills for Claude Code, Cursor, Codex, and other AI workflows.

## Skills

- [Slide Deck](./slide-deck/) — Builds presentation-ready HTML slide decks, one-pagers, and short animated demos.
- [General Learning Coach](./general-learning-coach/) — Helps me learn through questions and progressive hints instead of jumping straight to answers.
- [Data Science Research Coach](./ds-research-coach/) — Helps frame ML and business problems, investigate model behavior, design rigorous experiments, and develop independent DS judgment across competitions, research, and work.
- [Code Ownership](./code-ownership/) — Keeps agent-written changes reviewable with one-slice-at-a-time checkpoints, code-tracing questions, and hands-on practice. [Setup](./code-ownership/README.md).

Each skill is a folder containing `SKILL.md` and, optionally, reference files. Install the **whole folder**, not just `SKILL.md`, to preserve its references.

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:EKarasevnl/yegi-skills.git
cd yegi-skills
```

The repository is private, so the command assumes your SSH key has access. Alternatively, clone with your authenticated HTTPS GitHub credentials.

### 2. Install skills for your agent

Choose **global** installation (available in your other projects on this computer) or **project-local** installation (available only in the target project).

| Agent | Global skills directory | Project-local skills directory |
| --- | --- | --- |
| **Claude Code** | `~/.claude/skills/` | `<project>/.claude/skills/` |
| **Cursor** | `~/.cursor/skills/` | `<project>/.cursor/skills/` |
| **Codex** | `~/.agents/skills/` | `<project>/.agents/skills/` |

For **global** installation of all four skills, run the commands for your chosen agent **from inside the cloned `yegi-skills` directory**.

**Claude Code**

```bash
mkdir -p ~/.claude/skills
cp -R general-learning-coach ds-research-coach code-ownership slide-deck ~/.claude/skills/
```

**Cursor**

```bash
mkdir -p ~/.cursor/skills
cp -R general-learning-coach ds-research-coach code-ownership slide-deck ~/.cursor/skills/
```

**Codex**

```bash
mkdir -p ~/.agents/skills
cp -R general-learning-coach ds-research-coach code-ownership slide-deck ~/.agents/skills/
```

To install just one skill, replace the two names in the `cp` command with the name you want.

For **project-local** installation, use the same `cp -R` command but target the relevant `<project>/.claude/skills/`, `<project>/.cursor/skills/`, or `<project>/.agents/skills/` directory instead.

> **Tip:** Cursor also reads `.agents/skills/` and `~/.agents/skills/` locally, so a Codex installation can work in local Cursor too. However, to sync personal skills to **Cursor Cloud Agents**, install them in `~/.cursor/skills/` and enable **Settings → Agents → Sync Skills for Cloud Agents**. Project-local `.cursor/skills/` can be committed with the target project for team/cloud use.

### 3. Use a skill

Open a project in your agent, then explicitly invoke a skill or ask a question that matches its description. For example:

**General Learning Coach**

```text
Use the general-learning-coach skill. Help me reason through this problem with one question at a time and avoid spoilers.
```

**Slide Deck**

```text
Use the slide-deck skill. Create a clear HTML slide deck for this topic, following the skill's design and render-check process.
```

**Data Science Research Coach**

```text
Use the ds-research-coach skill. Read our existing experiment results, help me frame the problem, and guide me through hypotheses and rigorous experiments before suggesting model tweaks.
```

In **Codex**, you can also explicitly invoke the DS skill with `$ds-research-coach`. In **Claude Code** and **Cursor**, use the skill picker/invocation UI when available, or simply reference the skill by name in your prompt.

If the skill does not appear, open a new agent session or reload the application, and confirm that `<skills-directory>/<skill-name>/SKILL.md` exists.

### 4. Update your installed skills

```bash
cd /path/to/yegi-skills
git pull
```

Then repeat your agent's `cp -R` installation command. If you removed or renamed files in a skill, remove its old installed folder before copying the updated folder to avoid stale files.

## Official installation references

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Codex skills](https://developers.openai.com/codex/skills)
