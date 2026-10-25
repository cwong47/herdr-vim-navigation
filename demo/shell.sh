#!/bin/sh
# Pane shell for the demo recording: skips ~/.bash_profile and ~/.bashrc so
# the gif shows a plain prompt instead of your dotfiles, and loads
# demo/demo.bashrc instead. Args from herdr (e.g. -l) are ignored on purpose.
# PROMPT_COMMAND and DIRENV_* leak in via the environment and point at hooks
# a clean shell doesn't define.
unset PROMPT_COMMAND DIRENV_DIR DIRENV_FILE DIRENV_DIFF DIRENV_WATCHES
exec bash --noprofile --rcfile "$(dirname "$0")/demo.bashrc"
