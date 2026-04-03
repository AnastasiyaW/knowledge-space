---
title: Firewall and iptables
category: reference
tags: [linux-cli, iptables, firewall, nftables, ufw, networking, security]
---

# Firewall and iptables

iptables configures the Linux kernel's netfilter packet filtering framework. Rules are organized into tables and chains. This entry covers rule management, common patterns, persistence, and modern alternatives.

## Key Facts

- Default table: `filter` (for most firewall rules)
- Rules are evaluated top-to-bottom; first match wins
- Rules are NOT persistent by default - lost on reboot
- Modern replacement: `nftables`; simplified frontend: `ufw`

## Chains

| Chain | Traffic Direction |
|-------|---------|
| `INPUT` | Incoming to local host |
| `OUTPUT` | Outgoing from local host |
| `FORWARD` | Passing through (routing) |
| `PREROUTING` | Before routing decision (NAT) |
| `POSTROUTING` | After routing decision (NAT) |

## Targets (Actions)

| Target | Effect |
|--------|--------|
| `ACCEPT` | Allow packet |
| `DROP` | Silently discard |
| `REJECT` | Discard + send error to sender |
| `LOG` | Log to syslog (does not stop processing) |

## Viewing Rules

```bash
sudo iptables -L                      # list filter table rules
sudo iptables -L -nv                  # verbose, numeric (no DNS)
sudo iptables -L -nv --line-numbers   # include rule numbers
sudo iptables -t nat -L               # list NAT table rules
```

## Adding Rules

```bash
# Append to chain
sudo iptables -A INPUT -s 192.168.0.104 -j DROP     # drop from IP
sudo iptables -A INPUT -p tcp --dport 22 -j REJECT   # block SSH
sudo iptables -A OUTPUT -p tcp --dport 80 -j REJECT  # block outgoing HTTP

# Insert at top (highest priority)
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT   # allow SSH first

# Log all traffic
sudo iptables -A INPUT -j LOG
```

## Deleting Rules

```bash
sudo iptables -F INPUT            # flush all rules in INPUT chain
sudo iptables -F                  # flush all chains in filter table
sudo iptables -D INPUT 4          # delete rule number 4
```

## Default Policies

```bash
sudo iptables -P INPUT DROP       # deny all incoming by default
sudo iptables -P OUTPUT DROP      # deny all outgoing
sudo iptables -P FORWARD DROP     # deny all forwarded
sudo iptables -P INPUT ACCEPT     # allow all incoming
```

### Safe DROP Pattern

```bash
# ALWAYS allow SSH before setting DROP policy
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -P INPUT DROP
```

## Common Rule Patterns

```bash
# Allow established/related connections (stateful)
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow ping (ICMP)
sudo iptables -A INPUT -p icmp -j ACCEPT

# Allow port range
sudo iptables -A INPUT -p tcp --dport 8000:8080 -j ACCEPT

# Block subnet
sudo iptables -A INPUT -s 10.0.0.0/8 -j DROP

# NAT masquerade (internet sharing)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

## Saving and Restoring

```bash
sudo iptables-save > ~/iptables_config        # save to file
sudo iptables-restore < ~/iptables_config     # restore from file

# Persistent across reboots (Debian/Ubuntu)
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

## nftables (Modern Alternative)

```bash
sudo nft list ruleset       # view all rules
```

## ufw (Uncomplicated Firewall)

```bash
sudo ufw allow 22/tcp       # allow SSH
sudo ufw allow ssh           # same, by service name
sudo ufw deny 80/tcp         # block HTTP
sudo ufw enable              # activate firewall
sudo ufw status              # show rules
sudo ufw disable             # deactivate
```

## Network Utilities

```bash
hostname -I         # local IP addresses
ip a                # network interfaces and IPs
```

## Gotchas

- Setting `INPUT DROP` without first allowing SSH **locks you out** of remote servers
- Rules are ordered - `-I` (insert) adds at top, `-A` (append) adds at bottom
- `DROP` gives no response (attacker doesn't know port exists); `REJECT` sends error back
- `iptables -F` flushes rules but does NOT reset default policies
- IPv6 requires separate `ip6tables` rules
- nftables is the future - iptables is legacy on newer kernels

## See Also

- [[ssh-remote-access]] - Opening SSH port, fail2ban
- [[linux-security]] - Network security overview
- [[logging-and-journald]] - Firewall logging
