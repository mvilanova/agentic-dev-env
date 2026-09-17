#!/usr/bin/env python3
"""Herdr event hook: lay out a new workspace as a Claude pane plus a shell.

Fires on workspace.created (and can be invoked by hand as devenv.layout.apply).
A fresh workspace is one tab with one pane; this splits that pane to the right
for a plain shell in the same cwd, then starts Claude Code in the original pane.

Skips when:
- the workspace already has more than one pane (a restored session, or the
  layout was already applied), or
- the pane's cwd is not inside a git repo, unless require_git is turned off.

Config: $HERDR_PLUGIN_CONFIG_DIR/config.json, all keys optional:

    {"agent": "claude", "require_git": true, "ratio": 0.5, "shell_label": "shell"}

Set "agent" to null to lay out the panes without starting an agent.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from typing import Any

DEFAULTS: dict[str, Any] = {
    "agent": "claude",
    "require_git": True,
    "ratio": 0.5,
    "shell_label": "shell",
}


def log(message: str) -> None:
    # Plugin command output lands in `herdr plugin log list --plugin devenv.layout`.
    print(f"[devenv.layout] {message}", file=sys.stderr)


def load_config() -> dict[str, Any]:
    config = dict(DEFAULTS)
    config_dir = os.environ.get("HERDR_PLUGIN_CONFIG_DIR")
    if not config_dir:
        return config
    path = os.path.join(config_dir, "config.json")
    try:
        with open(path) as handle:
            config.update(json.load(handle))
    except FileNotFoundError:
        pass
    except (OSError, json.JSONDecodeError) as error:
        log(f"ignoring {path}: {error}")
    return config


def herdr(args: list[str]) -> dict[str, Any] | None:
    binary = os.environ.get("HERDR_BIN_PATH") or "herdr"
    result = subprocess.run([binary, *args], text=True, capture_output=True)
    if result.returncode != 0:
        log(f"herdr {' '.join(args)} failed: {result.stderr.strip()}")
        return None
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        log(f"herdr {' '.join(args)} returned no JSON")
        return None
    if "error" in payload:
        log(f"herdr {' '.join(args)}: {payload['error']}")
        return None
    return payload


def workspace_id() -> str | None:
    # Event hooks get HERDR_WORKSPACE_ID; fall back to the event payload, which
    # is also what an action invocation without a workspace context relies on.
    from_env = os.environ.get("HERDR_WORKSPACE_ID")
    if from_env:
        return from_env
    for key in ("HERDR_PLUGIN_EVENT_JSON", "HERDR_PLUGIN_CONTEXT_JSON"):
        raw = os.environ.get(key)
        if not raw:
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        found = find_key(payload, "workspace_id")
        if found:
            return found
    return None


def find_key(node: Any, key: str) -> str | None:
    if isinstance(node, dict):
        value = node.get(key)
        if isinstance(value, str):
            return value
        for child in node.values():
            found = find_key(child, key)
            if found:
                return found
    elif isinstance(node, list):
        for child in node:
            found = find_key(child, key)
            if found:
                return found
    return None


def workspace_panes(target: str) -> list[dict[str, Any]]:
    payload = herdr(["pane", "list"])
    if not payload:
        return []
    panes = payload.get("result", {}).get("panes", [])
    return [pane for pane in panes if pane.get("workspace_id") == target]


def is_git_repo(cwd: str) -> bool:
    result = subprocess.run(
        ["git", "-C", cwd, "rev-parse", "--git-dir"],
        text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def agent_name(kind: str, target: str) -> str:
    # Names must match [a-z][a-z0-9_-]{0,31} and be unique among live agents.
    base = re.sub(r"[^a-z0-9_-]", "", f"{kind}_{target}".lower()) or "agent"
    if not base[0].isalpha():
        base = f"a{base}"
    return base[:32]


def main() -> None:
    config = load_config()
    target = workspace_id()
    if not target:
        log("no workspace id in the environment; nothing to do")
        return

    # A brand new workspace can report its root pane a moment after the event.
    panes: list[dict[str, Any]] = []
    for _ in range(10):
        panes = workspace_panes(target)
        if panes:
            break
        time.sleep(0.2)

    if len(panes) != 1:
        log(f"{target} has {len(panes)} panes; leaving it alone")
        return

    root = panes[0]
    pane_id = root.get("pane_id")
    cwd = root.get("cwd") or os.path.expanduser("~")
    if not pane_id:
        log(f"{target} root pane has no id")
        return

    if config.get("require_git") and not is_git_repo(cwd):
        log(f"{cwd} is not a git repo; leaving {target} alone")
        return

    split = herdr([
        "pane", "split", pane_id,
        "--direction", "right",
        "--ratio", str(config.get("ratio", 0.5)),
        "--cwd", cwd,
        "--no-focus",
    ])
    if not split:
        return
    shell_pane = split.get("result", {}).get("pane", {}).get("pane_id")
    label = config.get("shell_label")
    if shell_pane and label:
        herdr(["pane", "rename", shell_pane, label])

    kind = config.get("agent")
    if not kind:
        log(f"laid out {target} without an agent")
        return
    if root.get("agent"):
        log(f"{pane_id} already runs {root['agent']}; skipping agent start")
        return

    herdr(["agent", "start", agent_name(kind, target), "--kind", kind, "--pane", pane_id])
    log(f"laid out {target}: {kind} in {pane_id}, shell in {shell_pane}")


if __name__ == "__main__":
    main()
