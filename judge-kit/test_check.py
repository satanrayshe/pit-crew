import json
import shutil
import subprocess
from pathlib import Path

import check
import pytest

GOOD_README = """\
# Demo project

## How Switch is used (and why it breaks without it)

Agents share one room.

## Architecture

```mermaid
flowchart LR
  A --> B
```

## Reproduce in 15 minutes

1. Install things.

## Demo video

https://youtu.be/abc123XYZ
"""

TEMPLATE_V2 = """\
version: 2
resources:
  helper:
    type: agent
    instructions: Help.
  lobby:
    type: room
    name: lobby
    description: Where it helps.
"""

# Built at run time so this file does not itself trip the secret scan.
FAKE_SECRETS = {
    "discord_bot_token": "M" + "T" * 25 + "." + "G" * 6 + "." + "x" * 38,
    "discord_webhook_url": "https://discord.com/api/webhooks/" + "1" * 18 + "/" + "y" * 68,
    "github_token": "gh" + "p_" + "a" * 36,
    "openai_or_anthropic_key": "sk" + "-ant-" + "b" * 40,
    "aws_access_key_id": "AK" + "IA" + "C" * 16,
    "google_api_key": "AI" + "za" + "d" * 35,
    "slack_token": "xo" + "xb-" + "1234567890-abcdef",
    "private_key": "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
}


def make_repo(root: Path, files: dict[str, str | bytes]) -> Path:
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
    return root


def good_files() -> dict[str, str | bytes]:
    return {"README.md": GOOD_README, "LICENSE": "MIT", "crew.template.yaml": TEMPLATE_V2}


def checks_of(root: Path, mode: str = "submission", max_mb: float = 10.0) -> dict[str, dict]:
    report = check.run(root, mode, max_mb, None)
    return {c["id"]: c for c in report["checks"]}


def test_complete_submission_passes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    make_repo(tmp_path, good_files())

    code = check.main([str(tmp_path)])

    report = json.loads(capsys.readouterr().out)
    assert code == 0
    assert report["passed"] is True
    assert report["files_from"] == "walk"
    assert [c["id"] for c in report["checks"]] == [
        "readme_switch_section",
        "readme_reproduce_section",
        "readme_architecture",
        "readme_demo_video",
        "license",
        "template",
        "secrets",
        "local_files",
        "large_files",
    ]
    assert report["checks"][3]["detail"] == "https://youtu.be/abc123XYZ"


def test_failing_check_exits_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    make_repo(tmp_path, {"README.md": GOOD_README})

    code = check.main([str(tmp_path)])

    report = json.loads(capsys.readouterr().out)
    assert code == 1
    assert report["passed"] is False


def test_missing_readme_fails_every_readme_check(tmp_path: Path) -> None:
    make_repo(tmp_path, {"LICENSE": "MIT", "crew.template.yaml": TEMPLATE_V2})

    checks = checks_of(tmp_path)

    for check_id in (
        "readme_switch_section",
        "readme_reproduce_section",
        "readme_architecture",
        "readme_demo_video",
    ):
        assert checks[check_id]["passed"] is False
        assert checks[check_id]["detail"] == "no README at the top of the repository"


def test_comments_in_code_blocks_are_not_headings(tmp_path: Path) -> None:
    make_repo(tmp_path, {"README.md": "# P\n\n```bash\n# install and use switch\nmake\n```\n"})

    checks = checks_of(tmp_path)

    assert checks["readme_switch_section"]["passed"] is False
    assert checks["readme_reproduce_section"]["passed"] is False


def test_readme_in_a_subfolder_does_not_count(tmp_path: Path) -> None:
    make_repo(tmp_path, {"docs/README.md": GOOD_README})

    assert checks_of(tmp_path)["readme_switch_section"]["passed"] is False


@pytest.mark.parametrize(
    "heading, counts",
    [
        ("## How Switch is used", True),
        ("## Using Switch", True),
        ("### Why Switch", True),
        ("## Switch", False),
        ("## How it works", False),
        ("## Switchboard usage", False),
    ],
)
def test_switch_section_heading(tmp_path: Path, heading: str, counts: bool) -> None:
    make_repo(tmp_path, {"README.md": f"# P\n\n{heading}\n\ntext\n"})

    assert checks_of(tmp_path)["readme_switch_section"]["passed"] is counts


@pytest.mark.parametrize(
    "heading, counts",
    [
        ("## Reproduce in 15 minutes", True),
        ("## Quick start", True),
        ("## Getting started", True),
        ("## Setup", True),
        ("## Installation", True),
        ("## Credits", False),
    ],
)
def test_reproduce_section_heading(tmp_path: Path, heading: str, counts: bool) -> None:
    make_repo(tmp_path, {"README.md": f"# P\n\n{heading}\n"})

    assert checks_of(tmp_path)["readme_reproduce_section"]["passed"] is counts


