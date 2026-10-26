#!/usr/bin/env python3
"""Close every other pane in the focused tab (like vim's ^W o, screen's ^A q),
or every other tab in the focused space (like vim's :tabonly).

Usage: only.py pane [pane_id]
       only.py tab [tab_id]
"""
import sys

from herdr_api import call, cli, focused_space
from move import leaves


def only_pane(pane=None):
    layout = call("layout.export", {"pane_id": pane} if pane else {})["result"]["layout"]
    keep = pane or layout["focused_pane_id"]
    for p in leaves(layout["root"]):
        if p != keep:
            cli("pane", "close", p)


def only_tab(tab=None):
    space = tab.split(":")[0] if tab else focused_space()
    tabs = cli("tab", "list", "--workspace", space)["result"]["tabs"]
    keep = tab or next(t["tab_id"] for t in tabs if t["focused"])
    for t in tabs:
        if t["tab_id"] != keep:
            cli("tab", "close", t["tab_id"])


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "pane"
    target = sys.argv[2] if len(sys.argv) > 2 else None
    {"pane": only_pane, "tab": only_tab}[what](target)
