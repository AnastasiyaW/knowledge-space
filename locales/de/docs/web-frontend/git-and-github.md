---
title: "Git und GitHub"
category: concepts
tags: [web-frontend, git, github, version-control]
level: 3
source_sha256: 04176bdda50662c6ea63cd251b7378ab8896b3a1fc89d48ee032b31c17e99f3a
translation: machine
translated_at: '2026-10-24'
---
# Git und GitHub {#git-and-github}

Git ist ein verteiltes Versionskontrollsystem. Jeder Entwickler besitzt die vollständige Repository-Historie. GitHub hostet Remote-Repositories und ermöglicht die Zusammenarbeit.

## Konfiguration {#configuration}

```bash
git config --global user.name "Name"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main
```

## Grundlegender Workflow {#basic-workflow}

```bash
git init                    # New repo
git clone <url>             # Clone existing

git status                  # Modified/staged/untracked
git add file.txt            # Stage specific file
git add .                   # Stage all (careful)
git commit -m "Add feature" # Commit staged changes
```

### Staging-Bereich {#staging-area}
```php
Working Directory  -->  Staging Area  -->  Repository
   (modified)         (git add)        (git commit)
```

## Änderungen anzeigen {#viewing-changes}

```bash
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git diff branch1 branch2    # Between branches
git log --oneline --graph   # Visual history
```

## Rückgängigmachen {#undoing}

```bash
git restore --staged file   # Unstage (keep changes)
git restore file            # Discard working changes
git commit --amend          # Fix last commit
git revert <hash>           # New commit undoing changes
git reset --soft HEAD~1     # Undo commit, keep staged
git reset --mixed HEAD~1    # Undo commit, keep in working dir
git reset --hard HEAD~1     # Undo commit, discard everything (dangerous!)
```

## Branches {#branches}

```bash
git branch feature          # Create
git switch feature          # Switch
git switch -c feature       # Create + switch
git branch -d feature       # Delete (safe)
git branch -D feature       # Force delete
```

## Mergen {#merging}

```bash
git switch main
git merge feature
```

**Fast-forward**: main hat keine neuen Commits, der Zeiger wird einfach vorwärts bewegt (kein Merge-Commit).
**Three-way-Merge**: beide Branches sind auseinandergelaufen, es wird ein Merge-Commit erstellt.

### Konfliktlösung {#conflict-resolution}
```text
<<<<<<< HEAD
current branch code
=======
incoming branch code
>>>>>>> feature
```
Manuell bearbeiten, Markierungen entfernen, `git add`, `git commit`.

## Rebase {#rebase}

```bash
git switch feature
git rebase main        # Replay feature commits on top of main
```

| | Merge | Rebase |
|-|-------|--------|
| Historie | Nicht linear (bleibt erhalten) | Linear (übersichtlicher) |
| Sicherheit | Sicher (kein Umschreiben) | Gefährlich für geteilte Branches |
| Wann | Öffentlich/geteilt | Lokal/privat vor dem Merge |

**Niemals bereits gepushte Commits auf geteilten Branches rebasen.**

## Cherry-Pick und Stash {#cherry-pick-and-stash}

```bash
git cherry-pick <hash>     # Apply specific commit
git stash                  # Save uncommitted changes
git stash pop              # Restore most recent
git stash list             # List all stashes
```

## .gitignore {#gitignore}

```gitignore
node_modules/
dist/
.env
.DS_Store
*.log
.vscode/
```

Vor dem ersten Commit hinzufügen. Bereits getrackte Dateien benötigen `git rm --cached`, um sie aus dem Tracking zu nehmen.

## GitHub Remote {#github-remote}

```bash
git remote add origin <url>
git push -u origin main      # Push + set tracking
git push                     # Push to tracked
git pull                     # Fetch + merge
git fetch                    # Download without merging
```

### Pull Requests {#pull-requests}
1. Feature-Branch erstellen, zum Remote pushen
2. PR auf GitHub öffnen (Basis: main, Vergleich: feature)
3. Code-Review, CI-Prüfungen
4. Mergen (Merge-Commit, Squash oder Rebase)

### Fork-Workflow {#fork-workflow}
1. Repository forken -> eigenen Fork klonen
2. Upstream-Remote hinzufügen
3. Branch erstellen, committen, zum Fork pushen
4. PR an das Original-Repository öffnen

## Commit-Nachrichten {#commit-messages}

```yaml
type: short summary (imperative, max 50 chars)

Longer explanation of why.
Closes #123
```

Typen: `feat:`, `fix:`, `refactor:`, `style:`, `docs:`, `test:`, `chore:`

## Stolperfallen {#gotchas}

- **node_modules committen**: vor dem ersten Commit immer in die .gitignore aufnehmen
- **Force Push**: `git push --force` überschreibt die Remote-Historie – gefährlich auf geteilten Branches
- **Detached HEAD**: Direkt auf einen Commit zu wechseln versetzt dich in den Detached-HEAD-Zustand; erstelle einen Branch, um deine Arbeit zu sichern
- **Große Dateien**: Git speichert die vollständige Historie; verwende Git LFS für Binärdateien
- **Sensible Daten committet**: selbst nach dem Entfernen bleiben sie in der Historie erhalten; verwende `git filter-repo` oder BFG

## Siehe auch {#see-also}

- [[npm-and-task-runners]] - .gitignore für node_modules
- [[frontend-build-systems]] - CI/CD-Build-Trigger
- [[terminal-basics]] - Terminal-Befehle für Git-Workflows
