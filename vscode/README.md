# VS Code Agent Mode Worktree Location

## Overview

In VS Code Agent Mode (Copilot SDK), Git worktrees are currently created under a repository-adjacent directory using the following pattern:

- `<parent-of-repo>/<repo>.worktrees/`

Example:

- `~/workspace/dotfiles.worktrees/`

## Configuration Status

There is currently no public VS Code setting (including `settings.json`) to change the Agent Mode worktree root to a custom path such as:

- `~/worktrees/<repo>/`

## Operational Workaround

If a unified location is required, a practical approach is to use a symbolic link from:

- `<parent-of-repo>/<repo>.worktrees`

to:

- `~/worktrees/<repo>/`
