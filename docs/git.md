# Git CLI Quick Reference

Please review [CONTRIBUTING.md](CONTRIBUTING.md) for processes in branching, pushing, and issue tracking.

## Checking Out a Branch

- **Switch to a new branch:**
  ```bash
  git checkout my-branch
  ```

## Adding Files and Committing Changes

- **Add all changes:**
  ```bash
  git add .
  ```
- **Add specific files:**
  ```bash
  git add path/to/file
  ```
- **Commit changes with a message:**
  ```bash
  git commit -m "Add feature X and fix issue Y"
  ```

## Pushing Changes

- **Send your changes to the remote:**
  ```bash
  git push
  ```

## Additional Useful Commands

- **Check Repository Status:**
  ```bash
  git status
  ```
- **Fetch Remote Updates:**
  ```bash
  git fetch
  ```
- **Update your Branch with the latest changes:**
  ```bash
  git rebase main
  ```
