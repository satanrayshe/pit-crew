# A pit crew of AI agents in one chat channel: setting up Switch from zero

*Shrey ([satanrayshe](https://github.com/satanrayshe)), for the Flip the
Switch hackathon, November 2026*

I entered Flip the Switch alone. On a solo entry the code is rarely what
goes wrong. What goes wrong is the work around it: I lose track of the
clock, miss a submission rule, never look at my own repository the way a
stranger would, and write the README at 2 a.m. A racing driver has a pit
crew for that, so I built one out of AI agents with
[Switch](https://github.com/sandbox-quantum/switch).

Pit Crew is one Switch template. It creates a chat channel and four agents
in it. The scout turns the event's rules into a checklist with a countdown
and flags rule risks. The builder works in your project and asks you on a
card before it pushes. The judge clones only what you pushed into an empty
folder and scores it against the rubric. The herald turns your commits into
a build log and drafts the README and posts. Friends can join the channel
and talk to the crew; only you can direct the builder.

This post is a tutorial you can follow without having used Switch before.
You will install Switch Console, run a Switch server on your own computer,
connect a chat app, import the template, give the crew a task, approve a
push from the chat and read the judge's verdict. After that I go through
what broke in my rehearsal and what I changed because of it.

## What I ran, and where

So far I have run Pit Crew end to end on a local setup, twice, on 4 and 5
November: once to find problems and once after fixing them.

- A Windows 11 computer with Ubuntu 24.04 in WSL and 7.4 GiB of RAM.
- A Switch server built from Switch's main branch as of 4 November, and
  Mattermost from Switch's own Docker Compose file, both inside WSL.
- Two Mattermost accounts: `user`, me as the owner, and `friend`, a
  second person who joins the channel and is not linked to Switch.
- Switch's headless agent controller instead of the Console app. It is the
  same session host Console runs for you when your agents run on your
  computer.
- Every agent on OpenCode 1.19.5 with its free model, big-pickle, which
  needs no account.
- The template run through the same two server calls Console makes when you
  select Import and Create all.

The first run covered 23 scenarios. The transcript, the room documents, the
judge's reports and the server logs are in
[evidence/rehearsal-mattermost](https://github.com/satanrayshe/pit-crew/tree/main/evidence/rehearsal-mattermost).
I have not yet run the crew on Discord or through the Console app. The
Console and Discord steps below follow Switch's documentation and Console's
source code. Where output and screenshots from my Discord run will go, the
post says TODO(discord-run) or TODO(screenshot).

Most of the code in the Pit Crew repository and in my pull requests to
Switch was written outside the crew. The crew does the work around the
code.

## A few words first

Switch puts AI agents into team chat. A *room* is a chat channel that Switch
manages: every person and agent in it reads the same messages, and the room
can hold *room documents*, shared markdown files that agents read and write
with tools. An *agent* is a coding agent you already use, such as Claude
Code, Codex or OpenCode, running on your computer under its own name, with
its own instructions and working folder. Switch doesn't ship models; you
bring the agent and whatever subscription it needs.

The *server* keeps the rooms, agents and rules, and a *bridge* connects it
to a chat app: Discord, Slack, Mattermost, Microsoft Teams or Telegram.
*Switch Console* is the desktop app that runs a server and your agents for
you. A *template* is a YAML file that describes agents and rooms to create;
Console turns its parameters into a form.

## What you need

- A computer running macOS, Windows or Linux. Console's Windows and Linux
  builds are in early access.
- Node.js 20 or later. Switch uses it to start your agents, and Console
  does not install it on your own computer.
- A coding agent you are signed in to: Claude Code, Codex or OpenCode.
  OpenCode's free models need no account, but they stop at a usage limit
  (more on that below).
- A chat app. I use Discord: it is free, each agent posts under its own
  name and picture, and approval cards get buttons. Slack and Mattermost
  work too. Telegram does not, because the template creates a channel and
  Switch cannot create chats on Telegram.
- A GitHub account for a small practice repository.

Plan on about half an hour of setup, ten minutes of it for the Discord bot.

## Step 1: install Switch Console

Download Console from the
[Switch releases page](https://github.com/sandbox-quantum/switch/releases).
You need 0.40 or later; the current stable release is 0.40.1, from 21
October. On Windows that is `switch-console-x64.exe` (or the `.msi`). On a
Mac, take the `arm64` `.dmg` for Apple silicon or the `x64` one for Intel.
On Linux there are `.deb`, `.rpm` and `.AppImage` builds.

When Console opens, a checklist called **Setting up Switch** appears in the
sidebar. Its steps can finish in any order, and some may already be ticked,
for example if a coding agent is already installed.

## Step 2: run a server on your computer

Select **Add a server**, then **Run a server on this computer**. Console
uses the PostgreSQL already on your computer if it is version 16 to 18, or
the copy it ships with otherwise. It starts the Switch server on free ports
that only your computer can reach, creates an admin account and signs you
in. Switch's docs say a first setup takes about a minute. The server it
starts has agent management turned on, which the template needs because it
creates agents.

You do not need Docker. Some pages on docs.switchagents.ai still say you
do, but the Add a server page in the Switch repository and the Console
0.40.0 changelog say the local server runs without it. If Docker happens to
be running, Console offers **Also run Mattermost**, a chat app you can use
without signing up anywhere.

A local server belongs to your computer: colleagues cannot connect to it,
and it does not come back by itself after you restart the computer.

TODO(screenshot): Console's server page once the local server is running.

## Step 3: check your coding agent

Open **Settings** at the bottom of the sidebar, then **Agent providers**.
Each provider's row says **Installed** or **Not installed**. Make sure your
coding agent is installed and that you have signed in to it with its own
command-line tool (for Claude Code, `claude auth login`).

The template picks a coding agent for each crew member from a list, taking
the first one that is ready on your computer: Claude Code, then Codex, then
OpenCode. The judge's list starts with Codex instead, so with both Claude
Code and Codex signed in, the judge runs on a different model family from
the builder and gives a second opinion.

## Step 4: connect Discord

Discord has no app manifest, so this part is done by hand. My notes, with
the reason for every permission, are in
[docs/discord-setup.md](https://github.com/satanrayshe/pit-crew/blob/main/docs/discord-setup.md).

1. Create a Discord server for your crew, for example "Pit Crew HQ".
2. In the [Discord Developer Portal](https://discord.com/developers/applications),
   select **New Application** and name it. Open **Bot**, reset the token
   and copy it into your password manager. It goes into Console and
   nowhere else.
3. Still under **Bot**, turn on **Server Members Intent** and **Message
   Content Intent**, then **Save Changes**. Without Message Content your
   agents receive messages with no text in them.
4. Open **OAuth2**, then **URL Generator**. Select the scopes `bot` and
   `applications.commands`, and the permissions View Channels, Send
   Messages, Send Messages in Threads, Manage Webhooks, Manage Channels,
   Manage Roles, Read Message History and Attach Files. Open the generated
   URL and add the bot to your server. Switch needs Manage Channels to
   create the crew's channel, Manage Webhooks to post as each agent, and
   Attach Files for the judge's reports.
5. In Discord's settings, turn on **Developer Mode**. Right-click your
   server's icon and select **Copy Server ID**. Switch calls this the
   Guild Id.
6. In Console, open your server's **Home** page. Under **Messaging apps**,
   select **Connect**, then **Discord**. Name the connection and paste the
   token and the guild id. Open **Advanced configuration**, leave **Allow
   creating channels from Switch** on and tick **Use for new rooms by
   default**. Then select **Connect**.
7. Console asks which Discord account is yours. Find yourself and select
   **This is me**.

Don't skip step 7. The builder answers only its owner, and until your
Discord account is linked to your Switch user, your messages look like a
stranger's. In my rehearsal the unlinked `friend` account got this reply
from the builder: "I only take instructions from my owner, and this chat
account isn't linked to a Switch user yet".

To check the connection, post an ordinary message in any channel of your
Discord server. The channel should show up under **Your Rooms** in Console,
and typing `/` in it should offer Switch's commands. A command cannot be
the first message in a channel, because posting is what makes a channel a
room.

TODO(discord-run): check every label above against Console 0.40.1 on
Windows.

TODO(screenshot): the Messaging apps page with the Discord connection.

On Slack or Mattermost the rest of this post is the same. The only
difference I know of is in webhooks, which come up near the end.

## Step 5: make a practice repository

For a first run, use a two-hour pretend event instead of your real
project. [rules/mini-hackathon.md](https://github.com/satanrayshe/pit-crew/blob/main/rules/mini-hackathon.md)
describes one: build a small command-line tool that prints the time left
until a deadline, with a README, a license and a diagram. In one sitting
you see the scout change pace and the judge block the entry, then pass it.

Create a public repository on GitHub, for example `pit-crew-mini`, with a
README and a `.gitignore` that has these two lines:

```gitignore
.switch/
.claude/settings.local.json
```

Some coding agents keep session files under `.switch/`, and Console can
write an agent id into `.claude/settings.local.json`. Neither belongs in a
public repository. Push both files and clone the repository to your
computer. The builder will work in that clone.

## Step 6: import the template

Get the template with
`git clone https://github.com/satanrayshe/pit-crew`, or download
[pit-crew.template.yaml](https://github.com/satanrayshe/pit-crew/blob/main/pit-crew.template.yaml)
on its own.

In Console, open **Templates** and select **Import template**. Drop the
file in, or paste its text, select **Import** and save it. Then, on the
template's page, select **Use template** and fill in the form:

| Field | For the practice run |
|---|---|
| Crew name | `mini1`. Agent names are unique on a server, so use a new crew name every run |
| What you are racing for | `Mini hackathon` |
| Deadline | Two hours from now with your UTC offset, like `2026-11-05T16:30:00+05:30` |
| Public repository | Your practice repository's `https://` URL |
| Project folder | Your clone of it |
| Mission and Judging rubric | The two blocks from rules/mini-hackathon.md |
| Messaging app | Should already show your Discord connection |

The **Advanced** fold sets which coding agent each crew member runs on and
where the judge gets its checking script. Select **Create all**.

TODO(screenshot): the filled-in form.

### What the template says

You don't have to edit the template to use it, but reading it is a quick
way to learn what Switch can do. Version 2 of the template format lists
*resources*, each with a key and a type. Pit Crew has four `agent`
resources and one `room`.

Parameters become the form. A `provider` parameter with a list as its
default is the fallback chain from step 3:

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

Each agent names its coding agent, its machine and its working folder. The
builder works in your project folder. The other three get folders of their
own under Console's agents directory, so they never write to your project:

```yaml
  builder:
    type: agent
    name: "{crew}-builder"
    provider: "{builder_provider}"
    machine: "{machine}"
    directory: "{project_dir}"
    addressing: owner-agents
  judge:
    type: agent
    name: "{crew}-judge"
    provider: "{judge_provider}"
    machine: "{machine}"
    directory: "{$agents_dir}/{judge.name}"
    addressing: { anyone_in: [pit] }
```

`addressing` decides who may talk to an agent. `owner-agents` means you and
the agents you own; `{anyone_in: [pit]}` means anyone in the pit room.
Switch's skill file, which every agent reads, adds a rule I had not
expected: the same policy decides who may answer the agent's approval
cards. A friend in the channel can ask the scout something, and even answer
the scout's cards, but can neither give the builder a task nor approve its
push.

The room lists its agents, two room documents filled from the form, and a
kickoff message:

```yaml
  pit:
    type: room
    name: "{crew}-pit"
    bridge: "{bridge}"
    agents: [scout, builder, judge, herald]
    docs:
      - name: mission
        content: "{mission}"
      - name: judging-rubric
        content: "{rubric}"
    kickoff: |
      @{scout.name} lights out. Load the mission and the rubric, create the pit board, and post the countdown with the first five checklist items.
      @{builder.name} @{judge.name} @{herald.name} one line each: what you do, and the one thing you need from me. Do not start any work yet.
```

`{scout.name}` refers to another resource by its key. An agent wakes only
when a message addresses it, so the kickoff mentions all four.

The rest of the file is the agents' instructions in plain English, plus the
room's rules. The one I spent longest on is the handoff map, because four
agents in one room could keep waking each other. Agents pass work with
Switch's `send_targeted_message` tool, and the map allows only these
handoffs: the scout may pass a person's request to any crewmate, the
builder sends commit notices to the herald and verify requests to the
judge, the herald may pass a README change to the builder, and the judge
hands off to nobody. A notice is never answered with another handoff. No
loop started in either rehearsal run. If one ever does,
`!interrupt-all-agents` stops everyone.

## Step 7: the kickoff

A channel named `mini1-pit` appears with the four agents in it. Switch
posts "Template kickoff on behalf of" you, with the kickoff text in that
post's thread, and each agent says "Starting a session to handle this"
while its coding agent starts.

The scout loads the mission and the rubric, creates a room document called
`pit-board` and posts the countdown with the first five checklist items,
each with an owner. In my second run it began:

> T-1h57m, 0/9 done. Pit board is up; mission and rubric loaded.

The builder, judge and herald answer in one line each. In that run the
builder said it needed "your actual task for the project (the kickoff isn't
one)" and finished with "Not starting anything yet." That sentence is there
because of the first thing that went wrong in my rehearsal, which I come
back to below.

If an agent says it could not start a session, address it again. On
OpenCode, when four sessions start at the same moment, one sometimes fails
with "database is locked".

Switch has no scheduler: an agent does nothing until a message addresses
it. So the scout works out the countdown from the computer's clock every
time it wakes, and the board is right whenever anyone asks.

TODO(discord-run): the kickoff as it appears in Discord.

## Step 8: give the crew a task

Start with the scout, which anyone in the room may address. The template
gives each agent a short alias, so `@scout` works as well as
`@mini1-scout`:

```text
@scout what is at risk?
```

In my rehearsal the friend's account asked this. The scout answered in 33
seconds, countdown first, and quoted the mission's rule that the repository
needs a LICENSE file, because the friend had just asked the builder to
delete it.

Then give the builder the job:

```text
@builder build the entry described in the mission, commit it, and push.
```

The builder says it has the task, posts a plan of at most five bullets and
works in your project folder. Before it says something works, it runs it
and reports the command and the last lines of the output. After each commit
it sends the herald a notice, and the herald adds one line to a room
document called `build-log`.

Each time an agent creates or updates a room document, Switch posts a
one-line notice in the channel, such as "created room document pit-board",
so you can follow the crew's bookkeeping from the chat.

## Step 9: approve the push from the chat

Before any push, the builder asks you with its question tool, and Switch
turns the question into a card in the chat. In my second run the card read:

> Push approval: Ready to push commit 29b47c5 (docs: add changelog entry) on
> main to file:///.../pit-crew-r2.git. This sends exactly that one commit.
> Approve?

with **Approve**, **Change plan** and **Cancel** buttons under it. I had the
second account, `friend`, press Approve first. Switch refused the press
with `NOT_AUTHORIZED: You may not address this agent` and the card stayed
open. Then I pressed Approve as the owner. The card changed to "Approve,
answered by @user from Mattermost" (my owner account was called `user`),
and the push went through four seconds later.

The builder asks the same way before it deletes files it did not create,
adds a dependency, touches `.env` files or keys, or spends money. In the
first run I cancelled a new dependency from a card and approved deleting a
stale file from another.

On Discord the card is a message with buttons, so answering it from the
phone app should work too. I have not tried that yet.

TODO(discord-run): approve a push from my phone.

TODO(screenshot): the card, and the friend's refused press.

## Step 10: read the judge's verdict

```text
@judge review
```

The judge says "On it, clean-room clone" and clones your public repository
into a new folder in its own directory. It runs
[judge-kit/check.py](https://github.com/satanrayshe/pit-crew/blob/main/judge-kit/README.md),
a script that needs only Python and git. It checks the README for a
section on how Switch is used, reproduce steps, a diagram and a video link,
and looks for a license, secrets and files that should never be committed.
Then
it reads the README as a stranger would, follows the setup steps that are
quick and safe, and scores each rubric line from 1 to 10 with one line of
evidence. The verdict comes first:

> BLOCKED at 29b47c5. check.py passes 8/9; the only failure is
> `readme_demo_video` [...] Scores: Switch 7, Works 10, Clarity 8,
> Hygiene 8.

The full report arrives as a markdown attachment, and the judge keeps a
`judge-scorecard` room document with a mission table, one row per item on
the scout's pit board. The scout counts an item as done only when that
table says so.

Because the judge clones from the public URL, work you have not pushed does
not exist for it. The real judges will see the same thing.

The mini hackathon blocks on purpose. Its mission asks for a demo video
link, and the `TODO(video-link)` marker fails that check. Link any video,
let the builder push it (another card) and ask `@judge review` again. In my
rehearsal I never linked a video, so the verdict on the main branch stayed
BLOCKED. The judge did say SHIP-READY when I asked it to judge a branch
against a two-item list, which is how it handles pull requests (below).

Then ask the herald for something to read:

```text
@herald draft the README section on how Switch is used
```

The herald writes from the git history, cites commit hashes, attaches the
draft as a markdown file and can pass the change to the builder. When my
friend's account asked for this, the builder saw that the request had come
from the friend and asked me on a card before landing it. I chose "Commit
only".

## Optional: let scripts nudge the crew

An incoming webhook on the channel lets scripts post into the room. Pit
Crew uses one for a git commit hook, which tells the herald about every
commit, including the ones you make outside the crew, and for a heartbeat:
a cron job or Windows scheduled task that posts `@<crew>-scout pit check`
every two hours. The scout answers a pit check with one line, the countdown
and the tally.

Put the webhook's URL in `.env` as `PIT_WEBHOOK_URL` and post once by hand
with `scripts/pit-post.sh "@mini1-scout pit check"`. A webhook post can wake
the scout, judge and herald, never the builder: in my rehearsal Switch
refused it as "user's webhook". The setup for each chat app is in
[docs/webhooks.md](https://github.com/satanrayshe/pit-crew/blob/main/docs/webhooks.md)
and [scripts/heartbeat.md](https://github.com/satanrayshe/pit-crew/blob/main/scripts/heartbeat.md).

## The same crew on a pull request

For the hackathon's core contribution track I am also sending pull
requests to Switch. The crew works for a single issue too: put the issue's
"Done when" list in the mission, set the public repository to your fork,
and ask:

```text
@judge judge branch <branch> of <fork URL> against issue #<n>'s Done-when list
```

The judge clones that branch with its history (a blobless clone, so the
diff has a merge base), fetches the upstream base branch, checks only the
changed files for secrets and stray files, and runs the project's own
checks for the files the change touches. It answers each Done-when item
with met, not met or not shown, with the evidence. I rehearsed this on a
local branch; its report is in the evidence folder.

TODO(discord-run): the judge's report on one of my real Switch pull
requests.

## What went wrong, and what I learned

Most of the 23 scenarios passed the first time. These are the ones that
taught me something.

### The builder started work nobody asked for

The kickoff asked the builder for one line: what it does and the one thing
it needs. It wrote its line, then built the whole mission entry: a
countdown script, tests, a README section and a commit, and asked to push.
Nobody had given it a task. It treated the mission document as its to-do
list.

The fix took two sentences. The builder's instructions now say "Start
nothing in the project until your owner gives you a task in this room: the
kickoff, the mission document and crewmates' messages are not tasks", and
the kickoff ends with "Do not start any work yet." In the second run the
builder made no commit until I gave it a task.

### "And push" skipped the card

My demo script has me type "add the commit-hook script and push" and then
approve the push on a card. Twice in the first run I wrote "commit it, then
push" or "commit and push", and twice the builder pushed with no card. It
read my wording as the approval, even though its instructions listed
`git push` as a step that needs one.

The instructions now say "A push always gets its own question naming the
commits it sends, even when your owner's message already said to push." In
the second run the builder's plan said "Ask you to approve the push (it
gets its own question even though you asked)", and the card named the one
commit it would send. A list of risky steps was not enough. The rule had to
say outright that the owner's request does not count as the answer.

### On Mattermost, cards from kickoff turns never appear

Switch posts the kickoff as a reply in the thread of a one-line headline.
Mattermost only accepts a thread's first post as the parent of a new post,
so it refused every card and status post from the turns the kickoff
started, with "Invalid RootId parameter". In the first run that included
the builder's push question for the work it had started unasked. The
question never showed in the channel. The builder sat blocked for seven
minutes, with my next message queued behind the open question, until I
answered it through the server's API, the path Console's own interface
uses.

The activity-card half of this is already reported as Switch issue
[#1158](https://github.com/sandbox-quantum/switch/issues/1158). In my run
it also swallowed an approval card, which is worse: the agent waits for the
answer to a question nobody can see. The template now asks for no
work in the kickoff turn, so no kickoff turn raises a card. If an agent
still seems stuck after the kickoff, look for an open question in Console.

TODO(discord-run): whether Discord shows cards from kickoff turns.

### Free models run out, and the room does not say so

Every agent in my rehearsal ran on OpenCode's free model, which needs no
sign-in. It followed the instructions more closely than I expected: the
tool names, the clean-room steps, the handoff map and the rules about the
owner and the friend. Most turns took between 12 seconds and 1 minute 41
seconds.

By a third run, after the two above, the free usage had run out. No agent
answered, and nothing in the room said why; OpenCode's own log said "Free
usage limit reached". Four agents share one account's limits, so plan for
that: `!follow-ups off` stops messages that do not mention an agent from
waking it, and `!interrupt-all-agents` stops everyone.

### Webhooks differ per chat app

The heartbeat and the commit hook post through an incoming webhook, and
each bridge filters posts in its own way:

- Discord drops posts from Switch's own webhooks and posts whose sender
  has an agent's name. Create a new webhook of your own on the channel and
  give it a name that is not an agent's.
- Mattermost ignores every post from the account Switch's bridge signs in
  as, and a webhook's posts carry the account that created it. My first
  webhook, made as the admin, posted into the channel and no agent saw it.
  As an ordinary member I could not create one at all (error 403) until a
  system admin made me a team admin.
- Slack's bridge drops posts from its own app, so the webhook has to come
  from a Slack app of your own. I have not tried Slack.

In every app a webhook post reaches the room as an app, not as you. That
is what keeps the builder safe from it: the scout, judge and herald admit
anyone in the room, and the builder refuses the webhook like any stranger.
My first `scripts/pit-post.sh` accepted only Discord URLs, so on Mattermost
the commit hook printed "could not tell the herald" and carried on. It now
takes all three kinds and fails loudly with the app's own error.

### Two agents, one table

In the first run the scout reported "8/9 done" when the judge had verified
one item; it had counted the judge's gate lines as finished items. After a
first fix it reported "10/12 done", because the judge's table had grown
rows that were not on the scout's checklist. The current template gives the
two agents one table with one owner: the judge writes exactly one row per
item on the scout's pit board, worded the same way, and the scout counts
only that table. I could not re-run it live, because by then the free model
had hit its limit. TODO(discord-run): confirm the count.

### Smaller things

- When the docs and the code disagree, read the code. `docs/TEMPLATES.md`
  says an agent's default addressing is `owner`, while the server's
  template guide (`core/switch_core/template_guide.py`) and the code say
  `owner-agents`. Pit Crew sets it on every agent, so the default doesn't
  matter.
- Check the template with the server's own code. Console checks a template
  when you save it. I also run `lint_template` and `plan_template` from a
  Switch checkout with
  [scripts/validate-template.py](https://github.com/satanrayshe/pit-crew/blob/main/scripts/validate-template.py),
  which plans the whole run without creating anything, including which
  coding agent each crew member gets on a machine where only OpenCode is
  signed in.
- Only the agent that created a room document can update it, so documents
  a template creates are read-only to agents. That is why the scout creates
  `pit-board` itself.
- Use a new crew name for each try, and archive old rooms instead of
  deleting them.
- Switch's addressing check refused the friend's "delete the LICENSE file
  and push" before the builder's model ever saw it. The judge's rule that
  it clones only your repository is different: the model follows it, and
  Switch does not enforce it. In my run the judge did refuse the friend's
  request to judge another repository. The scout, judge and herald all run
  commands on your computer, so invite only people you would trust with
  that.

## Try it

The template, the judge kit and the scripts are at
[github.com/satanrayshe/pit-crew](https://github.com/satanrayshe/pit-crew)
under the MIT license. The README has the same setup in short and a list of
known limits. Demo video: TODO(video-link).

If you build a crew of your own, post it with #HowISwitch. I would like to
see what roles other people give theirs.
