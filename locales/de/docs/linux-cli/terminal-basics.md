---
title: "Terminal-Grundlagen"
category: concepts
tags: [linux-cli, terminal, shell, keyboard-shortcuts]
level: 2
source_sha256: 226bc3671504aef21c85fa492a266bbc9b01ec5c68d78f43fae2757cbe7b4d52
translation: machine
translated_at: '2026-10-24'
---
# Terminal-Grundlagen {#terminal-basics}

Das Terminal (Terminal-Emulator) stellt ein Fenster bereit, in dem man mit der Shell interagieren kann, dem Kommandozeileninterpreter, der Benutzereingaben an den OS-Kernel weitergibt. Dieser Eintrag behandelt Shell-Typen, grundlegende Befehle und Tastenkürzel für eine effiziente Nutzung des Terminals.

## Wichtige Fakten {#key-facts}

- Die **Shell** interpretiert Befehle; das **Terminal** ist das grafische Fenster, in dem die Shell läuft
- Standard-Shell auf den meisten Linux-Distributionen: **bash** (Bourne Again Shell)
- Verfügbare Shells: sh, bash, dash, zsh, fish
- Das Linux-Dateisystem unterscheidet **Groß- und Kleinschreibung**: `File.txt` und `file.txt` sind verschiedene Dateien
- Standard-Port für SSH: **22**

## Shell-Typen {#shell-types}

| Shell | Hinweise |
|-------|----------|
| **sh** (Bourne) | POSIX-Standard, einfach |
| **bash** | Am weitesten verbreitet, Standard auf den meisten Distributionen, erweitert sh |
| **dash** | Schlanke POSIX-Shell, Standard-`/bin/sh` auf Ubuntu, schneller Start |
| **zsh** | Gemeinsame History, erweiterte Arrays, Rechtschreibkorrektur, Plugins (Oh My Zsh) |
| **fish** | Syntax-Highlighting, schnelle History-Suche, Web-Konfigurator |

```bash
echo $SHELL         # current shell path
echo $0             # current shell name
cat /etc/shells     # all available shells
chsh -s /bin/zsh    # change default login shell
```

Shell-Konfigurationsdateien:
- bash: `~/.bashrc` (interaktiv), `~/.bash_profile` (Login), `~/.bash_logout`
- zsh: `~/.zshrc`
- Global: `/etc/profile`, `/etc/bash.bashrc`

## Die ersten wichtigen Befehle {#essential-first-commands}

```bash
pwd             # print working directory
whoami          # print current username
clear           # clear screen (also Ctrl+L)
reset           # reset terminal to default state
history         # show command history
history -c      # clear history

# Getting help
man command     # full manual page
command --help  # brief usage info
whatis command  # one-line description
apropos keyword # search help by keyword
info command    # info page (alternative to man)
```

## Navigation {#navigation}

```bash
cd /path/to/dir   # absolute path
cd ~              # home directory (also just cd)
cd ..             # one level up
cd -              # previous directory
ls                # list contents
ls -l             # long format (permissions, size, date)
ls -a             # show hidden files (starting with .)
ls -la            # long + hidden
tree              # display directory tree
```

## Tastenkürzel – Navigation {#keyboard-shortcuts-navigation}

| Tastenkürzel | Aktion |
|--------------|--------|
| Ctrl+A | An den Zeilenanfang springen |
| Ctrl+E | An das Zeilenende springen |
| Alt+F | Ein Wort vorwärts springen |
| Alt+B | Ein Wort rückwärts springen |
| Ctrl+XX | Zwischen Zeilenanfang und aktueller Position wechseln |

## Tastenkürzel – Bearbeiten {#keyboard-shortcuts-editing}

| Tastenkürzel | Aktion |
|--------------|--------|
| Ctrl+U | Vom Cursor bis zum Zeilenanfang löschen |
| Ctrl+K | Vom Cursor bis zum Zeilenende löschen |
| Ctrl+W | Wort vor dem Cursor löschen |
| Alt+D | Vom Cursor bis zum Wortende löschen |
| Ctrl+D | Zeichen unter dem Cursor löschen |
| Alt+. | Letztes Argument des vorherigen Befehls einfügen |

## Tastenkürzel – Prozesssteuerung {#keyboard-shortcuts-process-control}

| Tastenkürzel | Aktion |
|--------------|--------|
| Ctrl+C | Aktuellen Befehl beenden (SIGINT) |
| Ctrl+Z | Aktuellen Befehl anhalten (Hintergrund) |
| Ctrl+D | Terminal schließen / EOF senden |
| Ctrl+L | Bildschirm leeren |
| Ctrl+S | Bildschirmausgabe anhalten |
| Ctrl+Q | Ausgabe fortsetzen |

## Tastenkürzel – History {#keyboard-shortcuts-history}

| Tastenkürzel | Aktion |
|--------------|--------|
| Ctrl+R | Inkrementelle Rückwärtssuche in der History |
| Up / Ctrl+P | Vorheriger Befehl |
| Down / Ctrl+N | Nächster Befehl |
| !! | Letzten Befehl ausführen |
| !x | Letzten Befehl ausführen, der mit x beginnt |
| ^alt^neu | Im letzten Befehl alt durch neu ersetzen |

## Linux beschaffen {#getting-linux}

- **WSL** (Windows 10+): beste Option für Windows-Nutzer, Installation über den Microsoft Store
- **VirtualBox**: beliebige Distribution als VM (mind. 2 GB RAM, mind. 20 GB Speicher)
- **Cloud-VPS**: Verbindung über SSH
- **macOS**: nativer Unix-Terminal, `brew` als Paketmanager verwenden

## Stolperfallen {#gotchas}

- `cd` ohne Argumente wechselt nach `~` (Home-Verzeichnis), nicht nach `/`
- `Ctrl+S` friert die Terminalausgabe ein – mit `Ctrl+Q` wird sie wieder freigegeben (typischer Panikmoment)
- `history -c` leert die History im Arbeitsspeicher, nicht aber die Datei `~/.bash_history` – mit `history -c && history -w` werden beide gelöscht
- Die Tab-Vervollständigung ist kontextabhängig: Ein Tab vervollständigt, ein doppelter Tab zeigt alle Optionen an

## Siehe auch {#see-also}

- [[bash-scripting]] - Grundlagen der Shell-Programmierung
- [[io-redirection-and-pipes]] - stdin/stdout/stderr und Pipes
- [[wsl]] - Windows-Subsystem für Linux
