# A webhook for the scripts

The commit hook and the heartbeat post into the pit room through an incoming
webhook on the `<crew>-pit` channel. `scripts/pit-post.sh` (and
`pit-post.ps1`) take a Discord, Slack or Mattermost webhook URL from
`PIT_WEBHOOK_URL`, in the environment or in `.env` at the top of your
pit-crew clone:

```sh
cp .env.example .env
# then edit .env:
PIT_WEBHOOK_URL=https://...
```

`.env` is in `.gitignore`. Treat the URL like a password: anyone who has it
can post into your room. `DISCORD_WEBHOOK_URL`, the old name, still works.

Whichever app you use, a webhook post reaches the room as an app, not as
you. It can address the scout, judge and herald, which admit anyone in the
pit room, and never the builder, which answers only its owner. Check it once
by hand before relying on it:

```sh
scripts/pit-post.sh "@<crew>-scout pit check"
```

If the message appears but the scout stays quiet, Switch did not take the
post into the room; see the notes for your app below.

## Discord

Step 8 of [discord-setup.md](discord-setup.md): a new webhook of your own on
the pit channel, not one of the Switch webhooks already listed there.

## Mattermost

We ran this in our local rehearsal
([evidence/rehearsal-mattermost/](../evidence/rehearsal-mattermost/README.md)).

1. Sign in as yourself, not as the admin account Switch's Mattermost
   connection uses. The bridge ignores every post from that account, and a
   webhook's posts carry the account that created it, so a webhook made
   with it posts into the channel and no agent ever sees it.
2. Open **Integrations**, **Incoming Webhooks**, **Add Incoming Webhook**,
   and pick the `<crew>-pit` channel. Mattermost lets only admins do this
   by default: as an ordinary team member we got an error 403, and it
   worked once a system admin made us a team admin. Incoming webhooks must
   also be turned on in the System Console (they were on our server
   without any setting).
3. Copy its URL, `https://<your server>/hooks/<id>`, into `.env` as
   `PIT_WEBHOOK_URL`. `http://` works for a server on your own machine.

Its posts reach the room as "user's webhook" when your account is `user`.
Switch keeps that apart from you: the builder refuses it like any stranger,
though it carries your Mattermost account.

## Slack

Not tried yet. Switch's Slack bridge relays posts from other Slack apps and
drops its own app's posts, so create the webhook in a Slack app of your own,
not in the one Switch uses: on api.slack.com/apps, **Incoming Webhooks**,
**Add New Webhook to Workspace**, and pick the `<crew>-pit` channel. Its URL
starts with `https://hooks.slack.com/`. Check it by hand as above, and
also check that the builder refuses it
(`scripts/pit-post.sh "@<crew>-builder say hi"`). Switch takes a Slack app's
post as that app only when Slack sends no user with it, and we have not
seen what Slack sends for a webhook.
