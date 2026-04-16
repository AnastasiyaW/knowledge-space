---
title: File Permissions
category: reference
tags: [linux-cli, permissions, chmod, chown, acl, security]
---

# File Permissions

Every file and directory in Linux has an owner, a group, and permission bits for three categories: owner (u), group (g), others (o). This entry covers reading, setting, and extending permissions.

## Key Facts

- Three permission types: read (r=4), write (w=2), execute (x=1)
- New files default to 666 minus umask; directories to 777 minus umask
- Only root can change file ownership
- ACLs provide fine-grained per-user/per-group permissions beyond the basic model

## Reading Permissions

```bash
ls -l file.txt
# -rw-r--r-- 1 alice users 2048 May 10 14:30 file.txt
```

```typescript
- rw- r-- r--
| |   |   +-- others: read only
| |   +------ group: read only
| +---------- owner: read + write
+------------- type (- = file, d = dir, l = symlink)
```

| Symbol | On files | On directories |
|--------|----------|----------------|
| `r` | Read contents | List contents |
| `w` | Modify file | Create/delete files inside |
| `x` | Run as program | Enter (cd into) |

## chmod - Change Permissions

### Symbolic Notation

```bash
chmod u+x file          # add execute for owner
chmod g-w file          # remove write for group
chmod o+r file          # add read for others
chmod a+x file          # add execute for all
chmod u+rwx,g-w,o-r file  # multiple changes
chmod u=rwx,g=rx,o= file  # set exact permissions
chmod -R 755 dir/       # recursive
```

Categories: `u` = owner, `g` = group, `o` = others, `a` = all

### Octal Notation

| Octal | Symbolic | Typical use |
|-------|----------|-------------|
| 755 | rwxr-xr-x | Executables, directories |
| 644 | rw-r--r-- | Regular files |
| 600 | rw------- | Private files (SSH keys) |
| 700 | rwx------ | Private directories |
| 777 | rwxrwxrwx | Fully open (avoid) |

```bash
chmod 644 file          # rw-r--r--
chmod 755 file          # rwxr-xr-x
chmod 700 file          # rwx------
```

## chown - Change Owner

```bash
sudo chown alice file              # change owner
sudo chown alice:devs file         # change owner and group
sudo chown :devs file              # change group only
sudo chown -R alice:devs dir/      # recursive
```

## chgrp - Change Group

```bash
sudo chgrp groupname file
sudo chgrp -R groupname dir/
```

## Special Permission Bits

### SUID (Set User ID) - bit 4

Executable runs with file **owner's** UID, not caller's.

```bash
chmod u+s file          # set SUID
chmod 4755 file         # octal
# ls -l shows: -rwsr-xr-x
```

Example: `/usr/bin/passwd` has SUID so any user can change their password.

### SGID (Set Group ID) - bit 2

On executables: runs with file's group. On directories: new files inherit directory's group.

```bash
chmod g+s dir/          # set SGID
chmod 2755 dir/         # octal
# ls -l shows: drwxr-sr-x
```

### Sticky Bit - bit 1

On directories: users can only delete files they own.

```bash
chmod +t dir/           # set sticky bit
chmod 1777 dir/         # octal
# ls -l shows: drwxrwxrwt
```

`/tmp` has sticky bit by default.

## umask - Default Permissions

Defines which bits are **removed** from default permissions.

```bash
umask              # show current umask
umask -S           # show in symbolic form
umask 022          # set umask
```

With umask 022: files get 644 (666-022), directories get 755 (777-022).

## ACL - Access Control Lists

Fine-grained permissions for individual users and groups.

```bash
# View
getfacl file

# Set
setfacl -m u:alice:rw file          # give alice read+write
setfacl -m g:devs:r file            # give group read
setfacl -x u:alice file             # remove alice's ACL entry
setfacl -b file                     # remove all ACL entries
setfacl -d -m u:alice:rw dir/       # set default ACL (inherited by new files)
setfacl -R -m u:alice:rw dir/       # recursive
```

ACL types: **Access ACL** (direct), **Default ACL** (inherited by new files in directories).

## chroot - Change Root

Isolates a process by changing its apparent root directory.

```bash
sudo chroot /new/root command
```

Use cases: privilege separation, recovery environments, honeypots. Not a complete security boundary on its own.

## Gotchas

- `chmod 777` is almost never the right solution - find the actual permission needed
- SUID on scripts is ignored by most kernels for security reasons
- `chown` requires root even if you own the file (prevents UID spoofing)
- ACL `+` indicator in `ls -l` output (e.g., `drwxr-xr-x+`) means ACLs are set
- umask is per-session - set it in `~/.bashrc` for persistence
- Recursive chmod on `/` will break the system

## See Also

- [[users-and-groups]] - User management and sudo
- [[linux-security]] - Security mechanisms overview
- [[ssh-remote-access]] - SSH key file permissions
