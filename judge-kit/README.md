# Judge kit

`check.py` runs the mechanical part of a review, so the judge agent spends
its turn on the parts that need judgment. It uses only the Python standard
library (3.10 or later) and git. If PyYAML is installed it parses templates
fully; otherwise it runs a structural check and says so in the report.

## A hackathon submission

```sh
git clone --depth 1 https://github.com/you/project clean-room-202611051200
python3 judge-kit/check.py clean-room-202611051200
```

| Check | Passes when |
|---|---|
| `readme_switch_section` | A README heading mentions Switch and how, why or use |
| `readme_reproduce_section` | A README heading is about reproducing, setting up, installing or running it |
| `readme_architecture` | The README has an architecture heading, a mermaid diagram or a link to an architecture file |
| `readme_demo_video` | The README links a YouTube, Loom or Vimeo video and has no `TODO(video-link)` marker |
| `license` | A LICENSE, LICENCE or COPYING file sits at the top |
| `template` | At least one `*.template.yaml` exists and each one parses as a Switch template |
| `secrets` | No Discord bot token or webhook URL, GitHub, OpenAI, Anthropic, AWS, Google or Slack key, or private key appears in any text file |
| `local_files` | No `.env`, nothing under `.switch/`, no `.claude/settings.local.json` is committed |
| `large_files` | No file is over 10 MB (`--max-file-mb` changes it) |

Headings inside fenced code blocks do not count. Secrets are reported with
their file, line and kind, and only the first six characters, so the report
itself never leaks one.

## A pull request

For a change to a large repository, scan only what the change touches, so the
project's own test fixtures do not drown the report:

```sh
git clone --branch my-feature https://github.com/you/fork pr-clone
git -C pr-clone fetch https://github.com/upstream/project main
python3 judge-kit/check.py pr-clone --mode hygiene --changed-since FETCH_HEAD
```

`hygiene` runs only `secrets`, `local_files` and `large_files`.
`--changed-since REF` limits them to files changed between the merge base
of REF and HEAD, so the clone needs enough history to find it (no
`--depth 1` here). A finding in a touched test file may still be a fixture;
the judge reads each one.

## Output

JSON on standard output:

```json
{
  "path": "/home/judge/clean-room-202611051200",
  "mode": "submission",
  "files_from": "git",
  "yaml_parser": "pyyaml",
  "passed": false,
  "checks": [
    {"id": "readme_demo_video", "passed": false, "detail": "README.md still has the TODO(video-link) marker", "findings": []}
  ]
}
```

`files_from` is `git` (tracked files only, which is what was pushed), `walk`
(not a git checkout, so every file), or the `git diff` range. Exit code 0
means every check passed, 1 that at least one failed, 2 a usage error or a
git failure.

## Tests

```sh
python3 -m pytest judge-kit
```
