# herdr-vim-navigation — demo tape
# Record from the repo root, in a terminal that is NOT inside herdr:
#     vhs demo/demo.tape
# Uses a throwaway "demo" session in its own herdr home (demo/home.sh, rebuilt
# each run), so your real session, other plugins and SSH machines stay out.
# Keys assume prefix = Ctrl+B and the bindings in ~/.config/herdr/config.toml.
#
# Captions: each step starts with a hidden `cap TITLE BODY` (from
# demo/demo.bashrc) typed into the focused pane, which pops a herdr toast
# and clears the pane, so only the toast shows in the recording.

Output demo/demo.gif
Output demo/demo.mp4

Set Shell "bash"
# Same character grid as FontSize 10 @ 1440x810, rendered 1.6x larger so
# glyphs get more pixels and stay sharp when GitHub scales the gif down.
Set FontSize 16
Set Width 2304
Set Height 1296
Set Padding 16
Set Theme "Catppuccin Mocha"
Set TypingSpeed 40ms

# ── Setup (hidden): demo session, 4 spaces, 3-pane layout in the first ──
# SHELL points herdr's panes at demo/shell.sh (no dotfiles, plain prompt).
# The herdr CLI inside a pane talks to that pane's session (HERDR_SOCKET_PATH),
# so the extra spaces land in "demo", not your real session.
# XDG_CONFIG_HOME/XDG_STATE_HOME point herdr at demo/home.sh's throwaway home:
# a copy of your config without the hostname/clock on the tab bar
# (demo/config.sh) and only this plugin linked.
Hide
Type "D=$(demo/home.sh); export SHELL=$PWD/demo/shell.sh PS1='$ ' XDG_CONFIG_HOME=$D/config XDG_STATE_HOME=$D/state; clear; herdr --session demo"
Enter
Sleep 3s
Type@5ms "for s in api:45 web:46 docs:43; do herdr workspace create --label ${s%:*} --env DEMO_LABEL=${s%:*} --env DEMO_COLOR=${s#*:} --no-focus >/dev/null; done"
Enter
Sleep 1.5s
# Each pane gets a colored label + content (see view in demo/demo.bashrc).
Type@5ms "DEMO_LABEL=editor DEMO_COLOR=44 DEMO_VIEW='cat -n scripts/move.py | head -20'; view"
Enter
Sleep 500ms
Ctrl+B
Type "|"
Sleep 800ms
Type@5ms "DEMO_LABEL=git DEMO_COLOR=42 DEMO_VIEW='git -c color.ui=always log --stat --oneline -1'; view"
Enter
Sleep 500ms
Ctrl+B
Type "-"
Sleep 800ms
Type@5ms "DEMO_LABEL=files DEMO_COLOR=41 DEMO_VIEW='ls -lG scripts'; view"
Enter
Sleep 500ms
Show

# ── Panes: move to edges (vim ^W H / ^W L) ──
Hide
Type@5ms "cap 'Move pane to edge' 'prefix H / L  (vim ^W H, ^W L)'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "H"
Sleep 1.5s
Ctrl+B
Type "L"
Sleep 1.5s

# ── Panes: skew the layout, then equalize (vim ^W =) ──
# Resize happens hidden via the CLI so the gif opens on a lopsided layout;
# --amount is a guess — tune it until the skew is obvious.
Hide
Type@5ms "herdr pane resize --current --direction right --amount 0.25; herdr pane resize --current --direction down --amount 0.2; cap 'Equalize panes' 'prefix =  (vim ^W =)'"
Enter
Sleep 500ms
Show
Sleep 2s
Ctrl+B
Type "="
Sleep 1.5s

