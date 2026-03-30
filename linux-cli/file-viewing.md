---
title: File Viewing and Text Processing
category: reference
tags: [cat, head, tail, less, more, grep, wc]
---
# File Viewing and Text Processing

Commands for reading, searching, and analyzing file contents without editing.

## Key Facts

- `cat` (concatenate) - output entire file; can combine multiple files: `cat f1 f2 > combined`
- `head` - first 10 lines by default; `head -n 20` or `head -20` for 20 lines; `head -c 30` for 30 bytes
- `tail` - last 10 lines by default; `tail -c 30` for last 30 bytes; `tail -f` follows file in real-time (logs)
- `more` - page-by-page forward-only viewer; `less` - page-by-page with backward scroll (less is more)
- `grep` - search for patterns in text; `-i` case-insensitive, `-v` invert match, `-r` recursive, `-c` count matches
- `wc` - word count; `-l` lines, `-w` words, `-c` bytes
- These commands are designed for [[io-redirection-and-pipes]] - they read stdin and write stdout
- `echo` - print text to terminal or redirect to file

## Patterns

```bash
# View file contents
cat /etc/hostname

# View first/last N lines
head -20 /var/log/syslog
tail -50 /var/log/auth.log

# Follow log file in real-time (Ctrl+C to stop)
tail -f /var/log/syslog

# Last 30 bytes of a file
tail -c 30 myfile.txt

# Search for pattern in file
grep 'error' /var/log/syslog
grep -i 'warning' /var/log/syslog    # case-insensitive
grep -v 'debug' /var/log/syslog      # exclude matches
grep -r 'TODO' ~/project/            # recursive search

# Count lines containing a pattern
grep -c 'cron' /var/log/syslog

# Count lines, words, chars in file
wc -l /etc/passwd
wc -w document.txt

# Combine: count cron mentions in syslog
cat /var/log/syslog | grep 'cron' | wc -l

# Filter SSH logs, exclude root
cat /var/log/syslog | grep 'ssh' | grep -v root

# Write text to file (overwrite)
echo "Hello world" > greeting.txt

# Append text to file
echo "new line" >> greeting.txt

# Input from keyboard to file (Ctrl+D to finish)
cat > notes.txt

# Append keyboard input to file
cat >> notes.txt
```

## Gotchas

- `>` overwrites file; `>>` appends - mixing them up destroys data
- `cat file.txt | grep pattern` works but `grep pattern file.txt` is more efficient (avoids useless cat)
- `tail -f` keeps the file handle open - if the file is rotated (logs), use `tail -F` instead
- `wc -l` counts newline characters - a file without a trailing newline will undercount by 1

## See Also

- [[io-redirection-and-pipes]] - connecting commands together
- [[text-editors]] - editing files (vim, nano)
- [[terminal-navigation]] - finding files to view
- `man grep` - https://man7.org/linux/man-pages/man1/grep.1.html
