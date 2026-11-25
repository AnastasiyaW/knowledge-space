---
title: "Contrôle de version avec Git"
category: concepts
tags: [devops, git, version-control, branching, github, gitflow]
level: 3
source_sha256: 28295dbf5226170298be0df88953fa2daeff2ca81e8467a9ddae3f02e86ca926
translation: machine
translated_at: '2026-10-24'
---
# Contrôle de version avec Git {#git-version-control}

Git est un système de contrôle de version distribué où chaque clone est un dépôt complet. Il est au cœur de tous les workflows DevOps, en tant que source de vérité pour le code et l'infrastructure.

## Workflow de base {#core-workflow}

```bash
git init                          # initialize
git clone URL                     # clone existing
git status                        # check changes
git add file.txt                  # stage specific file
git commit -m "message"           # commit
git push origin main              # push to remote
git pull origin main              # pull from remote
```

## Branches {#branching}

```bash
git branch feature-x              # create
git checkout -b feature-x         # create + switch
git merge feature-x               # merge into current
git branch -d feature-x           # delete local
git push origin feature-x         # push branch
```

## Historique et diff {#history-and-diff}

```bash
git log --oneline --graph         # compact graph
git diff                          # unstaged changes
git diff --staged                 # staged changes
git show commit-hash              # specific commit
```

## Annuler des modifications {#undoing-changes}

```bash
git checkout -- file              # discard unstaged
git reset HEAD file               # unstage
git reset --soft HEAD~1           # undo commit, keep changes
git reset --hard HEAD~1           # undo commit, discard changes
git revert commit-hash            # new commit undoing target
git stash / git stash pop         # temporary save/restore
```

## Stratégies de branchement {#branching-strategies}

### GitHub Flow {#github-flow}

- `main` toujours déployable
- Branches de fonctionnalités créées à partir de main
- Fusion via pull request après revue
- Déploiement après fusion
- Idéal pour : produits à version unique, sites web

### Git Flow {#git-flow}

- `main` (production) + `develop` (développement actif)
- Branches de fonctionnalités -> develop
- Branches de release pour la préparation de version
- Branches de hotfix pour les correctifs urgents
- Idéal pour : plusieurs versions simultanées

### Forking Workflow {#forking-workflow}

- Forker le dépôt, travailler dans le fork
- PR du fork vers le dépôt d'origine
- Idéal pour : open source, grandes équipes

## Monorepo vs Multirepo {#monorepo-vs-multirepo}

- **Monorepo** - tous les services dans un seul dépôt. Dépendances plus simples, refactoring transversal facilité. Risque : taille, performances
- **Multirepo** - dépôts séparés. Meilleure isolation, releases indépendantes. Risque : modifications inter-dépôts plus difficiles

### Submodules Git {#git-submodules}

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

## Fonctionnement interne {#internals}

- **Objets** : blobs (contenu), trees (répertoires), commits (instantanés)
- **HEAD** : pointeur vers le commit/la branche courant(e)
- **Index** : zone de préparation entre le répertoire de travail et le dépôt
- `.git/` contient toutes les données

## Pièges courants {#gotchas}

- `latest` n'est qu'une convention de nommage de tag, sans statut particulier pour Git
- `git reset --hard` est destructif, il est difficile de revenir en arrière
- Les submodules nécessitent une initialisation/mise à jour explicite après le clone
- `.gitignore` n'affecte que les fichiers non suivis : les fichiers déjà suivis nécessitent `git rm --cached`

## Voir aussi {#see-also}

- [[cicd-pipelines]] - Git déclenche le CI/CD
- [[gitops-and-argocd]] - Git comme source de vérité pour l'infra
- [[deployment-strategies]] - les branches pilotent les releases
