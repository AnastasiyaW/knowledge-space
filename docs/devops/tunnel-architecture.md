# Tunnel Architecture for Private Service Exposure

Exposing VM-hosted or NAT-ed services to the public internet without opening inbound firewall ports. Covers cloudflared, WireGuard, frp/rathole, Tailscale Funnel, and autossh patterns.

## Key Facts

- All options below avoid inbound port exposure: traffic exits the private network outbound, terminating at a relay or edge node — see [[datacenter-network-design]] for underlay context
- cloudflared uses QUIC over UDP/7844 (falls back to HTTP/2 over TCP/443); WireGuard is UDP-only
- Degraded threshold (cloudflared): failure rate must drop below **0.1% over 30 consecutive probes** before recovery from degraded state; **30-minute hysteresis** applies after recovery
- WireGuard `PersistentKeepalive=25` sends ~5 bytes/sec per peer; sufficient to hold most NAT mappings
- Tailscale Funnel **hard limit**: only `*.ts.net` hostnames; custom domains are not supported (open FR since 2022, unresolved as of 2026)
- Tailscale Funnel **port limit**: only 443, 8443, 10000 exposed externally
- cloudflared creds file (`.json`) is a **static secret**: anyone with read access can spawn a replica tunnel (MITM on all hostnames bound to that tunnel)
- autossh requires `-M 0` + `ServerAliveInterval` + `ExitOnForwardFailure=yes`; without `ExitOnForwardFailure` the SSH connection can hang permanently without autossh restarting it
- frp v0.68.x is stable; v2 rewrite (`0.68+`) is in active development with breaking changes from the v1 config format
- rathole (Rust) outperforms frp at high QPS; at 4000 QPS frp errors while rathole stays stable — negligible difference at <10 concurrent users

## Option Comparison

| Tool | Transport | Custom domain | Reliability | SSO | Security note |
|------|-----------|--------------|-------------|-----|---------------|
| cloudflared (on relay host) | QUIC/UDP-7844, fallback HTTP/2 | Yes (Cloudflare DNS) | High — stable host network path, single QUIC session | CF Access (free, Google/email) | Creds file on relay host: read access = replica MITM |
| cloudflared (sidecar per service) | QUIC/UDP-7844 | Yes | Low — anti-pattern per CF docs; N sessions × same failure mode | CF Access per tunnel | N creds files = N× attack surface |
| WireGuard (as VPN underlay) | UDP (configurable port) | Via relay proxy | High — stateless crypto, roaming-resilient | Depends on upstream proxy | Encrypts all transit; host sees only encrypted UDP |
| frp v0.68 | TCP or HTTP(S) | Yes (SNI demux) | Medium-high — mature, direct path | Authelia/oauth2-proxy (DIY) | Exposed TCP port on internet; origin IP visible if misconfigured |
| rathole | TCP | Yes (SNI demux) | High — Rust, lower latency than frp at scale | Authelia/oauth2-proxy (DIY) | Same as frp; smaller binary (~500 KiB) |
| Tailscale Funnel | STUN + DERP relay | **No** — `*.ts.net` only | Medium — DERP infra; undocumented bandwidth limits | Tailscale ACL (Google/GitHub IdP) | No custom domain: **hard blocker** for most production use |
| autossh + nginx | SSH (TCP/22 or custom) | Yes (nginx vhost) | High — SSH works through any NAT/firewall | Authelia/oauth2-proxy (DIY) | SSH crypto strong; head-of-line blocking on shared TCP |

## Recommended Architecture

### Primary: cloudflared on adjacent VPS + WireGuard VM↔VPS

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

**Why**: cloudflared sits on a stable VPS network (no NAT layers between it and Cloudflare). The unstable VM↔internet path is carried by WireGuard, which handles roaming and temporary packet loss gracefully (stateless crypto; handshake resumes in 1-2 s after path recovery). Tunnel credentials live on the VPS — not on any host where third parties have shell access.

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

