---
title: "OSINT und Reconnaissance"
category: techniques
tags: [security, osint, reconnaissance, shodan, google-dorking, metadata, enumeration]
level: 3
source_sha256: 237a9c888565812eaa12b322dd8067b3fc8208b09b87183d97a00f6ab68b75b1
translation: machine
translated_at: '2026-10-24'
---
Hmm, I realize I just emitted placeholder junk instead of a translation. Let me redo this properly.

Actually, I need to be honest: the previous output was a mistake. Here is the correct translation:

---
title: OSINT und Reconnaissance
category: techniques
tags: [security, osint, reconnaissance, shodan, google-dorking, metadata, enumeration]
---

# OSINT und Reconnaissance {#osint-and-reconnaissance}

Open-Source-Intelligence-Techniken: Shodan-/Censys-Infrastruktursuche, Google Dorking, Metadatenextraktion (EXIF, Dokumentmetadaten), Subdomain-Enumeration, Untersuchung von Benutzernamen und E-Mail-Adressen sowie Analyse der Wayback Machine.

## Key Facts {#key-facts}
- Shodan scannt den gesamten IPv4-Adressraum und indexiert Service-Banner – passive Aufklärung, ohne das Ziel zu berühren
- Google Dorking wurde 2002 (Johnny Long) systematisiert und ist nach wie vor äußerst wirksam
- EXIF-Daten von Fotos können GPS-Koordinaten, die Seriennummer der Kamera und die verwendete Bearbeitungssoftware enthalten
- Behördenwebsites sind eine wahre Fundgrube für Dokumentmetadaten (Autorennamen, interne Pfade)
- Certificate-Transparency-Logs (crt.sh) zeigen alle SSL-Zertifikate, die für eine Domain ausgestellt wurden
- Passives OSINT (öffentliche Daten) ist legal; aktives Scannen (Zugriff auf Zielsysteme) erfordert eine Autorisierung

## Shodan {#shodan}
Scannt den IPv4-Adressraum, prüft Ports und sammelt Banner:
```typescript
port:22                              # SSH servers
os:"Windows 7"                       # Specific OS
city:"Moscow"                        # Location
org:"Company"                        # Organization
ssl.cert.subject.CN:"example.com"   # SSL certificates
http.title:"Dashboard"              # Web interface titles
has_screenshot:true                  # With screenshots (VNC, RDP, webcams)
```

### Verwandte Tools {#related-tools}
- **Censys** – zertifikatsorientiert, strukturiertere Daten, besser für die TLS-Analyse geeignet
- **BinaryEdge** – Echtzeit-Threat-Intelligence, IoT-Erkennung, Überwachung von Datenleaks

## Google Dorking {#google-dorking}
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

Abwehr: korrekte `robots.txt`, serverseitige Zugriffskontrollen, `X-Robots-Tag: noindex` und regelmäßige Dork-Audits für die eigenen Domains.

## Metadatenextraktion {#metadata-extraction}

### EXIF-Daten (Bilder) {#exif-data-images}
```bash
exiftool image.jpg
```
Enthalten: Kameramodell, Seriennummer, GPS-Koordinaten, Datum/Uhrzeit, Bearbeitungssoftware, ursprüngliches Vorschaubild (kann die Bearbeitung überdauern).

### Dokumentmetadaten (DOCX, PDF, PPTX) {#document-metadata-docx-pdf-pptx}
- Autorenname (oft der echte Name aus dem Betriebssystemprofil)
- Organisationsname
- Erstellungs- und Änderungsdatum, Bearbeitungszeit
- Überarbeitungsverlauf, Druckerinformationen
- Werkzeuge: `exiftool`, `FOCA`

## Subdomain-Enumeration {#subdomain-enumeration}
```bash
sublist3r -d example.com            # Brute-force + public sources
amass enum -d example.com           # Comprehensive enumeration
subfinder -d example.com            # Fast passive enumeration
```
Weitere Quellen: Certificate Transparency (crt.sh), Versuche eines DNS-Zonentransfers, Suchmaschinen-Dorks (`site:*.example.com`).

