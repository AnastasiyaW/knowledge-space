---
title: OSINT and Reconnaissance
category: techniques
tags: [security, osint, reconnaissance, shodan, google-dorking, metadata, enumeration]
---

# OSINT and Reconnaissance

Open Source Intelligence techniques: Shodan/Censys infrastructure search, Google Dorking, metadata extraction (EXIF, document metadata), subdomain enumeration, username/email investigation, and Wayback Machine analysis.

## Key Facts
- Shodan scans the entire IPv4 space and indexes service banners - passive recon without touching target
- Google Dorking was systematized in 2002 (Johnny Long) and remains highly effective
- EXIF data from photos can contain GPS coordinates, camera serial number, and editing software used
- Government websites are goldmines for document metadata (author names, internal paths)
- Certificate Transparency logs (crt.sh) reveal all SSL certificates issued for a domain
- Passive OSINT (public data) is legal; active scanning (touching target systems) requires authorization

## Shodan
Scans IPv4 space, probes ports, collects banners:
```typescript
port:22                              # SSH servers
os:"Windows 7"                       # Specific OS
city:"Moscow"                        # Location
org:"Company"                        # Organization
ssl.cert.subject.CN:"example.com"   # SSL certificates
http.title:"Dashboard"              # Web interface titles
has_screenshot:true                  # With screenshots (VNC, RDP, webcams)
```

### Related Tools
- **Censys** - certificate-focused, more structured data, better for TLS analysis
- **BinaryEdge** - real-time threat intel, IoT discovery, data breach monitoring

## Google Dorking
```bash
site:example.com                     # Limit to domain
intitle:"index of"                   # Directory listings
inurl:admin                          # URLs with "admin"
filetype:pdf                         # Specific file types
intext:"password"                    # Content search

# Practical examples
filetype:env "DB_PASSWORD"           # Exposed .env files
filetype:sql "INSERT INTO" "password"  # Exposed database dumps
intitle:"phpinfo()" "PHP Version"    # PHP info pages
site:gov.* filetype:xlsx             # Government spreadsheets
inurl:"/view.shtml" intitle:"camera" # IP cameras
filetype:yml "password:"             # Exposed config files
```

Defense: proper `robots.txt`, server-side access controls, `X-Robots-Tag: noindex`, regular dork audits of your own domains.

## Metadata Extraction

### EXIF Data (Images)
```bash
exiftool image.jpg
```
Contains: camera model, serial number, GPS coordinates, date/time, editing software, original thumbnail (may survive editing).

### Document Metadata (DOCX, PDF, PPTX)
- Author name (often real name from OS profile)
- Organization name
- Creation/modification dates, editing time
- Revision history, printer information
- Tools: `exiftool`, `FOCA`

## Subdomain Enumeration
```bash
sublist3r -d example.com            # Brute-force + public sources
amass enum -d example.com           # Comprehensive enumeration
subfinder -d example.com            # Fast passive enumeration
```
Additional sources: Certificate Transparency (crt.sh), DNS zone transfer attempts, search engine dorks (`site:*.example.com`).

## Username / Email Investigation

### Cross-Platform Username Search
- **Sherlock** - checks 300+ platforms
- **Maigret** - advanced search with profile parsing
- **Holehe** - checks if email is registered on services (without alerting user)

### Email Investigation
- **Have I Been Pwned** - legitimate breach checking
- **DeHashed / IntelX** - advanced breach data search
- Email header analysis reveals: routing path, sender IP, SPF/DKIM results, mail client

### Account Enumeration
Many services reveal registration status during:
- Password reset ("email not found" vs "reset link sent")
- Registration ("email already in use")
- Timing differences in auth responses

## Web Archive Analysis
- **archive.org** (Wayback Machine) - historical website snapshots
- Reveals: previous owners, old contacts, removed content, changed profiles
- **archive.is** and **Google Web Cache** as alternatives
- Social media images stored on CDN for years even after "deletion"
- Use `web.archive.org/save/URL` to preserve evidence before removal

## Technology Stack Detection
- **Wappalyzer / BuiltWith** - identify CMS, frameworks, analytics, CDN
- HTTP response headers reveal server software and versions
- `robots.txt` and `sitemap.xml` disclose site structure
- Source code comments may contain credentials, internal paths, debug info

## DNS Reconnaissance
```bash
dig example.com ANY
dig axfr @ns1.example.com example.com   # Zone transfer attempt
fierce --domain example.com             # DNS enumeration
```

## IP Address Discovery
- DNS lookup for the domain
- Historical DNS records reveal real IPs behind CDNs
- CDN bypass: check subdomains not proxied, email headers, SSL certificate history
- Tools: SecurityTrails, ViewDNS.info, DNSdumpster

## Gotchas
- Shodan data can be stale - always verify findings are current
- Google dorking results change as Google re-indexes - save evidence immediately
- EXIF stripping is common on social media uploads (Facebook, Twitter) but not on all platforms
- Zone transfers (AXFR) are almost never allowed on properly configured servers
- Holehe can trigger rate limits and temporary account locks on some platforms
- Always distinguish between passive OSINT and active scanning for legal boundaries

## See Also
- [[penetration-testing-methodology]] - recon as first phase
- [[browser-and-device-fingerprinting]] - technical fingerprinting methods
- [[deepfake-and-document-forensics]] - image/document analysis
- [[network-traffic-analysis]] - nmap, active scanning
