---
title: Links and Inodes
category: concepts
tags: [linux-cli, inodes, hard-links, symlinks, ext4]
---

# Links and Inodes

Every file in Linux has an inode - a data structure storing metadata and pointers to data blocks. Filenames are just directory entries pointing to inodes. Understanding this model explains how hard links, symlinks, and file deletion actually work.

## Key Facts

- An **inode** stores permissions, owner, timestamps, size, and block pointers - everything except the filename
- A **directory** is a file containing `(filename -> inode number)` mappings
- Deleting a file removes the directory entry; data persists until all links are gone and blocks are overwritten
- `stat filename` shows inode details

## Inode Contents

| Field | Description |
|-------|-------------|
| `i_mode` | File type and permissions |
| `i_uid` / `i_gid` | Owner UID / Group GID |
| `i_size` | File size in bytes |
| `i_atime` | Last access time |
| `i_mtime` | Last modification time |
| `i_ctime` | Inode change time |
| `i_links_count` | Hard link count (0 = deleted) |
| `i_blocks` | Data block pointers |

### ext4 Improvements over ext3

- Inode size: 256 bytes (was 128)
- Timestamp precision: nanoseconds (was seconds)
- 48-bit inode numbers (was 32-bit)
- **Extents** replace indirect block pointers (better large file performance)
- Inode checksums

```bash
ls -li               # show files with inode numbers
stat filename         # detailed inode info
debugfs /dev/sda1     # interactive filesystem debugger
```

## Hard Links

A hard link is an additional directory entry pointing to the same inode. Same data, same inode number.

```bash
ln source_file hardlink_name
```

- Both names point to the **same inode** (same data blocks)
- Deleting one link does not remove the file (data persists while link count > 0)
- **Cannot** span filesystems
- **Cannot** link to directories
- `ls -li` shows same inode number for both names

## Symbolic Links (Symlinks)

A symlink is a special file containing a **path** to another file.

```bash
ln -s target_file symlink_name
ln -s /etc/nginx/nginx.conf ./nginx.conf
ls -la                # shows: symlink -> target
```

- **Can** span filesystems
- **Can** link to directories
- Broken if target is deleted (dangling symlink, shown in red)
- Has its own inode (different from target)

## Hard Links vs Symlinks

| Feature | Hard Link | Symlink |
|---------|-----------|---------|
| Same inode as target | Yes | No (own inode) |
| Cross filesystem | No | Yes |
| Link to directories | No | Yes |
| Survives target deletion | Yes (data persists) | No (becomes broken) |
| Size | Same as target | Path string length |

## How File Deletion Works

1. Directory entry (name -> inode link) is removed
2. Inode's `i_links_count` decremented
3. When link count reaches 0 AND no process has file open: inode and blocks marked as free
4. **Data remains on disk** until overwritten by new data

This is why file recovery is possible immediately after deletion but becomes less likely over time.

## ext Filesystem Block Groups

```javascript
Boot record
-- Block group 0 --
  superblock          (filesystem metadata)
  group descriptors
  block bitmap        (free blocks map)
  inode bitmap        (free inodes map)
  inode table
  data blocks
-- Block group 1 --
  superblock backup
  ...
```

## Gotchas

- Hard links share data - editing through one name changes what the other sees
- `cp` creates a new file with a new inode; `ln` creates another name for the same inode
- Symlinks have their own permissions but they are typically ignored - the target's permissions apply
- Moving a file within the same filesystem only changes the directory entry (fast); moving across filesystems copies data (slow)
- Running out of inodes (`df -i`) prevents creating new files even if disk space remains

## See Also

- [[disks-and-filesystems]] - ext4 structure, block groups, journaling
- [[file-permissions]] - Permission model stored in inodes
- [[filesystem-hierarchy]] - Directory layout
