---
title: "Git et GitHub"
category: concepts
tags: [web-frontend, git, github, version-control]
level: 3
source_sha256: 04176bdda50662c6ea63cd251b7378ab8896b3a1fc89d48ee032b31c17e99f3a
translation: machine
translated_at: '2026-10-24'
---
# Git et GitHub {#git-and-github}

Git est un système de contrôle de version distribué. Chaque développeur dispose de l'historique complet du dépôt. GitHub héberge les dépôts distants et permet la collaboration.

## Configuration {#configuration}

```bash
git config --global user.name "Name"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main
```

## Workflow de base {#basic-workflow}

```bash
git init                    # New repo
git clone <url>             # Clone existing

git status                  # Modified/staged/untracked
git add file.txt            # Stage specific file
git add .                   # Stage all (careful)
git commit -m "Add feature" # Commit staged changes
```

### Zone de préparation (staging area) {#staging-area}
```php
Working Directory  -->  Staging Area  -->  Repository
   (modified)         (git add)        (git commit)
```

## Consulter les modifications {#viewing-changes}

```bash
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git diff branch1 branch2    # Between branches
git log --oneline --graph   # Visual history
```

## Annuler des modifications {#undoing}

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

## Fusion {#merging}

```bash
git switch main
git merge feature
```

**Fast-forward** : main n'a aucun nouveau commit, le pointeur avance (pas de commit de fusion).
**Three-way merge** : les deux branches ont divergé, un commit de fusion est créé.

### Résolution des conflits {#conflict-resolution}
```text
<<<<<<< HEAD
current branch code
=======
incoming branch code
>>>>>>> feature
```
Édition manuelle, suppression des marqueurs, `git add`, `git commit`.

## Rebase {#rebase}

```bash
git switch feature
git rebase main        # Replay feature commits on top of main
```

| | Merge | Rebase |
|-|-------|--------|
| Historique | Non linéaire (préservé) | Linéaire (plus propre) |
| Sécurité | Sûr (pas de réécriture) | Dangereux pour les branches partagées |
| Quand | Public/partagé | Local/privé avant fusion |

**Ne jamais rebaser des commits déjà poussés sur des branches partagées.**

## Cherry-pick et stash {#cherry-pick-and-stash}

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

À ajouter avant le premier commit. Les fichiers déjà suivis nécessitent `git rm --cached` pour être retirés du suivi.

## Dépôt distant GitHub {#github-remote}

```bash
git remote add origin <url>
git push -u origin main      # Push + set tracking
git push                     # Push to tracked
git pull                     # Fetch + merge
git fetch                    # Download without merging
```

### Pull Requests {#pull-requests}
1. Créer une branche de fonctionnalité, la pousser sur le dépôt distant
2. Ouvrir une PR sur GitHub (base : main, compare : feature)
3. Revue de code, vérifications CI
4. Fusionner (commit de fusion, squash ou rebase)

### Workflow avec fork {#fork-workflow}
1. Forker le dépôt -> cloner votre fork
2. Ajouter le remote upstream
3. Créer une branche, committer, pousser vers le fork
4. Ouvrir une PR vers le dépôt d'origine

## Messages de commit {#commit-messages}

```yaml
type: short summary (imperative, max 50 chars)

Longer explanation of why.
Closes #123
```

Types : `feat:`, `fix:`, `refactor:`, `style:`, `docs:`, `test:`, `chore:`

## Pièges courants {#gotchas}

- **Committer node_modules** : toujours ajouter au .gitignore avant le premier commit
- **Force push** : `git push --force` écrase l'historique distant, dangereux sur les branches partagées
- **HEAD détaché** : extraire directement un commit place en état détaché ; créer une branche pour sauvegarder le travail
- **Gros fichiers** : git stocke l'historique complet ; utiliser Git LFS pour les fichiers binaires
- **Données sensibles committées** : même après suppression, elles restent dans l'historique ; utiliser `git filter-repo` ou BFG

## Voir aussi {#see-also}

- [[npm-and-task-runners]] - .gitignore pour node_modules
- [[frontend-build-systems]] - déclencheurs de build CI/CD
- [[terminal-basics]] - commandes du terminal pour les workflows git
