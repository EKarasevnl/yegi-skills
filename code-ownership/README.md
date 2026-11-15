# Code Ownership (POC v0.1)

Personal Claude Code skill + optional hook for keeping AI-generated changes small enough to understand, and using those changes to develop engineering ability.

## What the hook does

Hooks are scripts Claude Code runs at particular events. The included gate uses:

- **PreToolUse:** blocks agent editing and shell commands while a project is **locked**. Read/Grep/Glob remain available for coaching and inspection.
- **PostToolUse:** checks the cumulative Git diff against a backup line-change budget; after the budget is reached, it locks the project. This is a **post-edit** check and can overshoot in a single call.
- **Stop:** locks the current slice when Claude finishes a turn **with code changes**, so it cannot silently continue implementing.

The hook is **opt-in, per Git repository**. It leaves other repositories alone. No third-party Python packages required.

## Quick start — normal everyday setup (macOS / Cursor + Claude Code)

**Install once; enable the edit gate only in projects you choose.** The skill is available in every Claude Code session, but the hook will not interfere with a repository until you run `init` there.

### 1. Install the skill

```bash
git clone git@github.com:EKarasevnl/yegi-skills.git
cd yegi-skills
mkdir -p ~/.claude/skills
ln -s "$(pwd)/code-ownership" ~/.claude/skills/code-ownership
```

Use `cp -R code-ownership ~/.claude/skills/` instead of `ln -s` if you prefer a standalone copy. If you already have a skill at that path, inspect it instead of overwriting it. The symlink makes future `git pull` updates available locally. In Cursor, use the **Claude Code extension**; the hook configuration below is for Claude Code, not Cursor's native Agent.

### 2. Enable hooks globally (recommended default)

Open `~/.claude/settings.json` and **merge** the `hooks` object from [`hooks/settings.example.json`](./hooks/settings.example.json) into it; keep your existing settings and hook entries. The example runs Python 3 from `~/.claude/skills/code-ownership/hooks/ownership.py` on `PreToolUse`, `PostToolUse`, and `Stop`.

This is a *global hook installation*, not a global lock: repositories without an initialized ownership state are unaffected. To limit hook loading to **one test project** instead, merge the same configuration into that project's `.claude/settings.local.json` (do not commit personal configuration).

### 3. Make ownership coaching the default for substantial code changes (optional)

Skill installation and hook installation do **not** guarantee automatic skill invocation. For the behavior to be the default in your Claude Code sessions, add this short instruction to `~/.claude/CLAUDE.md` (create it if necessary, and preserve any existing content):

```markdown
For nontrivial coding tasks, use the code-ownership skill by default. Propose small, coherent implementation slices; implement just one slice per approval. After each slice, guide me through the actual diff with 5 questions by default (max 10, one at a time), including a small independent modification when useful. Do not immediately rescue me by writing my practice change. Require my explicit approval before the next slice. Avoid giant agent-facing documentation. Keep trivial edits and urgent fixes fast.
```

If you don't want the default, omit this instruction and invoke `/code-ownership` (or ask to use the skill) only when needed. Start a fresh Claude Code session after changing settings, and check `/hooks` to confirm that the commands are loaded.

### 4. Activate ownership gates in a test repository

From the **target project's terminal** (not inside the agent), with a clean Git working tree:

```bash
python3 ~/.claude/skills/code-ownership/hooks/ownership.py init --budget 250
python3 ~/.claude/skills/code-ownership/hooks/ownership.py status
```

The gate starts **locked**, so Claude can inspect and plan but cannot perform edits. Ask it to plan the feature in reviewable slices. Once you approve the first slice:

```bash
python3 ~/.claude/skills/code-ownership/hooks/ownership.py next --label "slice 1: eligibility rules"
```

Claude now implements **only that slice**. When it finishes its turn with changes or reaches the budget, the gate locks again. Review the actual diff in Cursor, work through the ownership checkpoint, and commit the reviewed changes. Then open the next slice:

```bash
python3 ~/.claude/skills/code-ownership/hooks/ownership.py status
git diff
git add <reviewed-files>
git commit -m "Implement eligibility rules"
python3 ~/.claude/skills/code-ownership/hooks/ownership.py next --label "slice 2: API integration"
```

`next` requires a **clean working tree** so slices don't accumulate into one huge unreviewed change. If you need to finish the *same* partially completed slice after a Stop event, first inspect the diff and then run `resume`. This is not permission to skip the learning checkpoint or begin another slice.

### Useful controls

| Command | Effect |
| --- | --- |
| `status` | Show lock state, current slice and remaining change budget |
| `pause` | Lock further agent edits |
| `resume` | Reopen the same incomplete slice after inspection, if under budget |
| `next --label "..."` | Start a new slice (clean Git tree required) |
| `off` | Disable the gate for this repository |

Prefix each command with `python3 ~/.claude/skills/code-ownership/hooks/ownership.py`. The **human runs unlock commands in their own terminal**; the coding agent must not unlock itself.

### Default behavior in a session

- **Before implementation:** Claude inspects the relevant code and proposes coherent slices; you or Claude may propose the breakdown.
- **During one unlocked slice:** Claude codes and tests; the backup budget defaults to **250 changed lines**. This is a rough cap, not a guarantee.
- **After the slice:** Claude points to the actual diff, announces **5 questions (max 10)**, and asks them one by one; a small self-written modification can count as one question.
- **When stuck:** Claude coaches with progressive hints instead of immediately writing the exercise for you.
- **After review:** You commit and explicitly unlock the next slice. No huge generated documentation is required.

**First smoke test:** While locked, ask Claude Code to create a harmless file in the test repository. The hook should reject the edit. While unlocked, ask it to make a tiny change and finish its turn; `status` should then report `locked`. Do not test first on production code.

## Limitations / safety

- **Not a sandbox or foolproof control.** Bash is blocked while locked, but when a slice is open, shell commands and single large tool calls can exceed the diff budget. Other editor extensions, manual edits, or external processes are outside the hook's control.
- Changes inside `.gitignore`d files aren't counted. Git diffs can be noisy; the budget is a rough guardrail. New or binary files are conservatively counted.
- `Stop` locks after Claude finishes a turn with uncommitted edits, even when the slice is not complete; the human can use `resume` after inspecting progress. It does not determine semantic completion.
- If a repo is dirty, `init`/`next` refuses to open a slice so you don't accidentally accumulate earlier changes.
- The hook executes with your user permissions. Review the Python code before installing. It persists only project state under `~/.local/state/yegi-code-ownership/` (or the `OWNERSHIP_STATE_DIR` environment variable for tests).
- Hook configuration is separate from the skill. Installing the skill alone does **not** enable mechanical enforcement.
- This only applies to Claude Code environments that load those settings, not every Cursor-native AI agent.

## First experiment

Pick a medium-sized feature in a disposable or personal project. Split it into 3–5 slices. For each slice, note roughly: time spent, ability to trace the code, whether you could make an independent small change, and whether the checkpoint improved understanding. Tune after a few sessions; don't write more documentation unless it serves your work.

Official documentation: https://code.claude.com/docs/en/hooks and https://code.claude.com/docs/en/skills