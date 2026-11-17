#!/usr/bin/env python3
"""Move the focused pane into a new tab (like Vim's ^W T, tmux's prefix !)
or a new space of its own. A pane already alone in its tab (or space) is left
where it is.

Usage: break.py tab|space [pane_id]
"""
import sys

from herdr_api import call, cli
from move import leaves

if __name__ == "__main__":
    where = sys.argv[1] if len(sys.argv) > 1 else ""
    if where not in ("tab", "space"):
        sys.exit("usage: break.py tab|space [pane_id]")
    pane = sys.argv[2] if len(sys.argv) > 2 else None
    layout = call("layout.export", {"pane_id": pane} if pane else {})["result"]["layout"]
    pane = pane or layout["focused_pane_id"]
    if where == "tab":
        if len(leaves(layout["root"])) > 1:
            cli("pane", "move", pane, "--new-tab", "--focus")
    elif cli("workspace", "get", pane.split(":")[0])["result"]["workspace"]["pane_count"] > 1:
        cli("pane", "move", pane, "--new-workspace", "--focus")
