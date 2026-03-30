---
title: Text Editors - Vim and Nano
category: reference
tags: [vim, nano, editor, text]
---
# Text Editors - Vim and Nano

Terminal-based text editors for file editing on Linux systems.

## Key Facts

- **Vim** is the default editor in most Linux distributions
- **Nano** is more beginner-friendly with on-screen shortcut hints
- Vim has modal editing: Normal mode (navigation), Insert mode (typing), Visual mode (selection), Command mode (`:`)
- Vim is invoked as `vim file.txt` or `vi file.txt`; Nano as `nano file.txt`
- `vimtutor` - interactive Vim tutorial built into the system
- Nano backup on save: `nano -B file.txt`
- Both editors are essential for editing config files over [[ssh-remote-access]]
- [[file-permissions]] must allow write (`w`) for the user to save changes

## Patterns

### Vim Essential Commands

```
# Modes
i          - Enter insert mode (before cursor)
a          - Enter insert mode (after cursor)
Esc        - Return to normal mode
v          - Enter visual (selection) mode

# Save and Quit
:w         - Save (write)
:q         - Quit (fails if unsaved changes)
:wq        - Save and quit (one command)
:q!        - Quit without saving (force)

# Navigation (Normal mode)
h j k l    - Left, Down, Up, Right
w / b      - Next / previous word
0 / $      - Start / end of line
gg / G     - Top / bottom of file
:42        - Go to line 42
Ctrl+d     - Page down
Ctrl+u     - Page up

# Editing (Normal mode)
dd         - Delete (cut) entire line
yy         - Yank (copy) entire line
p          - Paste after cursor
u          - Undo
Ctrl+r     - Redo
x          - Delete character under cursor
o          - New line below, enter insert mode
O          - New line above, enter insert mode

# Search and Replace
/pattern   - Search forward
?pattern   - Search backward
n / N      - Next / previous match
:%s/old/new/g   - Replace all occurrences in file
:%s/old/new/gc  - Replace all with confirmation

# Visual mode
v          - Character selection
V          - Line selection
Ctrl+v     - Block (column) selection
d          - Delete selected
y          - Yank selected
```

### Nano Essential Commands

```
Ctrl+S     - Save file
Ctrl+O     - Save as (offer filename)
Ctrl+X     - Exit nano
Ctrl+K     - Cut line
Ctrl+U     - Paste
Alt+6      - Copy line
Ctrl+W     - Search forward
Alt+R      - Find and replace
Ctrl+G     - Help
Alt+U      - Undo
Alt+E      - Redo
Ctrl+A     - Go to start of line
Ctrl+E     - Go to end of line
Alt+G      - Go to line number
Alt+N      - Toggle line numbers
```

## Gotchas

- Pressing `i` in Vim normal mode enters insert mode - many beginners type random text because they forget to press `i` first
- `:wq` and `:qw` are NOT the same - `:qw` is invalid
- If Vim seems unresponsive, you may have pressed `Ctrl+S` (terminal freeze) - press `Ctrl+Q` to resume
- `chmod u+x` is `chmod`, NOT `chown` - common typo when making scripts executable before editing
- Default editor for `crontab -e`, `visudo`, `git commit` is determined by `$EDITOR` or `$VISUAL` env vars

## See Also

- [[file-viewing]] - read-only file viewing commands
- [[bash-scripting]] - writing scripts that you edit with these editors
- [[file-permissions]] - making scripts executable after editing
- Vim documentation: https://vimhelp.org/
- Nano documentation: https://www.nano-editor.org/docs.php
