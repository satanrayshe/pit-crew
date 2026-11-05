<!-- room document 'pit-board', created by pit-scout at 2026-11-04 23:42:40.182951+00:00; snapshot taken at the end of the rehearsal -->

# pit-board

Updated: 2026-11-05T00:32Z (06:02 IST)
Deadline: 2026-11-06T05:09:00+05:30 = 2026-11-05T23:39:00Z
Last judged commit: f11fa02 (origin/main). Local, not pushed: f026b9b, dbf7422.

## Countdown
T-23h06m at the time above. Recomputed from the shell clock on every check, never from memory.

## Checklist (8/9 done)
Done only when judge-scorecard marks it done. Source: judge-scorecard updated 2026-11-05 00:08Z.

- [x] done - CLI tool prints time left to an ISO 8601 deadline, e.g. "T-1h12m" - owner: builder - DONE at e8d5f9f: fresh clone printed T-1h12m, 12/12 tests
- [x] done - README section on how Switch is used and why the work would not have happened the same way without it - owner: herald - gate PASS
- [x] done - README section with exact install and run commands, plus an example of its output - owner: herald - gate PASS; fix 2 verified at f11fa02 (reproduce now clones the judged repo)
- [x] done - README diagram of how the pit crew and the tool fit together - owner: herald - gate PASS (readme_architecture)
- [ ] open - README link to a demo video, or the marker TODO(video-link) until there is one - owner: herald / person - FAIL: README.md:49 still TODO(video-link); the only SHIP-READY blocker
- [x] done - LICENSE file - owner: builder - gate PASS
- [x] done - Switch template committed as pit-crew.template.yaml - owner: builder - gate PASS (parses)
- [x] done - no secrets, no .env file, no .switch folder - owner: builder (judge verifies) - gate PASS, 35 files clean
- [x] done - everything pushed to the public repository before the deadline - owner: builder / person - pushed through f11fa02; f026b9b and dbf7422 are still local

## Rule risks
- Demo video missing: mission allows "a link to a demo video, or the marker TODO(video-link) until there is one", but the judge gate requires the actual link for SHIP-READY. This is the only blocker.
- Unpushed work: "Work that is not pushed does not count." f026b9b (fix 3) and dbf7422 (README Switch section) are committed locally; origin/main is still f11fa02. The judge cannot count them until pushed.
- Residual wrong repo: pit-crew.template.yaml still defaults kit_url and the four icon_url values to github.com/satanrayshe/pit-crew, and docs/blog-draft.md:221 names it as upstream. Should point at https://git.pit.local/pit-crew.git.
- Stale evidence: f026b9b deletes evidence/judge-kit-self-check.json, but it is not pushed, so the judge still sees the stale file at origin/main.
- Deadline conflict: mission says "Two hours from the moment the crew starts"; room deadline is 2026-11-06T05:09:00+05:30 (~T-23h). This board counts to the room deadline; the person must confirm if the two-hour clause governs.
- Nothing is done until judge says so: only judge says SHIP-READY. Current verdict is BLOCKED.
- Scope: a late request to add python-dateutil was correctly held. Under 24h left, dependencies and new features are out unless the judge gate needs them.

## Next three tasks (most valuable first)
1. person - record and post the demo video link; it is the only SHIP-READY blocker (herald can supply the script).
2. builder - push f026b9b and dbf7422, and repoint the template kit_url/icon_url plus blog-draft upstream at https://git.pit.local/pit-crew.git.
3. judge - after the push, re-run the full clean-room review and update judge-scorecard.