@pytest.mark.parametrize(
    "body, counts",
    [
        ("## Architecture\n", True),
        ("```mermaid\nflowchart LR\n```\n", True),
        ("See [the diagram](docs/architecture.md).\n", True),
        ("The architecture is simple.\n", False),
    ],
)
def test_architecture(tmp_path: Path, body: str, counts: bool) -> None:
    make_repo(tmp_path, {"README.md": f"# P\n\n{body}"})

    assert checks_of(tmp_path)["readme_architecture"]["passed"] is counts


@pytest.mark.parametrize(
    "link",
    [
        "https://www.youtube.com/watch?v=abc123",
        "https://youtu.be/abc123",
        "https://www.loom.com/share/0123abcd",
        "https://vimeo.com/123456",
    ],
)
def test_video_links_that_count(tmp_path: Path, link: str) -> None:
    make_repo(tmp_path, {"README.md": f"# P\n\nWatch [the demo]({link}).\n"})

    result = checks_of(tmp_path)["readme_demo_video"]

    assert result["passed"] is True
    assert result["detail"] == link


def test_video_todo_marker_fails_even_with_a_link(tmp_path: Path) -> None:
    make_repo(tmp_path, {"README.md": GOOD_README + "\nTODO(video-link)\n"})

    result = checks_of(tmp_path)["readme_demo_video"]

    assert result["passed"] is False
    assert "TODO(video-link)" in result["detail"]


def test_no_video_link(tmp_path: Path) -> None:
    make_repo(tmp_path, {"README.md": "# P\n\nhttps://example.com/video\n"})

    assert checks_of(tmp_path)["readme_demo_video"]["passed"] is False


@pytest.mark.parametrize("name", ["LICENSE", "LICENSE.md", "license.txt", "COPYING"])
def test_license_names(tmp_path: Path, name: str) -> None:
    make_repo(tmp_path, {name: "MIT"})

    assert checks_of(tmp_path)["license"]["passed"] is True


def test_missing_license(tmp_path: Path) -> None:
    make_repo(tmp_path, {"README.md": GOOD_README, "docs/LICENSE": "MIT"})

    assert checks_of(tmp_path)["license"]["passed"] is False


def test_no_template(tmp_path: Path) -> None:
    make_repo(tmp_path, {"README.md": GOOD_README, "config.yaml": TEMPLATE_V2})

    result = checks_of(tmp_path)["template"]

    assert result["passed"] is False
    assert "no *.template.yaml" in result["detail"]


@pytest.mark.parametrize(
    "text, problem",
    [
        (TEMPLATE_V2, None),
        ("room:\n  name: lobby\n  description: x\n", None),
        ("version: 2\nresources: {}\n", "a version 2 template with no resources"),
        (
            "version: 2\nresources:\n  a: {type: robot}\n",
            "resources without a type of agent, room or group: a",
        ),
        ("- just\n- a list\n", "not a YAML mapping"),
        ("params: {}\n", "neither resources (version 2) nor room, agent, agents or group (version 1)"),
    ],
)
def test_template_parsing_with_pyyaml(tmp_path: Path, text: str, problem: str | None) -> None:
    pytest.importorskip("yaml")
    make_repo(tmp_path, {"a.template.yaml": text})

    result = checks_of(tmp_path)["template"]

    assert result["findings"] == [{"path": "a.template.yaml", "ok": problem is None, "problem": problem}]
    assert result["passed"] is (problem is None)


def test_template_that_is_not_yaml(tmp_path: Path) -> None:
    pytest.importorskip("yaml")
    make_repo(tmp_path, {"a.template.yml": "room: [unclosed\n"})

    result = checks_of(tmp_path)["template"]

    assert result["passed"] is False
    assert result["findings"][0]["problem"].startswith("not valid YAML")


@pytest.mark.parametrize(
    "text, ok",
    [
        (TEMPLATE_V2, True),
        ("room:\n  name: lobby\n", True),
        ("version: 2\nresources:\n\thelper: {}\n", False),
        ("params: {}\n", False),
    ],
)
def test_template_structural_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, text: str, ok: bool
) -> None:
    monkeypatch.setattr(check, "yaml", None)
    make_repo(tmp_path, {"a.template.yaml": text})

    report = check.run(tmp_path, "submission", 10.0, None)

    assert report["yaml_parser"] == "structural (PyYAML is not installed)"
    template = next(c for c in report["checks"] if c["id"] == "template")
    assert template["passed"] is ok


@pytest.mark.parametrize("kind", sorted(FAKE_SECRETS))
def test_each_secret_kind_is_found_and_redacted(tmp_path: Path, kind: str) -> None:
    secret = FAKE_SECRETS[kind]
    make_repo(tmp_path, {"notes.txt": f"line one\nkey = {secret}\n"})

    report = check.run(tmp_path, "hygiene", 10.0, None)

    secrets = report["checks"][0]
    assert secrets["id"] == "secrets"
    assert secrets["passed"] is False
    assert [(f["path"], f["line"], f["kind"]) for f in secrets["findings"]] == [("notes.txt", 2, kind)]
    assert secret not in json.dumps(report)


