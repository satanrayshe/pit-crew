# Evidence

What Pit Crew produces while we use it for the Flip the Switch hackathon.
Files are added as they happen and are not edited afterwards, except to
remove anything private (tokens, webhook URLs, email addresses).
`template-lint.txt` is the exception: it is re-run whenever the template
changes, so it matches the committed template.

## What is here now

| File | What it is |
|---|---|
| `template-lint.txt` | `scripts/validate-template.py` run on `pit-crew.template.yaml` with the Switch server's own code: lint findings, the run planned on three sample machines (Claude and Codex ready, only Codex ready, nothing ready), and the rendered room |
| `judge-kit-self-check.json` | `judge-kit/check.py` run on a clean clone of commit 2560729, this repository's first. Every check passes except `readme_demo_video`, which fails on purpose while the README still says `TODO(video-link)` |

## What will be collected

| File name | What it will be | Where it comes from |
|---|---|---|
| `judge-report-pit-crew-<UTC time>.md` | The judge's full report on a clean clone of this repository: gate, scores, top fixes, `check.py` output | The judge's `send_attachment` in the room |
| `judge-report-pr-<issue>-<UTC time>.md` | The judge's report on one of our Track 03 pull requests to Switch, item by item against the issue's "Done when" list | Same, from a review of the PR branch |
| `pit-board-<UTC time>.md` | Snapshots of the scout's `pit-board` document at milestones | Copied from the room document |
| `judge-scorecard-<UTC time>.md` | The judge's running scorecard | Copied from the room document |
| `build-log.md` | The herald's log of commits, one line each | Exported from the room document at the end |
| `screenshots/` | An approval card, a refused approval from a second account, verdicts | Screenshots from Discord and Console |

Each judge report names the commit it reviewed, so it can be checked against
the git history. Coding done in direct Claude Code sessions rather than by the
builder agent shows in the build log as commits from the commit hook.
