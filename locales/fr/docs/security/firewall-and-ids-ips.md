---
title: "Pare-feux et IDS/IPS"
category: tools
tags: [security, firewall, iptables, ids, ips, snort, suricata, waf]
level: 3
source_sha256: 0c5604db383747a88091cf3a2244f0213e2b39fe661b37a5e6115444a9b5bfc7
translation: machine
translated_at: '2026-10-24'
---
# Pare-feux et IDS/IPS {#firewalls-and-idsips}

Contrôles de sécurité au niveau réseau et applicatif : iptables/ufw pour les pare-feux Linux, Pare-feu Windows Defender, Snort et Suricata pour la détection/prévention d'intrusion, et WAF (ModSecurity, WAF cloud) pour la protection des applications web.

## Points clés {#key-facts}
- Un IDS détecte et alerte ; un IPS détecte et bloque en ligne
- La détection par signatures est rapide et précise pour les attaques connues, mais ne détecte pas les attaques zero-day
- La détection par anomalies repère les attaques inédites, mais génère davantage de faux positifs
- Suricata est multi-thread (plus rapide que Snort) et compatible avec les règles Snort
- Un WAF doit d'abord fonctionner en mode détection avant d'activer le blocage, afin d'ajuster les faux positifs
- La politique par défaut d'iptables devrait être DROP pour INPUT, ACCEPT pour OUTPUT

## iptables (Linux) {#iptables-linux}

### Configuration de base {#basic-setup}
```bash
# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH, HTTP, HTTPS
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Drop invalid packets
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

# Rate limiting (SSH brute force protection)
iptables -A INPUT -p tcp --dport 22 -m limit --limit 3/min --limit-burst 3 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP

# NAT masquerading
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Logging dropped packets
iptables -A INPUT -j LOG --log-prefix "DROPPED: "

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### ufw (Uncomplicated Firewall) {#ufw-uncomplicated-firewall}
```bash
ufw enable
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow from 192.168.1.0/24 to any port 3306
ufw status verbose
```

## Pare-feu Windows {#windows-firewall}
```powershell
# View enabled rules
Get-NetFirewallRule | Where-Object {$_.Enabled -eq 'True'} |
    Select-Object DisplayName, Direction, Action

# Create rule
New-NetFirewallRule -DisplayName "Block Telnet" -Direction Inbound `
    -Protocol TCP -LocalPort 23 -Action Block

# Enable/disable
Enable-NetFirewallRule -DisplayName "Block Telnet"
Disable-NetFirewallRule -DisplayName "Block Telnet"
```
Profils : Domaine, Privé, Public. Géré via l'interface graphique `wf.msc` ou PowerShell.

## Architecture des pare-feux réseau {#network-firewall-architecture}

### Topologies de déploiement {#deployment-topologies}

Deux approches fondamentales de placement du pare-feu :

1. **Pare-feu basé sur l'hôte** : installé sur chaque hôte. Chaque serveur/poste de travail exécute son propre pare-feu (iptables, Pare-feu Windows). Doit être configuré hôte par hôte ou automatisé via Ansible/Puppet
2. **Pare-feu réseau** : appareil unique protégeant un segment de réseau entier. Filtre le trafic de transit entre les zones. Configuré une seule fois pour l'ensemble du réseau

**Topologie d'entreprise standard** : le pare-feu se situe entre la liaison Internet et le LAN (réseau des serveurs/postes de travail). Tout le trafic doit transiter par le pare-feu, qui peut être combiné avec le routeur.

### Zones réseau {#network-zones}

```text
Internet
    |
[Firewall/Router]
    |           |
  [DMZ]       [LAN]
  (web,mail)  (internal servers, workstations)
```

- **DMZ (zone démilitarisée)** : hôtes accessibles depuis Internet (serveurs web, messagerie). Le pare-feu autorise le trafic entrant vers la DMZ mais bloque le trafic de la DMZ vers le LAN
- **LAN** : réseau interne. Le pare-feu bloque tout le trafic entrant depuis Internet et autorise le trafic sortant
- **Zone de gestion** : VLAN dédié aux interfaces de gestion du pare-feu et du routeur

### IPSet pour une gestion efficace des règles {#ipset-for-efficient-rule-management}

