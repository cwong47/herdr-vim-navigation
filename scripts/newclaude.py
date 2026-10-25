#!/usr/bin/env python3
"""Start claude (or any agent command) in a new space, tab or split.

Usage: newclaude.py space|tab|right|down
       newclaude.py --menu   (popup: w space, t tab, | right, - down)
The command replaces the shell (exec), so quitting it closes the pane.
config.env in the plugin's config dir sets CLAUDE_COMMAND (default: claude)
and CLAUDE_CWD (default: the focused pane's directory).
"""
import os
import subprocess
import sys
import termios
import tty

from herdr_api import cli, read_config

MENU = {"w": "space", "t": "tab", "|": "right", "-": "down"}


def menu():
    print("claude:  w space   t tab   | right   - down   esc cancel")
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        key = os.read(fd, 1).decode(errors="ignore")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    if key in MENU:
        # Detach so the popup closes before the new pane takes focus.
        subprocess.Popen([sys.executable, os.path.abspath(__file__), MENU[key]],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)


def start(mode):
    conf = read_config()
    command = conf.get("CLAUDE_COMMAND") or "claude"
    cwd = os.path.expanduser(conf.get("CLAUDE_CWD", ""))
    if not cwd:
        pane = cli("pane", "current").get("result", {}).get("pane", {})
        cwd = pane.get("foreground_cwd") or pane.get("cwd") or os.path.expanduser("~")

    if mode == "space":
        pane = cli("workspace", "create", "--cwd", cwd, "--focus")["result"]["root_pane"]
    elif mode == "tab":
        pane = cli("tab", "create", "--cwd", cwd, "--focus")["result"]["root_pane"]
    else:
        pane = cli("pane", "split", "--direction", mode, "--cwd", cwd, "--focus")["result"]["pane"]
    cli("pane", "run", pane["pane_id"], f"exec {command}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--menu":
        menu()
    elif mode in ("space", "tab", "right", "down"):
        start(mode)
    else:
        sys.exit("usage: newclaude.py space|tab|right|down|--menu")
