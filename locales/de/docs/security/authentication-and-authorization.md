---
title: "Authentifizierung und Autorisierung"
category: concepts
tags: [security, authentication, authorization, jwt, oauth, kerberos, mfa, rbac]
level: 3
source_sha256: 10b71eeb7fed49cac64c45ad9a7a41ac764baca2211d4c38be5ec5a4244c2b21
translation: machine
translated_at: '2026-10-24'
---
# Authentifizierung und Autorisierung {#authentication-and-authorization}

Mechanismen zur Authentifizierung (Identitätsnachweis) und Autorisierung (Zugriffsgewährung): Passwortrichtlinien, MFA, JWT-Token, OAuth 2.0/OIDC, Kerberos, RBAC und PAM. Behandelt sowohl konzeptionelle Muster als auch die Implementierung.

## Kernfakten {#key-facts}
- Authentifizierung = wer du bist; Autorisierung = was du tun darfst
- MFA-Faktoren: etwas, das du weißt + etwas, das du besitzt + etwas, das du bist
- SMS-basierte 2FA ist die schwächste MFA-Option (SIM-Swapping, SS7-Angriffe)
- FIDO2/WebAuthn-Hardware-Schlüssel sind die stärkste MFA für Endanwender
- OAuth 2.0 dient der Autorisierung (Access-Token); OIDC ergänzt darauf die Authentifizierung (ID-Token)
- NIST 800-63B rät von erzwungener Passwortrotation ab, da sie zu schwächeren Passwörtern führt

## Passwortsicherheit {#password-security}

### Passwortrichtlinien (modern) {#password-policies-modern}
- Mindestens 12 oder mehr Zeichen
- Komplexität wird empfohlen, aber nicht vorausgesetzt (Länge vor Komplexität laut NIST)
- Prüfung gegen Datenbanken kompromittierter Passwörter (Have I Been Pwned API)
- Keine erzwungene periodische Rotation (NIST 800-63B)
- Kontosperrung nach fehlgeschlagenen Versuchen (5 Versuche, Sperre für 15–30 Minuten)

### Passwort-Hashing {#password-hashing}
```python
# bcrypt (recommended)
import bcrypt
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password.encode(), salt)
# Verify
bcrypt.checkpw(input_password.encode(), hashed)
```

```javascript
// Node.js with bcryptjs
const bcrypt = require('bcryptjs');
const salt = await bcrypt.genSalt(10);
const hashed = await bcrypt.hash(password, salt);
const isMatch = await bcrypt.compare(inputPassword, hashed);
```

## Multi-Faktor-Authentifizierung (MFA) {#multi-factor-authentication-mfa}

| Methode | Sicherheit | Bedienbarkeit | Hinweise |
|--------|----------|-----|-------|
| FIDO2/WebAuthn | Sehr hoch | Gut | Hardware-Schlüssel (YubiKey), phishingresistent |
| TOTP | Hoch | Akzeptabel | Google Authenticator, Authy – zeitbasierte Codes |
| Push-Benachrichtigungen | Hoch | Gut | Freigabe über die Mobil-App |
| SMS-Codes | Niedrig | Einfach | SIM-Swapping, Abfangangriffe über SS7 |

## JWT (JSON Web Tokens) {#jwt-json-web-tokens}

### Aufbau {#structure}
Drei Base64-kodierte Teile, durch Punkte getrennt: `header.payload.signature`

### Implementierung (Node.js) {#implementation-nodejs}
```javascript
const jwt = require('jsonwebtoken');

// Generate
const token = jwt.sign(
  { userId: user.id, email: user.email },
  process.env.JWT_SECRET,
  { expiresIn: '24h' }
);

// Verify middleware
const auth = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (e) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

### NestJS-JWT-Strategie {#nestjs-jwt-strategy}
```typescript
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: process.env.JWT_SECRET,
    });
  }
  async validate(payload: any) {
    return { userId: payload.sub, email: payload.email };
  }
}
```

## OAuth 2.0 / OIDC {#oauth-20-oidc}

- **OAuth 2.0** – Autorisierungsframework (stellt Access-Token aus)
- **OIDC** (OpenID Connect) – Authentifizierungsschicht auf OAuth 2.0 (ID-Token)
- Flows: Authorization Code (serverseitige Anwendungen, am sichersten), Client Credentials (Service-zu-Service), Implicit (veraltet)

## Kerberos (Active Directory) {#kerberos-active-directory}

Ticketbasierte Authentifizierung – im Netzwerk werden keine Passwörter übertragen:
1. Der Client authentifiziert sich beim KDC (Key Distribution Center)
2. Das KDC stellt ein TGT (Ticket Granting Ticket) aus
3. Der Client verwendet das TGT, um Service-Tickets für bestimmte Dienste anzufordern
4. Der Dienst validiert das Ticket, ohne das KDC zu kontaktieren

Kerberos-Angriffe: Kerberoasting, AS-REP Roasting, Golden/Silver Tickets (siehe [[active-directory-attacks]]).

## LDAP {#ldap}
Verzeichnisdienstprotokoll zum Abfragen und Ändern von Benutzerdatenbanken. Wird mit Active Directory verwendet. Port 389 (unverschlüsselt), 636 (LDAPS).

## SSO (Single Sign-On) {#sso-single-sign-on}
Eine einzige Authentifizierung gewährt Zugriff auf mehrere Dienste. Verringert die Passwortmüdigkeit und zentralisiert die Zugriffskontrolle. Risiko: Die Kompromittierung von SSO bedeutet Zugriff auf alles.

## Muster {#patterns}

### RBAC (Role-Based Access Control) {#rbac-role-based-access-control}
```typescript
// NestJS Guard implementation
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}
  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>('roles', context.getHandler());
    if (!requiredRoles) return true;
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}
```

### PAM (Privileged Access Management) {#pam-privileged-access-management}
- Passwort-Tresor – verschlüsselte Speicherung von Zugangsdaten
- Sitzungsaufzeichnung – Überwachung administrativer Sitzungen
- Just-in-time-Zugriff – zeitlich begrenzte Rechteerhöhung mit Genehmigung
- Rotation von Zugangsdaten – automatisierte Passwortwechsel
- Break-Glass-Verfahren – Notfallzugriff mit lückenlosem Audit-Trail

### JWT-Refresh-Token-Rotation {#jwt-refresh-token-rotation}

```bash
Access Token:  short-lived (15 min), stateless verification
Refresh Token: long-lived (7 days), stored server-side, single-use

