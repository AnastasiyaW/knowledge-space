---
title: Terminal Navigation and Basic Commands
category: concepts
tags: [navigation, cd, ls, pwd, terminal, basics]
---
# Terminal Navigation and Basic Commands

Essential commands for moving through the Linux filesystem and getting help.

## Key Facts

- `pwd` (print working directory) - shows absolute path to current directory
- `cd` (change directory) - navigate the filesystem; `cd /` = root, `cd ~` = home, `cd ..` = parent, `cd -` = previous
- `ls` - list directory contents; `ls -l` = long format, `ls -a` = include hidden (dotfiles), `ls -alF` = full detail
- `ll` is typically an alias for `ls -alF`, defined in `~/.bashrc`
- Hidden files/directories start with `.` (dot) - only shown with `ls -a`
- `tree` - displays directory structure as a visual tree (install: `sudo apt install tree`)
- `clear` or `Ctrl+L` - clear terminal screen; `reset` - reset terminal settings
- Help system: `man <cmd>`, `<cmd> --help`, `whatis <cmd>` (one-line summary), `apropos <keyword>` (search manpages)
- `history` - show command history; `history -c` - clear history
- `Ctrl+R` - reverse search through command history
- [[file-permissions]] apply to directories too: `r` = list contents, `x` = traverse/enter, `w` = create/delete files inside

## Patterns

```bash
# Navigate to absolute path
cd /var/log

# Navigate to home directory (three equivalent ways)
cd ~
cd $HOME
cd

# Go up two levels
cd ../..

# List files sorted by modification time, newest first
ls -lt

# List only directories
ls -d */

# Recursive listing
ls -R /etc/ssh/

# Display directory tree, 2 levels deep
tree -L 2 /etc

# Search man pages for keyword
apropos partition

# Re-run last command
!!

# Re-run last command starting with 'apt'
!apt
```

## Gotchas

- `cd /home` navigates to absolute `/home` directory; `cd home` looks for `home` in current directory - easy to confuse
- `rmdir` only removes empty directories (safe delete); `rm -r` removes recursively including contents
- Tab completion works for paths and commands - double-tap Tab to show all options
- `Ctrl+S` freezes terminal output (XOFF); `Ctrl+Q` resumes it - often mistaken for a hang

## See Also

- [[file-operations]] - creating, copying, moving, deleting files
- [[io-redirection-and-pipes]] - redirecting output and chaining commands
- `man hier` - description of the filesystem hierarchy
- https://www.gnu.org/software/bash/manual/bash.html
