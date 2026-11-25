---
level: 3
source_sha256: efdf788b658ebb13062d71bda4d8c1cefe66662fa8faae0459a038475f85874d
translation: machine
translated_at: '2026-10-24'
---
# Architecture de tunnel pour l'exposition de services privés {#tunnel-architecture-for-private-service-exposure}

Exposition de services hébergés sur VM ou derrière NAT vers l'internet public, sans ouvrir de ports entrants sur le pare-feu. Couvre cloudflared, WireGuard, frp/rathole, Tailscale Funnel et les schémas autossh.

## Points clés {#key-facts}

- Toutes les options ci-dessous évitent l'ouverture de ports entrants : le trafic sort du réseau privé et se termine sur un relais ou un nœud de bord. Voir [[datacenter-network-design]] pour le contexte de la couche sous-jacente.
- cloudflared utilise QUIC sur UDP/7844 (repli sur HTTP/2 sur TCP/443) ; WireGuard fonctionne uniquement en UDP.
- Seuil de dégradation (cloudflared) : le taux d'échec doit descendre sous **0,1 % sur 30 sondes consécutives** avant la récupération de l'état dégradé ; une **hystérésis de 30 minutes** s'applique après la récupération.
- `PersistentKeepalive=25` de WireGuard envoie environ 5 octets/s par pair, ce qui suffit à maintenir la plupart des correspondances NAT.
- **Limite stricte** de Tailscale Funnel : seuls les noms d'hôte `*.ts.net` sont acceptés ; les domaines personnalisés ne sont pas pris en charge (demande de fonctionnalité ouverte depuis 2022, toujours non résolue en 2026).
- **Limite de ports** de Tailscale Funnel : seuls les ports 443, 8443 et 10000 sont exposés à l'extérieur.
- Le fichier d'identifiants cloudflared (`.json`) est un **secret statique** : toute personne ayant un accès en lecture peut lancer un tunnel répliqué (MITM sur tous les noms d'hôte liés à ce tunnel).
- autossh nécessite `-M 0`, `ServerAliveInterval` et `ExitOnForwardFailure=yes` ; sans `ExitOnForwardFailure`, la connexion SSH peut rester bloquée indéfiniment sans qu'autossh la redémarre.
- frp v0.68.x est stable ; la réécriture v2 (`0.68+`) est en développement actif, avec des ruptures par rapport au format de configuration v1.
- rathole (Rust) surpasse frp à fort débit : à 4000 QPS, frp génère des erreurs alors que rathole reste stable. La différence est négligeable en dessous de 10 utilisateurs simultanés.

## Comparaison des options {#option-comparison}

| Outil | Transport | Domaine personnalisé | Fiabilité | SSO | Note de sécurité |
|-------|-----------|----------------------|-----------|-----|------------------|
| cloudflared (sur hôte relais) | QUIC/UDP-7844, repli HTTP/2 | Oui (DNS Cloudflare) | Élevée : chemin réseau d'hôte stable, session QUIC unique | CF Access (gratuit, Google/e-mail) | Fichier d'identifiants sur l'hôte relais : accès en lecture = MITM par réplique |
| cloudflared (sidecar par service) | QUIC/UDP-7844 | Oui | Faible : anti-pattern selon la documentation CF ; N sessions × le même mode de défaillance | CF Access par tunnel | N fichiers d'identifiants = surface d'attaque multipliée par N |
| WireGuard (comme sous-couche VPN) | UDP (port configurable) | Via proxy relais | Élevée : cryptographie sans état, résistante au roaming | Dépend du proxy amont | Chiffre tout le transit ; l'hôte ne voit que de l'UDP chiffré |
| frp v0.68 | TCP ou HTTP(S) | Oui (démultiplexage SNI) | Moyenne à élevée : mature, chemin direct | Authelia/oauth2-proxy (sur mesure) | Port TCP exposé sur internet ; IP d'origine visible en cas de mauvaise configuration |
| rathole | TCP | Oui (démultiplexage SNI) | Élevée : Rust, latence plus faible que frp à grande échelle | Authelia/oauth2-proxy (sur mesure) | Identique à frp ; binaire plus petit (~500 KiB) |
| Tailscale Funnel | STUN + relais DERP | **Non** : `*.ts.net` uniquement | Moyenne : infrastructure DERP ; limites de bande passante non documentées | ACL Tailscale (IdP Google/GitHub) | Pas de domaine personnalisé : **bloquant majeur** pour la plupart des usages en production |
| autossh + nginx | SSH (TCP/22 ou port personnalisé) | Oui (vhost nginx) | Élevée : SSH fonctionne à travers tout NAT ou pare-feu | Authelia/oauth2-proxy (sur mesure) | Cryptographie SSH robuste ; blocage en tête de file (head-of-line blocking) sur TCP partagé |