IPSet crée des ensembles nommés d'adresses IP, de réseaux ou de ports, référençables dans les règles iptables. Bien plus efficace que des règles individuelles pour les grandes listes de blocage :

```bash
# Create a set for blocked IPs
ipset create blocklist hash:ip

# Add entries
ipset add blocklist 203.0.113.5
ipset add blocklist 198.51.100.0/24

# Reference in iptables
iptables -A INPUT -m set --match-set blocklist src -j DROP

# List set contents
ipset list blocklist

# Save/restore (persistent across reboots)
ipset save > /etc/ipset.conf
ipset restore < /etc/ipset.conf
```

**Performance** : avec iptables et 10 000 règles IP individuelles, le coût est O(n) par paquet. Avec IPSet et 10 000 IP, la recherche par table de hachage est en O(1). Pour les grandes listes de blocage (blocage géographique, flux de renseignements sur les menaces), IPSet est indispensable.

### Parcours du trafic dans le pare-feu {#traffic-flow-through-firewall}

Ordre de traversée des paquets dans iptables/netfilter :

```php
Incoming -> PREROUTING (NAT/mangle) -> routing decision
  -> INPUT (for firewall itself)
  -> FORWARD (transit traffic to other hosts)
Outgoing -> OUTPUT -> POSTROUTING (NAT/masquerade)
```

Pour un pare-feu réseau, la plupart des règles se placent dans la chaîne FORWARD (trafic de transit). La chaîne INPUT protège l'hôte du pare-feu lui-même.

### NAT ou masquerading {#nat-vs-masquerading}

Deux méthodes pour partager une IP publique avec un LAN :

| Caractéristique | NAT (SNAT) | Masquerading |
|---------|-----------|--------------|
| Type d'IP | Statique | Dynamique (DHCP/PPPoE) |
| Syntaxe de règle | `--to-source <IP>` | `-j MASQUERADE` |
| Performance | Meilleure (mise en cache) | Légère surcharge |
| Utilisation | Serveur avec IP fixe | Domicile/VPN avec IP dynamique |

```bash
# NAT with static IP (preferred for servers)
iptables -t nat -A POSTROUTING -s 10.0.0.0/16 -j SNAT --to-source 65.108.243.108

# Masquerading with dynamic IP
iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE
```

**Privilégiez toujours le NAT au masquerading lorsque vous disposez d'une IP statique** : il met en cache la correspondance d'adresse source et évite une recherche pour chaque paquet.

### Configuration complète du pare-feu en passerelle {#complete-firewall-setup-for-gateway}

Procédure pas à pas pour une passerelle à deux interfaces protégeant un LAN :

```bash
# 1. Enable IP forwarding (persistent)
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p

# 2. Allow SSH before setting DROP policy (avoid lockout!)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 3. Set default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 4. Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 5. NAT for LAN
iptables -t nat -A POSTROUTING -s 10.0.0.0/16 -j SNAT --to-source <PUBLIC_IP>

# 6. Allow LAN to internet (FORWARD chain)
iptables -A FORWARD -s 10.0.0.0/16 -j ACCEPT
iptables -A FORWARD -d 10.0.0.0/16 -m state --state ESTABLISHED,RELATED -j ACCEPT

# 7. Save rules
iptables-save > /etc/iptables/rules.v4
```

**Ordre critique :** autorisez SSH *avant* de définir la politique DROP. L'inverser vous verrouille immédiatement hors du système.

### Marquage de paquets et routage par politique {#packet-marking-and-policy-routing}

Acheminer le trafic par port avec la table mangle d'iptables et `ip rule` :

```bash
# Mark SSH packets (port 22) with mark 0x2
iptables -t mangle -A PREROUTING -i eth0 -p tcp --dport 22 -j CONNMARK --set-mark 0x2
iptables -t mangle -A OUTPUT -j CONNMARK --restore-mark

# Create routing table 120 for marked packets
ip route add default via 172.31.0.1 dev eth0 table 120

# Route marked packets through table 120
ip rule add fwmark 0x2 lookup 120
```

Cela envoie le trafic SSH via une autre passerelle que le trafic général, ce qui est utile pour le routage fractionné, le contournement de VPN ou l'acheminement du trafic vers des systèmes de supervision.

