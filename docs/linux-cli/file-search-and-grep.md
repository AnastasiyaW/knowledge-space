---
title: File Search and grep
category: reference
tags: [linux-cli, find, grep, locate, search]
---

# File Search and grep

Finding files by name/attributes with `find`, searching file contents with `grep`, and fast lookups with `locate`. These tools form the core of filesystem exploration and log analysis.

## find - Search by File Attributes

```bash
find [path] [options] [expression]
```

### Name Matching

```bash
find . -name "file.txt"         # exact name (case-sensitive)
find . -iname "file.txt"        # case-insensitive
find . -name "*.txt"            # wildcard: all .txt files
find . -name "report??"         # ? = exactly one character
find ~ -name "*.sh"             # search in home directory
find /var/log -name "*.log"     # search specific directory
```

### Type Filtering

```bash
find . -type f                  # regular files only
find . -type d                  # directories only
find . -type l                  # symbolic links only
```

### Size Filtering

```bash
find . -size +10k               # larger than 10 KB
find . -size -1M                # smaller than 1 MB
find . -size +100M              # larger than 100 MB
```

Size suffixes: `c` (bytes), `k` (KB), `M` (MB), `G` (GB)

### Depth Control

```bash
find ~ -maxdepth 1              # only in target dir
find ~ -maxdepth 2              # target + one level of subdirs
```

### Combined Conditions

```bash
find . -type f -name "*.sh"     # .sh files only
find . -size +10k -name "*.log" # .log files > 10 KB
```

### Execute Actions on Results

```bash
find . -name "*.tmp" -delete              # delete matches
find . -name "*.sh" -exec chmod +x {} \;  # chmod each found file
```

## grep - Search File Contents

```bash
grep [options] "pattern" [file_or_path]
```

### Common Flags

| Flag | Meaning |
|------|---------|
| `-r` | Recursive search |
| `-i` | Case-insensitive |
| `-n` | Show line numbers |
| `-v` | Invert match (lines NOT matching) |
| `-l` | Show only filenames |
| `-c` | Count matching lines |
| `-E` | Extended regex (same as `egrep`) |
| `--include="*.py"` | Filter by file type |

### Examples

```bash
grep "error" file.txt                          # single file
grep -r "error" /var/log/                      # recursive in directory
grep -rin "error" .                            # recursive, case-insensitive, line numbers
grep -rin --include="*.py" "error" .           # only Python files
grep -v root /etc/passwd                       # lines NOT containing "root"
```

### Pipeline Filtering

```bash
cat /var/log/syslog | grep 'ssh' | grep -v root
cat file | grep 'pattern' | wc -l             # count matching lines
command | grep 'keyword'                       # filter any command output
```

## Other Search Tools

### locate - Fast Database Search

```bash
locate filename         # find by name (faster than find)
updatedb                # rebuild database (run as root)
```

Note: `locate` uses a pre-built database that may be outdated. Run `updatedb` to refresh.

### whereis - Find Binary and Docs

```bash
whereis ls              # binary + man pages
whereis python3         # find Python 3 paths
```

### which - Find Executable in PATH

```bash
which python3           # /usr/bin/python3
which bash              # /bin/bash
```

## Patterns

### Find Large Files

```bash
find / -type f -size +500M -exec ls -lh {} \;
```

### Search and Replace in Files

```bash
grep -rl "old_text" . | xargs sed -i 's/old_text/new_text/g'
```

### Find Recently Modified Files

```bash
find . -type f -mtime -1         # modified in last 24 hours
find . -type f -mmin -60         # modified in last 60 minutes
```

## Gotchas

- `find` wildcards must be quoted (`"*.txt"`) or the shell expands them before find sees them
- `locate` may return stale results if database is old - always `updatedb` first
- `grep -r` follows symlinks by default - use `-R` (capital) to not follow on some systems
- `find . -name ???` matches any 3-character filename (not just digits)
- Redirect stderr when searching from root: `find / -name "file" 2>/dev/null`

## See Also

- [[text-processing]] - awk, sed, sort, uniq for post-processing search results
- [[io-redirection-and-pipes]] - Piping grep output to other commands
- [[logging-and-journald]] - Searching log files effectively
