# Git and contribution policy

## Worktree policy

When starting work from `main`:

- Use a separate Git worktree for each independent task.
- Never let two agents modify the same worktree.
- Use one branch per worktree.
- Prefer branch names such as `codex/<task-name>`.

## Commit messages

- Write commit messages using [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), in the format `<type>[optional scope][!]: <description>`, followed by an optional body and footer(s).
- Use `feat` for new features and `fix` for bug fixes. Other descriptive types such as `docs`, `chore`, `refactor`, and `test` are also allowed.
- Mark breaking changes with `!` before the colon or a `BREAKING CHANGE:` footer.

## Pull request content

- Do not include local machine absolute paths, usernames, home directories, or workspace paths in PR titles, descriptions, or comments.
- Use repository-relative paths when referring to files.

### Worktree location

- Store persistent worktrees under `~/worktrees/<repo>/`.
- Name Codex worktrees `codex-<task-name>`, for example:
  `~/worktrees/notes-with-ai/codex-data-security`.
- Do not create long-lived Git worktrees under `/tmp`, `/private/tmp`,
  `$TMPDIR`, or other temporary directories.
- If a worktree already exists for the task, reuse it only when it belongs
  exclusively to the current task and agent. Otherwise create a new worktree.

### Worktree setup

- Run repository setup instructions immediately after creating a worktree.
- Treat each worktree as an isolated workspace.
- Do not share runtime state such as PID files, ports, temporary files,
  build output, or caches unless the repository explicitly says they are safe
  to share.

### Before finishing

- Run the repository's formatting and validation commands.
- Inspect `git status` and `git diff`.
- Report:

  - the branch;
  - the worktree path;
  - the validation results.

- Do not remove the worktree unless explicitly requested.
