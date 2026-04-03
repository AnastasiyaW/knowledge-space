---
title: Web Server Security
category: techniques
tags: [security, nginx, apache, reverse-proxy, tls, load-balancing]
---

# Web Server Security

Secure configuration of web servers: Apache and Nginx virtual hosts, TLS/SSL setup with Let's Encrypt, reverse proxy patterns, load balancing, and security headers.

## Key Facts
- Nginx is preferred as reverse proxy for security (minimal attack surface, event-driven)
- Let's Encrypt provides free TLS certificates with automatic renewal
- Load balancing algorithms: round-robin (default), least_conn, ip_hash, random
- Security headers (HSTS, X-Frame-Options, CSP) should be set at the proxy level
- Always disable server version disclosure in production

## Apache Configuration
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

## Nginx Configuration
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

### Reverse Proxy
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

### Load Balancing
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

## TLS with Let's Encrypt
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d example.com -d www.example.com
# Auto-renewal via systemd timer
certbot renew
```

## Security Headers
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

## Gotchas
- TLS termination at load balancer means backend traffic is unencrypted unless re-encrypted
- `proxy_set_header X-Forwarded-For` is essential - without it, backend sees proxy IP, not client IP
- Let's Encrypt certificates expire in 90 days - ensure auto-renewal is working
- `add_header` in a nested `location` block overrides all headers from parent blocks in Nginx
- Misconfigured reverse proxy can become an open proxy for attackers

## See Also
- [[cryptography-and-pki]] - TLS protocol details
- [[firewall-and-ids-ips]] - network-level protection
- [[web-application-security-fundamentals]] - application-level attacks
- [[linux-system-hardening]] - OS-level hardening for web servers
