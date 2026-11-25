---
title: "Sécurité des serveurs web"
category: techniques
tags: [security, nginx, apache, reverse-proxy, tls, load-balancing]
level: 3
source_sha256: 684f70feed9bb5d6e4388cd5e42594845514ee617944bf859dd3978459dbcfb1
translation: machine
translated_at: '2026-10-24'
---
# Sécurité des serveurs web {#web-server-security}

Configuration sécurisée des serveurs web : hôtes virtuels Apache et Nginx, mise en place de TLS/SSL avec Let's Encrypt, schémas de reverse proxy, répartition de charge et en-têtes de sécurité.

## Points clés {#key-facts}
- Nginx est préféré comme reverse proxy pour la sécurité (surface d'attaque réduite, architecture événementielle)
- Let's Encrypt fournit des certificats TLS gratuits avec renouvellement automatique
- Algorithmes de répartition de charge : round-robin (par défaut), least_conn, ip_hash, random
- Les en-têtes de sécurité (HSTS, X-Frame-Options, CSP) doivent être définis au niveau du proxy
- Toujours désactiver la divulgation de la version du serveur en production

## Configuration Apache {#apache-configuration}
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

## Configuration Nginx {#nginx-configuration}
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

### Répartition de charge {#load-balancing}
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

## TLS avec Let's Encrypt {#tls-with-lets-encrypt}
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d example.com -d www.example.com
# Auto-renewal via systemd timer
certbot renew
```

## En-têtes de sécurité {#security-headers}
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

## Pièges à éviter {#gotchas}
- La terminaison TLS au niveau du répartiteur de charge signifie que le trafic vers les backends n'est pas chiffré, sauf s'il est re-chiffré
- `proxy_set_header X-Forwarded-For` est indispensable : sans lui, le backend voit l'IP du proxy et non celle du client
- Les certificats Let's Encrypt expirent au bout de 90 jours : vérifiez que le renouvellement automatique fonctionne
- `add_header` dans un bloc `location` imbriqué remplace tous les en-têtes définis dans les blocs parents dans Nginx
- Un reverse proxy mal configuré peut devenir un proxy ouvert exploitable par des attaquants

## Voir aussi {#see-also}
- [[cryptography-and-pki]] - détails du protocole TLS
- [[firewall-and-ids-ips]] - protection au niveau réseau
- [[web-application-security-fundamentals]] - attaques au niveau applicatif
- [[linux-system-hardening]] - durcissement du système d'exploitation pour les serveurs web
