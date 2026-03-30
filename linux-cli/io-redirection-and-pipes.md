---
title: I/O Redirection and Pipes
category: concepts
tags: [pipes, redirection, stdin, stdout, stderr, pipeline]
---
# I/O Redirection and Pipes

Connecting command inputs and outputs through streams, redirections, and pipelines.

## Key Facts

- Linux has 3 standard streams: stdin (0), stdout (1), stderr (2)
- `>` redirects stdout to file (overwrite); `>>` appends to file
- `2>` redirects stderr; `2>&1` merges stderr into stdout; `&>` or `*>` redirects all streams
- Pipe `|` sends stdout of one command as stdin to the next command
- Pipelines pass data left to right: `cmd1 | cmd2 | cmd3`
- `&&` runs next command only if previous succeeded (AND)
- `||` runs next command only if previous failed (OR)
- `;` runs next command regardless of previous exit status
- `&` runs command in background
- These operators form the foundation of [[bash-scripting]] and enable [[file-viewing]] pipeline patterns

## Patterns

```bash
# Redirect stdout to file (overwrite)
ls -la > listing.txt

# Redirect stdout to file (append)
echo "new entry" >> log.txt

# Redirect stderr to file
find / -name "*.conf" 2> errors.txt

# Redirect stdout and stderr to separate files
find / -type f -name "*.sh" 1>results.txt 2>errors.txt

# Merge stderr into stdout, then redirect both
command > output.txt 2>&1

# Redirect all streams to file (bash)
command &> all_output.txt

# Discard all output
command > /dev/null 2>&1

# Pipeline: filter and count
cat /var/log/syslog | grep 'cron' | wc -l

# Pipeline: filter logs, exclude user
cat /var/log/syslog | grep 'ssh' | grep -v root

# Pipeline: sort and deduplicate
cat names.txt | sort | uniq

# Pipeline: count installed packages
dpkg -l | wc -l

# Conditional execution: AND (both must succeed)
mkdir testdir && touch testdir/testfile

# Conditional execution: OR (fallback)
cat romeo_file.txt || echo "File not found"

# Conditional: show directory or create it
ls -al ~/testdir || mkdir ~/testdir

# Run regardless of previous result
cd /tmp ; ls

# Input from keyboard to file (Ctrl+D to end)
cat > notes.txt

# Here-document
cat <<EOF > config.txt
server=localhost
port=8080
EOF
```

## Gotchas

- `>` destroys existing file content - always use `>>` when appending to logs
- `grep pattern file` is more efficient than `cat file | grep pattern` (Useless Use of Cat)
- Order matters in `2>&1`: `command > file 2>&1` works; `command 2>&1 > file` does NOT merge properly
- `cmd1 && cmd2 || cmd3` is NOT a proper if/else - if cmd2 fails, cmd3 also runs
- Pipeline exit status is the exit status of the LAST command by default; use `set -o pipefail` to catch earlier failures
- `|` only pipes stdout - stderr still goes to terminal unless explicitly redirected

## See Also

- [[file-viewing]] - commands commonly used in pipelines (grep, wc, head, tail)
- [[bash-scripting]] - using redirections in scripts
- [[process-management]] - background processes with `&`
- `man bash` (section REDIRECTION) - https://www.gnu.org/software/bash/manual/bash.html#Redirections
