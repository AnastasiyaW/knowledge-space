---
title: "Pare-feu et iptables"
category: reference
tags: [linux-cli, iptables, firewall, nftables, ufw, networking, security]
level: 3
source_sha256: c964d76fccfd64a62b50bae9a9500e288d6e9e2ac99d2a6c7702a762896b01ba
translation: machine
translated_at: '2026-10-24'
---
# Pare-feu et iptables {#firewall-and-iptables}

iptables configure le framework de filtrage de paquets netfilter du noyau Linux. Les règles sont organisées en tables et en chaînes. Cette entrée couvre la gestion des règles, les schémas courants, la persistance et les alternatives modernes.

## Points clés {#key-facts}

- Table par défaut : `filter` (pour la plupart des règles de pare-feu)
- Les règles sont évaluées de haut en bas ; la première correspondance l'emporte
- Les règles ne sont PAS persistantes par défaut : elles sont perdues au redémarrage
- Remplacement moderne : `nftables` ; interface simplifiée : `ufw`

## Chaînes {#chains}

| Chaîne | Sens du trafic |
|-------|---------|
| `INPUT` | Entrant vers l'hôte local |
| `OUTPUT` | Sortant depuis l'hôte local |
| `FORWARD` | Transit (routage) |
| `PREROUTING` | Avant la décision de routage (NAT) |
| `POSTROUTING` | Après la décision de routage (NAT) |

## Cibles (actions) {#targets-actions}

| Cible | Effet |
|--------|--------|
| `ACCEPT` | Autoriser le paquet |
| `DROP` | Supprimer silencieusement |
| `REJECT` | Rejeter et envoyer une erreur à l'émetteur |
| `LOG` | Journaliser dans syslog (ne stoppe pas le traitement) |

## Consultation des règles {#viewing-rules}

```bash
sudo iptables -L                      # list filter table rules
sudo iptables -L -nv                  # verbose, numeric (no DNS)
sudo iptables -L -nv --line-numbers   # include rule numbers
sudo iptables -t nat -L               # list NAT table rules
```

## Ajout de règles {#adding-rules}

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

## Suppression de règles {#deleting-rules}

```bash
sudo iptables -F INPUT            # flush all rules in INPUT chain
sudo iptables -F                  # flush all chains in filter table
sudo iptables -D INPUT 4          # delete rule number 4
```

## Politiques par défaut {#default-policies}

```bash
sudo iptables -P INPUT DROP       # deny all incoming by default
sudo iptables -P OUTPUT DROP      # deny all outgoing
sudo iptables -P FORWARD DROP     # deny all forwarded
sudo iptables -P INPUT ACCEPT     # allow all incoming
```

### Motif DROP sécurisé {#safe-drop-pattern}

```bash
# ALWAYS allow SSH before setting DROP policy
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -P INPUT DROP
```

## Schémas de règles courants {#common-rule-patterns}

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

## Sauvegarde et restauration {#saving-and-restoring}

```bash
sudo iptables-save > ~/iptables_config        # save to file
sudo iptables-restore < ~/iptables_config     # restore from file

# Persistent across reboots (Debian/Ubuntu)
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

## nftables (alternative moderne) {#nftables-modern-alternative}

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

## Utilitaires réseau {#network-utilities}

```bash
hostname -I         # local IP addresses
ip a                # network interfaces and IPs
```

## Pièges courants {#gotchas}

- Définir `INPUT DROP` sans avoir d'abord autorisé SSH **vous verrouille hors** des serveurs distants
- Les règles sont ordonnées : `-I` (insert) ajoute en haut, `-A` (append) ajoute en bas
- `DROP` ne renvoie aucune réponse (l'attaquant ne sait pas que le port existe) ; `REJECT` renvoie une erreur
- `iptables -F` vide les règles mais NE réinitialise PAS les politiques par défaut
- IPv6 nécessite des règles `ip6tables` séparées
- nftables est l'avenir : iptables est obsolète sur les noyaux récents

## Voir aussi {#see-also}

- [[ssh-remote-access]] - Ouverture du port SSH, fail2ban
- [[linux-security]] - Vue d'ensemble de la sécurité réseau
- [[logging-and-journald]] - Journalisation du pare-feu
