---
title: "API-Authentifizierung und Sicherheit"
category: reference
tags: [security, authentication, authorization, oauth, jwt, tls, encryption]
level: 3
source_sha256: 0acb61926e8038ae186c13d84ad1c7f8d8a1afeb8b75cb9752c9d3a66073bef5
translation: machine
translated_at: '2026-10-24'
---
# API-Authentifizierung und Sicherheit {#api-authentication-and-security}

Authentifizierung belegt die Identität, Autorisierung bestimmt die Zugriffsrechte. Die Sicherheitsarchitektur umfasst Kryptografie, Protokolle und organisatorische Praktiken. Der Architekt identifiziert Schwachstellen und kommuniziert sie an die richtigen Personen.

## Authentifizierung vs. Autorisierung {#authentication-vs-authorization}

| Konzept | Frage | Beispiel |
|---------|-------|----------|
| **Identifikation** | Wer bist du? | Benutzername/Login |
| **Authentifizierung** | Beweise es | Passwort, Token, Biometrie |
| **Autorisierung** | Worauf darfst du zugreifen? | Berechtigungen, Rollen |

## Authentifizierungsmethoden {#authentication-methods}

### 1. API-Key {#1-api-key}
Einfacher Schlüssel im Header: `X-API-Key: abc123`. Einfach, aber eingeschränkt – typischerweise für Server-zu-Server-Kommunikation, nicht für die Authentifizierung auf Benutzerebene.

### 2. Basic Auth {#2-basic-auth}
Base64-kodiertes `username:password` im `Authorization`-Header. HTTPS ist zwingend erforderlich. Die Zugangsdaten werden bei jeder Anfrage übertragen.

### 3. Sitzungsbasiert (Cookies) {#3-session-based-cookies}
Der Server erstellt beim Login eine Sitzung und speichert die Sitzungs-ID in einem Cookie. Der Browser sendet das Cookie automatisch mit.
- Cookie-Attribute: `Secure` (nur HTTPS), `HttpOnly` (kein JS-Zugriff), `SameSite` (CSRF-Schutz)
- Erfordert Sitzungsspeicher (Keycloak, Redis)

### 4. JWT (JSON Web Token) {#4-jwt-json-web-token}
Eigenständiges Token: `header.payload.signature` (Base64-kodiert).

```yaml
Header:    {"alg": "HS256", "typ": "JWT"}
Payload:   {"user_id": 123, "roles": ["admin"], "exp": 1700000000}
Signature: HMAC-SHA256(base64(header) + "." + base64(payload), secret)
```

- **Zustandslos** – der Server speichert keine Sitzungen
- **Token-Paar** – Access-Token (kurzlebig, 15–30 Min.) + Refresh-Token (langlebig)

### 5. OAuth 2.0 {#5-oauth-20}
Framework für delegierte Autorisierung. Vier Rollen: Resource Owner, Client, Authorization Server, Resource Server.

**Grant-Typen:**

| Typ | Anwendungsfall |
|-----|----------------|
| Authorization Code | Serveranwendungen (am sichersten) |
| Client Credentials | Maschine-zu-Maschine |
| PKCE | Mobile Apps/SPAs |

**Authorization-Code-Flow:**
```text
1. Client redirects user to authorization server
2. User authenticates and grants permission
3. Auth server returns authorization code
4. Client exchanges code for access token (server-side)
5. Client uses access token to access resources
```

### 6. mTLS (Mutual TLS) {#6-mtls-mutual-tls}
Client und Server präsentieren beide Zertifikate. Wird in Szenarien mit hohen Sicherheitsanforderungen eingesetzt: Finanz-APIs, Kommunikation zwischen Diensten.

## Grundlagen der Kryptografie {#cryptography-fundamentals}

### Symmetrische Verschlüsselung {#symmetric-encryption}
Ein gemeinsamer geheimer Schlüssel für Ver- und Entschlüsselung. Schnell, aber der Schlüssel muss sicher übertragen werden.
- Pro: schnell, geeignet für große Datenmengen
- Contra: die Schlüsselübertragung ist die Schwachstelle

### Asymmetrische Verschlüsselung {#asymmetric-encryption}
Zwei Schlüssel: öffentlicher (verschlüsselt) und privater (entschlüsselt). Der Empfänger verteilt den öffentlichen Schlüssel frei.
- Pro: hohe Sicherheit, kein Risiko bei der Schlüsselübertragung, ermöglicht digitale Signaturen
- Contra: um Größenordnungen langsamer, höherer Rechenaufwand

