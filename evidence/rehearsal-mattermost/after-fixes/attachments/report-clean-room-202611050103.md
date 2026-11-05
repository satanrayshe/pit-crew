# Judge report — pit-crew-r2

- Repository: `file:///root/fts/rehearsal/git/pit-crew-r2.git`, branch `main`
- Commit reviewed: `29b47c575e74f02453b63f42763bc494a639dac8` (`29b47c5 docs: add changelog entry`)
- `origin/main` at review time: `29b47c575e74f02453b63f42763bc494a639dac8` (pushed, matches)
- Clean-room folder: `clean-room-202611050103`, `git clone --depth 1`
- Kit: `pit-crew-kit` pulled, `judge-kit/check.py`
- Verdict: **BLOCKED**

## Verdict

The tool, the README, the template, the license and hygiene all hold up, but the
README still says `TODO(video-link)` at line 49 and there is no real demo video
link anywhere in the pushed repository. The gate is explicit: the judge blocks
until there is a real link.

## Gate

| Gate item | Result | Evidence |
|---|---|---|
| README section on how Switch is used and why it stops working without it | PASS | `README.md:63-77`, table of Switch primitives vs "Without Switch" |
| Architecture diagram | PASS | `README.md:42-47` and `README.md:81-88` mermaid; longer version `docs/architecture.md` |
| Reproduce steps a stranger can follow | PASS (with one URL caveat) | `README.md:93-155`; step 1 says `git clone https://git.pit.local/pit-crew.git`, which is not the public repo a stranger has — the tool's own install/run is exact at `README.md:18-40` |
| Template/config that sets up the Switch side | PASS | `pit-crew.template.yaml`, `version: 2`, four agents + room + documents + kickoff; parses per check.py |
| Demo video link | **FAIL** | `README.md:49` `Demo video: TODO(video-link)`; no video URL anywhere in tracked files |
| License | PASS | `LICENSE`, MIT, copyright 2026 satanrayshe |
| No secrets | PASS | check.py `secrets` and `local_files` pass across 36 tracked files; only `.env.example` (empty value) is committed, and `.env` is gitignored |

## Mechanical checks (`python3 pit-crew-kit/judge-kit/check.py .`)

`passed: false`; 8 of 9 checks pass. Failing check only:

- `readme_demo_video`: "README.md still has the TODO(video-link) marker"

Passing: `readme_switch_section`, `readme_reproduce_section`,
`readme_architecture`, `license`, `template` (1 of 1 parses, PyYAML),
`secrets` (no patterns in 36 files), `local_files` (no `.env`, `.switch/` or
local agent settings), `large_files`.

## What I ran

Safe, quick steps only, in the clean-room clone:

- `python3 pit_clock.py --version` -> `0.1.0`
- `python3 pit_clock.py 2026-11-06T06:21:00+00:00 --now 2026-11-06T05:09:00+00:00` -> `T-1h12m`, exactly the README example
- `python3 -m unittest discover -s tests -v` -> 12 tests, all pass
- `git fetch --unshallow` (to inspect history for hygiene) -> 7 commits
- `judge-kit` tests: **skipped**, `pytest` is not installed here
- `ruff check .`: **skipped**, `ruff` is not installed here
- Switch Console/Discord reproduce steps: **skipped** — need a Discord account, a coding-agent sign-in and more than ten minutes; also out of scope for judging the tool

## Rubric scores

Use of Switch (30%) — **7/10**. `pit-crew.template.yaml:119-380` defines the
four agents, room, addressing and documents; `README.md:63-77` maps each
feature to a Switch primitive. Weakness: `evidence/` contains only the
template lint and a judge-kit self-check (`evidence/README.md`); the checklist,
build log and judge report the README says the crew produces are not yet
committed, so the public repo is thin evidence of a real run.

Works (30%) — **10/10**. Fresh clone, stdlib only; the README's exact command
reproduces `T-1h12m` (`pit_clock.py:52-76`), 12 unit tests pass
(`tests/test_pit_clock.py`), `--version` prints `0.1.0`.

Clarity (20%) — **8/10**. `README.md:1-47` explains the product, the tool and
the diagram before any setup; the crew and Switch tables are scannable. It is
still 257 lines with long "Known limits" and judge-kit sections, and the
`git.pit.local` clone URL in step 1 (`README.md:102`) will confuse a stranger.

Hygiene (20%) — **8/10**. 7 focused commits, e.g. `29b47c5` one line,
`e8d5f9f` 3 files/11 lines, `42981e9` 3 files/172 lines; no secrets, no
`.env`, no `.switch/`, no files over 10 MB (`check.py`). The 2,516-line initial
commit `2560729` is the only large one and is a plausible bootstrap.

## Three fixes that gain the most points per hour

1. **Publish the demo video and replace `TODO(video-link)` (`README.md:49`).**
   Unblocks the whole gate; nothing else can make this SHIP-READY.
2. **Commit the room evidence into `evidence/`** — `pit-board` snapshot,
   build-log export, judge reports (`evidence/README.md` already names these
   files). Directly raises "Use of Switch" and makes the crew's work visible
   to the real judges.
3. **Fix step 1's clone URL to the real public repository and move the tool
   to the top of the reproduce section.** Raises Clarity and removes the one
   false step a stranger would hit.
