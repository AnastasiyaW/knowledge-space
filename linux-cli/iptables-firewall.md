---
title: Iptables Firewall
category: patterns
tags: [iptables, firewall, networking, security, ufw]
---
# Iptables Firewall

Linux packet filtering firewall for controlling network traffic with chains and rules.

## Key Facts

- Three default chains: **INPUT** (incoming), **OUTPUT** (outgoing), **FORWARD** (routed/transit)
- Two primary targets: **ACCEPT** (allow), **DROP** (silently discard), **REJECT** (deny with response), **LOG** (log packet)
- Rules evaluated top-to-bottom; first match wins
- Default policy applies when no rules match (set with `-P`)
- `-A` appends rule to end; `-I` inserts at beginning (higher priority)
- Rules are NOT persistent across reboots - must save/restore explicitly
- `ufw` (Uncomplicated Firewall) is a simpler frontend for iptables on Ubuntu
- [[ssh-remote-access]] port (22) must be allowed BEFORE setting INPUT policy to DROP
- [[process-management]] - iptables is not a service; rules are kernel-level

## Patterns

```bash
# Install iptables (usually pre-installed)
sudo apt install iptables

# View current rules
sudo iptables -L                      # Basic listing
sudo iptables -L -nv --line-numbers   # Detailed with line numbers

# Add rules to chains
sudo iptables -A INPUT -j LOG         # Log all incoming
sudo iptables -A OUTPUT -j LOG        # Log all outgoing

# Block all traffic from specific IP
sudo iptables -A INPUT -s 192.168.0.104 -j DROP

# Allow traffic from specific IP
sudo iptables -A INPUT -s 192.168.0.107 -j ACCEPT

# Allow SSH (port 22) - CRITICAL: do this BEFORE setting DROP policy
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT

# Block outgoing HTTP (port 80)
sudo iptables -A OUTPUT -p tcp --dport 80 -j REJECT

# Block incoming SSH
sudo iptables -A INPUT -p tcp --dport 22 -j REJECT

# Set default policy (careful!)
sudo iptables -P INPUT DROP          # Block ALL incoming by default
sudo iptables -P INPUT ACCEPT        # Allow ALL incoming by default
sudo iptables -P OUTPUT ACCEPT       # Allow ALL outgoing by default

# Delete rule by line number
sudo iptables -D INPUT 4             # Delete rule #4 in INPUT chain

# Flush (clear) all rules in a chain
sudo iptables -F INPUT               # Clear INPUT rules
sudo iptables -F OUTPUT              # Clear OUTPUT rules
sudo iptables -F                     # Clear ALL chains

# Save rules to file
sudo iptables-save > ~/iptables_config

# Restore rules from file
sudo iptables-restore < ~/iptables_config

# View IP address (useful for rule creation)
hostname -I
ip a

# UFW alternative (simpler)
sudo ufw allow 22/tcp
sudo ufw allow 2222/tcp
sudo ufw deny 80/tcp
sudo ufw enable
sudo ufw reload
sudo ufw status
```

## Gotchas

- Setting `iptables -P INPUT DROP` without first allowing SSH (port 22) = instant lockout from remote server
- `-I` (insert at top) vs `-A` (append at bottom): order matters because first match wins
- `-F` flushes rules but does NOT reset default policy - if policy is DROP and you flush, everything is blocked
- Rules are lost on reboot unless saved with `iptables-save` and restored in startup script
- `iptables -D OUTPUT` is NOT valid for flushing - use `-F OUTPUT` to flush; `-D` requires a rule number
- `ufw` and manual iptables rules can conflict - choose one approach

## See Also

- [[ssh-remote-access]] - ensuring SSH access through firewall
- [[process-management]] - services that need firewall ports opened
- [[docker-basics]] - Docker modifies iptables rules for container networking
- `man iptables` - https://man7.org/linux/man-pages/man8/iptables.8.html
