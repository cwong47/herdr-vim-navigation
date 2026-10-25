#!/usr/bin/env python3
"""Equalize pane sizes in the focused tab (like vim's ^W =).

Usage: equalize.py [tab_id]
Panes side by side get equal widths, panes stacked get equal heights.
"""
import sys

from herdr_api import call


def slots(node, direction):
    """Number of panes laid out side by side along `direction`."""
    if node["type"] == "split" and node["direction"] == direction:
        return slots(node["first"], direction) + slots(node["second"], direction)
    return 1


def walk(node, path, out):
    if node["type"] != "split":
        return
    d = node["direction"]
    out.append((path, slots(node["first"], d) / slots(node, d)))
    walk(node["first"], path + [False], out)
    walk(node["second"], path + [True], out)


def equalize(tab_id=None):
    layout = call("layout.export", {"tab_id": tab_id}).get("result", {}).get("layout", {})
    root = layout.get("root")
    if not root:
        return
    todo = []
    walk(root, [], todo)
    for path, ratio in todo:
        call("layout.set_split_ratio", {"tab_id": layout["tab_id"], "path": path, "ratio": ratio})


if __name__ == "__main__":
    equalize(sys.argv[1] if len(sys.argv) > 1 else None)
