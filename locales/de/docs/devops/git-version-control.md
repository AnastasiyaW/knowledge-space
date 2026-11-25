---
title: "Git-Versionskontrolle"
category: concepts
tags: [devops, git, version-control, branching, github, gitflow]
level: 3
source_sha256: 28295dbf5226170298be0df88953fa2daeff2ca81e8467a9ddae3f02e86ca926
translation: machine
translated_at: '2026-10-24'
---
# Git-Versionskontrolle {#git-version-control}

Git ist ein verteiltes Versionskontrollsystem, bei dem jeder Klon ein vollständiges Repository ist. Es ist zentral für alle DevOps-Workflows und dient als Quelle der Wahrheit für Code und Infrastruktur.

## Kern-Workflow {#core-workflow}

```bash
git init                          # initialize
git clone URL                     # clone existing
git status                        # check changes
git add file.txt                  # stage specific file
git commit -m "message"           # commit
git push origin main              # push to remote
git pull origin main              # pull from remote
```

## Branching {#branching}

```bash
git branch feature-x              # create
git checkout -b feature-x         # create + switch
git merge feature-x               # merge into current
git branch -d feature-x           # delete local
git push origin feature-x         # push branch
```

## Historie und Diff {#history-and-diff}

```bash
git log --oneline --graph         # compact graph
git diff                          # unstaged changes
git diff --staged                 # staged changes
git show commit-hash              # specific commit
```

## Änderungen rückgängig machen {#undoing-changes}

```bash
git checkout -- file              # discard unstaged
git reset HEAD file               # unstage
git reset --soft HEAD~1           # undo commit, keep changes
git reset --hard HEAD~1           # undo commit, discard changes
git revert commit-hash            # new commit undoing target
git stash / git stash pop         # temporary save/restore
```

## Branching-Strategien {#branching-strategies}

### GitHub Flow {#github-flow}

- `main` ist immer deploybar
- Feature-Branches von main
- Merge über Pull Request nach dem Review
- Deployment nach dem Merge
- Am besten für: Produkte mit einer einzigen Version, Websites

### Git Flow {#git-flow}

- `main` (Produktion) + `develop` (aktive Entwicklung)
- Feature-Branches -> develop
- Release-Branches zur Vorbereitung von Versionen
- Hotfix-Branches für dringende Fixes
- Am besten für: mehrere parallele Versionen

### Forking-Workflow {#forking-workflow}

- Repository forken, in dem Fork arbeiten
- PR vom Fork in das Original
- Am besten für: Open Source, große Teams

## Monorepo vs. Multirepo {#monorepo-vs-multirepo}

- **Monorepo** - alle Services in einem Repo. Einfachere Abhängigkeiten, bereichsübergreifende Refactorings. Risiko: Größe, Performance
- **Multirepo** - separate Repos. Bessere Isolation, unabhängige Releases. Risiko: repoübergreifende Änderungen sind schwieriger

### Git-Submodule {#git-submodules}

```bash
git submodule add <url> <path>
git submodule update --remote
git clone --recurse-submodules <url>
```

## .gitignore {#gitignore}

```text
node_modules/
.env
*.log
terraform.tfstate
.terraform/
```

## Interna {#internals}

- **Objects**: Blobs (Inhalt), Trees (Verzeichnisse), Commits (Snapshots)
- **HEAD**: Zeiger auf den aktuellen Commit/Branch
- **Index**: Staging-Bereich zwischen Arbeitsverzeichnis und Repository
- `.git/` enthält alle Daten

## Fallstricke {#gotchas}

- `latest` ist nur eine Tag-Konvention und für Git nicht speziell
- `git reset --hard` ist destruktiv - lässt sich nicht einfach rückgängig machen
- Submodule erfordern nach dem Klonen explizites init/update
- `.gitignore` wirkt nur auf nicht getrackte Dateien - bereits getrackte Dateien benötigen `git rm --cached`

## Siehe auch {#see-also}

- [[cicd-pipelines]] - Git löst CI/CD aus
- [[gitops-and-argocd]] - Git als Quelle der Wahrheit für Infrastruktur
- [[deployment-strategies]] - Branching steuert Releases
