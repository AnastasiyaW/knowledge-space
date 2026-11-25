---
title: "Opérations sur les fichiers"
category: reference
tags: [linux-cli, files, directories, cp, mv, rm, mkdir]
level: 3
source_sha256: ccec64b01959176aa053d437c53069c6a8a1985ac80688d365351fedf1f146b3
translation: machine
translated_at: '2026-10-24'
---
# Opérations sur les fichiers {#file-operations}

Commandes essentielles pour créer, copier, déplacer, supprimer et afficher des fichiers et des répertoires. Ce sont les briques de base du travail quotidien en ligne de commande Linux.

## Points clés {#key-facts}

- `rm` n'a pas de corbeille : les fichiers sont supprimés définitivement
- `cp -r` est obligatoire pour les répertoires (récursif)
- `mv` gère à la fois le déplacement et le renommage
- `touch` crée des fichiers vides ou met à jour les horodatages de fichiers existants

## Créer {#create}

```bash
touch filename             # create empty file or update timestamp
touch f1 f2 f3             # create multiple files
mkdir dirname              # create directory
mkdir -p dir/sub/sub2      # create nested directories (no error if exists)
```

## Copier {#copy}

```bash
cp src dst                 # copy file
cp -r src/ dst/            # copy directory recursively
cp -p file dst             # preserve permissions and timestamps
```

## Déplacer / Renommer {#move-rename}

```bash
mv src dst                 # move or rename file/directory
mv old.txt new.txt         # rename in place
mv file.txt /other/dir/    # move to another directory
```

## Supprimer {#delete}

```bash
rm filename                # remove file
rm -r dirname/             # remove directory recursively
rm -rf dirname/            # force remove (no prompts)
rmdir dirname              # remove empty directory only (safe)
```

## Afficher le contenu d'un fichier {#view-file-contents}

```bash
cat file                   # print entire file
cat file1 file2            # concatenate and print
less file                  # page through (forward and backward)
more file                  # page through (forward only)
head file                  # first 10 lines
head -n 20 file            # first 20 lines
head -c 30 file            # first 30 bytes
tail file                  # last 10 lines
tail -n 20 file            # last 20 lines
tail -c 30 file            # last 30 bytes
tail -f file               # follow file in real time (logs)
```

## Écrire dans des fichiers {#write-to-files}

```bash
echo "text" > file         # write (overwrite)
echo "text" >> file        # append
cat > file                 # type from keyboard (Ctrl+D to end)
cat >> file                # append from keyboard
```

## Modèles d'usage {#patterns}

### Création de fichiers en lot {#batch-file-creation}

```bash
touch file{1..10}.txt      # creates file1.txt through file10.txt
mkdir -p project/{src,test,docs}  # create multiple subdirectories
```

### Suppression récursive sécurisée {#safe-recursive-delete}

```bash
# Always double-check path before rm -rf
ls dir/                    # verify contents first
rm -ri dir/                # interactive mode - asks for each file
```

## Pièges à éviter {#gotchas}

- `rm -rf /` est catastrophique : les systèmes modernes exigent `--no-preserve-root`, mais ne l'utilisez jamais
- `cp` sans `-r` ignore silencieusement les répertoires
- `mv` entre systèmes de fichiers copie puis supprime (plus lent qu'un déplacement au sein du même système de fichiers)
- `rmdir` ne supprime que les répertoires vides : utilisez `rm -r` pour un répertoire non vide
- `>` écrase le fichier sans avertissement ; utilisez `>>` pour ajouter du contenu à la fin
- `cat file.txt || echo error` : utile pour vérifier si un fichier est lisible

## Voir aussi {#see-also}

- [[file-search-and-grep]] - Recherche de fichiers et recherche dans le contenu
- [[text-processing]] - wc, sort, uniq, cut, awk, sed
- [[file-permissions]] - chmod, chown
- [[links-and-inodes]] - Liens physiques et liens symboliques
