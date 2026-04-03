---
title: File Operations
category: reference
tags: [linux-cli, files, directories, cp, mv, rm, mkdir]
---

# File Operations

Core commands for creating, copying, moving, deleting, and viewing files and directories. These are the building blocks of everyday Linux command-line work.

## Key Facts

- `rm` has no trash - files are gone permanently
- `cp -r` is required for directories (recursive)
- `mv` handles both moving and renaming
- `touch` creates empty files or updates timestamps on existing ones

## Create

```bash
touch filename             # create empty file or update timestamp
touch f1 f2 f3             # create multiple files
mkdir dirname              # create directory
mkdir -p dir/sub/sub2      # create nested directories (no error if exists)
```

## Copy

```bash
cp src dst                 # copy file
cp -r src/ dst/            # copy directory recursively
cp -p file dst             # preserve permissions and timestamps
```

## Move / Rename

```bash
mv src dst                 # move or rename file/directory
mv old.txt new.txt         # rename in place
mv file.txt /other/dir/    # move to another directory
```

## Delete

```bash
rm filename                # remove file
rm -r dirname/             # remove directory recursively
rm -rf dirname/            # force remove (no prompts)
rmdir dirname              # remove empty directory only (safe)
```

## View File Contents

```bash
cat file                   # print entire file
cat file1 file2            # concatenate and print
less file                  # page through (forward and backward)
more file                  # page through (forward only)
head file                  # first 10 lines
head -n 20 file            # first 20 lines
head -c 30 file            # first 30 bytes
tail file                  # last 10 lines
tail -n 20 file            # last 20 lines
tail -c 30 file            # last 30 bytes
tail -f file               # follow file in real time (logs)
```

## Write to Files

```bash
echo "text" > file         # write (overwrite)
echo "text" >> file        # append
cat > file                 # type from keyboard (Ctrl+D to end)
cat >> file                # append from keyboard
```

## Patterns

### Batch File Creation

```bash
touch file{1..10}.txt      # creates file1.txt through file10.txt
mkdir -p project/{src,test,docs}  # create multiple subdirectories
```

### Safe Recursive Delete

```bash
# Always double-check path before rm -rf
ls dir/                    # verify contents first
rm -ri dir/                # interactive mode - asks for each file
```

## Gotchas

- `rm -rf /` is catastrophic - modern systems require `--no-preserve-root` but never use it
- `cp` without `-r` silently skips directories
- `mv` across filesystems actually copies then deletes (slower than same-filesystem move)
- `rmdir` only removes empty directories - use `rm -r` for non-empty
- `>` overwrites file without warning; use `>>` to append
- `cat file.txt || echo error` - useful for checking if file is readable

## See Also

- [[file-search-and-grep]] - Finding files and searching content
- [[text-processing]] - wc, sort, uniq, cut, awk, sed
- [[file-permissions]] - chmod, chown
- [[links-and-inodes]] - Hard and symbolic links
