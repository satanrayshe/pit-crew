"""Mechanical checks a judge runs on a fresh clone of a hackathon submission.

Standard library only. Templates are parsed with PyYAML when it is installed;
without it a coarser structural check runs, and the report says which.

    python3 judge-kit/check.py path/to/clone
    python3 judge-kit/check.py path/to/clone --mode hygiene

Prints a JSON report and exits 0 when every check passes, 1 when any fails.
In a git checkout only tracked files count, since those are what was pushed.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

SECRET_PATTERNS = {
    "discord_bot_token": re.compile(r"\b[MNO][\w-]{23,27}\.[\w-]{6}\.[\w-]{27,40}\b"),
    "discord_webhook_url": re.compile(
        r"https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\d+/[\w-]{20,}"
    ),
    "github_token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_\w{22,})"),
    "openai_or_anthropic_key": re.compile(r"\bsk-(?:ant-|proj-)?[\w-]{20,}"),
    "aws_access_key_id": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "google_api_key": re.compile(r"\bAIza[\w-]{35}\b"),
    "slack_token": re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}"),
    "slack_webhook_url": re.compile(r"https://hooks\.slack\.com/(?:services|workflows|triggers)/[\w/-]{20,}"),
    "mattermost_webhook_url": re.compile(r"https?://[\w.-]+(?::\d+)?(?:/[\w.-]+)*/hooks/[a-z0-9]{26}\b"),
    "private_key": re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY(?: BLOCK)?-----"),
}
ENV_EXAMPLES = {".env.example", ".env.sample", ".env.template", ".env.dist"}

README_CHECKS = (
    "readme_switch_section",
    "readme_reproduce_section",
    "readme_architecture",
    "readme_demo_video",
)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
FENCED_BLOCK_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
SWITCH_USE_WORDS = {"use", "used", "uses", "using", "how", "why"}
REPRODUCE_RE = re.compile(
    r"reproduc|quick ?start|getting started|set ?up|install|how to run|run it|try it",
    re.IGNORECASE,
)
ARCHITECTURE_RE = re.compile(
    r"^#{1,6}\s+.*architecture|^```mermaid|\]\([^)]*architecture[^)]*\)",
    re.IGNORECASE | re.MULTILINE,
)
VIDEO_URL_RE = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/|live/)|youtu\.be/"
    r"|loom\.com/(?:share|embed)/|vimeo\.com/\d)[^\s)>\]]*"
)
VIDEO_TODO = "TODO(video-link)"
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:", re.MULTILINE)
RESOURCE_TYPES = {"agent", "room", "group"}
V1_KEYS = {"room", "agent", "agents", "group"}


@dataclass
class Check:
    id: str
    passed: bool
    detail: str
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Repo:
    root: Path
    files: list[str]
    files_from: str

    def text(self, rel: str) -> str | None:
        """The file's text, or None for a binary file."""
        data = (self.root / rel).read_bytes()
        if b"\0" in data[:8192]:
            return None
        return data.decode("utf-8", errors="replace")


def git_files(root: Path, command: str, *args: str) -> list[str]:
    result = subprocess.run(["git", "-C", str(root), command, "-z", *args], capture_output=True, check=True)
    return [n for n in result.stdout.decode("utf-8").split("\0") if n]


def list_files(root: Path, changed_since: str | None) -> tuple[list[str], str]:
    """The files that count, and where the list came from."""
    if changed_since is not None:
        span = f"{changed_since}...HEAD"
        names = git_files(root, "diff", "--name-only", "--diff-filter=d", span)
        if not names:
            raise ValueError(f"no file was added or changed between {changed_since} and HEAD")
        source = f"git diff {span}"
    elif (root / ".git").exists():
        names = git_files(root, "ls-files")
        source = "git"
    else:
        names = [
            p.relative_to(root).as_posix() for p in root.rglob("*") if ".git" not in p.relative_to(root).parts
        ]
        source = "walk"
    return sorted(n for n in names if (root / n).is_file()), source