## Architecture recommandée {#recommended-architecture}

### Principale : cloudflared sur VPS adjacent + WireGuard VM↔VPS {#primary-cloudflared-on-adjacent-vps-wireguard-vmvps}

```text
[Public users]
      |
      | HTTPS
      v
[Cloudflare Edge]
      |
      | QUIC (UDP 7844) / HTTP2 (TCP 443)
      v
[VPS — cloudflared + wg0 server]   10.99.0.1
      |
      | WireGuard (UDP 51820) — encrypted
      v
[VM behind NAT — wg0 client]       10.99.0.2
      |
      | localhost HTTP
      v
[Services: Jupyter :8888, ComfyUI :8189, filebrowser :8000]
```

**Pourquoi** : cloudflared s'exécute sur le réseau d'un VPS stable (aucune couche NAT entre lui et Cloudflare). Le chemin instable VM↔internet est porté par WireGuard, qui gère avec souplesse le roaming et les pertes de paquets temporaires (cryptographie sans état ; le handshake reprend en 1 à 2 s après la restauration du chemin). Les identifiants du tunnel résident sur le VPS, et non sur un hôte où des tiers disposent d'un accès shell.

**WireGuard : VPS (`/etc/wireguard/wg0.conf`) :**

```ini
[Interface]
Address = 10.99.0.1/24
ListenPort = 51820
PrivateKey = <vps-private-key>

[Peer]
# VM client
PublicKey = <vm-public-key>
AllowedIPs = 10.99.0.2/32
```

**WireGuard : VM (`/etc/wireguard/wg0.conf`) :**

```ini
[Interface]
Address = 10.99.0.2/32
PrivateKey = <vm-private-key>

[Peer]
# VPS
PublicKey = <vps-public-key>
Endpoint = vps.example.com:51820
AllowedIPs = 10.99.0.1/32
PersistentKeepalive = 25
```

Activer sur les deux nœuds :

```bash
wg-quick up wg0
systemctl enable wg-quick@wg0
```

**cloudflared : VPS (`/etc/cloudflared/config.yml`) :**

```yaml
tunnel: <tunnel-uuid>
credentials-file: /etc/cloudflared/<tunnel-uuid>.json
ingress:
  - hostname: dev.example.com
    service: http://10.99.0.2:8888
  - hostname: app.example.com
    service: http://10.99.0.2:8189
  - hostname: files.example.com
    service: http://10.99.0.2:8000
  - service: http_status:404
```

```bash
# Install and enable
cloudflared service install
systemctl enable --now cloudflared
# Restrict credentials file
chmod 0400 /etc/cloudflared/<tunnel-uuid>.json
chown cloudflared:cloudflared /etc/cloudflared/<tunnel-uuid>.json
```

**Vérifications préalables avant d'adopter cette architecture :**

```bash
# 1. Verify UDP outbound from VM is not blocked
nc -u <vps-ip> 51820 <<< "test"

# 2. Verify cloudflared tunnel health after 30 min
cloudflared tunnel info <tunnel-uuid>
# expect: "Status: healthy", not "degraded"

# 3. Check WireGuard handshake
wg show wg0 latest-handshakes
# expect: timestamp within last 30 s
```

### Solution de repli : autossh + nginx + Authelia (UDP bloqué) {#fallback-autossh-nginx-authelia-udp-blocked}

À utiliser lorsque le réseau bloque l'UDP sortant vers le port WireGuard. SSH/TCP est presque universellement autorisé.

**Service systemd : VM (`/etc/systemd/system/autossh-tunnel.service`) :**

