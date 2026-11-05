<!-- room document 'pit-board', created by fx-scout at 2026-11-05 00:59:10.769648+00:00; snapshot taken at the end of the after-fix run -->

# Pit board — Rehearsal mini hackathon (after the fixes)

Updated: 2026-11-05 01:05 UTC (scout)

## Countdown

**T-1h52m** to 2026-11-05T08:27:00+05:30 (02:57 UTC).
Pace: under 2h — features are frozen; only checklist items that remain.

## Checklist (10/12 done)

Done only when judge-scorecard's mission table says done. Counts follow that table (judge review of 29b47c5).

1. done — CLI prints time left to an ISO 8601 deadline, e.g. T-1h12m — builder
2. done — README: how Switch is used, and why the work would not have happened the same way without it — herald
3. done — README: exact install and run commands, plus example output — herald
4. done — README: diagram of how the pit crew and the tool fit together — herald
5. open — README: link to a real demo video — person
6. done — LICENSE file — builder
7. done — Switch template committed as pit-crew.template.yaml — builder
8. done — no secrets — builder
9. done — no .env file — builder
10. done — no .switch folder — builder
11. done — everything pushed to the public repository before the deadline — builder
12. open — judge gate (Switch / architecture / reproduce / template / video / license / no secrets) — judge

## Rule risks

- **No demo video link.** `README.md:49` still says `TODO(video-link)`. Mission: "a link to a demo video (the README may say TODO(video-link) meanwhile; the judge blocks until there is a real link)." Verdict is BLOCKED at 29b47c5 until a real link is pushed.
- **README step 1 clone URL is not the real repo.** It says `git clone https://git.pit.local/pit-crew.git`, so a stranger following the README exactly cannot get the code. Mission requires "a section with the exact commands to install and run the tool" and the rubric asks "does the tool run from a fresh clone by following the README exactly?"
- **New work must be pushed.** Mission: "Everything must be pushed to the public repository before the deadline. Work that is not pushed does not count." HEAD 29b47c5 currently equals origin/main; re-check after any new commit.
- **Crew evidence is not in the repo.** Rubric: "Use of Switch (30%): did the crew in the room do real work: a checklist, a reviewed push, a clean-room verdict?" Pit board, build log and judge report are room documents only; judge scored 7/10 partly for this.

## Next three tasks (most valuable first)

1. Person: publish a real demo video and give the link; that is the only mission blocker.
2. Builder: fix README step 1 to the actual public clone URL, commit and push.
3. Builder: once the video link lands, replace the TODO and commit the pit board, build log and judge report under evidence/, push, then judge re-reviews.
