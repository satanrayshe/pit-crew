"""Check a Switch template with the Switch server's own template code.

Lints the document the way Switch Console's Import page does, then plans a run
on sample machines and renders the room, without creating anything. Run it
with the Python environment of a Switch checkout's core project:

    uv run --project <switch checkout>/core python scripts/validate-template.py pit-crew.template.yaml

Exits 1 on any lint finding or failed check.
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from switch_core.agent_templates import plan_template
from switch_core.rooms_yaml import (
    PLACEHOLDER_RE,
    ParamSpec,
    RoomSpec,
    interpolate,
    resolve_params,
)
from switch_core.template_lint import lint_template
from switch_core.template_runs import AgentsNotCreated

SAMPLE_INPUTS = {
    "repo_url": "https://github.com/example/project",
    "project_dir": "/home/racer/project",
    "bridge": "Pit Crew Discord",
}
BUILTINS = {
    "$creator": "racer",
    "$creator_email": "racer@example.invalid",
    "$date": "2026-11-05",
    "$timestamp": "1793836800",
    "$agents_dir": "/home/racer/.switch/agents",
}


def machine(*ready: str) -> dict[str, Any]:
    return {
        "id": "m-1",
        "name": "laptop",
        "state": "online",
        "kind": "local",
        "providers": [
            {"provider": p, "installed": True, "auth": "ok" if p in ready else "missing"}
            for p in ("claude", "codex", "opencode")
        ],
    }


SCENARIOS = [
    ("claude signed in", [machine("claude", "codex")], True),
    ("only codex signed in", [machine("codex")], True),
    ("nothing signed in", [machine()], False),
]


def render_room(document: str, inputs: dict[str, Any]) -> tuple[RoomSpec, str]:
    data = yaml.safe_load(document)
    declared = {k: ParamSpec.model_validate(v) for k, v in (data.get("params") or {}).items()}
    values = {**BUILTINS, **resolve_params(declared, inputs)}
    body = interpolate({"room": data["room"], "kickoff": data["kickoff"]}, values)
    return RoomSpec.model_validate(body["room"]), body["kickoff"]


def leftover_placeholders(texts: list[str]) -> list[str]:
    return sorted({m for text in texts for m in PLACEHOLDER_RE.findall(text)})


def check_scenario(text: str, label: str, machines: list[dict[str, Any]], expect_run: bool) -> list[str]:
    print(f"\n== Plan: {label}")
    try:
        plan = plan_template(text, {}, SAMPLE_INPUTS, builtins=BUILTINS, machines=machines)
    except AgentsNotCreated as refused:
        for p in sorted(refused.problems, key=lambda p: p.slot):
            print(f"  refused  {p.slot}: {p.code}")
        return [f"{label}: the run was refused"] if expect_run else []
    if not expect_run:
        return [f"{label}: expected the run to be refused, but it was planned"]

    for agent in sorted(plan.new_agents, key=lambda a: a.name):
        rooms = plan.room_addressing.get(agent.name)
        who = f"anyone in {', '.join(rooms)}" if rooms else agent.addressing
        print(f"  agent    {agent.name:<14} provider={agent.provider:<9} addressing={who}")
        print(f"           directory={agent.directory}")
    room, kickoff = render_room(plan.document, plan.inputs)
    print(f"  room     {room.name} on {room.bridge}, users={room.users}")
    print(f"           agents={room.agents}")
    print(f"           docs={[d.name for d in room.docs]}")
    print(f"  kickoff  {kickoff.strip().splitlines()[0][:72]}...")

    problems = []
    names = [a.name for a in plan.new_agents]
    if sorted(room.agents) != sorted(names):
        problems.append(f"{label}: the room lists {room.agents}, not the agents created ({names})")
    unmentioned = [n for n in names if f"@{n}" not in kickoff]
    if unmentioned:
        problems.append(f"{label}: the kickoff does not wake {', '.join(unmentioned)}")
    texts = (
        [a.instructions for a in plan.new_agents]
        + [room.instructions or "", kickoff]
        + [d.content for d in room.docs]
    )
    left = leftover_placeholders(texts)
    if left:
        problems.append(f"{label}: placeholders left unfilled: {', '.join(left)}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("template", type=Path)
    args = parser.parse_args()
    text = args.template.read_text(encoding="utf-8")

    lint = lint_template(text)
    print(f"== Lint: {len(lint.errors)} error(s), {len(lint.warnings)} warning(s)")
    for finding in lint.errors + lint.warnings:
        print(f"  {finding.code}: {finding.message}")

    problems = [f.code for f in lint.errors + lint.warnings]
    for label, machines, expect_run in SCENARIOS:
        problems += check_scenario(text, label, machines, expect_run)

    print()
    if problems:
        print("FAILED")
        for p in problems:
            print(f"  {p}")
        return 1
    print("OK: no lint findings; every scenario planned or was refused as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
