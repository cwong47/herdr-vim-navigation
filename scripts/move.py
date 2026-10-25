#!/usr/bin/env python3
"""Move the focused pane to a full-height/width edge of its tab (like vim's ^W H/J/K/L).

Usage: move.py h|j|k|l [pane_id]
herdr refuses same-tab moves and can only split a single pane, so every pane
hops out to a temp tab and is moved back one by one, splitting the right leaf
each time to rebuild the tree with the pane at the edge. Processes survive
moves. Sizes are equalized afterwards (vim's equalalways).
"""
import sys

from equalize import equalize
from herdr_api import call, cli


def leaves(node):
    if node["type"] == "pane":
        return [node["pane_id"]]
    return leaves(node["first"]) + leaves(node["second"])


def without(node, pane):
    """Tree with `pane` removed (its sibling takes the parent's place)."""
    if node["type"] == "pane":
        return None if node["pane_id"] == pane else node
    first, second = without(node["first"], pane), without(node["second"], pane)
    if first is None:
        return second
    if second is None:
        return first
    return {**node, "first": first, "second": second}


def build(node, seed, tab, ids):
    """Grow leaf `seed` (the leftmost leaf of `node`) into `node` by moving panes in."""
    if node["type"] == "pane":
        return
    right = leaves(node["second"])[0]
    r = cli("pane", "move", ids[right], "--tab", tab, "--split", node["direction"],
            "--target-pane", ids[seed], "--no-focus")
    ids[right] = r["result"]["move_result"]["pane"]["pane_id"]
    build(node["first"], seed, tab, ids)
    build(node["second"], right, tab, ids)


def move(side, pane=None, focus=True):
    layout = call("layout.export", {"pane_id": pane} if pane else {})["result"]["layout"]
    root = layout["root"]
    if layout["zoomed"] or root["type"] == "pane":
        return

    tab = layout["tab_id"]
    cur = pane or layout["focused_pane_id"]
    edge = {"type": "pane", "pane_id": cur}
    rest = without(root, cur)
    direction = "right" if side in ("h", "l") else "down"
    first, second = (edge, rest) if side in ("h", "k") else (rest, edge)
    target = {"type": "split", "direction": direction, "ratio": 0.5,
              "first": first, "second": second}

    # The target's leftmost leaf stays in the tab as the seed; the rest hop out.
    seed = leaves(target)[0]
    ids = {p: p for p in leaves(root)}
    for p in leaves(root):
        if p != seed:
            r = cli("pane", "move", p, "--new-tab", "--no-focus")
            ids[p] = r["result"]["move_result"]["pane"]["pane_id"]
    build(target, seed, tab, ids)

    if focus:
        call("pane.focus", {"pane_id": ids[cur]})
    equalize(tab)


if __name__ == "__main__":
    side = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if side not in ("h", "j", "k", "l"):
        sys.exit("usage: move.py h|j|k|l [pane_id]")
    move(side, sys.argv[2] if len(sys.argv) > 2 else None)
