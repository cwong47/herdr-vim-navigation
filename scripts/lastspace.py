#!/usr/bin/env python3
"""Jump back to the last space (workspace) you were in, like `cd -` or screen's ^A ^A.

Usage: lastspace.py watch|toggle
`watch` is the plugin's startup hook: it subscribes to workspace.focused events
and records the current/previous space. `toggle` focuses the previous space,
starting the watcher first if it is not running.
"""
import json
import os
import signal
import socket
import subprocess
import sys
import time

from herdr_api import PLUGIN_ID, SOCK, call, focused_space, spaces, state_path

STATE = state_path("lastspace.json")
PID = state_path("lastspace.pid")


def load():
    try:
        with open(STATE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save(state):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, STATE)


def watcher_pid():
    try:
        with open(PID) as f:
            pid = int(f.read())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def watch():
    # herdr never stops startup hooks, so a watcher from an earlier server can
    # still be alive; the newest one takes over.
    old = watcher_pid()
    if old and old != os.getpid():
        try:
            os.kill(old, signal.SIGTERM)
        except OSError:
            pass
    with open(PID, "w") as f:
        f.write(str(os.getpid()))

    failures = 0
    while failures < 30:  # give up ~1 min after the server goes away
        try:
            s = socket.socket(socket.AF_UNIX)
            s.connect(SOCK)
            req = {"id": PLUGIN_ID, "method": "events.subscribe",
                   "params": {"subscriptions": [{"type": "workspace.focused"}]}}
            s.sendall((json.dumps(req) + "\n").encode())
            state = load()
            state["cur"] = focused_space()
            save(state)
            failures = 0
            for _ in s.makefile("rb"):
                # Re-read focus rather than parsing the event payload.
                cur = focused_space()
                state = load()
                if cur and cur != state.get("cur"):
                    state["prev"], state["cur"] = state.get("cur"), cur
                    save(state)
        except OSError:
            pass
        failures += 1
        time.sleep(2)


def toggle():
    if not watcher_pid():
        subprocess.Popen([sys.executable, os.path.abspath(__file__), "watch"],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)
        return
    prev = load().get("prev")
    if prev and prev in {w["workspace_id"] for w in spaces()}:
        call("workspace.focus", {"workspace_id": prev})


if __name__ == "__main__":
    command = {"watch": watch, "toggle": toggle}.get(sys.argv[1] if len(sys.argv) > 1 else "")
    if command is None:
        sys.exit("usage: lastspace.py watch|toggle")
    command()
