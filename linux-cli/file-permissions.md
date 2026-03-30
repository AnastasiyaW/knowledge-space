---
title: File Permissions and Ownership
category: concepts
tags: [chmod, chown, permissions, rwx, ownership, sticky-bit, umask]
---
# File Permissions and Ownership

Linux access control system based on owner, group, and others with read/write/execute bits.

## Key Facts

- Every file has an owner (user), a group, and permissions for three categories: user (u), group (g), others (o)
- Three permission types: read (r=4), write (w=2), execute (x=1)
- Permission string: `-rwxr-xr--` = type + user(rwx) + group(r-x) + others(r--)
- First character: `-` = regular file, `d` = directory, `l` = symlink
- Numeric (octal) notation: `chmod 755` = rwxr-xr-x; `chmod 644` = rw-r--r--
- New files created by a user inherit: user = creator, group = creator's primary group
- `chown` requires `sudo` for changing ownership (security)
- `chgrp` can be used by non-root if user belongs to the target group
- `umask` sets default permission mask for new files (default often `022` - new files get `644`, dirs get `755`)
- Directory permissions: `r` = list contents, `w` = create/delete files inside, `x` = enter/traverse
- [[users-and-groups]] determine which permission set (u/g/o) applies to a given user

### Special Bits

- **SUID** (set user ID, `chmod u+s`): file executes as the file owner, not the caller
- **SGID** (set group ID, `chmod g+s`): on dirs, new files inherit the directory's group
- **Sticky bit** (`chmod +t`): on dirs, only file owner can delete their files (e.g., `/tmp`)

## Patterns

```bash
# View permissions
ls -l file.txt
# -rw-r--r-- 1 alex users 2048 May 10 14:30 file.txt

# Symbolic notation
chmod u+x script.sh              # Add execute for owner
chmod g+rw,o-r file.txt          # Add rw for group, remove r for others
chmod a+r public.txt             # Add read for all (a = all)
chmod u+rwx,g+rx,o-rwx file.txt  # Owner: full, Group: rx, Others: none

# Numeric (octal) notation
chmod 755 script.sh     # rwxr-xr-x (common for scripts)
chmod 644 config.txt    # rw-r--r-- (common for config files)
chmod 600 id_rsa        # rw------- (SSH private key)
chmod 700 .ssh/         # rwx------ (SSH directory)

# Recursive permission change (directory + all contents)
chmod -R 755 /var/www/html/

# Change file owner
sudo chown maria report.doc

# Change owner and group
sudo chown maria:staff report.doc

# Change only group
sudo chown :remote_workers file.txt
# or
sudo chgrp remote_workers file.txt

# Set sticky bit on directory
chmod +t /shared/
chmod 1777 /tmp/    # 1 prefix = sticky bit

# Set SGID on directory
chmod g+s /project/

# View umask
umask
# 0022

# Set more restrictive umask
umask 0077   # New files: 600, new dirs: 700
```

## Gotchas

- `chmod` vs `chown`: `chmod` changes permissions, `chown` changes ownership - common to confuse them
- `chmod 666 script.sh` gives rw to everyone but NO execute - script will not run
- `chmod -R` on wrong directory can lock you out or expose sensitive files - always double-check the path
- `sudo chown :group file` (with colon prefix) changes group; `sudo chown user file` changes user only
- `/tmp` has sticky bit by default - users can create files but cannot delete others' files
- Directories need `x` (execute) permission to `cd` into them - `r` alone only lets you list filenames

## See Also

- [[users-and-groups]] - managing users, groups, and privileges
- [[file-operations]] - creating and manipulating files
- [[filesystem-hierarchy]] - standard directory layout and typical permissions
- `man chmod` - https://man7.org/linux/man-pages/man1/chmod.1.html
- `man chown` - https://man7.org/linux/man-pages/man1/chown.1.html
