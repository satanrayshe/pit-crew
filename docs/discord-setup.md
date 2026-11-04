# Connecting Discord

About ten minutes, by hand: Discord has no app manifest to fill this in for
you. The steps follow Switch's own page,
[Connect Discord](https://docs.switchagents.ai/flintai/switch/deploy/messaging-apps/discord),
plus the webhook Pit Crew's scripts use.

Why Discord for Pit Crew: each agent posts under its own name and avatar,
approval and question cards get real buttons you can press from your phone,
friends join with an invite link, and a channel webhook lets scripts post into
the room (the commit hook and the heartbeat).

You need a Switch server you are an admin of. If Switch Console set it up for
you (**Run a server on this computer**), you are.

## 1. A Discord server

Create one for your crew, for example "Pit Crew HQ". Any server you can add a
bot to and manage channels in will do.

## 2. The application and its bot

In the [Discord Developer Portal](https://discord.com/developers/applications),
select **New Application** and name it. Open the **Bot** tab, reset the token
and copy it into your password manager. Never put it in a repository or a
chat message; it goes into Switch Console only.

## 3. Privileged intents

Still under **Bot**, in **Privileged Gateway Intents**, turn on:

- **Server Members Intent**
- **Message Content Intent** (without it your agents receive messages with no
  text)

Then select **Save Changes**.

## 4. Invite the bot

Open **OAuth2**, then **URL Generator**. Select the scopes `bot` and
`applications.commands`, then these bot permissions:

- View Channels
- Send Messages, Send Messages in Threads
- Manage Webhooks (agents post under their own names through it)
- Manage Channels, Manage Roles (Switch creates the pit channel)
- Read Message History
- Attach Files (the judge's reports and the herald's drafts are attachments)

Open the generated URL and add the bot to your server.

## 5. The server id

In Discord, open **User Settings**, then **Developer**, and turn on
**Developer Mode**. Right-click your server's icon and select
**Copy Server ID**. Switch calls this the **Guild Id**.

## 6. Connect it in Switch Console

Select your Switch server in the sidebar and open its **Home** page. Under
**Messaging apps**, select **Connect**, then **Discord**. Give the connection
a name (for example "Pit Crew Discord") and paste the bot token and the guild
id. Before selecting **Connect**, open **Advanced configuration**, leave
**Allow creating channels from Switch** on (the template creates the pit
channel) and tick **Use for new rooms by default** (the template's
**Messaging app** field starts on the server's default app).

Console then asks which Discord account is yours: find yourself and select
**This is me**. Do not skip this. The builder answers only its owner, and
until your account is linked your messages look like a stranger's.

## 7. Smoke test

Post an ordinary message in any channel of your server. The channel should
appear under **Your Rooms** in Console, and typing `/` in it should offer the
Switch commands. A command cannot be the first message in a channel: posting
is what makes a channel a room.

## 8. The webhook for scripts (after the template has run)

The template creates a channel named `<crew>-pit`. In Discord, open that
channel's settings, then **Integrations**, **Webhooks**, and create a new one
with **New Webhook**. Do not copy the Switch Bridge or Switch Sessions URLs
already listed there: the bridge drops its own webhooks' posts. Do not name
it after an agent either; the bridge also drops posts whose sender has an
agent's name. Copy its URL into `.env` at the top of your pit-crew clone:

```sh
cp .env.example .env
# then edit .env:
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

`.env` is in `.gitignore`. Treat the URL like a password: anyone who has it
can post into your room. `scripts/pit-post.sh` (or `pit-post.ps1`) reads it
from the environment or from that file; see
[scripts/heartbeat.md](../scripts/heartbeat.md) for the heartbeat and the
README for the commit hook.

Messages the webhook posts reach the room as an app, not as you. The scout,
judge and herald admit anyone in the pit room, so a webhook post can address
them (check it once by hand, as heartbeat.md shows). The builder answers only
its owner, so a webhook can never give it work.

TODO(screenshot): the Messaging apps page with the Discord connection, and the
webhook settings in Discord.