### Recopie du trafic pour l'IDS {#traffic-mirroring-for-ids}

Rediriger des copies du trafic vers un système d'analyse sans affecter le flux original :

- **Petite échelle** : utiliser iptables mangle pour marquer et mettre en file d'attente les paquets destinés à l'IDS sur le même hôte
- **Grande échelle** : recopier le trafic vers une interface/un hôte distinct avec `tc` (contrôle de trafic) ou DPDK pour un traitement de paquets haute performance
- **Tunnelisation** : encapsuler le trafic recopié dans GRE/VXLAN pour préserver les en-têtes d'origine à travers le réseau

## IDS/IPS {#idsips}

### Types {#types}
- **NIDS/NIPS** : basés sur le réseau, surveillent le trafic en des points stratégiques
- **HIDS/HIPS** : basés sur l'hôte, surveillent l'activité sur chaque hôte
- **Par signatures** : détectent les schémas d'attaque connus
- **Par anomalies** : détection d'écarts par rapport à une référence
- **Hybride** : combine les deux approches

### Règles Snort {#snort-rules}
```bash
# Rule syntax: action protocol src_ip src_port -> dst_ip dst_port (options)
alert tcp any any -> $HOME_NET 80 (msg:"SQL Injection Attempt"; \
    content:"UNION SELECT"; nocase; sid:1000001; rev:1;)

alert tcp any any -> $HOME_NET 22 (msg:"SSH Brute Force"; \
    flow:to_server; threshold:type both, track by_src, count 5, seconds 60; \
    sid:1000002; rev:1;)
```

Composants d'une règle : action `alert`/`drop`/`log`, protocole, source/destination, correspondance de chaîne `content`, expression régulière `pcre`, direction `flow`, seuil de débit `threshold`, identifiant unique `sid`.

### Suricata {#suricata}
Alternative moderne et multi-thread à Snort :
- Compatible avec les règles Snort
- Journalisation au format EVE JSON (intégration SIEM plus simple)
- Analyse de protocoles intégrée (HTTP, TLS, DNS, SMB)
- Capacité d'extraction de fichiers
- Meilleures performances sur les systèmes multi-cœurs

## WAF (Web Application Firewall) {#waf-web-application-firewall}

### ModSecurity {#modsecurity}
```markdown
# Rule examples
SecRule REQUEST_URI "@contains /admin" \
    "id:1001,phase:1,deny,status:403,msg:'Admin access blocked'"

SecRule ARGS "@detectSQLi" \
    "id:1002,phase:2,deny,status:403,msg:'SQL Injection detected'"
```
- **OWASP Core Rule Set (CRS)** : jeu de règles par défaut complet
- Modes : détection seule (journalisation) ou blocage (refus)

### WAF cloud {#cloud-wafs}
- **AWS WAF** : s'intègre à CloudFront, ALB et API Gateway
- **Cloudflare WAF** : en périphérie, jeux de règles gérés
- **Azure Front Door WAF** : WAF cloud de Microsoft
- Fonctionnalités : mises à jour des règles gérées, règles personnalisées, limitation de débit, détection de bots

## Pièges à éviter {#gotchas}
- Les faux positifs d'un IPS peuvent bloquer du trafic légitime : commencez toujours en mode détection
- Snort est mono-thread ; Suricata convient mieux aux réseaux à fort débit
- Des techniques de contournement de WAF existent pour la plupart des signatures (encodage, fragmentation, variation de casse)
- Les règles iptables sont évaluées dans l'ordre : placez en tête les règles les plus sollicitées pour de meilleures performances
- ufw est une interface graphique d'iptables : les deux ne peuvent pas être gérés indépendamment sans conflits
- Un WAF cloud ajoute de la latence mais dispense de la maintenance des règles

## Voir aussi {#see-also}
- [[network-security-and-protocols]] : fondamentaux réseau sous-jacents
- [[network-traffic-analysis]] : tcpdump, Wireshark
- [[web-application-security-fundamentals]] : attaques contre lesquelles les WAF protègent
- [[siem-and-incident-response]] : corrélation des alertes IDS/IPS