```ini
[Unit]
Description=autossh reverse tunnel to VPS
After=network.target
Wants=network-online.target

[Service]
User=tunnel
Environment="AUTOSSH_GATETIME=0"
ExecStart=/usr/bin/autossh -M 0 \
  -o "ServerAliveInterval=60" \
  -o "ServerAliveCountMax=3" \
  -o "ExitOnForwardFailure=yes" \
  -o "StrictHostKeyChecking=accept-new" \
  -N \
  -R 18888:localhost:8888 \
  -R 18189:localhost:8189 \
  -R 18000:localhost:8000 \
  -i /etc/tunnel/id_ed25519 \
  tunnel@vps.example.com
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**nginx : VPS (`/etc/nginx/sites-available/dev.example.com`) :**

```nginx
server {
    listen 443 ssl;
    server_name dev.example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Authelia auth endpoint
    include /etc/nginx/snippets/authelia-location.conf;

    location / {
        include /etc/nginx/snippets/authelia-authrequest.conf;
        proxy_pass http://127.0.0.1:18888;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

Renouvellement du certificat Let's Encrypt :

```bash
certbot --nginx -d dev.example.com -d app.example.com -d files.example.com
systemctl enable --now certbot.timer
```

## Pièges courants {#gotchas}

- **Problème :** cloudflared exécuté dans une VM KVM/QEMU n'atteint qu'un taux de réussite de 6 % des ressources, malgré un WAN d'hôte stable. **Correction :** déplacer cloudflared sur l'hôte de la VM ou sur un VPS externe ; la session QUIC ne doit pas traverser une frontière NAT/virbr0. Le seuil de 0,1 %/30 sondes signifie que même de brèves réinitialisations NAT déclenchent une pénalité de dégradation de 30 minutes. Seul le passage à un chemin réseau stable résout durablement le problème ; aucun paramètre de réglage à l'intérieur de la VM ne suffit.

- **Problème :** motif sidecar cloudflared par service (un tunnel par conteneur ou service). **Correction :** utiliser une seule instance cloudflared adjacente pointant vers plusieurs noms d'hôte. Le guide officiel de déploiement Kubernetes déconseille explicitement les tunnels sidecar : « each cloudflared replica/pod can reach all Kubernetes services; there is no need for a dedicated tunnel per pod ». Les sessions multiples démultiplient le même mode de défaillance et multiplient la surface d'attaque liée aux identifiants.

- **Problème :** Tailscale Funnel ne peut pas servir `*.yourdomain.com`. **Correction :** aucune au sein de Tailscale Funnel ; la prise en charge des domaines personnalisés est une demande de fonctionnalité ouverte de longue date (issue GitHub `tailscale/tailscale#11563`). Utiliser cloudflared, autossh+nginx ou frp si des domaines personnalisés sont requis. Tailscale (sans Funnel) reste utile pour un accès interne uniquement sur `*.ts.net`.

- **Problème :** le fichier d'identifiants cloudflared (`<uuid>.json`) est un secret statique de type bearer. Toute personne ayant un accès en lecture au système de fichiers de l'hôte exécutant cloudflared peut lancer sa propre instance cloudflared et intercepter tout le trafic destiné aux noms d'hôte liés à ce tunnel. **Correction :** exécuter cloudflared sous un utilisateur dédié à faibles privilèges, avec `chmod 0400` sur le fichier d'identifiants. Si l'hôte est partagé avec des administrateurs non fiables, déplacer cloudflared sur un VPS distinct où les identifiants sont isolés (voir l'architecture recommandée ci-dessus). Remarque : `sudo` contourne trivialement les permissions de fichiers ; la séparation physique des hôtes est la seule mesure d'atténuation fiable.

- **Problème :** autossh reste bloqué indéfiniment. La connexion semble active au niveau TCP, mais la vivacité au niveau SSH est morte, donc autossh ne la redémarre pas. **Correction :** toujours définir `-M 0` (désactive le port de surveillance propre d'autossh et s'appuie sur le keepalive natif de SSH) avec `ServerAliveInterval=60 ServerAliveCountMax=3 ExitOnForwardFailure=yes`. Sans `ExitOnForwardFailure=yes`, un échec de liaison de redirection supprime silencieusement le port redirigé alors que la session SSH reste active ; autossh voit une connexion vivante et ne la redémarre jamais.

- **Problème :** WireGuard échoue derrière un NAT agressif (la connexion tombe après 1 à 2 minutes d'inactivité). **Correction :** abaisser `PersistentKeepalive` de 25 à 15 secondes. La valeur par défaut de 25 s convient à la plupart des équipements NAT, mais certains NAT d'entreprise ou mobiles expirent les correspondances UDP plus vite. Le surcoût de `PersistentKeepalive` est d'environ 5 octets/seconde par pair, quel que soit le réglage.

## Voir aussi {#see-also}

- [[datacenter-network-design]] : réseau sous-jacent, overlays VXLAN, conception de fabric BGP
- [[linux-server-administration]] : unités de service systemd, nftables, installation de WireGuard
- [[sre-principles]] : budgets de taux d'échec, hystérésis, schémas de récupération depuis un état dégradé
- Documentation des tunnels cloudflared : https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/
- Dépannage de la santé des tunnels cloudflared : https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-wan/troubleshooting/tunnel-health/
- Démarrage rapide WireGuard : https://www.wireguard.com/quickstart/
- Comparaison rathole et frp : https://github.com/rapiz1/rathole
- Tunnels persistants avec autossh : https://raymii.org/s/tutorials/Autossh_persistent_tunnels.html
- Domaine personnalisé pour Tailscale Funnel (demande ouverte) : https://github.com/tailscale/tailscale/issues/11563
