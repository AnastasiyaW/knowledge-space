---
title: "Kryptografie und PKI"
category: concepts
tags: [security, cryptography, encryption, tls, pki, hashing]
level: 3
source_sha256: ee3036a06dd4ae8551afabb7e951bf4b1390e8359df0c434e029c385f5ce14af
translation: machine
translated_at: '2026-10-24'
---
# Kryptografie und PKI {#cryptography-and-pki}

Symmetrische und asymmetrische Verschlüsselung, Hashing-Algorithmen, digitale Signaturen, Funktionsweise von TLS/SSL und Public Key Infrastructure. Grundlegende Bausteine für sichere Kommunikation und Datenschutz.

## Wichtige Fakten {#key-facts}
- Symmetrische Verschlüsselung (AES) ist für große Datenmengen schnell, hat aber das Problem der Schlüsselverteilung
- Asymmetrische Verschlüsselung (RSA, ECC) löst den Schlüsselaustausch, ist aber langsam – sie wird für Schlüsselaustausch und Signaturen verwendet, nicht für große Datenmengen
- ECC mit 256 Bit bietet vergleichbare Sicherheit wie RSA mit 3072 Bit bei kürzeren Schlüsseln
- TLS 1.3 hat den Handshake auf 1-RTT reduziert (gegenüber 2-RTT in 1.2), schwache Chiffren entfernt und schreibt PFS vor
- Perfect Forward Secrecy (PFS) bedeutet, dass die Kompromittierung des privaten Serverschlüssels vergangene Sitzungen nicht entschlüsselt
- MD5 und SHA-1 sind gebrochen – niemals für Sicherheitszwecke verwenden

## Symmetrische Verschlüsselung {#symmetric-encryption}
Derselbe Schlüssel für Verschlüsselung und Entschlüsselung:
- **AES** – aktueller Standard, Schlüssel mit 128/192/256 Bit
- **ChaCha20** – Stromchiffre, wird in TLS verwendet, mobilfreundlich (schneller ohne AES-NI)
- **DES/3DES** – veraltet, gebrochen bzw. abgekündigt
- Problem der Schlüsselverteilung: wie der Schlüssel zwischen den Parteien sicher geteilt wird

## Asymmetrische Verschlüsselung {#asymmetric-encryption}
Paar aus öffentlichem und privatem Schlüssel:
- **RSA** – basiert auf der Faktorisierung großer Primzahlen, mindestens 2048 Bit lange Schlüssel
- **ECC** (Elliptic Curve) – kürzere Schlüssel bei vergleichbarer Sicherheit
- **Diffie-Hellman** – Protokoll für den Schlüsselaustausch (selbst keine Verschlüsselung)
- Wird für Schlüsselaustausch und digitale Signaturen verwendet, nicht für große Datenmengen

## Hashing {#hashing}
Einwegfunktion mit Ausgabe fester Länge:

| Algorithmus | Status | Anwendungsfall |
|-------------|--------|----------------|
| SHA-256/SHA-3 | Aktueller Standard | Integritätsprüfung |
| MD5 | Gebrochen (Kollisionen) | Niemals für Sicherheitszwecke |
| SHA-1 | Veraltet (SHAttered 2017) | Nur noch für Altsysteme |
| bcrypt/scrypt/Argon2 | Aktueller Standard | Passwort-Hashing (bewusst langsam, gesalzen) |

Eigenschaften: deterministisch, Lawineneffekt, Resistenz gegen Urbilder, Kollisionsresistenz.

## Digitale Signaturen {#digital-signatures}
1. Der Absender bildet den Hash der Nachricht
2. Der Absender verschlüsselt den Hash mit dem **privaten Schlüssel** = Signatur
3. Der Empfänger entschlüsselt die Signatur mit dem **öffentlichen Schlüssel** des Absenders
4. Der Empfänger bildet unabhängig davon den Hash der Nachricht
5. Stimmen die Hashes überein, sind Nachricht authentisch und unverändert

## PKI (Public Key Infrastructure) {#pki-public-key-infrastructure}

### Vertrauenshierarchie {#trust-hierarchy}
- **Root CA** – selbstsigniert, von Betriebssystem/Browser als vertrauenswürdig eingestuft
- **Intermediate CA** – von der Root CA signiert, signiert Endzertifikate
- **Endzertifikat** – Server- und Client-Zertifikate
- **CRL/OCSP** – Prüfung auf Widerruf von Zertifikaten

Ein Zertifikat enthält: öffentlichen Schlüssel, Subject (Domain), Aussteller, Gültigkeitszeitraum, Signatur.

### Certificate Transparency {#certificate-transparency}
Öffentliche Logs aller ausgestellten Zertifikate. Werkzeuge: crt.sh, censys.io. Verwendet für:
- Erkennung fehlerhaft ausgestellter Zertifikate
- Subdomain-Enumeration während der Aufklärung

## TLS/SSL {#tlsssl}

### Protokollversionen {#protocol-versions}
- SSL – alle Versionen veraltet (SSLv3 durch den POODLE-Angriff gebrochen)
- TLS 1.0/1.1 – veraltet
- TLS 1.2 – aktuell breit unterstütztes Minimum
- TLS 1.3 – 1-RTT-Handshake, schwache Chiffren entfernt, PFS verpflichtend

### TLS-Handshake (1.2) {#tls-handshake-12}
```yaml
Client → Server: ClientHello (supported ciphers, random)
Server → Client: ServerHello (chosen cipher, random) + Certificate
Server → Client: Key Exchange parameters
Client → Server: Key Exchange + ChangeCipherSpec
Both: Encrypted application data
```

### TLS-Konfiguration (Nginx) {#tls-configuration-nginx}
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
```

### Let's Encrypt {#lets-encrypt}
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d example.com -d www.example.com
# Auto-renew via systemd timer: certbot renew
```

## Stolperfallen {#gotchas}
- Verschlüsselung im Ruhezustand ohne sauberes Schlüsselmanagement ist Sicherheitstheater – Schlüssel, die neben den verschlüsselten Daten gespeichert werden, bieten keinen Schutz
- TLS-Terminierung an einem Load Balancer bedeutet, dass der Datenverkehr zwischen LB und Backend unverschlüsselt ist, sofern er nicht erneut verschlüsselt wird
- Certificate Pinning verhindert MITM-Angriffe, erschwert aber die Rotation von Zertifikaten – mit Vorsicht einsetzen
- `bcrypt` hat eine Passwortgrenze von 72 Bytes – längere Passwörter werden stillschweigend abgeschnitten
- Selbstsignierte Zertifikate verschlüsseln den Datenverkehr, authentifizieren aber nicht die Identität

## Siehe auch {#see-also}
- [[authentication-and-authorization]] – JWT, OAuth, Kerberos verwenden Kryptografie
- [[tls-fingerprinting-and-network-identifiers]] – TCP/IP-Stack-Fingerprinting
- [[web-application-security-fundamentals]] – HTTPS, CSP-Header
- [Database Security](database-security.md) – Verschlüsselung im Ruhezustand und bei der Übertragung