Enable on both nodes:

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

**Pre-flight checks before committing to this architecture:**

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

### Fallback: autossh + nginx + Authelia (UDP blocked)

Use when the network blocks outbound UDP to the WireGuard port. SSH/TCP is almost universally allowed.

**systemd service — VM (`/etc/systemd/system/autossh-tunnel.service`):**

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

Let's Encrypt cert renewal:

```bash
certbot --nginx -d dev.example.com -d app.example.com -d files.example.com
systemctl enable --now certbot.timer
```

## Gotchas

- **Issue:** cloudflared inside a KVM/QEMU VM achieves 6% asset success rate despite stable host WAN — **Fix:** move cloudflared to the VM host or an external VPS; the QUIC session must not cross a NAT/virbr0 boundary. The 0.1%/30-probe threshold means even brief NAT resets trigger a 30-minute degraded penalty. Moving to a stable network path is the only reliable fix; there is no tuning parameter inside the VM.

- **Issue:** Sidecar-per-service cloudflared pattern (one tunnel per container/service) — **Fix:** use a single adjacent cloudflared instance pointing to multiple hostnames. The official Kubernetes deployment guide explicitly recommends against sidecar tunnels: "each cloudflared replica/pod can reach all Kubernetes services; there is no need for a dedicated tunnel per pod." Multiple sessions multiply the same failure mode and multiply the creds attack surface.

- **Issue:** Tailscale Funnel cannot serve `*.yourdomain.com` — **Fix:** none within Tailscale Funnel; custom domain support is a long-standing open feature request (GitHub issue `tailscale/tailscale#11563`). Use cloudflared, autossh+nginx, or frp if custom domains are required. Tailscale (not Funnel) remains useful for internal-only access on `*.ts.net`.

- **Issue:** cloudflared credentials file (`<uuid>.json`) is a static bearer secret — anyone with filesystem read access on the host running cloudflared can spawn their own cloudflared instance, intercepting all traffic to hostnames bound to that tunnel — **Fix:** run cloudflared as a dedicated low-privilege user with `chmod 0400` on the creds file. If the host is shared with untrusted admins, move cloudflared to a separate VPS where creds are isolated (see recommended architecture above). Note: `sudo` trivially bypasses file permission; physical host separation is the only reliable mitigation.

- **Issue:** autossh hangs permanently — connection appears alive at the TCP level but SSH-level liveness is dead, so autossh does not restart — **Fix:** always set `-M 0` (disables autossh's own monitor port, relies on SSH native keepalive instead) together with `ServerAliveInterval=60 ServerAliveCountMax=3 ExitOnForwardFailure=yes`. Without `ExitOnForwardFailure=yes`, a forward-bind failure silently drops the forwarded port while the SSH session stays up; autossh sees a live connection and never restarts.

- **Issue:** WireGuard fails through aggressive NAT (connection drops after 1-2 minutes of idle) — **Fix:** lower `PersistentKeepalive` from 25 to 15 seconds. The default 25 s works for most NAT devices; some corporate/mobile NATs time out UDP mappings faster. `PersistentKeepalive` overhead is ~5 bytes/second per peer regardless of setting.

## See Also

- [[datacenter-network-design]] — underlay networking, VXLAN overlays, BGP fabric design
- [[linux-server-administration]] — systemd service units, nftables, WireGuard installation
- [[sre-principles]] — failure rate budgets, hysteresis, degraded-state recovery patterns
- cloudflared tunnel docs: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/
- cloudflared tunnel health troubleshooting: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-wan/troubleshooting/tunnel-health/
- WireGuard quickstart: https://www.wireguard.com/quickstart/
- rathole vs frp benchmark: https://github.com/rapiz1/rathole
- autossh persistent tunnels: https://raymii.org/s/tutorials/Autossh_persistent_tunnels.html
- Tailscale Funnel custom domain FR: https://github.com/tailscale/tailscale/issues/11563
