---
title: "Prozessverwaltung"
category: reference
tags: [linux-cli, processes, signals, kill, ps, top, htop]
level: 3
source_sha256: 33c9daab4d53e4ae6d892e4f0fef4e8eae39b20a192c1f081ee381deb97e89e1
translation: machine
translated_at: '2026-10-24'
---
# Prozessverwaltung {#process-management}

Ein Prozess ist ein laufendes Programm mit PID, Zustand, Priorität und Ressourcenzuweisung. Dieser Eintrag behandelt das Anzeigen, Filtern und Steuern von Prozessen, was für Systemadministration und Fehlersuche unverzichtbar ist.

## Wichtige Fakten {#key-facts}

- Jeder Prozess hat eine PID (Process ID) und eine PPID (Parent Process ID)
- PID 1 ist der init- bzw. systemd-Prozess und der Elternprozess aller anderen
- **Daemon** = Hintergrundprozess (Systemdienst)
- **Thread** = Ausführungseinheit innerhalb eines Prozesses, teilt sich dessen Speicherbereich

## Prozesszustände {#process-states}

| Zustand | Symbol | Beschreibung |
|---------|--------|--------------|
| Running | R | Wird aktiv ausgeführt oder ist ausführbereit |
| Sleeping (interruptible) | S | Wartet auf ein Ereignis, kann unterbrochen werden |
| Sleeping (uninterruptible) | D | Wartet auf I/O, kann nicht unterbrochen werden |
| Stopped | T | Angehalten (Ctrl+Z oder Signal) |
| Zombie | Z | Beendet, aber der Elternprozess hat den Exit-Status noch nicht abgeholt |

## ps - Prozess-Snapshot {#ps-process-snapshot}

```bash
ps                          # processes in current terminal
ps aux                      # all processes, full info (BSD syntax)
ps -ef                      # all processes (UNIX syntax)
ps afx                      # process tree
ps -u username              # processes for specific user
ps -T -p PID                # show threads of a process
ps 1                        # info for PID 1
```

### Spalten von ps aux {#ps-aux-columns}

```text
USER  PID  %CPU  %MEM  VSZ  RSS  TTY  STAT  START  TIME  COMMAND
```

- **VSZ**: Größe des virtuellen Speichers
- **RSS**: Resident Set Size (tatsächlich belegter RAM)
- **STAT**: Prozesszustand

## top - Interaktiver Monitor {#top-interactive-monitor}

```bash
top                     # default (sort by CPU%)
top -o PID              # sort by PID
top -u username         # filter by user
top -p PID1,PID2        # monitor specific PIDs
```

### Tasten in top {#inside-top}

| Taste | Aktion |
|-------|--------|
| q | Beenden |
| k | Prozess beenden |
| r | Renice (Priorität ändern) |
| M | Nach Speicherverbrauch sortieren |
| P | Nach CPU-Auslastung sortieren |
| 1 | Statistiken pro CPU ein-/ausblenden |
| u | Nach Benutzer filtern |

### Load Average {#load-average}

Wird im Kopfbereich von top angezeigt: `load average: 0.15, 0.20, 0.18` (1, 5, 15 Minuten)

- Wert < CPU-Kerne = nicht überlastet
- Wert = Kerne = an der Kapazitätsgrenze
- Wert > Kerne = überlastet

## htop - Erweiterter Monitor {#htop-enhanced-monitor}

```bash
sudo apt install htop
htop                    # visual CPU/memory bars, mouse support
htop -u username        # filter by user
```

## Prozesse finden {#finding-processes}

```bash
pidof firefox           # PID by exact name
pgrep pattern           # PIDs matching pattern
pgrep -la nginx         # PIDs + full command lines
```

## Signale {#signals}

```bash
kill PID                # SIGTERM (graceful, default)
kill -9 PID             # SIGKILL (force, immediate)
kill -15 PID            # SIGTERM explicitly
kill -1 PID             # SIGHUP (reload config)
killall processname     # kill all by name
pkill pattern           # kill by pattern
kill -l                 # list all signals
```

| Signal | Nummer | Beschreibung |
|--------|--------|--------------|
| SIGHUP | 1 | Hangup / Konfiguration neu laden |
| SIGINT | 2 | Unterbrechung (Ctrl+C) |
| SIGQUIT | 3 | Beenden mit Core Dump |
| SIGKILL | 9 | Erzwungenes Beenden (kann nicht abgefangen werden) |
| SIGTERM | 15 | Geordnetes Beenden |
| SIGSTOP | 19 | Anhalten (kann nicht abgefangen werden) |
| SIGCONT | 18 | Angehaltenen Prozess fortsetzen |

## Prozesspriorität (nice) {#process-priority-nice}

Bereich: -20 (höchste Priorität) bis +19 (niedrigste).

```bash
nice -n 10 command      # start with lower priority
renice -n 5 -p PID      # change running process priority
```

## Prozesserzeugung {#process-creation}

1. Dem Prozess wird ein Name zugewiesen
2. Der Prozess wird in die Prozessliste aufgenommen
3. Die Priorität wird bestimmt
4. Der Process Control Block (PCB) wird angelegt
5. Ressourcen werden zugewiesen

### Prozessattribute {#process-attributes}

| Attribut | Beschreibung |
|----------|--------------|
| `pid` | Process ID |
| `ppid` | Parent Process ID |
| `fd` | Geöffnete Dateideskriptoren |
| `cwd` | Aktuelles Arbeitsverzeichnis |
| `environ` | Umgebungsvariablen |
| `nice` | Prioritätswert |

## Fallstricke {#gotchas}

- `kill -9` sollte die letzte Option sein, denn der Prozess kann nicht aufräumen (temporäre Dateien, Sperren, Sockets)
- Zombie-Prozesse lassen sich nicht beenden, da sie bereits tot sind; stattdessen den Elternprozess beenden
- Die Load Average in `top` berücksichtigt auch Prozesse im Zustand D (wartend auf I/O)
- `killall` beendet unter Solaris ALLE Prozesse, unter Linux dagegen anhand des Namens (in gemischten Umgebungen vorsichtig sein)
- Hintergrundprozesse mit `&` werden beendet, sobald das Terminal geschlossen wird; hier helfen `nohup` oder `disown`

## Siehe auch {#see-also}

- [[systemd-and-services]] - Dienstverwaltung mit systemctl
- [[monitoring-and-performance]] - Überwachung der Systemressourcen
- [[linux-kernel-and-boot]] - Kernel, init, Lebenszyklus von Prozessen
