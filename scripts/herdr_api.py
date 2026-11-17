"""Shared helpers: herdr's socket API, its CLI, and this plugin's state dir."""
import hashlib
import json
import os
import socket
import subprocess

PLUGIN_ID = "herdr-vim-navigation"
SOCK = os.environ.get("HERDR_SOCKET_PATH") or os.path.expanduser("~/.config/herdr/herdr.sock")


def _herdr_bin():
    # HERDR_BIN_PATH can point at a deleted binary after `herdr update`.
    path = os.environ.get("HERDR_BIN_PATH", "")
    return path if path and os.access(path, os.X_OK) else "herdr"


HERDR = _herdr_bin()

# Act on whatever has focus, not on the pane that happened to launch us.
ENV = {k: v for k, v in os.environ.items() if k != "HERDR_PANE_ID"}


def call(method, params=None):
    """One request over herdr's socket API; returns the decoded response."""
    s = socket.socket(socket.AF_UNIX)
    s.connect(SOCK)
    req = {"id": PLUGIN_ID, "method": method, "params": params or {}}
    s.sendall((json.dumps(req) + "\n").encode())
    buf = b""
    while not buf.endswith(b"\n"):
        chunk = s.recv(65536)
        if not chunk:
            break
        buf += chunk
    s.close()
    return json.loads(buf)


def cli(*args):
    """Run `herdr <args>` and decode its JSON output ({} when there is none)."""
    out = subprocess.run([HERDR, *args], env=ENV, capture_output=True, text=True).stdout
    return json.loads(out) if out.strip() else {}


def spaces():
    return call("workspace.list")["result"]["workspaces"]


def focused_space():
    return next((w["workspace_id"] for w in spaces() if w["focused"]), None)



def state_path(name):
    """A per-session state file. The state dir is per plugin, the socket per session."""
    base = os.environ.get("HERDR_PLUGIN_STATE_DIR") or os.path.join(
        os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state"), PLUGIN_ID)
    os.makedirs(base, exist_ok=True)
    session = hashlib.sha1(SOCK.encode()).hexdigest()[:12]
    return os.path.join(base, f"{session}-{name}")
