#!/bin/sh
# Writes a demo copy of your herdr config with the tab bar's right side
# (hostname, clock) emptied, and prints its path for HERDR_CONFIG_PATH.
#   demo/config.sh [src] [dest]
src="${1:-$HOME/.config/herdr/config.toml}"
dest="${2:-/tmp/herdr-demo-config.toml}"
awk '
  /^tab_bar_right[ \t]*=/ { print "tab_bar_right = []"; skip = !/\]/; next }
  skip { if (/^\]/) skip = 0; next }
  { print }
' "$src" > "$dest"
echo "$dest"
