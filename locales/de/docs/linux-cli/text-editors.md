---
title: "Terminal-Texteditoren"
category: reference
tags: [linux-cli, vim, nano, editors]
level: 3
source_sha256: b0cd44fa78212fbecfecd1af8cce49095b7e1616ac2eefa2cd8b9b696b6e5c30
translation: machine
translated_at: '2026-10-24'
---
# Terminal-Texteditoren {#terminal-text-editors}

nano ist einsteigerfreundlich, vim ist der Standard für Power-User und auf praktisch jedem Linux-System vorhanden. Dieser Eintrag behandelt die wichtigsten Tastenkürzel und Befehle für beide Editoren.

## Nano {#nano}

Start: `nano filename` oder `nano -B filename` (erstellt beim Speichern ein Backup).

### Dateioperationen {#file-operations}

| Shortcut | Aktion |
|----------|--------|
| Ctrl+S | Speichern |
| Ctrl+O | Speichern unter |
| Ctrl+X | Beenden |
| Ctrl+R | Datei einfügen |

### Bearbeitung {#editing}

| Shortcut | Aktion |
|----------|--------|
| Ctrl+K | Zeile ausschneiden |
| Alt+6 | Zeile kopieren |
| Ctrl+U | Einfügen |
| Alt+U | Rückgängig |
| Alt+E | Wiederholen |
| Alt+3 | Kommentieren/Kommentar entfernen |

### Suche {#search}

| Shortcut | Aktion |
|----------|--------|
| Ctrl+W | Vorwärts suchen |
| Ctrl+Q | Rückwärts suchen |
| Alt+R | Suchen und ersetzen |
| Alt+W | Nächsten suchen |

### Navigation {#navigation}

| Shortcut | Aktion |
|----------|--------|
| Ctrl+A / Ctrl+E | Zeilenanfang / Zeilenende |
| Ctrl+Y / Ctrl+V | Seite hoch / Seite runter |
| Alt+\ / Alt+/ | Dateianfang / Dateiende |
| Alt+G | Zu Zeilennummer springen |
| Alt+N | Zeilennummern ein-/ausblenden |

## Vim {#vim}

Modaler Editor mit drei Hauptmodi: **Normal**, **Insert**, **Visual**.

### Moduswechsel {#mode-switching}

```sql
i           Insert at cursor
a           Insert after cursor
I / A       Insert at line start / end
o / O       New line below / above, enter insert
Esc         Return to Normal mode
v           Visual mode (character)
V           Visual mode (line)
Ctrl+v      Visual block mode
```

### Cursorbewegung (Normal) {#cursor-movement-normal}

```text
h j k l     Left, down, up, right
w / b       Next / previous word
0 / $       Start / end of line
^           First non-blank character
gg          Top of file
G           Bottom of file
:[num]      Go to line
Ctrl+d/u    Half page down / up
{ / }       Previous / next paragraph
```

### Bearbeitung (Normal) {#editing-normal}

```sql
dd          Delete (cut) line
d$          Delete to end of line
dw          Delete word
cc          Change (delete + insert) line
J           Join line below
r[char]     Replace single character
.           Repeat last command
x           Delete character under cursor
```

### Textobjekte {#text-objects}

```sql
di(         Delete inside parentheses
ci"         Change inside quotes
da{         Delete around braces (including braces)
yi[         Yank inside brackets
```

### Zwischenablage {#clipboard}

```text
yy          Yank (copy) line
p / P       Paste after / before cursor
```

### Speichern und Beenden {#save-and-exit}

```bash
:w          Save
:wq         Save and quit
:q          Quit (fails if unsaved)
:q!         Force quit without saving
```

### Suchen und Ersetzen {#search-and-replace}

```text
/pattern    Search forward
?pattern    Search backward
n / N       Next / previous match
:%s/old/new/g    Replace all in file
:%s/old/new/gc   Replace with confirmation
```

### Rückgängig / Wiederholen {#undo-redo}

```text
u           Undo
Ctrl+r      Redo
```

### Fenster und Tabs {#windows-and-tabs}

```text
:e file     Open file
:tabe       New tab
gt / gT     Next / previous tab
:vsp        Vertical split
Ctrl+ww     Switch between windows
Ctrl+wq     Close window
```

### Marken {#marks}

```text
m{a-z}      Set local mark
'{a-z}      Jump to mark
''          Return to previous position
```

## Stolperfallen {#gotchas}

- Vim startet im Normal-Modus. Buchstabentasten führen Befehle aus, statt Text einzugeben.
- `:q!` verwirft alle Änderungen ohne Rückfrage.
- nano zeigt die Tastenkürzel unten am Bildschirm an (`^` steht für Strg).
- Vim ist auf nahezu allen Linux-Systemen vorinstalliert, nano muss unter Umständen nachinstalliert werden.
- `vi` ist auf vielen Systemen tatsächlich `vim` (Vi IMproved).
- In vim macht `u` jeweils eine Änderung rückgängig, `U` macht alle Änderungen in der aktuellen Zeile rückgängig.

## Siehe auch {#see-also}

- [[terminal-basics]] - Shell und Tastenkürzel
- [[file-operations]] - Dateien erstellen und anzeigen