def test_lookalikes_are_not_secrets(tmp_path: Path) -> None:
    text = "Set DISCORD_WEBHOOK_URL=, keys look like sk-... or ghp_..., in a task-runner-for-everything."
    make_repo(tmp_path, {"README.md": text})

    assert checks_of(tmp_path, "hygiene")["secrets"]["passed"] is True


def test_binary_files_are_not_scanned(tmp_path: Path) -> None:
    make_repo(tmp_path, {"image.png": b"\x89PNG\0" + FAKE_SECRETS["github_token"].encode()})

    assert checks_of(tmp_path, "hygiene")["secrets"]["passed"] is True


@pytest.mark.parametrize(
    "rel, flagged",
    [
        (".switch/agents/pit-builder.json", True),
        ("app/.switch/agents/x.json", True),
        (".env", True),
        (".env.local", True),
        (".env.example", False),
        (".claude/settings.local.json", True),
        (".claude/settings.json", False),
        ("docs/env.md", False),
    ],
)
def test_local_files(tmp_path: Path, rel: str, flagged: bool) -> None:
    make_repo(tmp_path, {rel: "{}"})

    result = checks_of(tmp_path, "hygiene")["local_files"]

    assert result["passed"] is not flagged
    if flagged:
        assert result["findings"][0]["path"] == rel


def test_large_files(tmp_path: Path) -> None:
    make_repo(tmp_path, {"demo.mp4": b"\0" * 2048, "small.txt": "hi"})

    result = checks_of(tmp_path, "hygiene", max_mb=0.001)["large_files"]

    assert result["passed"] is False
    assert [f["path"] for f in result["findings"]] == ["demo.mp4"]


def test_hygiene_mode_skips_submission_checks(tmp_path: Path) -> None:
    make_repo(tmp_path, {"main.py": "print('hi')\n"})

    report = check.run(tmp_path, "hygiene", 10.0, None)

    assert [c["id"] for c in report["checks"]] == ["secrets", "local_files", "large_files"]
    assert report["passed"] is True


def test_not_a_directory(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as exit_info:
        check.main([str(tmp_path / "missing")])

    assert exit_info.value.code == 2


def test_changed_since_needs_hygiene_mode(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as exit_info:
        check.main([str(tmp_path), "--changed-since", "main"])

    assert exit_info.value.code == 2


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout


def git_can_commit() -> bool:
    if shutil.which("git") is None:
        return False
    found = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
    return bool(found.stdout.strip())


needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git is not installed")
needs_git_commit = pytest.mark.skipif(not git_can_commit(), reason="git has no identity to commit with")


@needs_git
def test_only_tracked_files_count_in_a_git_checkout(tmp_path: Path) -> None:
    make_repo(
        tmp_path, {**good_files(), ".env": "DISCORD_WEBHOOK_URL=" + FAKE_SECRETS["discord_webhook_url"]}
    )
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", "README.md", "LICENSE", "crew.template.yaml")

    report = check.run(tmp_path, "submission", 10.0, None)

    assert report["files_from"] == "git"
    assert report["passed"] is True


@needs_git_commit
def test_changed_since_scans_only_changed_files(tmp_path: Path) -> None:
    make_repo(tmp_path, {"fixture.txt": FAKE_SECRETS["github_token"]})
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "base")
    git(tmp_path, "checkout", "-q", "-b", "feature")
    make_repo(tmp_path, {"new.py": "TOKEN = '" + FAKE_SECRETS["aws_access_key_id"] + "'\n"})
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "feature")

    report = check.run(tmp_path, "hygiene", 10.0, "main")

    assert report["files_from"] == "git diff main...HEAD"
    secrets = report["checks"][0]
    assert [(f["path"], f["kind"]) for f in secrets["findings"]] == [("new.py", "aws_access_key_id")]


@needs_git_commit
def test_changed_since_with_nothing_changed_fails_loudly(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_repo(tmp_path, {"main.py": "print('hi')\n"})
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "base")

    with pytest.raises(SystemExit) as exit_info:
        check.main([str(tmp_path), "--mode", "hygiene", "--changed-since", "main"])

    assert exit_info.value.code == 2
    assert "no file was added or changed between main and HEAD" in capsys.readouterr().err


@needs_git
def test_changed_since_with_an_unknown_ref_fails_loudly(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    git(tmp_path, "init", "-q")

    with pytest.raises(SystemExit) as exit_info:
        check.main([str(tmp_path), "--mode", "hygiene", "--changed-since", "no-such-ref"])

    assert exit_info.value.code == 2
    assert "git failed" in capsys.readouterr().err
