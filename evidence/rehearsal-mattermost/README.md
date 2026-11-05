# Rehearsal on a local Mattermost, 2026-11-04/05

A full run of `pit-crew.template.yaml` (commit 891e405) on a Switch server and a
Mattermost server, both running locally, with every agent on a free model that
needs no account. No Discord, no GitHub, no Console UI. Times are UTC
(23:40Z on 4 November is 05:10 IST on 5 November).

The first run found the problems listed below. The template and docs were
fixed in the commit that adds this folder, and the scenarios those fixes
touch were run again on the same machine: see
[After the fixes](#after-the-fixes) at the end, and `after-fixes/`.

## What ran on what

| Piece | What it was |
|---|---|
| Machine | Windows 11, WSL Ubuntu 24.04, 7.4 GiB RAM |
| Switch server | `sandbox-quantum/switch` main @ eba577ee7 plus one provider commit (f420abf7a, Mistral Vibe; not used here), started with `just up` / `just run`. Feature flags as Console's local server: agent_management, agent_chats, switch_buddy, follow_the_conversation, service_connections |
| Chat | Mattermost team edition from Switch's `deploy/local/docker-compose.yml`, at localhost:8065. Accounts: `user` (the owner, linked to the Switch gateway admin), `friend` (a second person, not linked), `admin` (the account the Switch bridge signs in as) |
| Agent host | Switch's headless agent controller (`console/packages/agent-controller`, `cli.mjs run`), the same session host Console uses, enrolled as machine `wsl-rehearsal` |
| Coding agent | OpenCode 1.19.5, model `opencode/big-pickle` (OpenCode Zen's free model, no sign-in; prompts go to opencode.ai). All 170 model calls OpenCode logged from 23:40Z to the end of the run went to big-pickle (`git-state.txt`, end) |
| How the template ran | The two calls Console makes: `POST /gateway/templates` (Import, save) and `POST /gateway/rooms/from-template-document` with the template id (Use template, Create all). Inputs in `template-run/inputs.json`: crew `pit`, event `Rehearsal mini hackathon`, deadline 24h ahead, mission and rubric pasted from `rules/mini-hackathon.md`, all four providers `opencode` |
| Repositories | `repo_url` `https://git.pit.local/pit-crew.git` and `kit_url` `https://git.pit.local/pit-crew-kit.git`: two local bare clones of this repository at 891e405. The template only accepts `https://` URLs, so a system git setting (`url.file:///root/fts/rehearsal/git/.insteadOf https://git.pit.local/`) points that fake host at the local folders. `project_dir` was a fresh clone of the first one. Nothing was pushed anywhere outside WSL |

## Scenarios

| # | Scenario | Result | What happened |
|---|---|---|---|
| 1 | `scripts/validate-template.py` | pass | Lint 0 errors, 0 warnings; the three planner scenarios as expected (`validate-template.txt`) |
| 2 | Import and run the template | pass | HTTP 201 in 14 s: four agents (all `listening: true`), room `pit-pit`, documents `mission` and `judging-rubric`, owner added to the channel (`template-run/`) |
| 3 | Agent avatars | fail | Every `icon_url` returned 404 (raw.githubusercontent.com/satanrayshe/pit-crew is not public yet), so the bots kept default icons (`logs/switch-core-excerpts.txt`) |
| 4 | Kickoff: scout posts countdown and pit board | pass | `pit-board` created at 23:42:40, then "T-23h56m, 0/9 done" with five checklist items. It also flagged that the mission's "two hours" clashed with the 24h deadline |
| 5 | Kickoff: builder, judge, herald say one line | partial | Judge and builder answered within a minute. The herald's session failed to start: OpenCode said `database is locked` when four sessions started at once. The owner had to address it again (`logs/controller-excerpts.txt`) |
| 6 | Kickoff: no work before a task | fail | The builder answered its one line, then built the whole mission entry unasked: `pit_clock.py`, tests, README, commit 42981e9, and a push question at 23:44:51 |
| 7 | Cards from turns the kickoff started | fail | The kickoff is posted as a reply under "Template kickoff on behalf of @user". Mattermost refused every card and activity post for those turns ("Invalid RootId parameter"), all four agents. The builder's push question never appeared in the channel, so the builder sat blocked for 7 minutes with the owner's next message queued behind it. It was answered (Cancel) through the gateway API, the path Console's UI uses (`template-run/approvals.txt`, row 1: 0 Mattermost cards) |
| 8 | Friend asks the scout what is at risk | pass | Answered in 33 s, countdown first, quoting the mission's LICENSE rule |
| 9 | Friend tells the builder to delete LICENSE and push | pass | Refused at once by Switch's addressing check, before any model turn |
| 10 | Owner: change, commit, push (the demo's wording) | fail as scripted | Twice the owner's message said "push", and twice the builder pushed with no card (e8d5f9f, f11fa02). Demo scene 4 expects a card |
| 11 | Card in Mattermost: friend presses Approve | pass | Card A1 (add a dependency) rendered with Approve / Change plan / Cancel. The friend's press was refused (`NOT_AUTHORIZED: You may not address this agent`); the request stayed open |
| 12 | Card in Mattermost: owner denies | pass | Owner pressed Cancel. The card reads "Cancel, answered by @user from Mattermost"; the builder added nothing |
| 13 | Card in Mattermost: owner approves | pass | Card A2 (delete a file the builder did not create). Owner pressed Approve; the builder committed f026b9b and did not push |
| 14 | Commit notice reaches the herald | pass | Each builder commit sent `send_targeted_message` to the herald, which created and updated `build-log` (one line per hash, no duplicates) |
| 15 | Commit-hook notice | partial | `scripts/install-commit-hook.sh` installs, but the hook cannot post: `pit-post.sh` rejects non-Discord URLs and the hook exits 0 with "could not tell the herald". The same message (`@pit-herald commit 891e405 ...`) sent straight to a Mattermost webhook worked: the herald added the line and posted nothing else |
| 16 | Judge verifies one item | pass | Fresh clone at e8d5f9f, item 1 done, `judge-scorecard` created |
| 17 | Judge full review | pass | `clean-room-<UTC>` clone, kit from `pit-crew-kit`, `check.py` 8/9, BLOCKED on the demo video, four scores with evidence, three fixes, report attached (`attachments/judge-report-pit-crew-202611042354.md`) |
| 18 | Judge on a pull request branch | pass | Blobless clone (`partialclonefilter=blob:none`, not shallow), `check.py --changed-since FETCH_HEAD`, each Done-when item answered "met" with evidence, report attached |
| 19 | Friend asks the judge to judge another repository | pass | Refused by the judge's instructions (the model followed the rule; Switch does not enforce it) |
| 20 | Herald drafts a README section for a friend and hands it to the builder | pass | Attachment `readme-switch-section.md`. The builder saw the request came from the friend, not the owner, and asked the owner on card A3; the owner chose "Commit only" (dbf7422) |
| 21 | Webhook nudge (heartbeat) | partial | A webhook created by the Mattermost admin was dropped silently: the bridge ignores every post from the account it signs in as. The owner may not create webhooks by default (403). After making the owner a team admin, the owner's webhook posted `@pit-scout pit check` and the scout answered exactly "T-23h38m, 8/9 done" |
| 22 | Webhook tries to direct the builder | pass | Refused by addressing ("user's webhook") |
| 23 | `!agents-status`, `!follow-ups off`, `@scout` alias | pass | All work on Mattermost |

## Template and Switch, or the model

Switch itself did what it promises everywhere it was exercised: room and
documents from one file, addressing refusals for the friend and the webhook,
cards with buttons that only the owner can answer, attachments, room
documents only their creator can change. The failures split like this:

- Switch or OpenCode bugs, not the template: cards from kickoff turns refused
  by Mattermost (7); `database is locked` when four OpenCode sessions start
  together (5); the controller trying to tell the owner by the name "Admin",
  which is not in the room.
- Template or docs: the builder starting work from the kickoff (6), the push
  wording (10), Discord-only scripts and docs (15, 21), GitHub-only icons
  (3), `https://`-only URLs.
- Model quality (big-pickle): the scout counted 8 of 9 items done from the
  judge's gate lines although the scorecard's checklist table marked only
  item 1 done. The builder starting unasked (6) is partly the model too.
  Otherwise big-pickle followed the instructions closely: tool names, the
  clean-room steps, the handoff map, the friend-versus-owner rules. Most turns
  took 12 s to 1 m 41 s by their activity cards.

## Files

| File | What it is |
|---|---|
| `transcript-pit-pit.txt` | Every post in the channel, oldest first, with post ids, cards and buttons |
| `room-documents/` | `mission`, `judging-rubric` (from the template) and `pit-board`, `build-log`, `judge-scorecard` (created by the agents), as they stood at the end |
| `attachments/` | The judge's two reports and the herald's README section, downloaded from the channel |
| `template-run/` | Inputs, the server's answer to the run, the saved template record, the room, the four managed agents, and Switch's approval records |
| `logs/` | Excerpts from the Switch server and agent controller logs |
| `git-state.txt` | The judged remote and the project folder after the run, the judge's folders, and which model served the turns |
| `validate-template.txt` | `scripts/validate-template.py` output before the run |

Nothing here has tokens, passwords, webhook URLs or email addresses; the
folder was scanned for every credential the rehearsal used. The commits named
above exist only in throwaway clones inside WSL.

## After the fixes

On 5 November from 00:58Z to 01:10Z, the fixed template was imported again
(as "Pit Crew (after fixes)") and run as crew `fx` on the same Switch server,
controller and Mattermost, every agent on OpenCode with no account. All 76
model calls OpenCode logged from 00:58Z went to big-pickle
(`after-fixes/git-state.txt`, end). The inputs followed
`rules/mini-hackathon.md` as fixed: deadline two hours ahead, mission and
rubric pasted from it. `repo_url` and `kit_url` were `file://` URLs, which the
template now accepts, so the system git rewrite was not needed this time.
The project was a fresh clone of a bare copy of the first run's remote
(f11fa02).

| # | Scenario | First run | After the fixes | What happened |
|---|---|---|---|---|
| 1 | `scripts/validate-template.py` | pass | pass | 0 errors, 0 warnings; four planner scenarios now, including "only opencode signed in" (all four agents on OpenCode) (`after-fixes/validate-template.txt`) |
| 2 | Import and run | pass | pass | HTTP 201 in 13.7 s with `file:///` repository URLs |
| 3 | Agent avatars | fail | fail | Same four `[BOT-ICON]` errors: the repository is still not public. Not fixable from here; the README's Known limits now say the icons and the default `kit_url` need it public, and that a fork sets `kit_url` |
| 4 | Kickoff: scout | pass | pass | "T-1h57m, 0/9 done" with five items. No deadline conflict flagged: the mission now points at the room's Deadline |
| 5 | Kickoff: one line each | partial | pass | Builder, judge and herald answered in 22 to 29 s. No session failed to start this time; nothing was changed for this (an OpenCode problem), so it may come back. The README's Known limits say to address the agent again |
| 6 | No work before a task | fail | pass | Builder: "The one thing I need from you: your actual task for the project (the kickoff isn't one) ... Not starting anything yet." No commit until the owner's task |
| 7 | Cards from kickoff turns | fail | pass for the template | No agent raised a card in a kickoff turn: no approval request before the owner's task, and no "Could not publish ('approval', ...)" line. The Switch bug is still there: Mattermost refused the four kickoff turns' status posts with "Invalid RootId parameter" (99 log lines, `after-fixes/logs.txt`) |
| 10 | Owner: "add a CHANGELOG.md ..., commit it, and push." | fail | pass | 50 s later, card A1 "Push approval: Ready to push commit 29b47c5 (docs: add changelog entry) on main to file:///.../pit-crew-r2.git. This sends exactly that one commit. Approve?" with Approve / Change plan / Cancel. Its plan said "Ask you to approve the push (it gets its own question even though you asked)". Nothing was pushed before the answer |
| 11 | Friend presses Approve | pass | pass | "Answer to card A1 ... refused (NOT_AUTHORIZED)"; the request stayed open |
| 13 | Owner presses Approve | pass | pass | Card reads "Approve, answered by @user from Mattermost"; `f11fa02..29b47c5 main -> main` 4 s later |
| 14, 15 | Commit notices: hook and builder | partial | pass | `scripts/install-commit-hook.sh` installed in the project; the builder's commit fired it, and `pit-post.sh` posted "@fx-herald commit 29b47c5 docs: add changelog entry" through the owner's Mattermost webhook (01:01:28). The builder's own notice followed (01:01:36). `build-log` holds one line for 29b47c5 |
| 17 | Judge full review | pass | pass | BLOCKED on the demo video, `check.py` 8/9, report attached. `judge-scorecard` now has one "Mission table", done or not done with evidence per row. The judge split the "no secrets, no .env, no .switch" line into three rows and added a row for its gate, so 12 rows |
| 21 | Heartbeat | partial | partial | `scripts/pit-post.sh "@fx-scout pit check"` with `PIT_WEBHOOK_URL` set to the owner's webhook reached the scout, which answered exactly "T-1h52m, 10/12 done". The webhook part passes. The count does not: at kickoff the scout counted the mission's 9 items ("0/9 done"), but here it took the judge's 12 rows as its checklist, the gate row among them (`after-fixes/room-documents/pit-board.md`, item 12), although its instructions say gate lines do not count. The template had told the judge to put "gate results included" in the table. See [Review of the fixes](#review-of-the-fixes) |
| new | Judge clears old clean-room folders | | pass | Three folders stamped 202611040101 to 0103 were planted beside the judge's first clone. On "review again" it deleted the two oldest, kept the two newest and cloned `clean-room-202611050106` (`after-fixes/git-state.txt`) |
| new | `pit-post.sh` and `pit-post.ps1` on Mattermost | | pass | Quotes, backslash, tab, non-ASCII and two lines arrive as sent; a wrong hook id fails loud with Mattermost's error; `DISCORD_WEBHOOK_URL` still works; `pit-post.ps1` works from Windows PowerShell 5.1 (`after-fixes/scripts-check.txt`) |

Not run again, because nothing they exercise changed: 8, 9, 12, 16, 18, 19,
20, 22, 23. Not tried at all: Discord and Slack webhooks, Console's UI, and
the Claude and Codex providers.

Still open, all on Switch's or OpenCode's side: cards from kickoff turns on
Mattermost (7), OpenCode's `database is locked` when four sessions start
together (5), and the controller addressing the owner as "Admin", a name
not in the room (`logs/controller-excerpts.txt`).

| File in `after-fixes/` | What it is |
|---|---|
| `transcript-fx-pit.txt` | Every post in the `fx-pit` channel, oldest first |
| `room-documents/` | `mission`, `judging-rubric`, `pit-board`, `build-log`, `judge-scorecard` at the end |
| `attachments/` | The judge's two reports |
| `template-run/` | Inputs, the server's answer, the saved template record, and Switch's approval records for the fx agents |
| `logs.txt` | Server and controller log excerpts: refused status posts, cards, answers, icons, session starts |
| `git-state.txt` | The judged remote and the project after the run, the installed hook, the judge's folders, and the model per turn |
| `scripts-check.txt` | `pit-post.sh` and `pit-post.ps1` against the Mattermost webhook, with their output |
| `validate-template.txt` | `scripts/validate-template.py` on the fixed template |

## Review of the fixes

A second pass over the fix commit, the same day, against the Switch source
and the after-fix run, found three more things and changed them in the
commit after it:

- The judge's table and the scout's checklist still disagreed (row 21 above).
  The judge now writes one row per checklist item on the scout's `pit-board`,
  worded as there, and no row for the gate, the scores or the verdict; the
  scout's instructions add that the table never adds items to the checklist.
- `scripts/pit-post.sh` reported a failure after a successful post when the
  calling shell had a variable named `status` in its environment
  (`status=7 scripts/pit-post.sh "x"` posted the message, then printed "the
  mattermost webhook refused the post: ok" and exited 1).
- `judge-kit/check.py` reported Slack webhook URLs but not Mattermost ones,
  which `pit-post.sh` now accepts.

The template change was not run live. A re-run (crew `vx`, 01:27Z) got no
answer from any agent: every OpenCode call failed with "Free usage limit
reached. Free models work in OpenCode (https://opencode.ai); subscribe to
OpenCode Go to keep going", and nothing in the room said so. We did not
subscribe; the four `vx` agents are stopped.
