---
title: "Outils de traitement de texte"
category: reference
tags: [linux-cli, awk, sed, sort, uniq, cut, tr, text]
level: 3
source_sha256: 72c55f391efd1d026d96e4dfa78b3e3afe798fac18106113eae88aada94eb8c1
translation: machine
translated_at: '2026-10-24'
---
# Outils de traitement de texte {#text-processing-tools}

Utilitaires en ligne de commande pour transformer, filtrer et analyser des données textuelles. Ces outils s'enchaînent via des tubes (pipes) pour former des pipelines de traitement de données puissants.

## wc - Word Count {#wc-word-count}

```bash
wc file.txt         # lines, words, bytes
wc -l file.txt      # count lines only
wc -w file.txt      # count words only
wc -c file.txt      # count bytes
cat file | wc -l    # count lines via pipe
```

## sort {#sort}

```bash
sort file.txt               # sort lines alphabetically
sort -r file.txt            # reverse order
sort -n file.txt            # numeric sort
sort -k2 file.txt           # sort by 2nd field
sort -t: -k3 -n /etc/passwd # sort by UID (field 3, colon delimiter)
sort -u file.txt            # sort and remove duplicates
```

## uniq {#uniq}

Supprime uniquement les lignes en double **consécutives** - toujours passer par `sort` d'abord pour une déduplication complète.

```bash
uniq file.txt               # remove consecutive duplicates
uniq -c file.txt            # prefix with occurrence count
uniq -d file.txt            # show only duplicates
sort file | uniq            # remove ALL duplicates
sort file | uniq -c | sort -rn  # frequency count (most common first)
```

## cut {#cut}

```bash
cut -d: -f1 /etc/passwd     # first field, colon delimiter
cut -d, -f2,4 file.csv      # 2nd and 4th fields, comma delimiter
cut -c1-10 file.txt         # first 10 characters per line
```

## awk {#awk}

```bash
awk '{print $1}' file              # print first column (whitespace-delimited)
awk -F: '{print $1}' /etc/passwd   # colon delimiter, print usernames
awk '{print NR, $0}' file          # line number + full line
awk '$3 > 1000' /etc/passwd        # filter where field 3 > 1000
awk '{sum += $1} END {print sum}' file  # sum first column
```

## sed - Stream Editor {#sed-stream-editor}

```bash
sed 's/old/new/' file           # replace first occurrence per line
sed 's/old/new/g' file          # replace all occurrences
sed -i 's/old/new/g' file       # in-place edit (modifies file)
sed -n '5,10p' file             # print lines 5-10 only
sed '/pattern/d' file           # delete lines matching pattern
sed 's/^/prefix/' file          # add prefix to each line
```

## tr - Translate Characters {#tr-translate-characters}

```bash
tr 'a-z' 'A-Z' < file          # lowercase to uppercase
tr -d '\r' < file.txt           # remove carriage returns (Windows line endings)
tr -s ' ' < file                # squeeze multiple spaces into one
```

## Patterns {#patterns}

### Top 10 Most Frequent Words {#top-10-most-frequent-words}

```bash
cat file | tr ' ' '\n' | sort | uniq -c | sort -rn | head -10
```

### Extract Usernames from passwd {#extract-usernames-from-passwd}

```bash
cut -d: -f1 /etc/passwd | sort
```

### CSV Column Sum {#csv-column-sum}

```bash
awk -F, '{sum += $3} END {print sum}' data.csv
```

### Remove Blank Lines {#remove-blank-lines}

```bash
sed '/^$/d' file
grep -v '^$' file    # alternative
```

### Find and Replace Across Files {#find-and-replace-across-files}

```bash
grep -rl "old" . | xargs sed -i 's/old/new/g'
```

## Gotchas {#gotchas}

- `uniq` ne supprime que les doublons **adjacents** - passer d'abord par `sort`
- `sed -i` modifie les fichiers sur place sans possibilité d'annulation - sauvegarder d'abord ou utiliser `sed -i.bak`
- La numérotation des champs `awk` commence à `$1` (et non `$0`, qui représente la ligne entière)
- `tr` lit uniquement depuis l'entrée standard - utiliser la redirection `< fichier`, et non `tr 'a' 'b' fichier`
- `cut` ne peut pas réordonner les champs - `cut -f3,1` affiche les champs dans l'ordre d'origine (1,3)

## See Also {#see-also}

- [[file-search-and-grep]] - Recherche et filtrage de contenu
- [[io-redirection-and-pipes]] - Enchaînement d'outils avec des tubes
- [[bash-scripting]] - Utiliser ces outils dans des scripts
