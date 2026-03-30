---
title: Links and Inodes
category: concepts
tags: [ln, symlink, hardlink, inode, filesystem]
---
# Links and Inodes

Hard links and symbolic links - two ways to reference files in the Linux filesystem.

## Key Facts

- Every file on disk has an **inode** - a data structure storing metadata (permissions, owner, size, data block pointers)
- Filenames are entries in a directory that point to an inode number
- **Hard link**: additional directory entry pointing to the same inode (same file, different name)
- **Symbolic (soft) link**: a separate file containing a path to the target (like a shortcut)
- Hard links share the same inode number; removing one does not affect others
- Soft links can span filesystems; hard links cannot
- Soft links can point to directories; hard links cannot (to prevent loops)
- `ls -li` shows inode numbers alongside file listings
- Hard link count is shown in `ls -l` output (second column)
- [[file-permissions]] on a hard link are the SAME as the original (same inode)
- [[filesystem-hierarchy]] determines which filesystem boundaries apply to hard links

## Patterns

```bash
# Create hard link
ln original.txt hardlink.txt

# Create symbolic (soft) link
ln -s /etc/nginx/nginx.conf ~/nginx-config

# Create soft link to directory
ln -s /var/log ~/logs

# View inode numbers
ls -li
# 1234567 -rw-r--r-- 2 user group 1024 file.txt
#  ^inode            ^link count

# Check if two files share an inode (are hard links)
stat file1.txt file2.txt   # compare Inode field

# Find all hard links to a file by inode
find / -inum 1234567

# Remove a link (does not affect other links or original)
rm hardlink.txt

# Common use: config file symlinks
ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite
```

## Gotchas

- Deleting the original file when using a soft link creates a **dangling link** (broken shortcut)
- Deleting a hard link does not delete the file data until ALL hard links are removed (link count reaches 0)
- `ln target linkname` (no `-s`) creates a hard link - easy to forget `-s` for symlinks
- `ls -s` is NOT the same as `ln -s` - `ls -s` shows file sizes in blocks
- Editing a hard link edits the original file (they are the same file)
- Soft links store the path as text - if you move the target, the link breaks

## See Also

- [[file-operations]] - creating and managing files
- [[file-permissions]] - permissions apply to the inode, not the link name
- [[filesystem-hierarchy]] - where links are commonly used
- `man ln` - https://man7.org/linux/man-pages/man1/ln.1.html
