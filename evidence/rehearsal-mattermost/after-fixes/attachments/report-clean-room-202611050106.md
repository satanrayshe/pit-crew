# Judge report — pit-crew-r2 (re-review)

- Repository: `file:///root/fts/rehearsal/git/pit-crew-r2.git`, branch `main`
- Commit reviewed: `29b47c575e74f02453b63f42763bc494a639dac8` (`29b47c5 docs: add changelog entry`)
- `origin/main` at review time: same hash (no new push since the last review)
- Clean-room folder: `clean-room-202611050106`, `git clone --depth 1`
- Kit: `pit-crew-kit` pulled (already up to date), `judge-kit/check.py`
- Verdict: **BLOCKED** (unchanged)

## Verdict

The pushed tip is still `29b47c5`, the commit I reviewed at 01:03. Nothing new
is in the public repository, so the previous verdict stands: the README still
says `TODO(video-link)` and the demo-video gate is still shut. Room activity
(pit-board 10/12, build-log) is not in the repository, and the judge scores
only what is pushed.

## Gate

| Gate item | Result | Evidence |
|---|---|---|
| README section on how Switch is used and why it stops working without it | PASS | `README.md:63-77` |
| Architecture diagram | PASS | `README.md:42-47`, `README.md:81-88` mermaid; `docs/architecture.md` |
| Reproduce steps a stranger can follow | PASS (URL caveat) | `README.md:93-155`; step 1 still clones `https://git.pit.local/pit-crew.git`, not the public repo |
| Template/config that sets up the Switch side | PASS | `pit-crew.template.yaml` (`version: 2`, four agents, room, documents, kickoff; parses) |
| Demo video link | **FAIL** | `README.md:49` `Demo video: TODO(video-link)`; no video URL tracked |
| License | PASS | `LICENSE` (MIT, copyright 2026 satanrayshe) |
| No secrets | PASS | check.py `secrets` and `local_files` pass over 36 tracked files |

## Mechanical checks (`python3 pit-crew-kit/judge-kit/check.py .`)

`passed: false`; 8 of 9 pass. Only failure: `readme_demo_video`. Same result as
the 01:03 review; see the previous attached report for the full check list.

## What I ran

- `python3 pit_clock.py 2026-11-06T06:21:00+00:00 --now 2026-11-06T05:09:00+00:00` -> `T-1h12m`
- `python3 -m unittest discover -s tests` -> 12 tests, OK
- `judge-kit` pytest and `ruff`: skipped, neither is installed here
- Console/Discord reproduce steps: skipped (needs an account, a sign-in, over 10 minutes)

## Rubric scores (unchanged)

| Rubric line | Score | Evidence |
|---|---|---|
| Use of Switch (30%) | 7/10 | `pit-crew.template.yaml:119-380`; `README.md:63-77`; `evidence/` still lacks a committed pit-board, build log or judge report |
| Works (30%) | 10/10 | `pit_clock.py` reproduces `T-1h12m` from the README command; 12/12 tests pass |
| Clarity (20%) | 8/10 | `README.md:1-47` clear up front; 257 lines and the `git.pit.local` URL at `README.md:102` |
| Hygiene (20%) | 8/10 | 7 focused commits; no secrets, no `.env`, no `.switch/`, no large files |

## Three fixes that gain the most points per hour

1. **Publish the demo video and replace `TODO(video-link)` (`README.md:49`).** The only gate blocker; nothing can be SHIP-READY without it.
2. **Commit the room evidence into `evidence/`** (pit-board snapshot, build log, this judge report). Makes the crew's real work visible in the repo and lifts "Use of Switch".
3. **Fix the step 1 clone URL and lead the reproduce section with the tool command.** Removes the one false step a stranger hits; lifts Clarity.
