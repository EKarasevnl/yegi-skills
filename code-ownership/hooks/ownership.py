#!/usr/bin/env python3
"""Opt-in Claude Code ownership checkpoint gate (standard-library-only POC).

The gate is intentionally a workflow guard, not a security sandbox.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

READ_ONLY_TOOLS = {
    "Read", "Glob", "Grep", "LS", "Search", "WebSearch", "WebFetch",
    "Skill", "AskUserQuestion", "TaskList", "TaskGet", "TodoRead",
}
DEFAULT_BUDGET = 250


def git(root, *args):
    proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                          text=True, check=False, timeout=5)
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def repo_root(path):
    try:
        return Path(git(Path(path), "rev-parse", "--show-toplevel").strip()).resolve()
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        return None


def state_path(root):
    base = Path(os.getenv("OWNERSHIP_STATE_DIR", "~/.local/state/yegi-code-ownership")).expanduser()
    name = hashlib.sha256(str(root).encode()).hexdigest()[:20]
    return base / name / "state.json"


def load(root):
    p = state_path(root)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save(root, state):
    p = state_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, p)


def is_clean(root):
    return not git(root, "status", "--porcelain", "--untracked-files=normal").strip()


def changed_lines(root, limit):
    """Count staged/unstaged tracked changes and untracked file contents vs HEAD.

    Requires a clean git tree when opening a slice. Large/binary/new files count
    above budget rather than being invisibly free.
    """
    total = 0
    diff = git(root, "diff", "--numstat", "HEAD", "--")
    for line in diff.splitlines():
        parts = line.split("\t", 2)
        if len(parts) < 3:
            continue
        if parts[0] == "-" or parts[1] == "-":
            return limit + 1
        total += int(parts[0]) + int(parts[1])
    for rel in git(root, "ls-files", "--others", "--exclude-standard", "-z").split("\0"):
        if not rel:
            continue
        path = root / rel
        if not path.is_file() or path.is_symlink() or path.stat().st_size > 2_000_000:
            return limit + 1
        b = path.read_bytes()
        if b"\x00" in b:
            return limit + 1
        total += len(b.splitlines())
    return total


def deny(reason):
    print(reason, file=sys.stderr)
    return 2


def hook_event(kind):
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    root = repo_root(data.get("cwd") or os.getcwd())
    if not root:
        return 0
    state = load(root)
    if not state or state.get("mode") == "off":
        return 0
    if kind == "stop":
        if state["mode"] == "open" and changed_lines(root, state["budget"]) > 0:
            state["mode"] = "locked"
            state["reason"] = "Claude finished a turn with code changes; review before more edits."
            save(root, state)
        return 0
    if kind == "post":
        if state["mode"] == "open" and changed_lines(root, state["budget"]) >= state["budget"]:
            state["mode"] = "locked"
            state["reason"] = "Change budget reached; inspect the diff and complete the checkpoint."
            save(root, state)
            print(state["reason"], file=sys.stderr)
        return 0
    tool = data.get("tool_name", "")
    if state["mode"] == "locked":
        if tool in READ_ONLY_TOOLS:
            return 0
        return deny("OWNERSHIP LOCK: No agent editing or shell commands until the human reviews "
                    "and unlocks the next slice in their own terminal. "
                    "Read/Grep/Glob and explanation remain available. "
                    f"Reason: {state.get('reason', 'checkpoint required')}")
    # Open: deny a known oversized single Write, and stop once the cumulative
    # Git diff reaches the budget. Shell edits can overshoot; see README.
    budget = state["budget"]
    used = changed_lines(root, budget)
    if used >= budget and tool not in READ_ONLY_TOOLS:
        state["mode"] = "locked"
        state["reason"] = "Change budget reached."
        save(root, state)
        return deny("OWNERSHIP LOCK: Slice reached its change budget. Review before continuing.")
    if tool == "Write":
        content = data.get("tool_input", {}).get("content", "")
        if isinstance(content, str) and len(content.splitlines()) + used > budget:
            return deny("OWNERSHIP BUDGET: This proposed Write is too large for one slice. "
                        "Split it into smaller coherent changes.")
    return 0


def command(args):
    root = repo_root(args.project or os.getcwd())
    if not root:
        raise SystemExit("Run this command from within a Git repository.")
    state = load(root)
    if args.cmd == "init":
        if not is_clean(root):
            raise SystemExit("Start with a clean Git working tree (commit/stash changes first).")
        save(root, {"mode": "locked", "budget": args.budget, "label": "", "reason": "Start a slice manually."})
        print(f"Enabled for {root}. Locked; budget {args.budget} changed lines. Run 'next' to open slice 1.")
    elif args.cmd == "next":
        if not state or state["mode"] == "off":
            raise SystemExit("First run 'init' in this repository.")
        if not is_clean(root):
            raise SystemExit("Commit or stash/revert the previous slice before opening another. "
                             "This keeps each checkpoint small and independently reviewable.")
        state.update(mode="open", label=args.label, reason="")
        save(root, state)
        print(f"Slice OPEN: {args.label}. Claude will auto-lock when it finishes its next turn or hits the budget.")
    elif args.cmd == "resume":
        if not state or state["mode"] != "locked":
            raise SystemExit("Resume applies only to an existing locked slice.")
        if not state["label"]:
            raise SystemExit("No slice exists; use next --label first.")
        if changed_lines(root, state["budget"]) >= state["budget"]:
            raise SystemExit("Slice is at its change budget. Review and commit it, or "
                             "explicitly start a new clean slice.")
        state.update(mode="open", reason="")
        save(root, state)
        print(f"Resumed current slice: {state['label']}")
    elif args.cmd == "pause":
        if not state:
            raise SystemExit("First run 'init'.")
        state.update(mode="locked", reason="Paused by human.")
        save(root, state)
        print("Locked; read-only coaching remains possible.")
    elif args.cmd == "off":
        if state:
            state.update(mode="off", reason="Disabled by human.")
            save(root, state)
        print("Disabled for this repository.")
    else:
        if not state:
            print("Not enabled in this repository.")
        else:
            remaining = "n/a"
            if state["mode"] != "off":
                remaining = max(0, state["budget"] - changed_lines(root, state["budget"]))
            print(f"Mode: {state['mode']} | Slice: {state['label'] or 'none'} | "
                  f"Budget: {state['budget']} | Remaining lines: {remaining}")
            if state.get("reason"):
                print(f"Reason: {state['reason']}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cmd", choices=["init", "next", "resume", "pause", "status", "off", "pre", "post", "stop"])
    parser.add_argument("--project", help="Project path, defaults to current working directory")
    parser.add_argument("--budget", type=int, default=DEFAULT_BUDGET)
    parser.add_argument("--label", default="implementation slice")
    args = parser.parse_args()
    if args.budget < 1:
        parser.error("--budget must be positive")
    try:
        return hook_event(args.cmd) if args.cmd in {"pre", "post", "stop"} else command(args)
    except (RuntimeError, OSError, ValueError) as exc:
        # Fail closed if an enabled gate is broken, so it can't be silently bypassed.
        print(f"OWNERSHIP HOOK ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
