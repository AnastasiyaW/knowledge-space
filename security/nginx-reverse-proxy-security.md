---
title: Nginx Reverse Proxy Security
category: infrastructure-security
tags: [nginx, reverse-proxy, deployment, ssl, hardening, headers]
---

# Nginx Reverse Proxy Security

## Key Facts

- Reverse proxy sits between clients and backend servers - handles TLS termination, load balancing, request filtering
- SSL/TLS termination at nginx: clients connect via HTTPS to nginx, nginx connects to backend via HTTP on internal network
- Security headers (CSP, HSTS, X-Frame-Options) should be added at the reverse proxy level for consistency
- Rate limiting at nginx layer protects backend from DDoS and brute-force before requests reach application code
- [[cors-and-origin-security]] headers can be managed centrally at the nginx level
- [[file-upload-security]] rules can be enforced via nginx client_max_body_size and location restrictions

## Patterns

```nginx
# Secure reverse proxy configuration
server {
    listen 443 ssl http2;
    server_name app.example.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    # Backend proxy
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Request size limit
        client_max_body_size 10m;
    }

    # Static files
    location / {
        root /var/www/client/dist;
        try_files $uri $uri/ /index.html;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name app.example.com;
    return 301 https://$host$request_uri;
}
```

```bash
# Test SSL configuration
# Check certificate
openssl s_client -connect app.example.com:443 -servername app.example.com

# Test configuration syntax
nginx -t

# Security scan
curl -I https://app.example.com  # Check response headers
```

## Gotchas

- `proxy_pass http://backend` (no trailing slash) and `proxy_pass http://backend/` (trailing slash) behave differently with location paths
- `X-Forwarded-For` header can be spoofed by client - use `set_real_ip_from` with trusted proxy addresses and `real_ip_header X-Forwarded-For`
- Default `client_max_body_size` is 1MB - file uploads will fail silently with 413 error if not increased
- HSTS header should NOT be set until you are certain HTTPS is fully working - it locks browsers to HTTPS with no easy undo
- Backend must read `X-Forwarded-Proto` to generate correct URLs - without it, backend generates http:// links behind HTTPS proxy
- When deploying both frontend and backend behind same domain, `proxy_pass` path matching order matters - most specific paths first

## See Also

- [Nginx Security Hardening Guide](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
