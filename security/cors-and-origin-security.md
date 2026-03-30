---
title: CORS and Origin Security
category: web-security
tags: [cors, origin, same-origin-policy, csrf, cross-origin, headers]
---

# CORS and Origin Security

## Key Facts

- Same-Origin Policy (SOP) prevents scripts from one origin from reading responses from another origin
- Origin = scheme + hostname + port (e.g., `https://example.com:443`)
- CORS (Cross-Origin Resource Sharing) is a controlled relaxation of SOP via HTTP headers
- Preflight request (OPTIONS) sent for non-simple requests: custom headers, methods other than GET/HEAD/POST, non-standard Content-Type
- `Access-Control-Allow-Origin: *` allows any origin - NEVER use with credentials (`withCredentials: true`)
- [[jwt-authentication]] tokens sent in Authorization header trigger preflight requests
- CORS is enforced by browsers only - server-to-server requests are not subject to CORS

## Patterns

```javascript
// Express.js CORS configuration
const cors = require('cors');

// Restrictive - specific origins only
app.use(cors({
  origin: ['https://myapp.com', 'https://admin.myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,  // Allow cookies/auth headers
  maxAge: 86400,  // Cache preflight for 24h
}));

// DANGEROUS - never do this in production
app.use(cors({ origin: '*', credentials: true }));
// Browsers will reject this combination
```

```python
# NestJS CORS configuration
# main.ts
app.enableCors({
    origin: ['https://myapp.com'],
    methods: 'GET,POST,PUT,DELETE',
    credentials: True,
    allowedHeaders: 'Content-Type,Authorization',
})
```

```nginx
# Nginx CORS headers
location /api/ {
    if ($request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' 'https://myapp.com';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type';
        add_header 'Access-Control-Max-Age' 86400;
        return 204;
    }
    add_header 'Access-Control-Allow-Origin' 'https://myapp.com';
    proxy_pass http://backend;
}
```

## Gotchas

- CORS does NOT prevent the request from being sent - it prevents the browser from reading the response; the server still processes it
- Wildcard `*` in `Access-Control-Allow-Origin` cannot be used with `credentials: true` - must specify exact origin
- For multiple allowed origins, the server must dynamically set `Access-Control-Allow-Origin` based on request `Origin` header - validate against whitelist first
- CORS errors appear in browser console but never reach your JavaScript error handlers
- `null` origin (local files, sandboxed iframes) should NEVER be whitelisted - attackers can forge it
- Missing `Vary: Origin` header when dynamically setting origin can cause CDN/proxy caching issues

## See Also

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [OWASP CORS Misconfiguration](https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny)
- [CWE-942 Overly Permissive Cross-domain Whitelist](https://cwe.mitre.org/data/definitions/942.html)
