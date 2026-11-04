#!/usr/bin/env bash
# Install a git post-commit hook that tells the herald about each commit, by
# posting "@<crew>-herald commit <short hash> <subject>" into the pit room.
#
#   scripts/install-commit-hook.sh <crew> [repository]
#
# It fires for every commit in that repository, the builder's included; the
# builder sees the hook and leaves the notice to it.
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "usage: $0 <crew> [repository]" >&2
  exit 2
fi
crew="$1"
repo="${2:-.}"
if ! printf '%s' "$crew" | grep -Eq '^[a-z][a-z0-9-]{1,20}$'; then
  echo "install-commit-hook: '$crew' is not a crew name (lowercase letters, digits and -)" >&2
  exit 2
fi

post_script="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/pit-post.sh"
hooks="$(git -C "$repo" rev-parse --path-format=absolute --git-path hooks)"
hook="$hooks/post-commit"
marker="# installed by pit-crew"

if [ -e "$hook" ] && ! grep -qF "$marker" "$hook"; then
  echo "install-commit-hook: $hook exists and was not installed by Pit Crew; leaving it alone" >&2
  exit 1
fi

mkdir -p "$hooks"
cat >"$hook" <<EOF
#!/bin/sh
$marker
sha=\$(git rev-parse --short HEAD)
subject=\$(git log -1 --format=%s)
"$post_script" "@$crew-herald commit \$sha \$subject" ||
  echo "pit-crew: could not tell the herald about \$sha" >&2
EOF
chmod +x "$hook"
echo "Installed $hook: each commit now posts \"@$crew-herald commit <hash> <subject>\" to the room."
