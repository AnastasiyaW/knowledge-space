---
title: Linux & CLI - Knowledge Base Index
type: MOC
---
# Linux & CLI - Knowledge Base

Reference knowledge base for Linux command line, shell scripting, and system administration.

## Core Concepts

- [[terminal-navigation]] - pwd, cd, ls, tree, help system, history
- [[file-operations]] - cp, mv, rm, touch, mkdir, find
- [[file-viewing]] - cat, head, tail, less, more, grep, wc, echo
- [[file-permissions]] - chmod, chown, chgrp, umask, rwx, special bits (SUID, SGID, sticky)
- [[users-and-groups]] - useradd, adduser, passwd, usermod, sudo, groups, /etc/passwd, /etc/shadow
- [[filesystem-hierarchy]] - FHS, /etc, /var, /tmp, df, du, mount, tar
- [[links-and-inodes]] - hard links, symbolic links, inodes, ln
- [[io-redirection-and-pipes]] - stdin, stdout, stderr, pipes, &&, ||, >, >>

## Tools & Patterns

- [[text-editors]] - vim (modes, motions, commands), nano (shortcuts)
- [[process-management]] - ps, top, htop, kill, systemctl, pidof, services
- [[package-management]] - apt, apt-get, dpkg, snap, install/remove/update
- [[ssh-remote-access]] - ssh, ssh-keygen, sshd_config, key-based auth, ~/.ssh/config
- [[cron-scheduling]] - crontab, cron syntax, @hourly/@daily, automation
- [[iptables-firewall]] - INPUT/OUTPUT/FORWARD chains, rules, policies, iptables-save
- [[docker-basics]] - images, containers, volumes, docker run, docker-compose
- [[bash-scripting]] - shebang, variables, if/case, for/while/until, functions
- [[terminal-shortcuts]] - Ctrl+R, Ctrl+C, Ctrl+Z, navigation, editing, history

## Quick Reference by Task

| Task | Entry | Key Commands |
|------|-------|-------------|
| Navigate filesystem | [[terminal-navigation]] | `cd`, `ls`, `pwd`, `tree` |
| Create/delete files | [[file-operations]] | `touch`, `mkdir`, `cp`, `mv`, `rm` |
| Read file contents | [[file-viewing]] | `cat`, `head`, `tail`, `less`, `grep` |
| Edit files | [[text-editors]] | `vim`, `nano` |
| Set permissions | [[file-permissions]] | `chmod`, `chown`, `chgrp` |
| Manage users | [[users-and-groups]] | `adduser`, `passwd`, `usermod`, `sudo` |
| Connect remote | [[ssh-remote-access]] | `ssh`, `ssh-keygen`, `ssh-copy-id` |
| Install software | [[package-management]] | `apt install`, `snap install`, `dpkg -i` |
| Monitor processes | [[process-management]] | `ps`, `top`, `kill`, `systemctl` |
| Schedule tasks | [[cron-scheduling]] | `crontab -e`, cron syntax |
| Firewall rules | [[iptables-firewall]] | `iptables -A/-D/-F/-P`, `ufw` |
| Run containers | [[docker-basics]] | `docker run`, `docker ps`, `docker volume` |
| Write scripts | [[bash-scripting]] | `#!/bin/bash`, `if/for/while`, functions |
| Chain commands | [[io-redirection-and-pipes]] | `\|`, `>`, `>>`, `&&`, `\|\|` |
