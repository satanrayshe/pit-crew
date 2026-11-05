# Judge report — Pit Crew

- **Verdict: BLOCKED**
- Reviewed: `origin/main` at `e8d5f9f` (`e8d5f9fd84c43d38cfe2ce4c2c7a0fe3f76fad64`)
- Clean room: `clean-room-202611042354` (fresh `git clone --depth 1` of https://git.pit.local/pit-crew.git)
- Kit: `pit-crew-kit` pulled before the review; `judge-kit/check.py` (submission mode)
- Date: 2026-11-04 23:55 UTC

## Why blocked

One gate item is missing: a **demo video link**. `README.md:49` still reads
`Demo video: TODO(video-link)`, and `judge-kit/check.py` fails
`readme_demo_video` for the same reason. The mission allows the TODO marker
while there is no video, but the judge gate requires the link itself before a
SHIP-READY verdict — and `rules/mini-hackathon.md:53-55` says the same.
Everything else in the gate passes.

## Gate

| Gate item | Result | Evidence |
|---|---|---|
| README section on how Switch is used and why it stops working without it | PASS | `README.md:63-77` "How Switch is used (and why it breaks without it)", with a `Without Switch` column and `docs/architecture.md:66-79` |
| Architecture diagram | PASS | `README.md:42-47` mermaid; full diagrams in `docs/architecture.md:7-42` |
| Reproduce steps a stranger can follow | PASS | `README.md:93-155` "Reproduce in about 30 minutes" (8 numbered steps) |
| Template/config that sets up the Switch side | PASS | `pit-crew.template.yaml` (version 2, 4 agents, 1 room, 2 docs, kickoff), parses via check.py |
| Demo video link | **FAIL** | `README.md:49` `TODO(video-link)` |
| License | PASS | `LICENSE` (MIT, 2026 satanrayshe) |
| No secrets | PASS | check.py: no secret patterns in 35 files; no `.env`, `.switch/` or `.claude/settings.local.json`; `.env.example` is empty and documented |

Mechanical check: **8 of 9 pass**, exit code 1. The only failure is
`readme_demo_video`. Full JSON kept at `/tmp/opencode/check-full-202611042354.json`.

## What I ran, and what I skipped

Ran in the fresh clone:

- `python3 pit_clock.py 2026-11-06T06:21:00+00:00 --now 2026-11-06T05:09:00+00:00` → `T-1h12m` (exact README example)
- `python3 pit_clock.py 2026-11-06T05:09:00+05:30` → `T-23h45m`
- `python3 pit_clock.py --version` → `0.1.0`
- `python3 -m unittest discover -s tests` → `Ran 12 tests ... OK`
- `python3 pit-crew-kit/judge-kit/check.py clean-room-202611042354` → 8/9, only the video marker fails
- `git fetch --unshallow` on the clone to read history for the hygiene score

Skipped, with reasons:

- Installing Switch Console, running a Switch server, and the Discord bridge setup (`README.md` steps 2-7): needs a sign-in and more than ten minutes.
- `scripts/validate-template.py`: needs a separate Switch checkout (`uv run --project <switch>/core ...`), outside the two repos I may clone.
- `ruff` and `python3 -m pytest judge-kit`: neither ruff nor pytest is installed here; the project's own documented test command is `unittest`, which passed. No dependency install was attempted.

## Scores (room rubric, 1-10 each)

| Rubric line (weight) | Score | Evidence |
|---|---|---|
| **Use of Switch (30%)** — did the crew in the room do real work: checklist, reviewed push, clean-room verdict? | **9** | `pit-board` room document tracks the checklist/countdown; builder pushed `42981e9` then `e8d5f9f` after the owner asked; this judge's `judge-scorecard` records the item-1 clean-room verdict. Template `pit-crew.template.yaml:117-380` encodes the four agents, room, docs, addressing and kickoff. |
| **Works (30%)** — does the tool run from a fresh clone by following the README exactly? | **9** | Fresh clone at `e8d5f9f`: README command printed `T-1h12m`, `--version` printed `0.1.0`, 12/12 unittests passed. One mark off: `README.md:102` tells a stranger to clone `github.com/satanrayshe/pit-crew`, a different URL from the repository being judged, so the README's own starting path does not land on this revision. |
| **Clarity (20%)** — could a stranger understand the README in two minutes? | **8** | `README.md` is well ordered (what it is, quick tool example, crew table, Switch table, diagram, reproduce, judge kit, known limits), but it is 257 lines spanning two audiences. `evidence/judge-kit-self-check.json` is stale (run on `2560729`, says "Reproduce in 15 minutes") and `README.md:51` still has `TODO(screenshot)`. |
| **Hygiene (20%)** — small commits, no secrets, no stray files. | **8** | check.py: no secrets, no committed `.env`/`.switch/`, no file over 10 MB in 35 files. The two submission commits are small and conventional (`42981e9` feat, 172 insertions; `e8d5f9f` feat, 11 insertions). Off: `891e405` is a large docs/rules commit (17 files, 443 lines changed), and the committed `evidence/judge-kit-self-check.json` is a stale `/tmp` run. |

Weighted: 9×0.30 + 9×0.30 + 8×0.20 + 8×0.20 = **8.6 / 10**, held at BLOCKED by the missing video link.

## Three fixes, most points per hour

1. **Record and link a demo video (or a 60-90 s screen capture), replace `TODO(video-link)`.** This is the only blocker; it flips BLOCKED to SHIP-READY on its own. About 30-45 minutes.
2. **Fix the clone URL in the README's reproduce section** so it names the repository judges actually clone (or state plainly that `https://git.pit.local/pit-crew.git` is the entry and the GitHub repo is the upstream project). Cheap, and it removes the biggest "works as documented" doubt.
3. **Refresh or delete `evidence/judge-kit-self-check.json`** so it matches `e8d5f9f` (it currently cites `2560729`, a `/tmp` path and "Reproduce in 15 minutes"). Keeps evidence credible and removes stale noise.

## Notes

- Single-item recheck this session: checklist item 1 (CLI prints time left to an ISO 8601 deadline, e.g. `T-1h12m`) — **done** at `e8d5f9f`.
- No other repository or branch was cloned; only the two URLs the room allows.
