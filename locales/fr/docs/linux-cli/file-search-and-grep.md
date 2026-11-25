---
title: "Recherche de fichiers avec find et grep"
category: reference
tags: [linux-cli, find, grep, locate, search]
level: 3
source_sha256: 8a690c90536f33649bae622778ed4f013887ecfc7ca19c2a68415a83dbb7127e
translation: machine
translated_at: '2026-10-24'
---
# Recherche de fichiers avec find et grep {#file-search-and-grep}

Rechercher des fichiers par nom ou attributs avec `find`, rechercher dans le contenu des fichiers avec `grep`, et effectuer des recherches rapides avec `locate`. Ces outils constituent le socle de l'exploration du système de fichiers et de l'analyse des journaux.

## find - Rechercher par attributs de fichier {#find-search-by-file-attributes}

```bash
find [path] [options] [expression]
```

### Correspondance de nom {#name-matching}

```bash
find . -name "file.txt"         # exact name (case-sensitive)
find . -iname "file.txt"        # case-insensitive
find . -name "*.txt"            # wildcard: all .txt files
find . -name "report??"         # ? = exactly one character
find ~ -name "*.sh"             # search in home directory
find /var/log -name "*.log"     # search specific directory
```

### Filtrage par type {#type-filtering}

```bash
find . -type f                  # regular files only
find . -type d                  # directories only
find . -type l                  # symbolic links only
```

### Filtrage par taille {#size-filtering}

```bash
find . -size +10k               # larger than 10 KB
find . -size -1M                # smaller than 1 MB
find . -size +100M              # larger than 100 MB
```

Suffixes de taille : `c` (octets), `k` (Ko), `M` (Mo), `G` (Go)

### Contrôle de la profondeur {#depth-control}

```bash
find ~ -maxdepth 1              # only in target dir
find ~ -maxdepth 2              # target + one level of subdirs
```

### Conditions combinées {#combined-conditions}

```bash
find . -type f -name "*.sh"     # .sh files only
find . -size +10k -name "*.log" # .log files > 10 KB
```

### Exécuter des actions sur les résultats {#execute-actions-on-results}

```bash
find . -name "*.tmp" -delete              # delete matches
find . -name "*.sh" -exec chmod +x {} \;  # chmod each found file
```

## grep - Rechercher dans le contenu des fichiers {#grep-search-file-contents}

```bash
grep [options] "pattern" [file_or_path]
```

### Options courantes {#common-flags}

| Option | Signification |
|------|---------|
| `-r` | Recherche récursive |
| `-i` | Insensible à la casse |
| `-n` | Afficher les numéros de ligne |
| `-v` | Inverser la correspondance (lignes ne correspondant PAS) |
| `-l` | Afficher uniquement les noms de fichiers |
| `-c` | Compter les lignes correspondantes |
| `-E` | Expressions régulières étendues (identique à `egrep`) |
| `--include="*.py"` | Filtrer par type de fichier |

### Exemples {#examples}

```bash
grep "error" file.txt                          # single file
grep -r "error" /var/log/                      # recursive in directory
grep -rin "error" .                            # recursive, case-insensitive, line numbers
grep -rin --include="*.py" "error" .           # only Python files
grep -v root /etc/passwd                       # lines NOT containing "root"
```

### Filtrage par pipeline {#pipeline-filtering}

```bash
cat /var/log/syslog | grep 'ssh' | grep -v root
cat file | grep 'pattern' | wc -l             # count matching lines
command | grep 'keyword'                       # filter any command output
```

## Autres outils de recherche {#other-search-tools}

### locate - Recherche rapide dans la base de données {#locate-fast-database-search}

```bash
locate filename         # find by name (faster than find)
updatedb                # rebuild database (run as root)
```

Remarque : `locate` utilise une base de données pré-construite qui peut être obsolète. Exécutez `updatedb` pour la rafraîchir.

### whereis - Trouver le binaire et la documentation {#whereis-find-binary-and-docs}

```bash
whereis ls              # binary + man pages
whereis python3         # find Python 3 paths
```

### which - Trouver un exécutable dans PATH {#which-find-executable-in-path}

```bash
which python3           # /usr/bin/python3
which bash              # /bin/bash
```

## Modèles d'utilisation {#patterns}

### Trouver les gros fichiers {#find-large-files}

```bash
find / -type f -size +500M -exec ls -lh {} \;
```

### Rechercher et remplacer dans les fichiers {#search-and-replace-in-files}

```bash
grep -rl "old_text" . | xargs sed -i 's/old_text/new_text/g'
```

### Trouver les fichiers modifiés récemment {#find-recently-modified-files}

```bash
find . -type f -mtime -1         # modified in last 24 hours
find . -type f -mmin -60         # modified in last 60 minutes
```

## Pièges à éviter {#gotchas}

- Les jokers de `find` doivent être entre guillemets (`"*.txt"`), sinon le shell les développe avant que find ne les voie
- `locate` peut renvoyer des résultats périmés si la base de données est ancienne : exécutez toujours `updatedb` au préalable
- `grep -r` suit les liens symboliques par défaut : utilisez `-R` (majuscule) pour ne pas les suivre sur certains systèmes
- `find . -name ???` correspond à tout nom de fichier de 3 caractères (et pas seulement aux chiffres)
- Redirigez stderr lors d'une recherche depuis la racine : `find / -name "file" 2>/dev/null`

## Voir aussi {#see-also}

- [[text-processing]] - awk, sed, sort, uniq pour post-traiter les résultats de recherche
- [[io-redirection-and-pipes]] - Envoyer la sortie de grep vers d'autres commandes par pipe
- [[logging-and-journald]] - Rechercher efficacement dans les fichiers journaux
