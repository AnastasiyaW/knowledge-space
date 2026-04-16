---
title: Git and GitHub
category: concepts
tags: [web-frontend, git, github, version-control]
---

# Git and GitHub

Git is a distributed version control system. Every developer has full repo history. GitHub hosts remote repos and enables collaboration.

## Configuration

```bash
git config --global user.name "Name"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main
```

## Basic Workflow

```bash
git init                    # New repo
git clone <url>             # Clone existing

git status                  # Modified/staged/untracked
git add file.txt            # Stage specific file
git add .                   # Stage all (careful)
git commit -m "Add feature" # Commit staged changes
```

### Staging Area
```php
Working Directory  -->  Staging Area  -->  Repository
   (modified)         (git add)        (git commit)
```

## Viewing Changes

```bash
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git diff branch1 branch2    # Between branches
git log --oneline --graph   # Visual history
```

## Undoing

```bash
git restore --staged file   # Unstage (keep changes)
git restore file            # Discard working changes
git commit --amend          # Fix last commit
git revert <hash>           # New commit undoing changes
git reset --soft HEAD~1     # Undo commit, keep staged
git reset --mixed HEAD~1    # Undo commit, keep in working dir
git reset --hard HEAD~1     # Undo commit, discard everything (dangerous!)
```

## Branches

```bash
git branch feature          # Create
git switch feature          # Switch
git switch -c feature       # Create + switch
git branch -d feature       # Delete (safe)
git branch -D feature       # Force delete
```

## Merging

```bash
git switch main
git merge feature
```

**Fast-forward**: main has no new commits, pointer moves forward (no merge commit).
**Three-way merge**: both branches diverged, creates merge commit.

### Conflict Resolution
```text
<<<<<<< HEAD
current branch code
=======
incoming branch code
>>>>>>> feature
```
Manually edit, remove markers, `git add`, `git commit`.

## Rebase

```bash
git switch feature
git rebase main        # Replay feature commits on top of main
```

| | Merge | Rebase |
|-|-------|--------|
| History | Non-linear (preserves) | Linear (cleaner) |
| Safety | Safe (no rewrite) | Dangerous for shared branches |
| When | Public/shared | Local/private before merge |

**Never rebase pushed commits on shared branches.**

## Cherry-Pick and Stash

```bash
git cherry-pick <hash>     # Apply specific commit
git stash                  # Save uncommitted changes
git stash pop              # Restore most recent
git stash list             # List all stashes
```

## .gitignore

```gitignore
node_modules/
dist/
.env
.DS_Store
*.log
.vscode/
```

Add before first commit. Already-tracked files need `git rm --cached` to untrack.

## GitHub Remote

```bash
git remote add origin <url>
git push -u origin main      # Push + set tracking
git push                     # Push to tracked
git pull                     # Fetch + merge
git fetch                    # Download without merging
```

### Pull Requests
1. Create feature branch, push to remote
2. Open PR on GitHub (base: main, compare: feature)
3. Code review, CI checks
4. Merge (merge commit, squash, or rebase)

### Fork Workflow
1. Fork repo -> clone your fork
2. Add upstream remote
3. Branch, commit, push to fork
4. Open PR to original

## Commit Messages

```yaml
type: short summary (imperative, max 50 chars)

Longer explanation of why.
Closes #123
```

Types: `feat:`, `fix:`, `refactor:`, `style:`, `docs:`, `test:`, `chore:`

## Gotchas

- **Committing node_modules**: always .gitignore before first commit
- **Force push**: `git push --force` overwrites remote history - dangerous on shared branches
- **Detached HEAD**: checkout a commit directly puts you in detached state; create branch to save work
- **Large files**: git stores full history; use Git LFS for binary files
- **Sensitive data committed**: even after removal, exists in history; use `git filter-repo` or BFG

## See Also

- [[npm-and-task-runners]] - .gitignore for node_modules
- [[frontend-build-systems]] - CI/CD build triggers
- [[terminal-basics]] - Terminal commands for git workflows