## Untersuchung von Benutzernamen / E-Mail-Adressen {#username-email-investigation}

### Plattformübergreifende Suche nach Benutzernamen {#cross-platform-username-search}
- **Sherlock** – prüft mehr als 300 Plattformen
- **Maigret** – erweiterte Suche mit Profil-Parsing
- **Holehe** – prüft, ob eine E-Mail-Adresse bei Diensten registriert ist (ohne den Benutzer zu benachrichtigen)

### E-Mail-Untersuchung {#email-investigation}
- **Have I Been Pwned** – seriöse Prüfung auf Datenlecks
- **DeHashed / IntelX** – erweiterte Suche in Leak-Daten
- Analyse der E-Mail-Header offenbart: Routing-Pfad, Absender-IP, SPF-/DKIM-Ergebnisse, E-Mail-Client

### Kontenaufzählung (Account Enumeration) {#account-enumeration}
Viele Dienste verraten den Registrierungsstatus bei:
- Passwort-Zurücksetzung („E-Mail nicht gefunden“ vs. „Zurücksetzungslink gesendet“)
- Registrierung („E-Mail-Adresse bereits in Verwendung“)
- Zeitunterschieden bei Authentifizierungsantworten

## Analyse von Web-Archiven {#web-archive-analysis}
- **archive.org** (Wayback Machine) – historische Website-Snapshots
- Offenbart: frühere Eigentümer, alte Kontakte, entfernte Inhalte, geänderte Profile
- **archive.is** und **Google Web Cache** als Alternativen
- Social-Media-Bilder werden auch nach einer „Löschung“ jahrelang auf CDNs gespeichert
- Mit `web.archive.org/save/URL` lassen sich Belege vor einer Entfernung sichern

## Erkennung des Technologie-Stacks {#technology-stack-detection}
- **Wappalyzer / BuiltWith** – identifizieren CMS, Frameworks, Analytics und CDN
- HTTP-Antwort-Header verraten Server-Software und Versionen
- `robots.txt` und `sitemap.xml` offenbaren die Seitenstruktur
- Quellcode-Kommentare können Zugangsdaten, interne Pfade und Debug-Informationen enthalten

## DNS-Aufklärung {#dns-reconnaissance}
```bash
dig example.com ANY
dig axfr @ns1.example.com example.com   # Zone transfer attempt
fierce --domain example.com             # DNS enumeration
```

## Ermittlung von IP-Adressen {#ip-address-discovery}
- DNS-Abfrage für die Domain
- Historische DNS-Einträge verraten die echten IPs hinter CDNs
- Umgehung von CDNs: Subdomains prüfen, die nicht über den Proxy laufen, E-Mail-Header, Historie der SSL-Zertifikate
- Tools: SecurityTrails, ViewDNS.info, DNSdumpster

## Stolperfallen {#gotchas}
- Shodan-Daten können veraltet sein – Ergebnisse stets auf Aktualität prüfen
- Google-Dorking-Ergebnisse ändern sich mit der Neuindexierung durch Google – Belege sofort sichern
- EXIF-Daten werden bei Uploads in sozialen Netzwerken (Facebook, Twitter) häufig entfernt, bei nicht allen Plattformen jedoch nicht
- Zonentransfers (AXFR) sind auf korrekt konfigurierten Servern nahezu nie erlaubt
- Holehe kann bei einigen Plattformen Rate-Limits und vorübergehende Kontosperren auslösen
- Passives OSINT und aktives Scannen müssen aus rechtlichen Gründen stets klar unterschieden werden

## Siehe auch {#see-also}
- [[penetration-testing-methodology]] – Aufklärung als erste Phase
- [[browser-and-device-fingerprinting]] – technische Fingerprinting-Methoden
- [[deepfake-and-document-forensics]] – Bild- und Dokumentanalyse
- [[network-traffic-analysis]] – nmap, aktives Scannen
