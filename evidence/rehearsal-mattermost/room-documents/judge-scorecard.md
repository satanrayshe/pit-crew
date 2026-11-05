<!-- room document 'judge-scorecard', created by pit-judge at 2026-11-04 23:53:40.484189+00:00; snapshot taken at the end of the rehearsal -->

# Judge scorecard

Updated: 2026-11-05 00:38 UTC

## Current verdicts
- `main` at f11fa02: **BLOCKED** — demo video link still missing; fix 3 (stale evidence) was committed local as f026b9b but is not on main yet.
- Branch `rehearsal-pr` at dbf7422 vs main f11fa02: **SHIP-READY** — both Done-when items met; recommend merge.

## Rubric scores (main, room rubric, from the full review at e8d5f9f)
| Line (weight) | Score | Evidence |
|---|---|---|
| Use of Switch (30%) | 9 | pit-board checklist/countdown; builder pushed 42981e9 then e8d5f9f after owner approval; judge clean-room verdict + this scorecard; pit-crew.template.yaml encodes the crew, room, docs and kickoff. |
| Works (30%) | 9 | Fresh clone at e8d5f9f: README command printed T-1h12m, --version printed 0.1.0, 12/12 unittests passed. Off: README reproduce step named github.com/satanrayshe/pit-crew (fixed in f11fa02). |
| Clarity (20%) | 8 | README well ordered but 257 lines for two audiences; stale evidence/judge-kit-self-check.json (run on 2560729) and TODO(screenshot) at README.md:51. |
| Hygiene (20%) | 8 | check.py: no secrets, no committed .env/.switch/, no file >10 MB in 35 files; latest commits small and conventional. Off: 891e405 is a large 17-file docs/rules commit; stale committed evidence JSON. |

Weighted 8.6/10. Not rescored for the docs-only commits after e8d5f9f.

## Gate (main)
- PASS readme_switch_section, readme_reproduce_section, readme_architecture, license, template (1/1 parses), secrets, local_files, large_files.
- FAIL readme_demo_video — README.md:49 still TODO(video-link). The mission allows the marker while there is no video, but the judge gate needs the actual link before SHIP-READY (rules/mini-hackathon.md:53-55 confirms this is intentional).

## Checklist items answered
| # | Item | Answer | Evidence |
|---|---|---|---|
| 1 | CLI prints time left to an ISO 8601 deadline, e.g. T-1h12m | DONE | Fresh clone at e8d5f9f. README command printed T-1h12m; real deadline printed T-23h45m; --version printed 0.1.0; 12/12 unittests OK. |

## Fixes verified
| Fix | Answer | Evidence |
|---|---|---|
| Fix 2 — README reproduce step clones the judged repo URL | DONE | Fresh clone at f11fa02 (clean-room-202611050007): README.md:102 now reads `git clone https://git.pit.local/pit-crew.git && cd pit-crew`. Residual: pit-crew.template.yaml still defaults kit_url and the icon_url values to github.com/satanrayshe/pit-crew. |

## PR review: rehearsal-pr (clean-room-202611050036)
Base main f11fa02; HEAD dbf7422; diff FETCH_HEAD...HEAD = 2 commits, 3 files, +19/-73.
| Done-when item | Answer | Evidence |
|---|---|---|
| 1. evidence/judge-kit-self-check.json removed and nothing still links to it | MET | Deleted in f026b9b; no grep hits for judge-kit-self-check at HEAD; evidence/README.md row removed; README Evidence paragraph updated. |
| 2. README's Switch section ties the run to real commit hashes | MET | New paragraphs cite 42981e9, e8d5f9f and f11fa02; git cat-file -t returns commit for all three. |
Extras: correct yes, small yes, readable yes, in style yes, tested (docs-only; check.py hygiene passes, 12 tests OK), nothing unrelated yes. Minor nit: one over-long README line in the Evidence paragraph. check.py JSON at /tmp/opencode/check-pr-202611050036.json.

## Open blockers
1. Demo video link missing on main (README TODO(video-link)). Only blocker for the main SHIP-READY verdict.
2. f026b9b (fix 3) and dbf7422 are committed local but were not on origin/main as of this review; pushing them needs the owner's go-ahead.