def top_level(repo: Repo, *prefixes: str) -> list[str]:
    return [f for f in repo.files if "/" not in f and f.upper().startswith(prefixes)]


def mentions_switch_use(heading: str) -> bool:
    words = set(re.findall(r"[a-z]+", heading.lower()))
    return "switch" in words and bool(words & SWITCH_USE_WORDS)


def check_readme(repo: Repo) -> list[Check]:
    readmes = top_level(repo, "README")
    if not readmes:
        return [
            Check(check_id, False, "no README at the top of the repository") for check_id in README_CHECKS
        ]
    readme = readmes[0]
    text = repo.text(readme) or ""
    headings = HEADING_RE.findall(FENCED_BLOCK_RE.sub("", text))

    def heading_check(check_id: str, matches: Callable[[str], object], what: str) -> Check:
        found = next((h for h in headings if matches(h)), None)
        if found is None:
            return Check(check_id, False, f"{readme} has no heading about {what}")
        return Check(check_id, True, f'{readme}: "{found}"')

    architecture = ARCHITECTURE_RE.search(text)
    if architecture is None:
        architecture_check = Check(
            "readme_architecture", False, f"{readme} has no architecture heading, diagram or link"
        )
    else:
        architecture_check = Check("readme_architecture", True, f"{readme}: {architecture.group(0).strip()}")

    video = VIDEO_URL_RE.search(text)
    if VIDEO_TODO in text:
        video_check = Check("readme_demo_video", False, f"{readme} still has the {VIDEO_TODO} marker")
    elif video is None:
        video_check = Check("readme_demo_video", False, f"{readme} links no YouTube, Loom or Vimeo video")
    else:
        video_check = Check("readme_demo_video", True, video.group(0))

    return [
        heading_check("readme_switch_section", mentions_switch_use, "how Switch is used"),
        heading_check("readme_reproduce_section", REPRODUCE_RE.search, "reproducing or setting it up"),
        architecture_check,
        video_check,
    ]


def check_license(repo: Repo) -> Check:
    found = top_level(repo, "LICENSE", "LICENCE", "COPYING")
    if not found:
        return Check("license", False, "no LICENSE file at the top of the repository")
    return Check("license", True, ", ".join(found))


def template_problem_pyyaml(text: str) -> str | None:
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return f"not valid YAML: {str(e).splitlines()[0]}"
    if not isinstance(data, dict):
        return "not a YAML mapping"
    if data.get("version") == 2 or "resources" in data:
        resources = data.get("resources")
        if not isinstance(resources, dict) or not resources:
            return "a version 2 template with no resources"
        untyped = [
            str(key)
            for key, spec in resources.items()
            if not isinstance(spec, dict) or spec.get("type") not in RESOURCE_TYPES
        ]
        if untyped:
            return f"resources without a type of agent, room or group: {', '.join(untyped)}"
        return None
    if not V1_KEYS & set(data):
        return "neither resources (version 2) nor room, agent, agents or group (version 1)"
    return None


def template_problem_structural(text: str) -> str | None:
    tabbed = next((n for n, line in enumerate(text.splitlines(), 1) if line.startswith("\t")), None)
    if tabbed is not None:
        return f"line {tabbed} is indented with a tab, which YAML does not allow"
    keys = set(TOP_LEVEL_KEY_RE.findall(text))
    if "resources" not in keys and not V1_KEYS & keys:
        return "no top-level resources, room, agent, agents or group key"
    return None


def check_templates(repo: Repo) -> Check:
    templates = [f for f in repo.files if f.endswith((".template.yaml", ".template.yml"))]
    if not templates:
        return Check("template", False, "no *.template.yaml file sets up the Switch side")
    problem_of = template_problem_pyyaml if yaml is not None else template_problem_structural
    findings = []
    for rel in templates:
        problem = problem_of(repo.text(rel) or "")
        findings.append({"path": rel, "ok": problem is None, "problem": problem})
    failed = sum(1 for f in findings if not f["ok"])
    detail = f"{len(templates) - failed} of {len(templates)} template(s) parse"
    return Check("template", failed == 0, detail, findings)


