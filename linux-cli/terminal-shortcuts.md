---
title: Terminal Keyboard Shortcuts
category: reference
tags: [shortcuts, keyboard, hotkeys, terminal, productivity]
---
# Terminal Keyboard Shortcuts

Essential keyboard shortcuts for efficient terminal navigation and editing.

## Key Facts

- Shortcuts work in bash and most readline-based shells
- Navigation shortcuts move the cursor without arrow keys (faster for touch typists)
- History shortcuts allow re-running and searching previous commands
- `Ctrl+C` sends SIGINT (interrupt) to running [[process-management]] processes
- `Ctrl+Z` suspends the current foreground process (resume with `fg` or `bg`)
- `Ctrl+D` sends EOF (end of file) - exits shell or ends input to [[file-viewing]] `cat >`
- `Tab` auto-completes commands and file paths; double-Tab shows all options
- These shortcuts are part of GNU Readline, used in bash, python REPL, and many CLI tools

## Patterns

### Navigation
```
Ctrl+A         Move to start of line
Ctrl+E         Move to end of line
Ctrl+F         Move forward one character
Ctrl+B         Move backward one character
Alt+F          Move forward one word
Alt+B          Move backward one word
Ctrl+XX        Toggle between current position and start of line
```

### Editing
```
Ctrl+U         Delete from cursor to start of line
Ctrl+K         Delete from cursor to end of line
Ctrl+W         Delete word before cursor
Alt+D          Delete word after cursor
Ctrl+D         Delete character under cursor
Ctrl+H         Delete character before cursor (backspace)
Ctrl+Y         Paste (yank) last deleted text
Alt+U          Undo last edit
```

### Process Control
```
Ctrl+C         Kill (interrupt) current process
Ctrl+Z         Suspend current process (use 'fg' to resume)
Ctrl+D         Exit shell / end input (EOF)
Ctrl+S         Freeze terminal output (XOFF)
Ctrl+Q         Resume terminal output (XON)
Ctrl+L         Clear screen (same as 'clear' command)
```

### History
```
Ctrl+R         Reverse search through history
Ctrl+P / Up    Previous command
Ctrl+N / Down  Next command
!!             Re-run last command
!$             Last argument of previous command
!abc           Run most recent command starting with 'abc'
^old^new       Replace 'old' with 'new' in last command and run
history -c     Clear command history
```

### Auto-complete
```
Tab            Auto-complete command/path
Tab Tab        Show all possible completions
~Tab Tab       List all Linux users
```

## Gotchas

- `Ctrl+S` freezes terminal - looks like a hang; `Ctrl+Q` unfreezes; this catches many beginners
- `Ctrl+Z` does NOT kill the process - it stays suspended in memory; use `fg` to bring it back or `kill %1`
- `Ctrl+C` in the middle of typing clears the current line AND creates a new prompt
- `Ctrl+D` on an empty line exits the shell - can accidentally close SSH sessions
- History search with `Ctrl+R` matches anywhere in the command, not just the beginning

## See Also

- [[terminal-navigation]] - basic terminal commands
- [[text-editors]] - vim and nano have their own shortcut systems
- [[io-redirection-and-pipes]] - `Ctrl+D` sends EOF to stdin
- GNU Readline: https://www.gnu.org/software/readline/
