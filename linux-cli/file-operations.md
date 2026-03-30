---
title: File Operations
category: reference
tags: [files, cp, mv, rm, touch, mkdir, find]
---
# File Operations

Core commands for creating, copying, moving, deleting, and finding files and directories.

## Key Facts

- `touch file1 file2 file3` - create multiple empty files at once (also updates timestamps on existing files)
- `mkdir -p path/to/nested` - create nested directories in one command
- `cp -r src/ dest/` - copy directory recursively; without `-r`, only copies files
- `mv` serves dual purpose: move AND rename
- `rm -r dir/` - recursive delete; `rm -f` - force (no confirmation); `rm -rf` = dangerous combination
- `rmdir` - safe delete, only removes empty directories
- `find` uses `?` for single character wildcard and `*` for multiple characters
- [[file-permissions]] determine who can create/delete files in a directory (need `w` on parent dir)
- [[links-and-inodes]] - hard and soft links are created with `ln`
- File ownership: new files inherit the creating user and their primary group

## Patterns

```bash
# Create directory with subdirectories
mkdir -p project/{src,docs,tests}

# Copy file preserving attributes
cp -p original.conf backup.conf

# Copy directory recursively
cp -r /etc/nginx/ ~/nginx-backup/

# Move (rename) file
mv oldname.txt newname.txt

# Move multiple files to directory
mv file1.txt file2.txt /tmp/

# Delete file (no confirmation)
rm unwanted.txt

# Delete directory and contents recursively
rm -r old_project/

# Find files by name pattern (case-insensitive)
find /var/log -iname "*.log"

# Find files by exact character count in name (??? = 3 chars)
find . -name "???"

# Find files by type
find / -type f -name "*.sh"      # files only
find /home -type d -name "config" # directories only

# Find files by size
find /var -size +100M             # larger than 100MB
find /tmp -size -1k               # smaller than 1KB

# Find and delete (careful!)
find /tmp -name "*.tmp" -delete

# Batch file creation
touch report_{01..12}.txt
```

## Gotchas

- `rm -rf /` will destroy your system - modern distros require `--no-preserve-root` but never use it
- `mv file dir/` moves INTO dir; `mv file dir` renames file to "dir" if dir does not exist
- `cp` without `-r` silently skips directories - no error, just ignored
- `find *` uses shell globbing, not find's pattern matching - use `find . -name "???"` instead
- When using `find -name` with wildcards, always quote the pattern: `find . -name "*.log"` not `find . -name *.log`

## See Also

- [[terminal-navigation]] - navigating the filesystem
- [[file-viewing]] - reading file contents
- [[file-permissions]] - controlling access to files
- `man find` - https://man7.org/linux/man-pages/man1/find.1.html
