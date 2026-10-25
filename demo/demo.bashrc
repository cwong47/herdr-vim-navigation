# Loaded by demo/shell.sh for every pane in the demo session.
PS1='$ '

# view: redraw this pane — a colored DEMO_LABEL banner (background color
# DEMO_COLOR, an ANSI 41-47 code) and the output of DEMO_VIEW, so viewers can
# follow each pane as it moves.
view() {
  clear
  [ -n "$DEMO_LABEL" ] && printf '\033[1;30;%sm  %s  \033[0m\n\n' "${DEMO_COLOR:-47}" "$DEMO_LABEL"
  [ -n "$DEMO_VIEW" ] && eval "$DEMO_VIEW"
}

# cap TITLE BODY: show a herdr toast captioning the next demo step, then
# redraw the pane so the typed command never shows in the recording.
cap() {
  herdr notification show "$1" --body "$2" --position top-right --sound none >/dev/null
  view
}

# Spaces created with --env DEMO_LABEL=... draw themselves on start.
[ -n "$DEMO_LABEL$DEMO_VIEW" ] && view
