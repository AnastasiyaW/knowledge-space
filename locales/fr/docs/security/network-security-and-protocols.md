---
title: "Sécurité réseau et protocoles"
category: concepts
tags: [security, networking, osi, tcp-ip, dns, dhcp, vpn, firewall]
level: 3
source_sha256: eb064525297a1f2f65234655e88efa251c46d6c096092822e27a62f90ee73e55
translation: machine
translated_at: '2026-10-24'
---
# Sécurité réseau et protocoles {#network-security-and-protocols}

Fondamentaux des réseaux du point de vue de la sécurité : modèle OSI, pile TCP/IP, mécanismes DNS, DHCP, technologies VPN (OpenVPN, WireGuard) et authentification des e-mails (SPF/DKIM/DMARC).

## Points clés {#key-facts}
- Modèle OSI : Physique, Liaison de données, Réseau, Transport, Session, Présentation, Application
- TCP est fiable et ordonné ; UDP est rapide et sans connexion
- Plages d'adresses IP privées : 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
- Résolution DNS : cache du client -> /etc/hosts -> cache du résolveur -> racine -> TLD -> serveur faisant autorité
- WireGuard est plus simple, plus rapide et plus facile à auditer qu'OpenVPN (4000 LOC contre plus de 100K)
- SPF + DKIM + DMARC, utilisés ensemble, préviennent l'usurpation d'e-mails

## Modèle OSI (aspects pertinents pour la sécurité) {#osi-model-security-relevant}
| Couche | Nom | Préoccupation de sécurité |
|-------|------|-----------------|
| 7 | Application | Attaques HTTP, DNS, SMTP, WAF |
| 4 | Transport | TCP/UDP, scan de ports, SYN floods |
| 3 | Réseau | Usurpation d'IP, attaques de routage, pare-feux |
| 2 | Liaison de données | Usurpation ARP, MAC flooding, 802.1X |
| 1 | Physique | Écoute physique (wiretapping), accès physique |

## TCP/IP {#tcpip}

### Three-Way Handshake {#tcp-three-way-handshake}

TCP établit une connexion fiable avant tout transfert de données, en trois étapes :

```php
Client                    Server
  |--- SYN (seq=x) ------->|     Step 1: Client sends SYN with random sequence number
  |<-- SYN-ACK (seq=y, -----|     Step 2: Server responds with SYN-ACK, acknowledges x+1
  |    ack=x+1)             |
  |--- ACK (ack=y+1) ----->|     Step 3: Client acknowledges, connection established
```

**Implications pour la sécurité** :
- **Attaque par SYN flood** : l'attaquant envoie de nombreux paquets SYN sans jamais achever la poignée de main, épuisant les ressources du serveur. Parades : SYN cookies, limitation de débit
- Le numéro de séquence initial aléatoire empêche le détournement de connexion (des séquences prévisibles ont été exploitées par le passé)
- La fermeture de connexion utilise un échange FIN en quatre étapes (FIN -> ACK -> FIN -> ACK)

### TCP vs UDP {#tcp-vs-udp}

| Caractéristique | TCP | UDP |
|---------|-----|-----|
| Livraison | Garantie, ordonnée | Au mieux, non ordonnée |
| Établissement | Trois temps | Aucun |
| Surcharge | Élevée (en-têtes, accusés de réception) | Minimale |
| Cas d'usage | HTTP, SSH, e-mail, transfert de fichiers | DNS, VoIP, streaming, jeux |
| Connexion | Avec état (stateful) | Sans état (stateless) |

### Routage et tables de routage {#routing-and-route-tables}

Les paquets sont acheminés selon la table de routage, c'est-à-dire un ensemble de règles associant des réseaux de destination à des passerelles de saut suivant :

```bash
# View routing table
ip route show
# or legacy:
route -n

# Typical output:
# default via 192.168.1.1 dev eth0    <- default gateway
# 192.168.1.0/24 dev eth0 scope link  <- directly connected network
# 10.0.0.0/8 via 192.168.1.254 dev eth0  <- static route

# Add static route
ip route add 10.0.0.0/8 via 192.168.1.254 dev eth0

# Delete route
ip route del 10.0.0.0/8
```

**Sélection de route** : la correspondance la plus spécifique l'emporte (préfixe le plus long). Un paquet destiné à 10.1.2.3 correspond à /24 plutôt qu'à /8 si les deux routes existent. Si aucune route spécifique ne correspond, la passerelle par défaut est utilisée.

**Sécurité** : des modifications non autorisées des routes peuvent rediriger le trafic (empoisonnement de routes). Utilisez RPKI/ROA pour valider les routes BGP dans les réseaux de production.

### Sous-réseaux IPv4 (CIDR) {#ipv4-subnetting-cidr}
```text
/24 = 255.255.255.0     = 254 usable hosts
/25 = 255.255.255.128   = 126 usable hosts
/26 = 255.255.255.192   = 62 usable hosts
/16 = 255.255.0.0       = 65534 usable hosts
```

### IPv6 {#ipv6}
- Adresses sur 128 bits : `2001:0db8:85a3::8a2e:0370:7334`
- Lien local : `fe80::/10` ; unicast global : `2000::/3`
- Prise en charge native d'IPsec dans les en-têtes du protocole
- Les environnements en double pile (dual-stack) créent une surface supplémentaire de fingerprinting
- Beaucoup d'outils de sécurité ne prennent pas encore pleinement en charge IPv6

### Routage {#routing}
```bash
ip route show
ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0
ip route add default via 192.168.1.1
traceroute example.com
mtr example.com          # Combined ping + traceroute
```

## DNS {#dns}

