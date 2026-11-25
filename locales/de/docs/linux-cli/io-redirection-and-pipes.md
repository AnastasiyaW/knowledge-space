---
title: "I/O-Umleitung und Pipes"
category: concepts
tags: [linux-cli, redirection, pipes, stdin, stdout, stderr]
level: 3
source_sha256: 3fb685db844db4f00b2137b3c700f5148be9f4a33ab794094fa1f64f76cc3291
translation: machine
translated_at: '2026-10-24'
---
# I/O-Umleitung und Pipes {#io-redirection-and-pipes}

Jeder Prozess unter Linux verfügt über drei Standardströme: stdin (0), stdout (1) und stderr (2). Die Umleitung leitet diese Ströme in Dateien um, und Pipes verketten Befehle miteinander. Dieses Konzept ist grundlegend für sicheren Umgang mit der Shell.

## Standardströme {#standard-streams}

| Stream | FD | Standard | Beschreibung |
|--------|------|---------|-------------|
| stdin | 0 | Tastatur | Standardeingabe |
| stdout | 1 | Terminal | Standardausgabe |
| stderr | 2 | Terminal | Standardfehlerausgabe |

## Umleitungsoperatoren {#redirection-operators}

```bash
command > file          # stdout to file (overwrite)
command >> file         # stdout to file (append)
command 2> file         # stderr to file
command 2>> file        # stderr to file (append)
command < file          # file as stdin
command > /dev/null     # discard stdout
```

### Kombinieren von Strömen {#combining-streams}

```bash
command 1> out.txt 2> err.txt       # stdout and stderr to separate files
command 1> all.txt 2>&1             # both to same file
command &> all.txt                  # shorthand for above (bash)
command > /dev/null 2>&1            # discard all output
```

### Beispiele {#examples}

```bash
echo "text" > file.txt              # write to file
echo "text" >> file.txt             # append to file
echo "error" >&2                    # send to stderr
cat > file.txt                      # type from keyboard into file (Ctrl+D to end)
find / -name "*.sh" > found.txt 2> errors.txt  # separate stdout/stderr
```

## Pipes {#pipes}

Die stdout-Ausgabe eines Befehls als stdin an den nächsten senden:

```bash
command1 | command2                 # basic pipe
cat file.txt | grep "error"        # filter output
ls -la | less                      # page through output
cat file | grep 'pattern' | wc -l  # count matches
command | tee file.txt              # pipe AND write to file simultaneously
```

## Befehlsverkettung {#command-chaining}

```bash
cmd1 && cmd2    # run cmd2 ONLY if cmd1 succeeds (exit 0)
cmd1 || cmd2    # run cmd2 ONLY if cmd1 fails (non-zero)
cmd1 ; cmd2     # run cmd2 regardless of cmd1 result
```

### Praktische Beispiele {#practical-examples}

```bash
mkdir testdir && touch testdir/file    # create dir then file in it
ls ~/dir || mkdir ~/dir                # list or create if missing
cat file.txt || echo "error reading"   # print or report error
head file.txt && echo "Done"           # print then confirm
```

## Exit-Codes {#exit-codes}

```bash
echo $?        # last command's exit code
exit 0         # success
exit 1         # general error
exit 2         # misuse of builtins
```

Konvention: **0 = Erfolg**, ungleich 0 = Fehler.

```bash
command && echo "success" || echo "failed"
```

## Muster {#patterns}

### Nur Fehler protokollieren {#log-errors-only}

```bash
command 2>&1 | grep -i error
```

### Ausgabe erfassen und anzeigen {#capture-output-and-display}

```bash
command | tee output.log    # show on screen AND save to file
command 2>&1 | tee -a combined.log  # append both streams to log
```

### Stille Ausführung {#silent-execution}

```bash
command > /dev/null 2>&1    # completely silent
```

## Stolperfallen {#gotchas}

- `>` überschreibt ohne Warnung - verwende `>>`, um anzuhängen
- Die Reihenfolge bei `2>&1` ist wichtig: `cmd > file 2>&1` funktioniert, `cmd 2>&1 > file` bewirkt nicht dasselbe
- Pipes verbinden nur stdout - stderr geht weiterhin ins Terminal, sofern es nicht umgeleitet wird
- `|` erzeugt eine Subshell - innerhalb einer Pipe gesetzte Variablen bleiben außerhalb nicht erhalten
- `tee` eignet sich gut zum Debuggen von Pipes: Einfügen, um Zwischendaten sichtbar zu machen

## Siehe auch {#see-also}

- [[bash-scripting]] - Umleitung in Skripten verwenden
- [[text-processing]] - Werkzeuge, die häufig in Pipelines eingesetzt werden
- [[terminal-basics]] - Grundlagen der Shell
