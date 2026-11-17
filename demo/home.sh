#!/bin/sh
# Builds a throwaway herdr home for the demo and prints its path: your config
# (via demo/config.sh), this plugin linked, and nothing else, so the recording
# shows none of your own plugins, startup spaces or saved SSH machines.
#   D=$(demo/home.sh); export XDG_CONFIG_HOME=$D/config XDG_STATE_HOME=$D/state
# Run from the repo root. The path stays short: herdr's socket lives under it.
set -eu
dest="${1:-/tmp/herdr-demo}"
# Stop a demo server left over from the last run before wiping its home.
[ -d "$dest" ] && env -u HERDR_SOCKET_PATH -u HERDR_SESSION XDG_CONFIG_HOME="$dest/config" \
  XDG_STATE_HOME="$dest/state" herdr session stop demo >/dev/null 2>&1 || true
rm -rf "$dest"
mkdir -p "$dest/config/herdr" "$dest/state"
demo/config.sh "${HERDR_DEMO_CONFIG:-$HOME/.config/herdr/config.toml}" "$dest/config/herdr/config.toml" >/dev/null
env -u HERDR_SOCKET_PATH -u HERDR_SESSION XDG_CONFIG_HOME="$dest/config" XDG_STATE_HOME="$dest/state" \
  herdr plugin link "$PWD" >/dev/null
echo "$dest"