def redact(secret: str) -> str:
    return f"{secret[:6]}... ({len(secret)} chars)"


def check_secrets(repo: Repo) -> Check:
    findings = []
    for rel in repo.files:
        text = repo.text(rel)
        if text is None:
            continue
        for kind, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append({"path": rel, "line": line, "kind": kind, "match": redact(match.group(0))})
    findings.sort(key=lambda f: (f["path"], f["line"]))
    if findings:
        return Check(
            "secrets", False, f"{len(findings)} possible secret(s); rotate any that are real", findings
        )
    return Check("secrets", True, f"no secret patterns in {len(repo.files)} file(s)")


def local_file_reason(rel: str) -> str | None:
    parts = rel.split("/")
    if ".switch" in parts:
        return "Switch agent config, which holds the agent's API token"
    if parts[-1] == ".env" or (parts[-1].startswith(".env.") and parts[-1] not in ENV_EXAMPLES):
        return "environment file"
    if parts[-2:] == [".claude", "settings.local.json"]:
        return "Claude Code local settings"
    return None


def check_local_files(repo: Repo) -> Check:
    findings = [{"path": f, "reason": r} for f in repo.files if (r := local_file_reason(f)) is not None]
    if findings:
        return Check("local_files", False, f"{len(findings)} local-only file(s) are committed", findings)
    return Check("local_files", True, "no .env, .switch/ or local agent settings committed")


def check_large_files(repo: Repo, max_mb: float) -> Check:
    limit = max_mb * 1024 * 1024
    findings = [
        {"path": f, "mb": round(size / 1024 / 1024, 2)}
        for f in repo.files
        if (size := (repo.root / f).stat().st_size) > limit
    ]
    if findings:
        return Check(
            "large_files",
            False,
            f"{len(findings)} file(s) over {max_mb:g} MB; host videos elsewhere",
            findings,
        )
    return Check("large_files", True, f"no file over {max_mb:g} MB")


def run(root: Path, mode: str, max_mb: float, changed_since: str | None) -> dict[str, Any]:
    files, files_from = list_files(root, changed_since)
    repo = Repo(root, files, files_from)
    checks = []
    if mode == "submission":
        checks += check_readme(repo)
        checks += [check_license(repo), check_templates(repo)]
    checks += [check_secrets(repo), check_local_files(repo), check_large_files(repo, max_mb)]
    return {
        "path": str(root),
        "mode": mode,
        "files_from": files_from,
        "yaml_parser": "pyyaml" if yaml is not None else "structural (PyYAML is not installed)",
        "passed": all(c.passed for c in checks),
        "checks": [asdict(c) for c in checks],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a cloned hackathon submission.")
    parser.add_argument("path", type=Path, help="the cloned repository")
    parser.add_argument(
        "--mode",
        choices=["submission", "hygiene"],
        default="submission",
        help="submission runs every check; hygiene only secrets, local files and sizes (for a pull request)",
    )
    parser.add_argument("--max-file-mb", type=float, default=10.0, help="flag files larger than this")
    parser.add_argument(
        "--changed-since",
        metavar="REF",
        help="hygiene mode: check only the files changed between REF and HEAD, as in a pull request",
    )
    args = parser.parse_args(argv)
    if not args.path.is_dir():
        parser.error(f"{args.path} is not a directory")
    if args.changed_since is not None and args.mode != "hygiene":
        parser.error("--changed-since needs --mode hygiene")
    try:
        report = run(args.path.resolve(), args.mode, args.max_file_mb, args.changed_since)
    except subprocess.CalledProcessError as e:
        parser.exit(2, f"git failed: {e.stderr.decode('utf-8', errors='replace').strip()}\n")
    except ValueError as e:
        parser.exit(2, f"{e}\n")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