Flow:
1. Login -> access_token + refresh_token
2. API calls with access_token in Authorization header
3. On 401 -> POST /refresh with refresh_token
4. Server invalidates old refresh_token, issues new pair
5. If old refresh_token reused -> token theft detected -> revoke all tokens for user
```

### Passkeys (FIDO2/WebAuthn) {#passkeys-fido2webauthn}

Moderne passwortlose Authentifizierung auf Basis von Public-Key-Kryptografie:
```yaml
Registration:
1. Server sends challenge (random bytes)
2. Authenticator generates key pair
3. Private key stored on device (never leaves)
4. Public key sent to server

Authentication:
1. Server sends challenge
2. Authenticator signs challenge with private key
3. Server verifies signature with stored public key
```
- Phishingresistent: kryptografische Bindung an den Ursprung (RP ID)
- Keine gemeinsamen Geheimnisse, die auf dem Server gestohlen werden könnten
- Unterstützt: Chrome, Safari, Firefox, alle gängigen Plattformen

### ABAC vs. RBAC {#abac-vs-rbac}

| Merkmal | RBAC | ABAC |
|---------|------|------|
| Granularität | Rollenbasiert | Attributbasiert (Benutzer, Ressource, Umgebung) |
| Komplexität | Einfach | Komplex, aber flexibel |
| Beispiel | admin, editor, viewer | user.dept == resource.dept AND time < 17:00 |
| Geeignet für | Klar definierte Rollen | Dynamischen, kontextabhängigen Zugriff |

```python
# ABAC-style policy check
def can_access(user, resource, action):
    if action == "read" and resource.classification == "public":
        return True
    if user.department == resource.department and user.clearance >= resource.sensitivity:
        return True
    if user.role == "admin" and not resource.restricted:
        return True
    return False
```

## Stolperfallen {#gotchas}
- JWT-Token können nach der Ausstellung nicht widerrufen werden – verwende kurze Gültigkeitsdauern und Refresh-Token
- Das Speichern von JWT im localStorage ist anfällig für XSS; HttpOnly-Cookies sind sicherer, benötigen aber CSRF-Schutz
- Der OAuth-Implicit-Flow ist veraltet – verwende immer Authorization Code + PKCE
- Eine Zeitabweichung über 5 Minuten bei Kerberos führt zu Authentifizierungsfehlern
- „Angemeldet bleiben“-Cookies müssen bei einer Passwortänderung trotzdem ungültig gemacht werden
- JWT-Angriff mit `alg: none` – validiere den Algorithmus immer serverseitig und vertraue nie dem Token-Header
- Refresh-Token-Rotation ohne Widerrufsverfolgung erlaubt Token-Replay – speichere eine Token-Family-ID und widerrufe die gesamte Family bei erkannter Wiederverwendung
- Passkeys verhindern Phishing, erfordern aber für die Kontowiederherstellung einen Fallback – plane die Wiederherstellungsabläufe sorgfältig
- bcrypt hat eine Eingabegrenze von 72 Byte – lange Passwörter zuerst mit SHA-256 hashen und danach mit bcrypt (Vorab-Hashing)

## Siehe auch {#see-also}
- [[cryptography-and-pki]] – zugrunde liegende kryptografische Mechanismen
- [[web-application-security-fundamentals]] – Sitzungsverwaltung, CSRF
- [[active-directory-attacks]] – Kerberoasting, Golden Ticket
- [[windows-security-and-powershell]] – Interna der Windows-Authentifizierung, SAM, LSASS
