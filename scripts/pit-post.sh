#!/usr/bin/env bash
# Post a message into the pit room through a Discord webhook.
#
#   scripts/pit-post.sh "@pit-scout pit check"
#   echo "@pit-herald commit abc1234 docs: fix typo" | scripts/pit-post.sh
#
# The webhook URL comes from DISCORD_WEBHOOK_URL, or else from the
# DISCORD_WEBHOOK_URL line of the .env file at the top of this repository.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
url="${DISCORD_WEBHOOK_URL:-}"
if [ -z "$url" ] && [ -f "$root/.env" ]; then
  url="$(sed -n 's/^DISCORD_WEBHOOK_URL=//p' "$root/.env" | tail -n 1 | tr -d "\r\"'")"
fi
if [ -z "$url" ]; then
  echo "pit-post: DISCORD_WEBHOOK_URL is not set, in the environment or in $root/.env" >&2
  exit 1
fi
case "$url" in
  https://discord.com/api/webhooks/* | https://discordapp.com/api/webhooks/*) ;;
  *)
    echo "pit-post: DISCORD_WEBHOOK_URL is not a Discord webhook URL" >&2
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

printf '%s' "$message" |
  curl --silent --show-error --fail-with-body --max-time 15 --form "content=<-" "$url"
