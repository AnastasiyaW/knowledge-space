---
level: 3
source_sha256: efdf788b658ebb13062d71bda4d8c1cefe66662fa8faae0459a038475f85874d
translation: machine
translated_at: '2026-10-24'
---
Note: the input has no YAML front matter, so nothing to translate there. Code placeholders CODE_0 through CODE_9 must be kept as is.

Let me produce the translation now.

# Tunnel-Architektur für die Bereitstellung privater Dienste {#tunnel-architecture-for-private-service-exposure}

Bereitstellung von VM-gehosteten oder per NAT angebundenen Diensten im öffentlichen Internet, ohne eingehende Firewall-Ports zu öffnen. Behandelt werden cloudflared, WireGuard, frp/rathole, Tailscale Funnel und autossh-Muster.

## Wichtige Fakten {#key-facts}

- Alle nachfolgenden Optionen vermeiden die Exposition eingehender Ports: Der Datenverkehr verlässt das private Netzwerk ausgehend und endet an einem Relay- oder Edge-Knoten — Kontext zur Underlay-Ebene siehe [[datacenter-network-design]]
- cloudflared verwendet QUIC über UDP/7844 (Fallback auf HTTP/2 über TCP/443); WireGuard ist ausschließlich UDP
- Schwellenwert für den Degraded-Zustand (cloudflared): Die Fehlerrate muss über **30 aufeinanderfolgende Probes** unter **0,1 %** fallen, bevor der Zustand Degraded verlassen wird; nach der Erholung gilt eine **Hysterese von 30 Minuten**
- WireGuard `PersistentKeepalive=25` sendet ca. 5 Byte/s pro Peer; das reicht aus, um die meisten NAT-Zuordnungen aufrechtzuerhalten
- Tailscale Funnel **harte Grenze**: nur `*.ts.net`-Hostnamen; eigene Domains werden nicht unterstützt (offener Feature-Request seit 2022, Stand 2026 ungelöst)
- Tailscale Funnel **Port-Beschränkung**: nach außen werden nur 443, 8443 und 10000 freigegeben
- Die cloudflared-Credentials-Datei (`.json`) ist ein **statisches Geheimnis**: Wer Lesezugriff darauf hat, kann einen Replica-Tunnel starten (MITM auf allen Hostnamen, die an diesen Tunnel gebunden sind)
- autossh benötigt `-M 0` + `ServerAliveInterval` + `ExitOnForwardFailure=yes`; ohne `ExitOnForwardFailure` kann die SSH-Verbindung dauerhaft hängen, ohne dass autossh sie neu startet
- frp v0.68.x ist stabil; die v2-Neuentwicklung (`0.68+`) ist in aktiver Entwicklung und enthält Breaking Changes gegenüber dem v1-Konfigurationsformat
- rathole (Rust) übertrifft frp bei hohen QPS-Werten; bei 4000 QPS liefert frp Fehler, während rathole stabil bleibt — bei weniger als 10 gleichzeitigen Nutzern ist der Unterschied vernachlässigbar

## Vergleich der Optionen {#option-comparison}