# ── Panes: maximize height, then width (vim ^W _ / ^W |) ──
# The three panes sit side by side after H/L, so files drops to the bottom
# edge (hidden) and focus goes up into the top row, giving both axes a split.
# prefix = restores the sizes at the end.
Hide
Ctrl+B
Type "J"
Sleep 1.5s
Ctrl+B
Type "k"
Sleep 300ms
Type@5ms "cap 'Maximize height / width' 'prefix _ / +  (vim ^W _, ^W |)'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "_"
Sleep 1.5s
Ctrl+B
Type "+"
Sleep 1.5s
Ctrl+B
Type "="
Sleep 1.5s

# ── Panes: maximize both axes, not zoom ──
# Same layout and focus as above; prefix = restores the sizes again.
Hide
Type@5ms "cap 'Maximize (both, not zoom)' 'prefix M  (vim ^W _ ^W |)'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "M"
Sleep 2s
Ctrl+B
Type "="
Sleep 1.5s

# ── Spaces: jump to last / first ──
Hide
Type@5ms "cap 'Last / first space' 'prefix }  then  prefix {'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "}"
Sleep 1.5s
Ctrl+B
Type "{"
Sleep 1.5s

# ── Spaces: toggle last space (screen ^A ^A) ──
Hide
Type@5ms "cap 'Previous space (toggle)' 'prefix b  (screen ^A ^A, cd -)'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "b"
Sleep 1.5s
Ctrl+B
Type "b"
Sleep 1.5s

# ── Spaces: reorder — popup, keep pressing ^J / ^K, Enter to close ──
Hide
Type@5ms "cap 'Reorder spaces' 'prefix ^J / ^K, keep pressing, Enter to close'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Ctrl+J
Sleep 1s
Ctrl+J
Sleep 800ms
Ctrl+J
Sleep 1s
Ctrl+K
Sleep 1s
Enter
Sleep 2s

# ── Tabs: close every other tab (vim :tabonly) ──
# Two extra tabs are added hidden via the CLI so there is something to close.
Hide
Type@5ms "herdr tab create --label logs --no-focus >/dev/null; herdr tab create --label scratch --no-focus >/dev/null; cap 'Close other tabs' 'prefix ^Q  (vim :tabonly)'"
Enter
Sleep 500ms
Show
Sleep 2s
Ctrl+B
Ctrl+Q
Sleep 1.5s

# ── Panes: close every other pane (vim ^W o, screen ^A q) ──
Hide
Type@5ms "cap 'Close other panes' 'prefix Q  (vim ^W o, screen ^A q)'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "Q"
Sleep 2s

# ── Panes: break out to a new tab (vim ^W T, tmux prefix !) ──
# Two panes are split back in, hidden, so there is something to break out.
Hide
Ctrl+B
Type "|"
Sleep 800ms
Type@5ms "DEMO_LABEL=logs DEMO_COLOR=45 DEMO_VIEW='git -c color.ui=always log --oneline -8'; view"
Enter
Sleep 500ms
Ctrl+B
Type "-"
Sleep 800ms
Type@5ms "DEMO_LABEL=tests DEMO_COLOR=46 DEMO_VIEW='ls -lG demo'; cap 'Pane to new tab' 'prefix T  (vim ^W T, tmux prefix !)'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "T"
Sleep 2s

# ── Panes: break out to a new space ──
Hide
Type@5ms "cap 'Pane to new space' 'prefix 1  then  prefix W'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "1"
Sleep 1.5s
Ctrl+B
Type "W"
Sleep 2.5s

# ── Panes: join into another tab as a split (tmux join-pane) ──
# Focus is in the space break-space just made; the picker lists panes in every
# other tab, space 1 first, so Enter lands the pane beside space 1's first pane.
Hide
Type@5ms "cap 'Pane into another tab' 'prefix @, pick a pane, Enter  (tmux join-pane)'"
Enter
Sleep 300ms
Show
Sleep 1.5s
Ctrl+B
Type "@"
Sleep 1.5s
Type "j"
Sleep 800ms
Type "j"
Sleep 800ms
Type "k"
Sleep 800ms
Type "k"
Sleep 1s
Enter
Sleep 2.5s
