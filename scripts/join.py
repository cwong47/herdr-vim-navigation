#!/usr/bin/env python3
"""Move the focused pane into another tab as a split (like tmux's join-pane).

Usage: join.py [pane_id]     remember the pane and open the picker popup
       join.py --interactive  the picker: j/k or arrows select a target pane,
                              Enter/l/| split right, -/s split down, Esc/q cancel
The picker lists panes in every other tab (herdr refuses same-tab moves).
"""
import os
import sys
import termios
import tty

from herdr_api import call, cli, spaces, state_path

STATE = state_path("join-source")


def targets(src):
    """(pane, tab, label) for every pane outside the source pane's tab."""
    src_tab = next(p["tab_id"] for p in panes() if p["pane_id"] == src)
    space = {w["workspace_id"]: w["label"].strip() for w in spaces()}
    tab = {t["tab_id"]: t["label"] for t in cli("tab", "list")["result"]["tabs"]}
    return [(p["pane_id"], p["tab_id"],
             f"{space.get(p['workspace_id'], '?')} / {tab.get(p['tab_id'], '?')} / "
             f"{p.get('label') or p.get('terminal_title_stripped') or p['pane_id']}")
            for p in panes() if p["tab_id"] != src_tab]


def panes():
    return cli("pane", "list")["result"]["panes"]


def draw(rows, sel, height):
    top = max(0, min(sel - height // 2, len(rows) - height))
    out = ["\x1b[H\x1b[2J", "j/k: select  Enter/l: right  -/s: down  Esc/q: cancel\r\n"]
    for i, (_, _, label) in enumerate(rows[top:top + height], top):
        line = label[:os.get_terminal_size().columns - 3]
        out.append(f"\x1b[7m❯ {line}\x1b[0m\r\n" if i == sel else f"  {line}\r\n")
    sys.stdout.write("".join(out))
    sys.stdout.flush()


KEYS = {"k": -1, "\x1b[A": -1, "\x10": -1, "j": 1, "\x1b[B": 1, "\x0e": 1}
SPLIT = {"\r": "right", "l": "right", "|": "right", "-": "down", "s": "down"}


def interactive():
    try:
        with open(STATE) as f:
            src = f.read().strip()
    except FileNotFoundError:
        return
    rows = targets(src)
    if not rows:
        return
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    sel = 0
    try:
        while True:
            draw(rows, sel, os.get_terminal_size().lines - 1)
            buf = os.read(fd, 64).decode(errors="ignore")
            while buf:
                key = buf[:3] if buf.startswith("\x1b[") else buf[0]
                buf = buf[len(key):]
                if key in ("\x1b", "q", "\x03"):
                    return
                if key in KEYS:
                    sel = (sel + KEYS[key]) % len(rows)
                elif key in SPLIT:
                    pane, tab, _ = rows[sel]
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                    cli("pane", "move", src, "--tab", tab, "--target-pane", pane,
                        "--split", SPLIT[key], "--focus")
                    return
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == "__main__":
    if sys.argv[1:] == ["--interactive"]:
        interactive()
        sys.exit(0)
    pane = sys.argv[1] if len(sys.argv) > 1 else None
    pane = pane or call("layout.export")["result"]["layout"]["focused_pane_id"]
    with open(STATE, "w") as f:
        f.write(pane)
    cli("plugin", "pane", "open", "--plugin", "herdr-vim-navigation",
        "--entrypoint", "join-picker", "--placement", "popup", "--focus")
