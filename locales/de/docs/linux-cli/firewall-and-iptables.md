---
title: "Firewall und iptables"
category: reference
tags: [linux-cli, iptables, firewall, nftables, ufw, networking, security]
level: 3
source_sha256: c964d76fccfd64a62b50bae9a9500e288d6e9e2ac99d2a6c7702a762896b01ba
translation: machine
translated_at: '2026-10-24'
---
# Firewall und iptables {#firewall-and-iptables}

iptables konfiguriert das Paketfilter-Framework Netfilter des Linux-Kernels. Regeln sind in Tabellen und Ketten organisiert. Dieser Eintrag behandelt die Verwaltung von Regeln, gängige Muster, Persistenz und moderne Alternativen.

## Wichtige Fakten {#key-facts}

- Standardtabelle: `filter` (für die meisten Firewall-Regeln)
- Regeln werden von oben nach unten ausgewertet; der erste Treffer gewinnt
- Regeln sind standardmäßig NICHT persistent – sie gehen beim Neustart verloren
- Moderner Nachfolger: `nftables`; vereinfachtes Frontend: `ufw`

## Ketten {#chains}

| Kette | Verkehrsrichtung |
|-------|---------|
| `INPUT` | Eingehend zum lokalen Host |
| `OUTPUT` | Ausgehend vom lokalen Host |
| `FORWARD` | Durchleitung (Routing) |
| `PREROUTING` | Vor der Routing-Entscheidung (NAT) |
| `POSTROUTING` | Nach der Routing-Entscheidung (NAT) |

## Targets (Aktionen) {#targets-actions}

| Target | Wirkung |
|--------|--------|
| `ACCEPT` | Paket erlauben |
| `DROP` | Still verwerfen |
| `REJECT` | Verwerfen + Fehlermeldung an den Absender senden |
| `LOG` | In syslog protokollieren (stoppt die Verarbeitung nicht) |

## Regeln anzeigen {#viewing-rules}

```bash
sudo iptables -L                      # list filter table rules
sudo iptables -L -nv                  # verbose, numeric (no DNS)
sudo iptables -L -nv --line-numbers   # include rule numbers
sudo iptables -t nat -L               # list NAT table rules
```

## Regeln hinzufügen {#adding-rules}

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

## Regeln löschen {#deleting-rules}

```bash
sudo iptables -F INPUT            # flush all rules in INPUT chain
sudo iptables -F                  # flush all chains in filter table
sudo iptables -D INPUT 4          # delete rule number 4
```

## Standardrichtlinien {#default-policies}

```bash
sudo iptables -P INPUT DROP       # deny all incoming by default
sudo iptables -P OUTPUT DROP      # deny all outgoing
sudo iptables -P FORWARD DROP     # deny all forwarded
sudo iptables -P INPUT ACCEPT     # allow all incoming
```

### Sicheres DROP-Muster {#safe-drop-pattern}

```bash
# ALWAYS allow SSH before setting DROP policy
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -P INPUT DROP
```

## Gängige Regelmuster {#common-rule-patterns}

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

## Speichern und Wiederherstellen {#saving-and-restoring}

```bash
sudo iptables-save > ~/iptables_config        # save to file
sudo iptables-restore < ~/iptables_config     # restore from file

# Persistent across reboots (Debian/Ubuntu)
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

## nftables (moderne Alternative) {#nftables-modern-alternative}

```bash
sudo nft list ruleset       # view all rules
```

## ufw (Uncomplicated Firewall) {#ufw-uncomplicated-firewall}

```bash
sudo ufw allow 22/tcp       # allow SSH
sudo ufw allow ssh           # same, by service name
sudo ufw deny 80/tcp         # block HTTP
sudo ufw enable              # activate firewall
sudo ufw status              # show rules
sudo ufw disable             # deactivate
```

## Netzwerk-Werkzeuge {#network-utilities}

```bash
hostname -I         # local IP addresses
ip a                # network interfaces and IPs
```

## Fallstricke {#gotchas}

- Das Setzen von `INPUT DROP` ohne vorheriges Erlauben von SSH **sperrt dich aus** entfernten Servern aus
- Regeln sind geordnet – `-I` (insert) fügt oben ein, `-A` (append) fügt unten an
- `DROP` gibt keine Antwort (der Angreifer erfährt nicht, dass der Port existiert); `REJECT` sendet einen Fehler zurück
- `iptables -F` leert die Regeln, setzt aber NICHT die Standardrichtlinien zurück
- IPv6 erfordert separate `ip6tables`-Regeln
- nftables ist die Zukunft – iptables ist auf neueren Kerneln veraltet

## Siehe auch {#see-also}

- [[ssh-remote-access]] - Öffnen des SSH-Ports, fail2ban
- [[linux-security]] - Überblick über Netzwerksicherheit
- [[logging-and-journald]] - Protokollierung der Firewall
