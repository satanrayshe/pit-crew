# A pit crew of AI agents in one Discord channel, built with Switch

*Draft for the Flip the Switch Best Blog entry. Screenshots are marked
TODO(screenshot).*

I entered the Flip the Switch hackathon alone. Working solo, the code is
rarely what hurts. The rest is: keeping an eye on the clock, rereading the
rules to check you have not missed a requirement, reviewing your own work as
a stranger would, and writing the README and the video script at 2 a.m. In
racing, a driver has a pit crew for that. I built one out of AI agents, in a
single Discord channel, with Switch.

This post walks through what Switch is, how to set it up on your own laptop,
how the Pit Crew template works line by line, and what I learned along the
way. You can follow it without having used Switch before.

## What Switch is

[Switch](https://github.com/sandbox-quantum/switch) is open source
infrastructure for putting AI agents into team chat. Every channel becomes a
*room*: a shared log of messages, documents and roles that every person and
agent in it reads. Agents join a room like any other member, under their own
name and avatar.

Switch does not ship agents or models. You bring your own coding agent
(Claude Code, Codex, OpenCode, Cursor or Antigravity) and your own chat app
(Slack, Discord, Teams, Telegram or Mattermost). **Switch Console** is the
desktop app that runs your agents on your machine and connects them to a
Switch server.

## Setting it up

Plan on half an hour the first time. You need Node.js 20 or later on your
computer: Switch starts your agents with it, and Console does not install it
for you.

1. **Install Switch Console 0.40 or later** from the
   [releases page](https://github.com/sandbox-quantum/switch/releases). The
   macOS build is stable; Windows and Linux are in early access.
2. **Add a server, then Run a server on this computer.** Console downloads
   what it needs, starts a local Switch server and signs you in. No Docker
   is needed.
3. **Check your coding agent.** In Settings, Agent providers, your agent
   should show as installed and signed in. If not, sign in with the agent's
   own CLI and press Recheck.
4. **Connect a chat app.** I used Discord, because each agent gets its own
   name and avatar there and approval cards get real buttons. It takes about
   ten minutes: create a bot in the Discord developer portal, turn on two
   intents, invite it with a handful of permissions, and paste its token and
   your server's id into Console. The step people skip is the last one:
   **link your Discord account** ("This is me"). Until you do, an agent that
   answers only its owner treats you as a stranger. My step-by-step notes are
   in [docs/discord-setup.md](discord-setup.md).

TODO(screenshot): Console's server home with the Discord connection listed.

## The template

Everything Pit Crew does is in one file,
[`pit-crew.template.yaml`](../pit-crew.template.yaml). A Switch template is
YAML that says what to create. Version 2 of the format lists *resources*,
each with a key and a type: here four agents and one room.

### Params become a form

```yaml
params:
  crew:
    type: string
    label: Crew name
    default: pit
    pattern: "[a-z][a-z0-9-]{1,20}"
  judge_provider:
    type: provider
    label: Judge runs on
    default: [codex, claude, opencode]
    input: advanced
```

When you import the template, Console turns `params` into a form. A
`provider` param with a list default is a fallback chain: the first coding
agent in the list that is ready on your machine is used. Each Pit Crew agent
has its own. The judge's starts with Codex and the builder's with Claude, so
with both signed in the judge gives a second opinion from a different model
family. `input: advanced` folds a field away.

### An agent

```yaml
  builder:
    type: agent
    name: "{crew}-builder"
    display_name: Builder
    provider: "{builder_provider}"
    machine: "{machine}"
    directory: "{project_dir}"
    addressing: owner-agents
    instructions: |
      You are Builder, the only member of this pit crew who changes the
      project. ...
```

`provider`, `machine` and `directory` are required, and Switch never guesses
them. The builder works in your project folder; the other three get their own
folders (`"{$agents_dir}/{scout.name}"`).

`addressing` decides who may talk to an agent, and, as I learned from the
skill file every agent gets, **who may answer its approval cards**:

- The builder is `owner-agents`: you, and agents you own. A friend in the
  channel can watch it work but cannot give it a task or approve its push.
- The scout, judge and herald are `{anyone_in: [pit]}`: anyone in the pit
  room may address them. That is what makes the channel friendly to visitors.

### The room

```yaml
  pit:
    type: room
    name: "{crew}-pit"
    agents: [scout, builder, judge, herald]
    docs:
      - name: mission
        content: "{mission}"
      - name: judging-rubric
        content: "{rubric}"
    kickoff: |
      @{scout.name} lights out. Load the mission and the rubric, create
      the pit board, and post the countdown ...
```

`{scout.name}` refers to another resource by its key. `docs` become room
documents that every agent can load. The `kickoff` is posted for you once the
room exists. Agents only start working when a message addresses them, so the
kickoff has to mention each one.

## How the crew works together

- **The scout** turns the mission (the hackathon's rules, or an issue's "Done
  when" list) into a checklist on a room document called `pit-board`, with a
  countdown it works out from the shell clock every time it wakes.
- **The builder** codes in your project folder. Before a push, a new
  dependency or anything that touches secrets, it asks you with its question
  tool, which shows up in Discord as a card with Approve, Change plan and
  Cancel. Discord works on a phone, so you can approve from anywhere.
- **The judge** never edits anything. For every review it clones the public
  repository into a new, empty folder, runs a small script of mechanical
  checks (README sections, license, secrets, stray files), follows the README
  like a stranger would, and scores the work against the rubric. It is the
  only one allowed to say SHIP-READY.
- **The herald** writes from the git history: a build log, README sections, a
  blog draft, social posts. It never publishes.

Agents hand work to each other with the `send_targeted_message` tool. Loops
were my main worry with four agents in one room, so the room's instructions
fix a one-way map: the builder notifies the herald and asks the judge; the
herald may pass a README change to the builder; the judge hands off to
nobody; and a notice is never answered with another handoff. If something
still runs away, `!interrupt-all-agents` stops everyone.

TODO(screenshot): an approval card in Discord, and the judge's verdict with
its report attached.

## Running it

In Console, open Templates, select Import template, choose or drop in the
file, select Import and save it. On the template's page, select Use
template, fill in a crew name, your public repository, your local clone of
it, the deadline and the mission, then select Create all. Console creates
four agents and a channel, and the kickoff wakes them. Then try:

- `@scout what is at risk?`
- `@builder <a small task>`, then approve its push on the card
- `@judge review`
- `@herald draft the README section on how Switch is used`

For a first run, [`rules/mini-hackathon.md`](../rules/mini-hackathon.md) is a
two-hour fake event, short enough to see the scout change pace and the judge
go from BLOCKED to SHIP-READY in one sitting.

## Using it on a pull request

The same crew works for one issue. Put the issue's "Done when" list in the
mission, and ask the judge to review a branch: it clones the branch with its
history, fetches the base branch, checks only the files the change touches
for secrets and stray files, runs the project's own checks, and answers each
Done-when item with met, not met or not shown. We are using it this way on
our own pull requests to Switch, and the judge's reports will go in the
repository's `evidence/` folder.

## What I learned

- When the docs and the code disagree, the code wins. For example,
  `docs/TEMPLATES.md` says an agent's default addressing is `owner`, while
  the server's own template guide and code say `owner-agents`. Reading
  `core/switch_core/template_v2.py` and `template_lint.py` answered every
  question the docs left open.
- Lint your template with the server's code. The server runs its checker
  on every template you save and refuses one it could never create. I also
  ran `lint_template` and `plan_template` from a Switch checkout
  ([`scripts/validate-template.py`](../scripts/validate-template.py)),
  which plans the whole run, including which provider each agent gets,
  without creating anything.
- Only the agent that created a room document can update it. Documents a
  template creates are read-only to agents, so the scout creates `pit-board`
  itself.
- There is no scheduler. An agent wakes when a message addresses it,
  nothing else. The countdown is therefore recomputed on every wake, and a
  cron job posting `@pit-scout pit check` through a Discord webhook gives the
  scout a heartbeat.
- Agent names are unique on a server. Use a fresh crew name for each
  rehearsal (`t1`, `t2`), and archive old rooms rather than deleting them.
- Not every chat app can create channels. The template creates its own
  channel, which works on Discord, Slack and Mattermost but not Telegram.
- Four agents share your coding agent's limits. `!follow-ups off` stops
  replies that do not mention an agent from waking it, which saves quota.

## Try it

The template, the judge kit and the scripts are at
https://github.com/satanrayshe/pit-crew under the MIT license. The README has
a reproduction guide that takes about half an hour. If you build your own crew, post it with
#HowISwitch; I would like to see what roles other people give theirs.
