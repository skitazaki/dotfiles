# Git worktree policy

When working on tasks in parallel:

- Use a separate Git worktree for each independent task.
- Never let two agents modify the same worktree.
- Use one branch per worktree.
- Prefer branch names such as `codex/<task-name>`.
- Run repository setup instructions immediately after creating a worktree.
- Do not share runtime state such as PID files, ports, temporary files,
  build output, or caches unless the repository explicitly says they are safe
  to share.
- Before finishing:
  - run the repository's formatting and validation commands;
  - inspect `git diff`;
  - report the branch, worktree, and validation results.
