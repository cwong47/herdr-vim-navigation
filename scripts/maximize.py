#!/usr/bin/env python3
"""Make the focused pane as tall or wide as it can get (like Vim's ^W _ / ^W |).

Usage: maximize.py height|width [pane_id]
Every split on the way to the pane that stacks along the chosen axis is pushed
toward the pane; the other axis is left alone. herdr clamps split ratios to
0.1-0.9, so neighbours keep a sliver instead of Vim's one line.
"""
import sys

from herdr_api import call


def path_to(node, pane, path=()):
    """Splits from the root down to `pane`, as (path, direction, pane_in_second)."""
    if node["type"] == "pane":
        return [] if node["pane_id"] == pane else None
    for second, child in ((False, node["first"]), (True, node["second"])):
        rest = path_to(child, pane, path + (second,))
        if rest is not None:
            return [(list(path), node["direction"], second)] + rest
    return None


def maximize(axis, pane=None):
    layout = call("layout.export", {"pane_id": pane} if pane else {})["result"]["layout"]
    root = layout["root"]
    if layout["zoomed"] or root["type"] == "pane":
        return
    direction = "down" if axis == "height" else "right"
    for path, d, second in path_to(root, pane or layout["focused_pane_id"]):
        if d == direction:
            call("layout.set_split_ratio", {"tab_id": layout["tab_id"], "path": path,
                                            "ratio": 0.0 if second else 1.0})


if __name__ == "__main__":
    axis = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if axis not in ("height", "width"):
        sys.exit("usage: maximize.py height|width [pane_id]")
    maximize(axis, sys.argv[2] if len(sys.argv) > 2 else None)