### Hybride Verschlüsselung (HTTPS) {#hybrid-encryption-https}
Asymmetrische Verschlüsselung zum sicheren Austausch des symmetrischen Schlüssels, anschließend symmetrische Verschlüsselung für die eigentliche Datenübertragung. Das Beste aus beiden Welten.

### TLS-Handshake {#tls-handshake}
```hcl
1. Client sends supported cipher suites
2. Server selects cipher, sends certificate with public key
3. Client verifies certificate against CA
4. Key exchange (Diffie-Hellman or RSA)
5. Symmetric key established for session
6. All subsequent data encrypted symmetrically
```

## Digitale Signaturen {#digital-signatures}

1. Der Absender erstellt einen Hash des Dokuments
2. Der Hash wird mit dem **privaten Schlüssel** des Absenders verschlüsselt = digitale Signatur
3. Der Empfänger entschlüsselt die Signatur mit dem **öffentlichen Schlüssel** des Absenders und erhält den Hash
4. Der Empfänger berechnet unabhängig davon den Hash des Dokuments
5. Stimmen die Hashes überein, ist das Dokument authentisch und unverändert

Das **Certificate-Authority-(CA)-System** verifiziert die Identität. Die CA führt ein Register gültiger und widerrufener Zertifikate.

## Hashing {#hashing}

Eine Einweg-Transformation mit einer Ausgabe fester Länge. Jede Änderung auch nur eines Zeichens erzeugt einen völlig anderen Hash. Einsatz für: Speicherung von Passwörtern, Prüfung der Datenintegrität, digitale Signaturen.

## Checkliste zur Anwendungssicherheit {#application-security-checklist}

| Bereich | Bedrohungen | Gegenmaßnahmen |
|---------|-------------|----------------|
| Eingabevalidierung | SQL-Injection, XSS | Parametrisierte Abfragen, Sanitisierung |
| Sitzungsverwaltung | Session Hijacking | Eindeutige IDs, Secure/HttpOnly-Cookies |
| Datenverschlüsselung | Abhören | AES im Ruhezustand, TLS bei der Übertragung |
| API-Sicherheit | Code-Injection | API-Gateway, Eingabevalidierung |
| Protokollierung | Unentdeckte Angriffe | ELK Stack, Grafana, Audit-Trail |
| Code-Scanning | Schwachstellen | OWASP ZAP, SonarQube |
| Fehlerbehandlung | Informationslecks | Eigene Fehlerseiten, Details nur intern |
| Rate Limiting | DoS/DDoS | Limits pro Benutzer/IP |

## Sicherheit auf Datenebene {#data-level-security}

- **Verschlüsselung im Ruhezustand** – AES, TDE. Regelmäßige Schlüsselrotation
- **Verschlüsselung bei der Übertragung** – TLS/SSL für sämtliche Übertragungen
- **Datenmaskierung** – maskierte Werte für Nicht-Produktivumgebungen
- **Zugriffskontrolle** – RBAC, Prinzip der minimalen Rechte
- **DLP** – Überwachung und Blockierung unautorisierter Datenübertragungen
- **Unveränderliche Backups (WORM)** – Write Once, Read Many
- **Zero Trust** – jede Anfrage unabhängig von ihrer Herkunft verifizieren

## Fallstricke {#gotchas}

- **JWT im Local Storage** – anfällig für XSS. Bei Web-Anwendungen HttpOnly-Cookies bevorzugen
- **API-Keys in URLs** – sichtbar in Logs und im Browserverlauf. Stattdessen Header verwenden
- **OAuth Implicit Flow** – veraltet. Stattdessen Authorization Code + PKCE verwenden
- **Selbstsignierte Zertifikate** – SSL-Prüfung nur in der Entwicklung deaktivieren, niemals in Produktion
- **Fehlermeldungen** – „Invalid username“ vs. „Invalid password“ verrät, welche Angabe korrekt ist. Stattdessen generisch „Invalid credentials“ verwenden

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] – Grundlagen des HTTP-Protokolls, CORS
- [[security-architecture]] – Sicherheits-Workflow des Architekten
- [[authentication-and-authorization]] – SSO-Muster, SAML, OpenID Connect
