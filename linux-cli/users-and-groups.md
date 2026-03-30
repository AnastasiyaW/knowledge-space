---
title: Users and Groups Management
category: concepts
tags: [users, groups, useradd, passwd, sudo, root]
---
# Users and Groups Management

Creating, modifying, and managing Linux users, groups, and privileges.

## Key Facts

- `/etc/passwd` - user account info: `username:x:UID:GID:comment:home:shell`
- `/etc/shadow` - password hashes (requires root to read)
- `/etc/group` - group definitions
- `/etc/sudoers` - sudo privilege configuration (edit ONLY with `visudo`)
- Regular user UIDs typically start at 1000 in modern systems
- UID 0 = root (superuser)
- `useradd` - low-level utility, creates minimal user record
- `adduser` - higher-level Perl script, interactive, creates home dir and sets password
- `su` (substitute user) - switch to another user; `sudo su` = become root
- `sudo` (super user do) - execute single command as root
- Membership in `sudo` group grants root privileges via sudo
- [[file-permissions]] are evaluated against user's UID and GIDs

## Patterns

```bash
# View current user info
whoami                  # username only
id                      # UID, GID, all groups
groups                  # group list
groups root             # groups of specific user

# Switch to root
sudo su
su root                 # requires root password

# Create user (interactive, recommended)
sudo adduser newemployee

# Create user (low-level, minimal)
sudo useradd -m -s /bin/bash -d /home/jdoe jdoe
# -m = create home dir, -s = set shell, -d = home path

# Set/change password
sudo passwd officemanager

# Modify user
sudo usermod -aG docker jdoe     # Add to supplementary group
sudo usermod -s /bin/zsh jdoe    # Change shell
sudo usermod -L smileygirl       # Lock (disable) account
sudo usermod -U smileygirl       # Unlock account

# Delete user
sudo userdel olduser             # Remove user only
sudo userdel -r olduser          # Remove user + home directory

# Group management
sudo groupadd developers         # Create group
sudo addgroup testers             # Create group (alternative)
sudo groupdel obsolete_group      # Delete group

# Edit sudoers file (ALWAYS use visudo)
sudo visudo

# View /etc/passwd entry
grep jdoe /etc/passwd
# jdoe:x:1005:1003:John Doe:/home/jdoe:/bin/bash
#  user:pw:UID:GID:comment:home:shell
```

## Gotchas

- `useradd` vs `adduser`: `useradd` does NOT create home directory by default (need `-m`); `adduser` does everything interactively
- `usermod -G group user` REPLACES all supplementary groups; use `-aG` to APPEND
- Never edit `/etc/sudoers` directly - always use `visudo` which validates syntax before saving
- `sudo passwd username` sets password for another user; `passwd` alone changes your own
- Locked accounts (`usermod -L`) can still log in via SSH keys - lock is password-only
- `/etc/shadow` stores hashed passwords - if second field is `!` or `*`, password login is disabled

## See Also

- [[file-permissions]] - how user/group identity maps to file access
- [[ssh-remote-access]] - key-based authentication for users
- [[process-management]] - processes run under user identity
- `man useradd` - https://man7.org/linux/man-pages/man8/useradd.8.html
- `man sudoers` - https://man7.org/linux/man-pages/man5/sudoers.5.html
