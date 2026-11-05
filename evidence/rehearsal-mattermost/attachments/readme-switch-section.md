## How Switch is used (and why it breaks without it)

Pit Crew has no server or bot of its own. Everything it does is a Switch
feature, set up by [`pit-crew.template.yaml`](pit-crew.template.yaml):

| Pit Crew feature | Switch primitive | Without Switch |
|---|---|---|
| Four agents and a channel from one file | Version 2 template: four `type: agent` resources, one `type: room`, a kickoff | Four terminals set up by hand |
| Each agent on the coding agent you pick | `type: provider` params, each a fallback chain such as `[claude, codex, opencode]` | One vendor, or glue code per vendor |
| Only you direct the builder; friends can talk to the rest | `addressing: owner-agents` on the builder, `{anyone_in: [pit]}` on the others | Anyone in the chat could set the agent in your project to work, or nobody else could join |
| Approve a push from your phone | The builder's question tool becomes a card with buttons in Discord; who may press it follows the agent's addressing | Sit at the terminal, or let the agent push unchecked |
| Agents hand work to each other | `send_targeted_message` inside the room | Copy and paste between terminals |
| Shared checklist, scorecard and build log | Room documents (`create_room_document`, `update_room_document`, `load_internal_documents`), plus the template's `docs:` | Four contexts that drift apart |
| Reports and drafts land in the chat | `send_attachment` | Files nobody else sees |
| Git hooks and a scheduler can nudge agents | The Discord bridge relays third-party webhook posts into the room | No way in from outside |

The countdown itself is plain Python 3 with no Switch import (`pit_clock.py`,
42981e9; the `--version` flag came in e8d5f9f). Switch did not write it. Switch
supplied the run around it: the scout turned the mission into a countdown on
the `pit-board` room document, the builder made and verified the commits, the
judge clean-room cloned `origin/main` and filled in `judge-scorecard`, and the
herald recorded those same commits in `build-log`. The README's reproduce step
now clones `https://git.pit.local/pit-crew.git` (f11fa02), so a reader repeats
the judge's steps rather than trusting a working tree.

**Why it stops working without Switch.** Delete the room and the template and
there is no crew left: no agents to address, no owner-only gate before the
builder pushes, no place for the judge to post a verdict or the herald a
draft, and no shared `build-log`, `pit-board` or `judge-scorecard`. What
remains is a countdown script and a README. The thing being judged — four
agents racing one deadline, with the person only in the loop where it
matters — is the Switch part.
