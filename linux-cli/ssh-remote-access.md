---
title: SSH Remote Access
category: patterns
tags: [ssh, remote, keys, sshd, security]
---
# SSH Remote Access

Secure Shell protocol for encrypted remote access to Linux systems.

## Key Facts

- SSH default port: **22** (TCP)
- Server package: `openssh-server`; Client package: `openssh-client`
- Service daemon: `sshd`, managed via [[process-management]] `systemctl`
- Connection syntax: `ssh user@host` or `ssh user@ip_address`
- Key pair: private key (kept secret, `~/.ssh/id_rsa`) + public key (shared, `~/.ssh/id_rsa.pub`)
- Authorized keys stored server-side in `~/.ssh/authorized_keys`
- Server config: `/etc/ssh/sshd_config`; Client config: `~/.ssh/config`
- Key-based auth is more secure than password auth
- [[file-permissions]] are critical for SSH keys: private key must be `600`, `.ssh/` must be `700`
- [[iptables-firewall]] rules must allow port 22 (or custom port) for SSH to work
- SSH available natively in Windows since Windows 10

## Patterns

```bash
# Connect to remote host
ssh user@192.168.1.10
ssh user@hostname

# Connect on non-default port
ssh -p 2222 user@host

# Generate SSH key pair (RSA 4096-bit)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Creates ~/.ssh/id_rsa (private) and ~/.ssh/id_rsa.pub (public)

# Copy public key to server (easiest method)
ssh-copy-id -i ~/.ssh/id_rsa.pub user@server_ip

# Manual key copy (if ssh-copy-id unavailable)
cat ~/.ssh/id_rsa.pub | ssh user@server_ip \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
   cat >> ~/.ssh/authorized_keys && \
   chmod 600 ~/.ssh/authorized_keys"

# Set correct permissions on keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/authorized_keys

# SSH config file for aliases (~/.ssh/config)
# Host myserver
#   HostName 192.168.1.10
#   User admin
#   Port 2222
#   IdentityFile ~/.ssh/id_rsa

# Connect using config alias
ssh myserver

# Server setup
sudo apt install openssh-server
sudo systemctl start sshd
sudo systemctl enable sshd
sudo systemctl status sshd

# Disable password authentication (after confirming key auth works)
# In /etc/ssh/sshd_config:
#   PasswordAuthentication no
#   PubkeyAuthentication yes
sudo systemctl restart sshd

# Open SSH port in firewall (UFW)
sudo ufw allow 22/tcp
sudo ufw reload

# Open custom SSH port in firewall
sudo ufw allow 2222/tcp
```

## Gotchas

- If key permissions are too open (`chmod 644 id_rsa`), SSH refuses to use the key - must be `600`
- Disabling password auth (`PasswordAuthentication no`) before confirming key auth works = locked out
- After editing `/etc/ssh/sshd_config`, must restart sshd: `sudo systemctl restart sshd`
- Changing SSH port requires updating [[iptables-firewall]] rules AND client connection commands
- `ssh user@ip` - the username must be the LINUX user on the remote system, not your local username
- SSH tunnels can be killed by fail2ban after too many rapid connections - use persistent connections

## See Also

- [[iptables-firewall]] - firewall rules for SSH access
- [[users-and-groups]] - SSH authenticates Linux user accounts
- [[file-permissions]] - critical permissions for SSH key files
- `man sshd_config` - https://man7.org/linux/man-pages/man5/sshd_config.5.html
- `man ssh` - https://man7.org/linux/man-pages/man1/ssh.1.html
