---
title: "Dateisuche mit find und grep"
category: reference
tags: [linux-cli, find, grep, locate, search]
level: 3
source_sha256: 8a690c90536f33649bae622778ed4f013887ecfc7ca19c2a68415a83dbb7127e
translation: machine
translated_at: '2026-10-24'
---
Hmm, I need to be careful: the document's code placeholders are the only content I should produce, and I must output the translated document. Let me produce the translation.

---
title: Dateisuche mit find und grep
category: reference
tags: [linux-cli, find, grep, locate, search]
---

# Dateisuche mit find und grep {#file-search-and-grep}

Das Suchen von Dateien nach Name und Attributen mit `find`, das Durchsuchen von Dateiinhalten mit `grep` und schnelle Abfragen mit `locate`. Diese Werkzeuge bilden das Kernstück der Dateisystemerkundung und Log-Analyse.

## find - Suche nach Dateiattributen {#find-search-by-file-attributes}

```bash
find [path] [options] [expression]
```

### Namensabgleich {#name-matching}

```bash
find . -name "file.txt"         # exact name (case-sensitive)
find . -iname "file.txt"        # case-insensitive
find . -name "*.txt"            # wildcard: all .txt files
find . -name "report??"         # ? = exactly one character
find ~ -name "*.sh"             # search in home directory
find /var/log -name "*.log"     # search specific directory
```

### Typfilterung {#type-filtering}

```bash
find . -type f                  # regular files only
find . -type d                  # directories only
find . -type l                  # symbolic links only
```

### Größenfilterung {#size-filtering}

```bash
find . -size +10k               # larger than 10 KB
find . -size -1M                # smaller than 1 MB
find . -size +100M              # larger than 100 MB
```

Größensuffixe: `c` (Bytes), `k` (KB), `M` (MB), `G` (GB)

### Tiefensteuerung {#depth-control}

```bash
find ~ -maxdepth 1              # only in target dir
find ~ -maxdepth 2              # target + one level of subdirs
```

### Kombinierte Bedingungen {#combined-conditions}

```bash
find . -type f -name "*.sh"     # .sh files only
find . -size +10k -name "*.log" # .log files > 10 KB
```

### Aktionen auf Ergebnisse ausführen {#execute-actions-on-results}

```bash
find . -name "*.tmp" -delete              # delete matches
find . -name "*.sh" -exec chmod +x {} \;  # chmod each found file
```

## grep - Dateiinhalte durchsuchen {#grep-search-file-contents}

```bash
grep [options] "pattern" [file_or_path]
```

### Häufige Optionen {#common-flags}

| Option | Bedeutung |
|------|---------|
| `-r` | Rekursive Suche |
| `-i` | Groß-/Kleinschreibung ignorieren |
| `-n` | Zeilennummern anzeigen |
| `-v` | Treffer invertieren (Zeilen, die NICHT passen) |
| `-l` | Nur Dateinamen anzeigen |
| `-c` | Passende Zeilen zählen |
| `-E` | Erweiterte Regex (wie `egrep`) |
| `--include="*.py"` | Nach Dateityp filtern |

### Beispiele {#examples}

```bash
grep "error" file.txt                          # single file
grep -r "error" /var/log/                      # recursive in directory
grep -rin "error" .                            # recursive, case-insensitive, line numbers
grep -rin --include="*.py" "error" .           # only Python files
grep -v root /etc/passwd                       # lines NOT containing "root"
```

### Filtern über Pipelines {#pipeline-filtering}

```bash
cat /var/log/syslog | grep 'ssh' | grep -v root
cat file | grep 'pattern' | wc -l             # count matching lines
command | grep 'keyword'                       # filter any command output
```

## Weitere Suchwerkzeuge {#other-search-tools}

### locate - Schnelle Datenbanksuche {#locate-fast-database-search}

```bash
locate filename         # find by name (faster than find)
updatedb                # rebuild database (run as root)
```

Hinweis: `locate` nutzt eine vorgefertigte Datenbank, die veraltet sein kann. Mit `updatedb` lässt sie sich aktualisieren.

### whereis - Binärdateien und Dokumentation finden {#whereis-find-binary-and-docs}

```bash
whereis ls              # binary + man pages
whereis python3         # find Python 3 paths
```

### which - Ausführbare Datei im PATH finden {#which-find-executable-in-path}

```bash
which python3           # /usr/bin/python3
which bash              # /bin/bash
```

## Muster {#patterns}

### Große Dateien finden {#find-large-files}

```bash
find / -type f -size +500M -exec ls -lh {} \;
```

### Suchen und Ersetzen in Dateien {#search-and-replace-in-files}

```bash
grep -rl "old_text" . | xargs sed -i 's/old_text/new_text/g'
```

### Kürzlich geänderte Dateien finden {#find-recently-modified-files}

```bash
find . -type f -mtime -1         # modified in last 24 hours
find . -type f -mmin -60         # modified in last 60 minutes
```

## Stolperfallen {#gotchas}

- `find`-Platzhalter müssen in Anführungszeichen stehen (`"*.txt"`), sonst expandiert die Shell sie, bevor `find` sie sieht
- `locate` kann veraltete Ergebnisse liefern, wenn die Datenbank alt ist – daher immer zuerst `updatedb` ausführen
- `grep -r` folgt standardmäßig Symlinks – auf einigen Systemen `-R` (groß) verwenden, um Symlinks nicht zu folgen
- `find . -name ???` trifft jeden Dateinamen mit 3 Zeichen (nicht nur Ziffern)
- Stderr umleiten, wenn ab dem Wurzelverzeichnis gesucht wird: `find / -name "file" 2>/dev/null`

## Siehe auch {#see-also}

- [[text-processing]] - awk, sed, sort, uniq zur Nachbearbeitung von Suchergebnissen
- [[io-redirection-and-pipes]] - Weiterleiten der grep-Ausgabe an andere Befehle
- [[logging-and-journald]] - Effektives Durchsuchen von Logdateien
