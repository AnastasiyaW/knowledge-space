---
title: "Nginx: nginx-http2-vulnerability-disclosure — Nginx Http2 Vulnerability Disclosure"
category: "projects"
date: 2026-11-19
tags: ["nginx", "nginx-http2-vulnerability-disclosure", "project"]
aliases: ["Nginx: nginx-http2-vulnerability-disclosure"]
---

# Nginx: nginx-http2-vulnerability-disclosure — Nginx Http2 Vulnerability Disclosure

Nginx HTTP/2 vulnerability disclosure covers two memory-corruption flaws in NGINX, fixed in 1.30.7 and 1.31.9, for admins running HTTP/2.

**Development line:** project:nginx · thread nginx-http2-vulnerability-disclosure  
**Last event:** 2026-11-19 · 3 dated since 2026-11-18 · **Researched:** 2026-11-20 · confidence: high

## What it is

NGINX HTTP/2 vulnerability disclosure is a coordinated security release for two memory-corruption bugs in the NGINX web server HTTP/2 module. One is an integer underflow in HTTP/2 flow-control window accounting. The other is a use-after-free in reverse-proxy connection handling.

An unauthenticated remote attacker can crash workers or run arbitrary code on a server with HTTP/2 enabled. Exploitation needs an active HTTP/2 listening configuration and worker privilege access. The fix is a package update, or disabling the HTTP/2 directives.

## Development line

- **2026-11-18 — Nginx: nginx-http2-vulnerability-disclosure update.** NGINX maintainers released security fix versions 1.30.7 and 1.31.9 for the HTTP/2 vulnerabilities CVE-2026-123007 and CVE-2026-123633.
- **2026-11-19 — Researchers report two NGINX HTTP/2 RCE flaws; fixes released November 18.** Researchers using AI tools reported two NGINX vulnerabilities. One has been present since 2015, the other for about six years. Both could allow unauthenticated code execution on servers. NGINX developers released patch updates on 18 November.
- **2026-11-19 — NGINX releases fixes for two HTTP/2 remote code execution vulnerabilities.** On 18 November, NGINX developers released updates for two vulnerabilities that researchers found in the web server using AI tools. One bug had been in the code since 2015 and the other for about six years. Both could allow code execution on the server without an account.
- **2026-11-19 — further details on this date.**
  - CVE-2026-123007 is an HTTP/2 send\_window integer underflow present since version 1.9.5. CVE-2026-123633 is an HTTP/2 connection use-after-free present since version 1.19.7. Both have a CVSS v4.0 critical score of 9.2. (2026-11-19) — <https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities>
  - The fix is to upgrade to NGINX Mainline 1.31.9 or NGINX Stable 1.30.7. Until then, disabling HTTP/2 on the listen directives mitigates it at once. (2026-11-19) — <https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities>

## What changed

Researchers found an integer underflow in stream window management, present since the initial HTTP/2 implementation. They also found a connection use-after-free in reverse-proxy processing. After coordinated disclosure, maintainers patched stream credit validation and connection lifecycle management on mainline and stable. They published fixed releases and a configuration workaround.

## How to use this

1. Check the server configuration files for HTTP/2, enabled through listen directives or http2 directives.
  — <https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities>
2. Upgrade NGINX Open Source to Stable 1.30.7 or Mainline 1.31.9, or apply the matching vendor update.
  — <https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities>
3. If a binary upgrade cannot be scheduled yet, disable the http2 parameter in every listen block and reload the configuration.
  — <https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities>

## Best practices

- Audit all ingress controllers and edge reverse proxies automatically, so unpatched NGINX releases do not stay deployed.
  — <https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities>
- Run workers unprivileged and apply container security profiles, so worker-level memory corruption stays contained.
  — <https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities>

## Superseded by this

- The belief that unpatched NGINX with HTTP/2 enabled is safe from unauthenticated remote code execution no longer holds.
  — <https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities>

## Still unknown

- Community forum discussions exist, but no direct article or discussion URLs are available to cite.

## Sources

| source | title | read |
|---|---|---|
| https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities | NGINX HTTP/2 Remote Code Execution Vulnerabilities Disclosure | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:nginx, thread nginx-http2-vulnerability-disclosure, 3 dated events 2026-11-18 → 2026-11-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
