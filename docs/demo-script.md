# Demo video: storyboard (under 3 minutes)

Target length 2:45. Every shot is a real turn, sped up where marked; nothing
is staged in an editor. The form asks tracks 1 and 2 to show "the agent
working in a real chat with your teammates", so a second person (a friend on
their own Discord account) appears in scenes 3 and 4.

## Before recording

- Pre-warm the four agents so their sessions are already running
  (`!agents-status` shows all four green), and run `!follow-ups off` so stray
  chatter does not wake anyone mid-take.
- Use a crew name you have not used before, for example `demo1`; agent names
  are unique on the server.
- Keep lines in Discord code blocks short; long code-block lines can be split
  and cut off.
- Hide anything private: email addresses, tokens, the webhook URL, account
  pages in Console settings.
- Record the phone screen for scene 4 separately and cut it in.
- Run scene 4 once off camera. The builder asks on a card before every
  push, even when your message says "and push"; an older version of the
  template took those words as the approval and pushed without a card.
- The judge blocks Pit Crew until its README links a video, so the
  SHIP-READY shot in scene 7 needs a video link already in the README (an
  unlisted rehearsal cut), or shoot that scene on the mini-hackathon
  repository.

## Scenes

| Time | Scene | On screen | Voice-over |
|---|---|---|---|
| 0:00 to 0:10 | Hook | Split screen: you at the desk late at night, and the Discord channel `#demo1-pit` with four agent avatars. The scout's latest line reads like `T-38h, 5/14 done`. | "Solo at a hackathon you are the driver and the whole pit crew. This is the crew." |
| 0:10 to 0:30 | One template | Console, Templates, Import template, drop `pit-crew.template.yaml`, Import, save, Use template. The form: crew, repository, project folder, deadline, mission; the Advanced fold with a provider per agent. Create all. Four agent cards appear, a Discord channel is created, the kickoff posts, and (4x) the scout posts the pit board while the others say hello. Caption: "One YAML file: 4 agents, 1 room, 2 documents, 1 kickoff." | "One template sets up four agents and a channel. Each can run on Claude Code, Codex or OpenCode." |
| 0:30 to 0:45 | The scout | Your friend types `@scout what is at risk?` The scout answers with the countdown and two risks, quoting the rule: the README does not say how Switch is used; no demo link. Cut to the `pit-board` document in Console. | "The scout turns the rules into a checklist and a countdown, and it answers anyone in the room." |
| 0:45 to 1:15 | The builder, and who is in charge | You type `@builder add the commit-hook script and push`. It posts a five-line plan; the status shows it working. A card appears: push to origin/main, Approve / Change plan / Cancel. Your friend presses Approve and is refused. You approve from your phone (phone footage). It pushes; you can see it notify the herald and ask the judge to verify. | "Only I can direct the builder or approve its push, even from my phone. My friends can talk to the rest of the crew." |
| 1:15 to 1:35 | The judge on Pit Crew | `On it, clean-room clone`. Then the judge's real verdict (expect BLOCKED on the demo link), with its scores and `judge-report.md` attached. Overlay: "The judge only sees what is pushed, like the real judges." | "The judge clones the public repo into an empty folder and scores it against the rubric. It is the only one allowed to say ship-ready." |
| 1:35 to 2:10 | A real pull request to Switch | You type `@judge judge branch feat/mistral-vibe-provider of my Switch fork against issue #774's Done-when list`. The judge clones the branch, runs `check.py --mode hygiene --changed-since` against upstream main and the project's own tests for the touched files, and answers each Done-when item with met, not met or not shown, with evidence. Cut to the pull request on GitHub with `Closes #774`. Caption: "Same crew, a real Track 03 pull request." | "We used the crew on our own pull requests to Switch. The crew kept the checklist and judged every push from a clean clone." |
| 2:10 to 2:25 | Closing the loop | `@herald draft the "How Switch is used" section and a #HowISwitch post`. An attachment arrives; the herald hands the README change to the builder; you approve the push on a card. `@judge re-check`: `SHIP-READY`. | "The herald writes from the git history and never publishes. The judge re-checks, and now it passes." |
| 2:25 to 2:40 | Why Switch | The architecture diagram from `docs/architecture.md`. | "Take Switch away and this is four terminals: no shared room, no approvals from my phone, no friends in the loop." |
| 2:40 to 2:45 | Close | "Pit Crew ran this hackathon with us." Repository URL and #HowISwitch. | Same words. |

If a different pull request is ready first, swap the branch and issue number
in scene 6; keep the shape.

## After recording

Upload to YouTube as unlisted, then replace `TODO(video-link)` in the README
with the link. The judge kit fails the submission until you do.
