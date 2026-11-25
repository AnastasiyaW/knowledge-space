---
title: "Dateioperationen"
category: reference
tags: [linux-cli, files, directories, cp, mv, rm, mkdir]
level: 3
source_sha256: ccec64b01959176aa053d437c53069c6a8a1985ac80688d365351fedf1f146b3
translation: machine
translated_at: '2026-10-24'
---
# Dateioperationen {#file-operations}

Grundlegende Befehle zum Erstellen, Kopieren, Verschieben, Löschen und Anzeigen von Dateien und Verzeichnissen. Dies sind die Bausteine der täglichen Arbeit auf der Linux-Kommandozeile.

## Wichtige Fakten {#key-facts}

- `rm` kennt keinen Papierkorb – Dateien sind dauerhaft verloren
- `cp -r` ist für Verzeichnisse erforderlich (rekursiv)
- `mv` übernimmt sowohl das Verschieben als auch das Umbenennen
- `touch` erstellt leere Dateien oder aktualisiert die Zeitstempel vorhandener Dateien

## Erstellen {#create}

```bash
touch filename             # create empty file or update timestamp
touch f1 f2 f3             # create multiple files
mkdir dirname              # create directory
mkdir -p dir/sub/sub2      # create nested directories (no error if exists)
```

## Kopieren {#copy}

```bash
cp src dst                 # copy file
cp -r src/ dst/            # copy directory recursively
cp -p file dst             # preserve permissions and timestamps
```

## Verschieben / Umbenennen {#move-rename}

```bash
mv src dst                 # move or rename file/directory
mv old.txt new.txt         # rename in place
mv file.txt /other/dir/    # move to another directory
```

## Löschen {#delete}

```bash
rm filename                # remove file
rm -r dirname/             # remove directory recursively
rm -rf dirname/            # force remove (no prompts)
rmdir dirname              # remove empty directory only (safe)
```

## Dateiinhalte anzeigen {#view-file-contents}

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

## In Dateien schreiben {#write-to-files}

```bash
echo "text" > file         # write (overwrite)
echo "text" >> file        # append
cat > file                 # type from keyboard (Ctrl+D to end)
cat >> file                # append from keyboard
```

## Muster {#patterns}

### Stapelweises Erstellen von Dateien {#batch-file-creation}

```bash
touch file{1..10}.txt      # creates file1.txt through file10.txt
mkdir -p project/{src,test,docs}  # create multiple subdirectories
```

### Sicheres rekursives Löschen {#safe-recursive-delete}

```bash
# Always double-check path before rm -rf
ls dir/                    # verify contents first
rm -ri dir/                # interactive mode - asks for each file
```

## Fallstricke {#gotchas}

- `rm -rf /` ist katastrophal – moderne Systeme erfordern `--no-preserve-root`, aber verwenden Sie es niemals
- `cp` ohne `-r` überspringt Verzeichnisse stillschweigend
- `mv` über Dateisystemgrenzen hinweg kopiert und löscht anschließend (langsamer als ein Verschieben innerhalb desselben Dateisystems)
- `rmdir` entfernt nur leere Verzeichnisse – verwenden Sie `rm -r` für nicht leere Verzeichnisse
- `>` überschreibt Dateien ohne Warnung; verwenden Sie `>>`, um anzuhängen
- `cat file.txt || echo error` – nützlich, um zu prüfen, ob eine Datei lesbar ist

## Siehe auch {#see-also}

- [[file-search-and-grep]] - Dateien finden und Inhalte durchsuchen
- [[text-processing]] - wc, sort, uniq, cut, awk, sed
- [[file-permissions]] - chmod, chown
- [[links-and-inodes]] - Harte und symbolische Links
