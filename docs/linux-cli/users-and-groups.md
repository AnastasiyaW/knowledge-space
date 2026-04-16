---
title: Users and Groups
category: reference
tags: [linux-cli, users, groups, sudo, su, passwd]
---

# Users and Groups

Linux is a multi-user system. Users can be human accounts, system service accounts, or the superuser (root). Groups organize users for shared permissions. This entry covers user management, authentication files, and privilege escalation.

## User Types

| Type | UID Range | Examples |
|------|-----------|---------|
| Superuser (root) | 0 | Full system access |
| System users | 1-999 | daemon, sshd, www-data |
| Regular users | 1000+ | Human accounts |

## Key Files

| File | Purpose |
|------|---------|
| `/etc/passwd` | User accounts (readable by all) |
| `/etc/shadow` | Password hashes (root only) |
| `/etc/group` | Group definitions |

### /etc/passwd Format

```text
username:x:UID:GID:GECOS:home_dir:shell
alice:x:1001:1001:Alice Smith:/home/alice:/bin/bash
```

## Querying User Info

```bash
whoami              # current username
id                  # UID, GID, all groups
id username         # info for specific user
groups              # groups of current user
groups username     # groups of specific user
who                 # who is logged in
w                   # logged in + what they're doing
last                # login history
lastlog             # all users' last login dates
```

## Creating Users

```bash
# useradd - low-level, minimal
sudo useradd username                     # no home, no password
sudo useradd -m username                  # with home directory
sudo useradd -m -s /bin/bash username     # with home + bash shell

# adduser - interactive wrapper (Debian/Ubuntu)
sudo adduser username                     # prompts for password, info

# Set password
sudo passwd username
```

## Modifying Users

```bash
sudo usermod -s /bin/bash user       # change shell
sudo usermod -d /new/home user       # change home directory
sudo usermod -l newname oldname      # rename user
sudo usermod -aG group user          # add to supplementary group (-a = APPEND)
sudo usermod -G g1,g2 user           # set supplementary groups (REPLACES existing)
sudo usermod -L user                 # lock account
sudo usermod -U user                 # unlock account
```

## Deleting Users

```bash
sudo userdel username           # delete user (keep home)
sudo userdel -r username        # delete user AND home directory
```

## Group Management

```bash
sudo groupadd groupname         # create group
sudo groupdel groupname         # delete group
sudo groupmod -n new old        # rename group
```

## Switching Users

### su (Substitute User)

```bash
su username             # switch (keeps current environment)
su - username           # switch with full login environment
su -                    # switch to root (full login)
sudo su                 # switch to root via sudo
```

### sudo (Superuser Do)

```bash
sudo command            # run as root
sudo -u username cmd    # run as specific user
sudo -i                 # interactive root shell
sudo -b command         # background execution
```

**su vs sudo:**
- `su` requires **target user's** password; no logging
- `sudo` requires **your** password; all actions logged; needs `/etc/sudoers` config

### visudo

```bash
sudo visudo             # safely edit /etc/sudoers (validates syntax)
```

Grant sudo access:
```bash
sudo usermod -aG sudo username    # Debian/Ubuntu
sudo usermod -aG wheel username   # RHEL/CentOS/Fedora
```

## Patterns

### Create User with Full Setup

```bash
sudo useradd -m -s /bin/bash -G sudo newuser
sudo passwd newuser
```

### List All Real Users

```bash
awk -F: '$3 >= 1000 && $3 < 65534 {print $1}' /etc/passwd
```

## Gotchas

- `usermod -G` without `-a` **replaces** all supplementary groups - always use `-aG` to append
- `useradd` does NOT create home directory by default - use `-m` flag
- Locked accounts (`usermod -L`) add `!` prefix to password hash in `/etc/shadow`
- Root account may be disabled on some distros (Ubuntu) - use `sudo` instead
- Deleting a user does not kill their running processes

## See Also

- [[file-permissions]] - Permission model, chmod, ACLs
- [[ssh-remote-access]] - Key-based authentication
- [[linux-security]] - DAC, MAC, capabilities