### Types d'enregistrements {#record-types}
| Enregistrement | Rôle |
|--------|---------|
| A / AAAA | Nom d'hôte vers IPv4 / IPv6 |
| MX | Serveur de messagerie (avec priorité) |
| CNAME | Alias vers un autre nom d'hôte |
| TXT | Enregistrements texte (SPF, DKIM, vérification) |
| PTR | DNS inverse (IP vers nom d'hôte) |
| NS | Serveur de noms du domaine |
| SOA | Métadonnées de zone (serial, refresh, retry) |
| SRV | Localisation de services (AD, SIP) |

### Exemple de fichier de zone {#zone-file-example}
```text
$TTL 3600
@    IN SOA  ns1.example.com. admin.example.com. (2024010101 3600 600 86400 3600)
@    IN NS   ns1.example.com.
@    IN A    93.184.216.34
www  IN A    93.184.216.34
@    IN MX   10 mail.example.com.
@    IN TXT  "v=spf1 mx -all"
```

### Sécurité du DNS {#dns-security}
- Les transferts de zone (AXFR) doivent être restreints aux seuls serveurs secondaires autorisés
- DNSSEC signe les enregistrements DNS pour empêcher toute altération
- DNS-over-HTTPS (DoH) et DNS-over-TLS (DoT) chiffrent les requêtes DNS

## Authentification des e-mails {#email-authentication}
- **SPF** - enregistrement TXT DNS listant les adresses IP des serveurs de messagerie autorisés
- **DKIM** - signature cryptographique dans les en-têtes de l'e-mail (prouve l'intégrité du message)
- **DMARC** - politique de traitement des échecs SPF/DKIM (none/quarantine/reject)

## VPN {#vpn}

### OpenVPN {#openvpn}
```bash
# Server setup with easy-rsa for PKI
apt install openvpn easy-rsa
# Config: /etc/openvpn/server.conf
# Uses TLS for control channel, symmetric encryption for data
```

### WireGuard {#wireguard}
```bash
apt install wireguard
wg genkey | tee privatekey | wg pubkey > publickey

# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server_private_key>
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32

wg-quick up wg0
```

## DHCP {#dhcp}
```css
# /etc/dhcp/dhcpd.conf
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    default-lease-time 600;
}
```
Sécurité : attaque par épuisement DHCP (saturation du pool), faux serveur DHCP (MITM). Défense : DHCP snooping sur les commutateurs administrables.

## SNMP {#snmp}
- v1/v2c : chaînes de communauté en clair (en pratique, des mots de passe)
- v3 : authentification et chiffrement (toujours utiliser v3)
- SNMP exposé = configuration complète de l'équipement exposée

## Boîte à outils de diagnostic réseau {#network-diagnostics-toolkit}

Utilitaires essentiels pour vérifier la connectivité et diagnostiquer les pannes :

### ping - Accessibilité ICMP {#ping-icmp-reachability}
```bash
# Basic connectivity check
ping -c 5 example.com

# Specify interface
ping -c 3 -I eth0 192.168.1.1

# Large packet test (MTU/fragmentation issues)
ping -c 3 -s 1400 example.com
```

**Interprétation :**
- `Destination Host Unreachable` - problème de routage, vérifiez la passerelle par défaut
- `Request timed out` - l'hôte est arrêté ou l'ICMP est bloqué
- Perte de paquets > 0 % - connexion instable ou congestion
- Variation du RTT - gigue réseau, vérifiez les sauts intermédiaires

**Limite :** de nombreux hôtes bloquent l'ICMP. Un ping échoué ne prouve pas que l'hôte est arrêté.

### traceroute - Découverte du chemin {#traceroute-path-discovery}
```bash
# Trace route to destination (max 30 hops)
traceroute -m 30 example.com

# Use TCP instead of UDP (better firewall traversal)
traceroute -T -p 443 example.com
```

Affiche chaque saut de routeur entre la source et la destination. Les astérisques (`* * *`) indiquent les sauts qui ne répondent pas ; c'est normal pour les routeurs configurés pour ne pas renvoyer les messages ICMP TTL-exceeded.

### dig / nslookup - Vérification DNS {#dig-nslookup-dns-verification}
```bash
# Query default resolver
dig example.com

# Query specific nameserver
dig @1.1.1.1 example.com

# Reverse DNS lookup
dig -x 8.8.8.8

# Check a specific record type
dig example.com MX
dig example.com TXT
```

```bash
# nslookup equivalent
nslookup example.com
nslookup example.com 8.8.8.8  # query specific server
nslookup -type=PTR 8.8.8.8    # reverse lookup
```

**Usage pratique :** après la migration d'un domaine vers un nouveau serveur, interrogez plusieurs serveurs DNS publics pour vérifier la propagation :
```bash
for ns in 1.1.1.1 8.8.8.8 77.88.8.8; do
    echo "=== $ns ===" && dig @$ns example.com +short
done
```

## Pièges courants {#gotchas}
- IPv6 peut divulguer des informations réelles sur le réseau même lorsque IPv4 passe par le VPN
- Les requêtes DNS ne sont pas chiffrées par défaut : le FAI ou l'administrateur réseau peut voir tous les domaines consultés
- WireGuard ne gère pas le NAT traversal dans toutes les configurations par défaut
- Les journaux DHCP associent les attributions d'IP aux adresses MAC et aux noms d'hôte, ce qui est crucial pour l'analyse d'incidents
- Les chaînes de communauté SNMPv1/v2c sont souvent « public » / « private » par défaut

## Voir aussi {#see-also}
- [[firewall-and-ids-ips]] - iptables, Snort, Suricata
- [[network-traffic-analysis]] - tcpdump, Wireshark, nmap
- [[linux-system-hardening]] - paramètres réseau sysctl
- [[cryptography-and-pki]] - certificats TLS, PKI
