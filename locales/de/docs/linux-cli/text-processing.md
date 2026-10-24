---
title: "Textverarbeitungswerkzeuge"
category: reference
tags: [linux-cli, awk, sed, sort, uniq, cut, tr, text]
level: 3
source_sha256: 72c55f391efd1d026d96e4dfa78b3e3afe798fac18106113eae88aada94eb8c1
translation: machine
translated_at: '2026-10-24'
---
# Textverarbeitungswerkzeuge {#text-processing-tools}

Kommandozeilenprogramme zum Umwandeln, Filtern und Analysieren von Textdaten. Diese Werkzeuge lassen sich über Pipes zu leistungsfähigen Datenverarbeitungs-Pipelines verketten.

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

Entfernt nur **aufeinanderfolgende** doppelte Zeilen - für vollständiges Deduplizieren immer zuerst `sort` ausführen.

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

- `uniq` entfernt nur **benachbarte** Duplikate - vorher über `sort` leiten
- `sed -i` ändert Dateien direkt und ohne Rückgängig-Möglichkeit - vorher sichern oder `sed -i.bak` verwenden
- Die Feldnummerierung in `awk` beginnt bei `$1` (nicht bei `$0` - das ist die gesamte Zeile)
- `tr` liest nur von stdin - `< file` verwenden, nicht `tr 'a' 'b' file`
- `cut` kann Felder nicht neu anordnen - `cut -f3,1` gibt die Felder in ursprünglicher Reihenfolge (1,3) aus

## See Also {#see-also}

- [[file-search-and-grep]] - Suchen und Filtern von Inhalten
- [[io-redirection-and-pipes]] - Programme über Pipes verbinden
- [[bash-scripting]] - Verwendung dieser Werkzeuge in Skripten
