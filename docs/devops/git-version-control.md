---
title: Git Version Control
category: concepts
tags: [devops, git, version-control, branching, github, gitflow]
---

# Git Version Control

Git is a distributed version control system where every clone is a full repository. Core to all DevOps workflows as the source of truth for code and infrastructure.

## Core Workflow

```bash
git init                          # initialize
git clone URL                     # clone existing
git status                        # check changes
git add file.txt                  # stage specific file
git commit -m "message"           # commit
git push origin main              # push to remote
git pull origin main              # pull from remote
```

## Branching

```bash
git branch feature-x              # create
git checkout -b feature-x         # create + switch
git merge feature-x               # merge into current
git branch -d feature-x           # delete local
git push origin feature-x         # push branch
```

## History and Diff

```bash
git log --oneline --graph         # compact graph
git diff                          # unstaged changes
git diff --staged                 # staged changes
git show commit-hash              # specific commit
```

## Undoing Changes

```bash
git checkout -- file              # discard unstaged
git reset HEAD file               # unstage
git reset --soft HEAD~1           # undo commit, keep changes
git reset --hard HEAD~1           # undo commit, discard changes
git revert commit-hash            # new commit undoing target
git stash / git stash pop         # temporary save/restore
```

## Branching Strategies

### GitHub Flow

- `main` always deployable
- Feature branches from main
- Merge via pull request after review
- Deploy after merge
- Best for: single-version products, websites

### Git Flow

- `main` (production) + `develop` (active development)
- Feature branches -> develop
- Release branches for version prep
- Hotfix branches for urgent fixes
- Best for: multiple simultaneous versions

### Forking Workflow

- Fork repository, work in fork
- PR from fork to original
- Best for: open source, large teams

## Monorepo vs Multirepo

- **Monorepo** - all services in one repo. Simpler deps, cross-cutting refactoring. Risk: size, performance
- **Multirepo** - separate repos. Better isolation, independent releases. Risk: cross-repo changes harder

### Git Submodules

```bash
git submodule add <url> <path>
git submodule update --remote
git clone --recurse-submodules <url>
```

## .gitignore

```text
node_modules/
.env
*.log
terraform.tfstate
.terraform/
```

## Internals

- **Objects**: blobs (content), trees (dirs), commits (snapshots)
- **HEAD**: pointer to current commit/branch
- **Index**: staging area between working dir and repo
- `.git/` contains all data

## Gotchas

- `latest` is just a tag convention, not special to Git
- `git reset --hard` is destructive - cannot be undone easily
- Submodules require explicit init/update after clone
- `.gitignore` only affects untracked files - already tracked files need `git rm --cached`

## See Also

- [[cicd-pipelines]] - Git triggers CI/CD
- [[gitops-and-argocd]] - Git as source of truth for infra
- [[deployment-strategies]] - branching drives releases
