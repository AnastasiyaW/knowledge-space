---
title: SSH Remote Access
category: reference
tags: [linux-cli, ssh, scp, tunnels, keys, remote]
---

# SSH Remote Access

SSH (Secure Shell) provides encrypted remote access to Linux systems. This entry covers server setup, key-based authentication, tunneling, SCP file transfers, and security hardening.

## Key Facts

- Default port: **22**
- Key-based auth is more secure than passwords
- SSH config file simplifies connections with aliases
- Tunnels enable secure port forwarding for any protocol

## Installation

```bash
# Server (Debian/Ubuntu)
sudo apt install openssh-server openssh-client

# Server (RHEL/CentOS)
sudo yum install openssh-server openssh-clients

# Service
sudo systemctl start sshd
sudo systemctl enable sshd
```

## Basic Connection

```bash
ssh user@server_ip                    # basic
ssh user@server_ip -p 2222            # custom port
ssh -i ~/.ssh/id_rsa user@server      # specify key
ssh -v user@server                    # verbose (debug)
```

## Key Generation

```bash
ssh-keygen -t ed25519 -C "email@example.com"    # modern, recommended
ssh-keygen -t rsa -b 4096 -C "email@example.com"  # RSA alternative
ssh-keygen -t ecdsa -b 521                       # ECDSA
```

Files created:
- `~/.ssh/id_ed25519` - private key (NEVER share)
- `~/.ssh/id_ed25519.pub` - public key (safe to share)

## Copying Public Key to Server

```bash
# Method 1: ssh-copy-id (easiest)
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server
ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 2222 user@server

# Method 2: manual
cat ~/.ssh/id_ed25519.pub | ssh user@server \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
   cat >> ~/.ssh/authorized_keys && \
   chmod 600 ~/.ssh/authorized_keys"
```

## Required File Permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_ed25519       # private key
chmod 644 ~/.ssh/id_ed25519.pub   # public key
chmod 600 ~/.ssh/authorized_keys
```

## Server Configuration: /etc/ssh/sshd_config

```properties
Port 22                          # change to reduce brute-force noise
PermitRootLogin no               # disable root login
PasswordAuthentication yes       # set to 'no' after keys work
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers alice bob             # whitelist users (optional)
```

After editing: `sudo systemctl restart sshd`

## Client Config: ~/.ssh/config

```properties
Host myserver
    HostName 192.168.1.100
    User alice
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

Host internal
    HostName 10.0.0.5
    User admin
    ProxyJump bastion              # jump through bastion host
```

Usage: `ssh myserver` connects using defined settings.

## SCP - Secure Copy

```bash
scp file.txt user@server:/remote/path/          # local -> remote
scp user@server:/remote/file.txt ./local/       # remote -> local
scp -r ./dir user@server:/remote/path/          # directory (recursive)
scp -P 2222 file.txt user@server:/path/         # custom port
scp -i ~/.ssh/id_rsa file.txt user@server:/path/  # specify key
```

## Port Forwarding (Tunnels)

```bash
# Local forwarding: access remote service locally
ssh -L 8080:localhost:80 user@server
ssh -L 8080:internal-host:80 user@jump-server

# Remote forwarding: expose local service on remote
ssh -R 9090:localhost:80 user@server

# SOCKS proxy
ssh -D 1080 user@server    # SOCKS5 proxy on localhost:1080

# Background tunnel (no shell)
ssh -N -f -L 8080:localhost:80 user@server
```

## Firewall Rules for SSH

```bash
# ufw
sudo ufw allow 22/tcp
sudo ufw allow ssh

# iptables
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT

# firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

## Security Best Practices

1. **Change default port** from 22
2. **Disable root login**: `PermitRootLogin no`
3. **Key-only auth**: `PasswordAuthentication no`
4. **Install fail2ban** to block brute-force IPs:
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable --now fail2ban
   ```
5. **Use strong key types**: ed25519 or RSA 4096
6. **Keep backup** of private key in secure location

## Troubleshooting

```bash
ssh -v user@server          # verbose output
ssh -vvv user@server        # very verbose

# Server-side logs
sudo journalctl -u sshd -f
sudo tail -f /var/log/auth.log

# Test connectivity
nc -zv server_ip 22
```

Common issues:
- **Permission denied (publickey)**: wrong key, wrong `~/.ssh/` permissions, key not in `authorized_keys`
- **Connection refused**: sshd not running, wrong port, firewall blocking
- **Host key verification failed**: server fingerprint changed - edit `~/.ssh/known_hosts`

## Gotchas

- SCP uses `-P` (capital) for port; SSH uses `-p` (lowercase)
- `ssh-copy-id` requires password auth to be enabled
- Multiple SSH connections in rapid succession can trigger fail2ban
- ProxyJump requires SSH access to both bastion and target
- `-N -f` background tunnels stay running until manually killed

## See Also

- [[firewall-and-iptables]] - Firewall configuration
- [[users-and-groups]] - User accounts for SSH
- [[linux-security]] - Security mechanisms
