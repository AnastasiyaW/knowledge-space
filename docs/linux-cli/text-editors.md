---
title: Terminal Text Editors
category: reference
tags: [linux-cli, vim, nano, editors]
---

# Terminal Text Editors

nano is beginner-friendly; vim is the power-user standard found on virtually every Linux system. This entry covers essential shortcuts and commands for both editors.

## Nano

Launch: `nano filename` or `nano -B filename` (create backup on save).

### File Operations

| Shortcut | Action |
|----------|--------|
| Ctrl+S | Save |
| Ctrl+O | Save as |
| Ctrl+X | Exit |
| Ctrl+R | Insert file |

### Editing

| Shortcut | Action |
|----------|--------|
| Ctrl+K | Cut line |
| Alt+6 | Copy line |
| Ctrl+U | Paste |
| Alt+U | Undo |
| Alt+E | Redo |
| Alt+3 | Comment/uncomment |

### Search

| Shortcut | Action |
|----------|--------|
| Ctrl+W | Search forward |
| Ctrl+Q | Search backward |
| Alt+R | Search and replace |
| Alt+W | Find next |

### Navigation

| Shortcut | Action |
|----------|--------|
| Ctrl+A / Ctrl+E | Start / end of line |
| Ctrl+Y / Ctrl+V | Page up / page down |
| Alt+\ / Alt+/ | Top / bottom of file |
| Alt+G | Go to line number |
| Alt+N | Toggle line numbers |

## Vim

Modal editor with three main modes: **Normal**, **Insert**, **Visual**.

### Mode Switching

```
i           Insert at cursor
a           Insert after cursor
I / A       Insert at line start / end
o / O       New line below / above, enter insert
Esc         Return to Normal mode
v           Visual mode (character)
V           Visual mode (line)
Ctrl+v      Visual block mode
```

### Cursor Movement (Normal)

```
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

### Editing (Normal)

```
dd          Delete (cut) line
d$          Delete to end of line
dw          Delete word
cc          Change (delete + insert) line
J           Join line below
r[char]     Replace single character
.           Repeat last command
x           Delete character under cursor
```

### Text Objects

```
di(         Delete inside parentheses
ci"         Change inside quotes
da{         Delete around braces (including braces)
yi[         Yank inside brackets
```

### Clipboard

```
yy          Yank (copy) line
p / P       Paste after / before cursor
```

### Save and Exit

```
:w          Save
:wq         Save and quit
:q          Quit (fails if unsaved)
:q!         Force quit without saving
```

### Search and Replace

```
/pattern    Search forward
?pattern    Search backward
n / N       Next / previous match
:%s/old/new/g    Replace all in file
:%s/old/new/gc   Replace with confirmation
```

### Undo / Redo

```
u           Undo
Ctrl+r      Redo
```

### Windows and Tabs

```
:e file     Open file
:tabe       New tab
gt / gT     Next / previous tab
:vsp        Vertical split
Ctrl+ww     Switch between windows
Ctrl+wq     Close window
```

### Marks

```
m{a-z}      Set local mark
'{a-z}      Jump to mark
''          Return to previous position
```

## Gotchas

- Vim starts in Normal mode - pressing letters executes commands, not typing text
- `:q!` discards all changes without confirmation
- nano shows keyboard shortcuts at the bottom (`^` means Ctrl)
- Vim is pre-installed on nearly all Linux systems; nano may need to be installed
- `vi` on many systems is actually `vim` (Vi IMproved)
- In vim, `u` undoes one change at a time; `U` undoes all changes on current line

## See Also

- [[terminal-basics]] - Shell and keyboard shortcuts
- [[file-operations]] - File creation and viewing
