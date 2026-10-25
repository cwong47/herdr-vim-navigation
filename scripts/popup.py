#!/usr/bin/env python3
"""Open one of this plugin's popup panes (an action can't open a popup directly).

Usage: popup.py <entrypoint>
"""
import sys

from herdr_api import PLUGIN_ID, cli

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: popup.py <entrypoint>")
    cli("plugin", "pane", "open", "--plugin", PLUGIN_ID, "--entrypoint", sys.argv[1],
        "--placement", "popup", "--focus")