| Tool | Transport | Eigene Domain | Zuverlässigkeit | SSO | Sicherheitshinweis |
|------|-----------|--------------|-----------------|-----|---------------------|
| cloudflared (auf Relay-Host) | QUIC/UDP-7844, Fallback HTTP/2 | Ja (Cloudflare DNS) | Hoch — stabiler Netzwerkpfad des Hosts, einzelne QUIC-Session | CF Access (kostenlos, Google/E-Mail) | Credentials-Datei auf dem Relay-Host: Lesezugriff = Replica-MITM |
| cloudflared (Sidecar pro Dienst) | QUIC/UDP-7844 | Ja | Niedrig — laut CF-Dokumentation ein Anti-Pattern; N Sessions × gleicher Fehlerfall | CF Access pro Tunnel | N Credentials-Dateien = N-fache Angriffsfläche |
| WireGuard (als VPN-Underlay) | UDP (konfigurierbarer Port) | Über Relay-Proxy | Hoch — zustandslose Kryptografie, roaming-resistent | Abhängig vom vorgelagerten Proxy | Verschlüsselt den gesamten Transit; der Host sieht nur verschlüsseltes UDP |
| frp v0.68 | TCP oder HTTP(S) | Ja (SNI-Demux) | Mittel bis hoch — ausgereift, direkter Pfad | Authelia/oauth2-proxy (selbst zu konfigurieren) | Offener TCP-Port im Internet; Origin-IP sichtbar bei Fehlkonfiguration |
| rathole | TCP | Ja (SNI-Demux) | Hoch — Rust, geringere Latenz als frp im großen Maßstab | Authelia/oauth2-proxy (selbst zu konfigurieren) | Wie frp; kleineres Binary (~500 KiB) |
| Tailscale Funnel | STUN + DERP-Relay | **Nein** — nur `*.ts.net` | Mittel — DERP-Infrastruktur; undokumentierte Bandbreitenlimits | Tailscale ACL (Google/GitHub IdP) | Keine eigene Domain: **harter Ausschlussgrund** für die meisten produktiven Einsätze |
| autossh + nginx | SSH (TCP/22 oder benutzerdefiniert) | Ja (nginx-vhost) | Hoch — SSH funktioniert durch jedes NAT/jede Firewall | Authelia/oauth2-proxy (selbst zu konfigurieren) | SSH-Kryptografie ist stark; Head-of-Line-Blocking auf gemeinsamer TCP-Verbindung |

## Empfohlene Architektur {#recommended-architecture}

### Primär: cloudflared auf benachbartem VPS + WireGuard VM↔VPS {#primary-cloudflared-on-adjacent-vps-wireguard-vmvps}

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

**Begründung**: cloudflared läuft in einem stabilen VPS-Netzwerk (zwischen ihm und Cloudflare liegen keine NAT-Ebenen). Der instabile Pfad VM↔Internet wird über WireGuard geführt, das Roaming und vorübergehenden Paketverlust sauber verkraftet (zustandslose Kryptografie; der Handshake wird 1–2 s nach Wiederherstellung des Pfads fortgesetzt). Die Tunnel-Credentials liegen auf dem VPS — nicht auf einem Host, auf den Dritte Shell-Zugriff haben.

**WireGuard — VPS (`/etc/wireguard/wg0.conf`):**

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

**WireGuard — VM (`/etc/wireguard/wg0.conf`):**

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

Auf beiden Knoten aktivieren:

```bash
wg-quick up wg0
systemctl enable wg-quick@wg0
```

**cloudflared — VPS (`/etc/cloudflared/config.yml`):**

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

**Preflight-Prüfungen vor der Entscheidung für diese Architektur:**

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

### Fallback: autossh + nginx + Authelia (UDP blockiert) {#fallback-autossh-nginx-authelia-udp-blocked}

Einsatz, wenn das Netzwerk ausgehendes UDP zum WireGuard-Port blockiert. SSH/TCP ist nahezu überall erlaubt.

**systemd-Dienst — VM (`/etc/systemd/system/autossh-tunnel.service`):**

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

**nginx — VPS (`/etc/nginx/sites-available/dev.example.com`):**

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

Erneuerung des Let's-Encrypt-Zertifikats:

```bash
certbot --nginx -d dev.example.com -d app.example.com -d files.example.com
systemctl enable --now certbot.timer
```

## Stolperfallen {#gotchas}

- **Problem:** cloudflared innerhalb einer KVM/QEMU-VM erreicht trotz stabiler WAN-Verbindung des Hosts nur eine Erfolgsquote von 6 % bei Assets — **Lösung:** cloudflared auf den VM-Host oder einen externen VPS verlagern; die QUIC-Session darf keine NAT-/virbr0-Grenze überqueren. Der Schwellenwert von 0,1 % über 30 Probes bedeutet, dass selbst kurze NAT-Resets eine 30-minütige Degraded-Strafe auslösen. Der Umzug auf einen stabilen Netzwerkpfad ist die einzige verlässliche Lösung; innerhalb der VM gibt es keinen Abstimmungsparameter.

