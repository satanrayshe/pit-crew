#!/usr/bin/env bash
# Post a message into the pit room through the channel's incoming webhook:
# Discord, Slack or Mattermost.
#
#   scripts/pit-post.sh "@pit-scout pit check"
#   echo "@pit-herald commit abc1234 docs: fix typo" | scripts/pit-post.sh
#
# The webhook URL comes from PIT_WEBHOOK_URL, or else DISCORD_WEBHOOK_URL (its
# old name): from the environment, or else from that line of the .env file at
# the top of this repository.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
url=""
for name in PIT_WEBHOOK_URL DISCORD_WEBHOOK_URL; do
  url="${!name:-}"
  if [ -z "$url" ] && [ -f "$root/.env" ]; then
    url="$(sed -n "s/^$name=//p" "$root/.env" | tail -n 1 | tr -d "\r\"'")"
  fi
  [ -z "$url" ] || break
done
if [ -z "$url" ]; then
  echo "pit-post: PIT_WEBHOOK_URL is not set, in the environment or in $root/.env" >&2
  exit 1
fi
case "$url" in
  https://discord.com/api/webhooks/* | https://discordapp.com/api/webhooks/*) app=discord ;;
  https://hooks.slack.com/*) app=slack ;;
  https://*/hooks/* | http://*/hooks/*) app=mattermost ;;
  *)
    echo "pit-post: PIT_WEBHOOK_URL is not a Discord, Slack or Mattermost incoming webhook URL" >&2
    exit 1
    ;;
esac

if [ "$#" -gt 0 ]; then
  message="$*"
else
  message="$(cat)"
fi
if [ -z "$message" ]; then
  echo "pit-post: nothing to post" >&2
  exit 1
fi

# {"text": "<message>"} for Slack and Mattermost, with the message escaped for
# JSON. Other control characters are dropped.
json_text() {
  printf '%s\n' "$1" | tr -d '\000-\010\013\014\016-\037' | awk '
    {
      if (NR > 1) out = out "\\n"
      n = length($0)
      for (i = 1; i <= n; i++) {
        c = substr($0, i, 1)
        if (c == "\\") c = "\\\\"
        else if (c == "\"") c = "\\\""
        else if (c == "\t") c = "\\t"
        else if (c == "\r") c = "\\r"
        out = out c
      }
    }
    END { printf "{\"text\": \"%s\"}", out }'
}

if [ "$app" = discord ]; then
  reply="$(printf '%s' "$message" |
    curl --silent --show-error --fail-with-body --max-time 15 --form "content=<-" "$url")" || status=$?
else
  reply="$(json_text "$message" |
    curl --silent --show-error --fail-with-body --max-time 15 \
      --header 'Content-Type: application/json' --data-binary @- "$url")" || status=$?
fi
if [ "${status:-0}" -ne 0 ]; then
  echo "pit-post: the $app webhook refused the post: ${reply:-no answer}" >&2
  exit 1
fi
