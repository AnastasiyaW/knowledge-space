---
title: "Sicherheit von Webservern"
category: techniques
tags: [security, nginx, apache, reverse-proxy, tls, load-balancing]
level: 3
source_sha256: 684f70feed9bb5d6e4388cd5e42594845514ee617944bf859dd3978459dbcfb1
translation: machine
translated_at: '2026-10-24'
---
# Sicherheit von Webservern {#web-server-security}

Sichere Konfiguration von Webservern: Apache- und Nginx-Virtual-Hosts, TLS/SSL-Einrichtung mit Let's Encrypt, Reverse-Proxy-Muster, Lastverteilung und Security-Header.

## Wichtige Fakten {#key-facts}
- Nginx wird aus Sicherheitsgründen als Reverse Proxy bevorzugt (minimale Angriffsfläche, ereignisgesteuert)
- Let's Encrypt stellt kostenlose TLS-Zertifikate mit automatischer Erneuerung bereit
- Lastverteilungsalgorithmen: round-robin (Standard), least_conn, ip_hash, random
- Security-Header (HSTS, X-Frame-Options, CSP) sollten auf Proxy-Ebene gesetzt werden
- Die Offenlegung der Serverversion sollte in Produktivumgebungen immer deaktiviert werden

## Apache-Konfiguration {#apache-configuration}
```bash
# /etc/apache2/sites-available/example.conf
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/example
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

a2ensite example.conf
a2enmod ssl rewrite
systemctl reload apache2
```

## Nginx-Konfiguration {#nginx-configuration}
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/example;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Reverse Proxy {#reverse-proxy}
```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Lastverteilung {#load-balancing}
```nginx
upstream backend {
    server 10.0.0.1:8080 weight=3;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

## TLS mit Let's Encrypt {#tls-with-lets-encrypt}
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d example.com -d www.example.com
# Auto-renewal via systemd timer
certbot renew
```

## Security-Header {#security-headers}
```nginx
# Add to server or location block
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'" always;

# Hide server version
server_tokens off;
```

## Stolperfallen {#gotchas}
- TLS-Terminierung am Load Balancer bedeutet, dass der Backend-Verkehr unverschlüsselt ist, sofern er nicht erneut verschlüsselt wird
- `proxy_set_header X-Forwarded-For` ist unverzichtbar – ohne diesen Header sieht das Backend die IP des Proxys statt die des Clients
- Let's Encrypt-Zertifikate laufen nach 90 Tagen ab – die automatische Erneuerung muss funktionieren
- `add_header` in einem verschachtelten `location`-Block überschreibt in Nginx alle Header aus übergeordneten Blöcken
- Eine fehlkonfigurierte Reverse-Proxy-Installation kann für Angreifer zu einem offenen Proxy werden

## Siehe auch {#see-also}
- [[cryptography-and-pki]] - Details zum TLS-Protokoll
- [[firewall-and-ids-ips]] - Schutz auf Netzwerkebene
- [[web-application-security-fundamentals]] - Angriffe auf Anwendungsebene
- [[linux-system-hardening]] - Härtung des Betriebssystems für Webserver
