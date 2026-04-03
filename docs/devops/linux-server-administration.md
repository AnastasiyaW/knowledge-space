---
title: Linux Server Administration
category: concepts
tags: [devops, linux, sysadmin, ssh, systemd, networking, filesystem]
---

# Linux Server Administration

Essential Linux skills for DevOps: filesystem navigation, process management, networking, user management, and service configuration.

## Filesystem Hierarchy

```
/       root of everything
/home   user home directories
/etc    system configuration
/var    variable data (logs, databases)
/tmp    temporary files
/opt    optional/third-party software
/usr    user programs and utilities
/bin    essential binaries
/proc   process info (virtual)
```

## Essential Commands

```bash
# Navigation
pwd; cd /path; ls -la; ls -lh

# File operations
touch file; cp src dst; mv src dst; rm file; rm -rf dir
mkdir -p a/b/c; cat file; less file; head -n 20 file; tail -f file

# Search
find / -name "*.log"
find / -type f -size +100M
grep -r "pattern" /dir; grep -i "pattern" file

# Permissions (r=4, w=2, x=1)
chmod 755 file; chmod +x script.sh; chown user:group file

# Text processing
cat file | grep "error" | wc -l
awk '{print $1}' file; sed 's/old/new/g' file
sort file | uniq; cut -d',' -f1,3 file
```

## User Management

```bash
useradd username; passwd username
usermod -aG groupname user
userdel username; groups username; id username
su - username; sudo command; visudo
```

## Process Management

```bash
ps aux; ps aux | grep nginx
top; htop
kill PID; kill -9 PID
systemctl start/stop/enable/status svc
journalctl -u svc
```

## Systemd Service Files

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=appuser
ExecStart=/usr/bin/myapp --config /etc/myapp.conf
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload; systemctl enable myapp; systemctl start myapp
```

## Networking

```bash
ip addr show; ip route show
ss -tulnp                    # listening ports
ping host; curl http://host:port
nslookup domain; dig domain; traceroute host
```

### Firewall (ufw)

```bash
ufw enable; ufw allow 22; ufw allow 80; ufw allow 443; ufw status
```

## SSH

```bash
ssh user@host; ssh -i key.pem user@host; ssh -p 2222 user@host
ssh-keygen -t rsa -b 4096; ssh-copy-id user@host
scp file user@host:/path; scp user@host:/path/file .
```

## Package Management

```bash
# Debian/Ubuntu
apt update; apt install pkg; apt remove pkg; apt upgrade

# RHEL/CentOS
yum install pkg; yum update; dnf install pkg
```

## Shell Scripting

```bash
#!/bin/bash
NAME="DevOps"
echo "Hello, $NAME"

if [ -f "/etc/nginx/nginx.conf" ]; then
    echo "Config exists"
fi

for i in 1 2 3; do echo "Item $i"; done

deploy() {
    kubectl apply -f manifests/ -n "$1"
}
deploy "production"

# Exit codes
command_that_might_fail
if [ $? -eq 0 ]; then echo "Success"; else echo "Failed"; fi
```

## SRE Toolchain

```bash
# Quick network check
timeout 1 bash -c 'cat < /dev/null > /dev/tcp/8.8.8.8/443'; echo $?

# SSL certificate check
docker run harisekhon/nagios-plugins check_ssl_cert.pl --host "google.com" -c 14 -w 30

# Colorize output
grc -c grc.conf journalctl -f

# Extract IPs
egrep '([0-9]{1,3}\.){3}[0-9]{1,3}' file
```

## Scheduled Tasks

- `cron` for recurring: `crontab -e`
- `systemd timers` for modern Linux
- `at` for one-time delayed execution (useful for automatic rollbacks)

## Gotchas

- Permission digits: owner|group|others. 755 = rwxr-xr-x
- `tail -f` for live log following is essential for debugging
- `usermod -aG docker $USER` requires logout/login to take effect
- Never run `rm -rf /` - always double-check paths

## See Also

- [[docker-fundamentals]] - containers on Linux
- [[ansible-configuration-management]] - automated Linux management
- [[sre-incident-management]] - debugging on Linux servers
- [[aws-cloud-fundamentals]] - EC2 instances run Linux