- **Problem:** Sidecar-Muster mit cloudflared pro Dienst (ein Tunnel pro Container/Dienst) — **Lösung:** eine einzelne benachbarte cloudflared-Instanz verwenden, die auf mehrere Hostnamen zeigt. Der offizielle Kubernetes-Deployment-Leitfaden rät ausdrücklich von Sidecar-Tunneln ab: „each cloudflared replica/pod can reach all Kubernetes services; there is no need for a dedicated tunnel per pod.“ Mehrere Sessions vervielfachen denselben Fehlerfall und vervielfachen die Angriffsfläche der Credentials.

- **Problem:** Tailscale Funnel kann `*.yourdomain.com` nicht bereitstellen — **Lösung:** innerhalb von Tailscale Funnel gibt es keine Lösung; die Unterstützung eigener Domains ist ein seit Langem offener Feature-Request (GitHub-Issue `tailscale/tailscale#11563`). Wenn eigene Domains erforderlich sind, cloudflared, autossh+nginx oder frp verwenden. Tailscale (nicht Funnel) bleibt nützlich für den rein internen Zugriff auf `*.ts.net`.

- **Problem:** Die cloudflared-Credentials-Datei (`<uuid>.json`) ist ein statisches Bearer-Geheimnis — wer Dateisystem-Lesezugriff auf dem Host hat, auf dem cloudflared läuft, kann eine eigene cloudflared-Instanz starten und den gesamten Verkehr zu Hostnamen abfangen, die an diesen Tunnel gebunden sind — **Lösung:** cloudflared als dedizierter Benutzer mit geringen Rechten ausführen und die Credentials-Datei mit `chmod 0400` schützen. Wenn der Host mit nicht vertrauenswürdigen Administratoren geteilt wird, cloudflared auf einen separaten VPS verlagern, auf dem die Credentials isoliert sind (siehe empfohlene Architektur oben). Hinweis: `sudo` umgeht Dateiberechtigungen problemlos; nur die physische Trennung der Hosts ist eine verlässliche Gegenmaßnahme.

- **Problem:** autossh hängt dauerhaft — die Verbindung wirkt auf TCP-Ebene aktiv, die SSH-Lebendprüfung ist jedoch tot, daher startet autossh nicht neu — **Lösung:** immer `-M 0` setzen (deaktiviert den eigenen Monitor-Port von autossh und verlässt sich stattdessen auf das native SSH-Keepalive) zusammen mit `ServerAliveInterval=60 ServerAliveCountMax=3 ExitOnForwardFailure=yes`. Ohne `ExitOnForwardFailure=yes` verwirft ein Fehler beim Binden des Forwards den weitergeleiteten Port stillschweigend, während die SSH-Session bestehen bleibt; autossh sieht eine aktive Verbindung und startet nie neu.

- **Problem:** WireGuard schlägt bei aggressivem NAT fehl (Verbindung bricht nach 1–2 Minuten Inaktivität ab) — **Lösung:** `PersistentKeepalive` von 25 auf 15 Sekunden senken. Der Standardwert von 25 s funktioniert für die meisten NAT-Geräte; manche Firmen- oder Mobilfunk-NATs laufen bei UDP-Zuordnungen schneller ab. Der Overhead von `PersistentKeepalive` liegt unabhängig von der Einstellung bei ca. 5 Byte/s pro Peer.

## Siehe auch {#see-also}

- [[datacenter-network-design]] — Underlay-Netzwerk, VXLAN-Overlays, BGP-Fabric-Design
- [[linux-server-administration]] — systemd-Dienst-Units, nftables, WireGuard-Installation
- [[sre-principles]] — Fehlerraten-Budgets, Hysterese, Muster zur Wiederherstellung aus dem Degraded-Zustand
- cloudflared-Tunnel-Dokumentation: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/
- cloudflared-Tunnel-Health-Troubleshooting: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-wan/troubleshooting/tunnel-health/
- WireGuard-Schnellstart: https://www.wireguard.com/quickstart/
- rathole-vs-frp-Benchmark: https://github.com/rapiz1/rathole
- autossh-persistente-Tunnel: https://raymii.org/s/tutorials/Autossh_persistent_tunnels.html
- Tailscale-Funnel-FR für eigene Domains: https://github.com/tailscale/tailscale/issues/11563
