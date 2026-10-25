#!/usr/bin/env python3
"""Focus the first (top) or last (bottom) space in the sidebar.

Usage: focusspace.py first|last
"""
import sys

from herdr_api import call, spaces

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else ""
    if which not in ("first", "last"):
        sys.exit("usage: focusspace.py first|last")
    ws = spaces()
    if ws:
        target = ws[0] if which == "first" else ws[-1]
        call("workspace.focus", {"workspace_id": target["workspace_id"]})
