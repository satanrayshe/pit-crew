<!-- room document 'judge-scorecard', created by fx-judge at 2026-11-05 01:04:19.778343+00:00; snapshot taken at the end of the after-fix run -->

# Judge scorecard — pit-crew-r2

Re-reviewed at `clean-room-202611050106` (01:06 UTC): the pushed tip is still commit `29b47c5` (`29b47c575e74f02453b63f42763bc494a639dac8`), unchanged since the 01:03 review, and equal to `origin/main`. `check.py`: 8/9, failing only `readme_demo_video`. No new evidence has been pushed.

## Verdict: BLOCKED

## Scores

| Rubric line | Score | Evidence |
|---|---|---|
| Use of Switch (30%) | 7/10 | `pit-crew.template.yaml:119-380` (4 agents, room, addressing, documents, kickoff); `README.md:63-77` Switch-primitive table. Evidence folder only has template lint + judge-kit self-check; no committed pit-board, build log or judge report. |
| Works (30%) | 10/10 | `pit_clock.py` prints `T-1h12m` from the README's exact command; 12/12 unittest tests pass; stdlib only. |
| Clarity (20%) | 8/10 | `README.md:1-47` product, tool and diagrams up front; 257 lines and a `git.pit.local` clone URL at `README.md:102` cost points. |
| Hygiene (20%) | 8/10 | 7 commits, mostly small (`29b47c5` 1 line, `e8d5f9f` 11 lines); no secrets, no `.env`, no `.switch/`, no >10 MB files. |

## Open blockers

- BLOCKER: no real demo video link. `README.md:49` is `Demo video: TODO(video-link)`; no video URL in any tracked file. The gate blocks until a real link is pushed.

## Mission table

| Mission item | Done or not done | Evidence |
|---|---|---|
| CLI prints time left to an ISO 8601 deadline, e.g. T-1h12m | done | `pit_clock.py:52-76`; ran `python3 pit_clock.py 2026-11-06T06:21:00+00:00 --now 2026-11-06T05:09:00+00:00` -> `T-1h12m` |
| README: how Switch is used and why the work would not be the same without it | done | `README.md:63-77` "How Switch is used (and why it breaks without it)" |
| README: exact install and run commands, plus example output | done | `README.md:18-40`; reproduced output `T-1h12m` |
| README: diagram of how the pit crew and the tool fit together | done | `README.md:42-47` mermaid; also `README.md:81-88` and `docs/architecture.md` |
| README: link to a real demo video | not done | `README.md:49` is `TODO(video-link)`; no YouTube/Loom/Vimeo URL tracked |
| LICENSE file | done | `LICENSE`, MIT |
| Switch template committed as `pit-crew.template.yaml` | done | `pit-crew.template.yaml`, `version: 2`, parses in check.py |
| No secrets | done | check.py `secrets` passes over 36 files; no token/key/webhook patterns |
| No `.env` file | done | check.py `local_files` passes; only empty `.env.example` committed, `.env` gitignored |
| No `.switch` folder | done | check.py `local_files` passes; none tracked |
| Everything pushed before the deadline | done | HEAD `29b47c5` equals `git ls-remote origin refs/heads/main` at 01:06 UTC |
| README section on Switch / architecture / reproduce / template / video / license / no secrets (gate) | not done | Gate fails only on the demo video item above; the other six gate items pass |
