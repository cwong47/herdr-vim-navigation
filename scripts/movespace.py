#!/usr/bin/env python3
"""Move the focused space (workspace) up or down in the sidebar.

Usage: movespace.py up|down [--interactive]
With --interactive (run in a popup), keep moving with ^K/^J, k/j or arrows;
Enter, Esc or q exits.
"""
import os
import sys
import termios
import tty

from herdr_api import call, focused_space, spaces


def move(cur, direction):
    ids = [w["workspace_id"] for w in spaces()]
    # insert_index counts slots before removing cur, so moving down skips one extra.
    i = ids.index(cur)
    if direction == "up" and i > 0:
        call("workspace.move", {"workspace_id": cur, "insert_index": i - 1})
    elif direction == "down" and i < len(ids) - 1:
        call("workspace.move", {"workspace_id": cur, "insert_index": i + 2})


def status(cur):
    ws = spaces()
    w = next(w for w in ws if w["workspace_id"] == cur)
    sys.stdout.write(f"\r\x1b[K{w['number']}/{len(ws)}  {w['label'][:40]}")
    sys.stdout.flush()


KEYS = {"\x0b": "up", "k": "up", "\x1b[A": "up",
        "\x0a": "down", "j": "down", "\x1b[B": "down"}


def interactive(cur):
    print("^K/^J k/j arrows: move   Enter/Esc: done")
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        while True:
            status(cur)
            buf = os.read(fd, 64).decode(errors="ignore")
            while buf:
                key = buf[:3] if buf.startswith("\x1b[") else buf[0]
                buf = buf[len(key):]
                if key in ("\r", "\x1b", "q", "\x03"):
                    return
                if key in KEYS:
                    move(cur, KEYS[key])
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == "__main__":
    direction = sys.argv[1] if len(sys.argv) > 1 else ""
    if direction not in ("up", "down"):
        sys.exit("usage: movespace.py up|down [--interactive]")
    cur = focused_space()
    if cur is None:
        sys.exit(0)
    move(cur, direction)
    if "--interactive" in sys.argv[2:]:
        interactive(cur)
