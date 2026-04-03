---
title: Terminal Basics
category: concepts
tags: [linux-cli, terminal, shell, keyboard-shortcuts]
---

# Terminal Basics

The terminal (terminal emulator) provides a window to interact with the shell - the command-line interpreter that passes user input to the OS kernel. This entry covers shell types, essential commands, and keyboard shortcuts for efficient terminal usage.

## Key Facts

- The **shell** interprets commands; the **terminal** is the GUI window hosting the shell
- Default shell on most Linux distros: **bash** (Bourne Again Shell)
- Shells available: sh, bash, dash, zsh, fish
- Linux filesystem is **case-sensitive**: `File.txt` and `file.txt` are different files
- SSH default port: **22**

## Shell Types

| Shell | Notes |
|-------|-------|
| **sh** (Bourne) | POSIX standard, basic |
| **bash** | Most popular, default on most distros, extends sh |
| **dash** | Lightweight POSIX shell, default `/bin/sh` on Ubuntu, fast startup |
| **zsh** | Shared history, improved arrays, spell correction, plugins (Oh My Zsh) |
| **fish** | Syntax highlighting, fast history search, web configurator |

```bash
echo $SHELL         # current shell path
echo $0             # current shell name
cat /etc/shells     # all available shells
chsh -s /bin/zsh    # change default login shell
```

Shell config files:
- bash: `~/.bashrc` (interactive), `~/.bash_profile` (login), `~/.bash_logout`
- zsh: `~/.zshrc`
- Global: `/etc/profile`, `/etc/bash.bashrc`

## Essential First Commands

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

## Navigation

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

## Keyboard Shortcuts - Navigation

| Shortcut | Action |
|----------|--------|
| Ctrl+A | Move to start of line |
| Ctrl+E | Move to end of line |
| Alt+F | Move one word forward |
| Alt+B | Move one word backward |
| Ctrl+XX | Toggle between start and current position |

## Keyboard Shortcuts - Editing

| Shortcut | Action |
|----------|--------|
| Ctrl+U | Delete from cursor to start of line |
| Ctrl+K | Delete from cursor to end of line |
| Ctrl+W | Delete word before cursor |
| Alt+D | Delete from cursor to end of word |
| Ctrl+D | Delete character under cursor |
| Alt+. | Insert last argument of previous command |

## Keyboard Shortcuts - Process Control

| Shortcut | Action |
|----------|--------|
| Ctrl+C | Kill current command (SIGINT) |
| Ctrl+Z | Suspend current command (background) |
| Ctrl+D | Close terminal / send EOF |
| Ctrl+L | Clear screen |
| Ctrl+S | Stop output to screen |
| Ctrl+Q | Resume output |

## Keyboard Shortcuts - History

| Shortcut | Action |
|----------|--------|
| Ctrl+R | Reverse incremental history search |
| Up / Ctrl+P | Previous command |
| Down / Ctrl+N | Next command |
| !! | Run last command |
| !x | Run last command starting with x |
| ^old^new | Replace old with new in last command |

## Getting Linux

- **WSL** (Windows 10+): best option for Windows users, install from Microsoft Store
- **VirtualBox**: any distro as VM (2GB+ RAM, 20GB+ disk)
- **Cloud VPS**: connect via SSH
- **macOS**: native Unix terminal, use `brew` as package manager

## Gotchas

- `cd` with no arguments goes to `~` (home), not `/`
- `Ctrl+S` freezes terminal output - use `Ctrl+Q` to unfreeze (common panic moment)
- `history -c` clears in-memory history but not `~/.bash_history` file - use `history -c && history -w` to clear both
- Tab completion is context-aware: first Tab completes, double-Tab shows all options

## See Also

- [[bash-scripting]] - Shell scripting fundamentals
- [[io-redirection-and-pipes]] - stdin/stdout/stderr and pipes
- [[wsl]] - Windows Subsystem for Linux
