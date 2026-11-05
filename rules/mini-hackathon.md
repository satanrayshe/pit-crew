# Mini hackathon: a two-hour event for trying Pit Crew

A made-up event, short enough that you see the scout change pace, the judge
block and then pass, and the herald write it up, in one sitting. Use it the
first time you run the template.

## How to run it

1. Create a small public GitHub repository for the entry, for example
   `pit-crew-mini`, with an empty README and a `.gitignore` listing
   `.switch/` and `.claude/settings.local.json` (coding agents and Console
   can keep agent files there). Push both, and clone it.
2. Import `pit-crew.template.yaml` and fill the form:
   - **Crew name**: something new, such as `mini1`.
   - **What you are racing for**: `Mini hackathon`.
   - **Deadline**: two hours from now, with your UTC offset, for example
     `2026-11-05T16:30:00+05:30`.
   - **Public repository** and **Project folder**: the repository you just
     made, and your clone of it.
   - **Mission** and **Judging rubric**: paste the two blocks below.
3. Select **Create all**. Then, in the new channel, try in this order:
   - `@scout what is at risk?`
   - `@builder build the entry described in the mission`
   - approve the push on the builder's card
   - `@judge review`
   - `@herald draft the README section on how Switch is used`

## Mission (paste this)

```text
Mini hackathon. The deadline is the room's Deadline field.
Build a command-line tool, in any language, that prints how long is left until a deadline given as an ISO 8601 time, for example "T-1h12m".
The repository must have:
- a README with a section on how Switch is used and why the work would not have happened the same way without it
- a section with the exact commands to install and run the tool, and an example of its output
- a diagram of how the pit crew and the tool fit together (a mermaid block is fine)
- a link to a demo video (the README may say TODO(video-link) meanwhile; the judge blocks until there is a real link)
- a LICENSE file
- the Switch template that set up the crew, committed as pit-crew.template.yaml
- no secrets, no .env file, no .switch folder
Everything must be pushed to the public repository before the deadline. Work that is not pushed does not count.
```

## Judging rubric (paste this)

```text
Use of Switch (30%): did the crew in the room do real work: a checklist, a reviewed push, a clean-room verdict?
Works (30%): does the tool run from a fresh clone by following the README exactly?
Clarity (20%): could a stranger understand the README in two minutes?
Hygiene (20%): small commits, no secrets, no stray files.
```

The demo-video item is there on purpose: with the marker in the README the
judge's kit reports it as missing, so you see a BLOCKED verdict and then a
SHIP-READY one once you link any video and commit the template.
