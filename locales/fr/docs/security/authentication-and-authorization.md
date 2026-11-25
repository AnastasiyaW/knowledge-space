---
title: "Authentification et autorisation"
category: concepts
tags: [security, authentication, authorization, jwt, oauth, kerberos, mfa, rbac]
level: 3
source_sha256: 10b71eeb7fed49cac64c45ad9a7a41ac764baca2211d4c38be5ec5a4244c2b21
translation: machine
translated_at: '2026-10-24'
---
# Authentification et autorisation {#authentication-and-authorization}

Mécanismes d'authentification (prouver son identité) et d'autorisation (accorder un accès) : politiques de mots de passe, MFA, jetons JWT, OAuth 2.0/OIDC, Kerberos, RBAC et PAM. Couvre à la fois les modèles conceptuels et leur implémentation.

## Points clés {#key-facts}
- Authentification = qui vous êtes ; autorisation = ce que vous pouvez faire
- Facteurs MFA : quelque chose que vous connaissez + quelque chose que vous possédez + quelque chose que vous êtes
- Le 2FA par SMS est l'option MFA la plus faible (SIM swapping, attaques SS7)
- Les clés matérielles FIDO2/WebAuthn sont le MFA grand public le plus robuste
- OAuth 2.0 sert à l'autorisation (jetons d'accès) ; OIDC ajoute par-dessus l'authentification (jetons ID)
- NIST 800-63B déconseille la rotation forcée des mots de passe, car elle conduit à des mots de passe plus faibles

## Sécurité des mots de passe {#password-security}

### Politiques de mots de passe (modernes) {#password-policies-modern}
- Minimum 12 caractères ou plus
- Complexité encouragée mais non obligatoire (la longueur prime sur la complexité selon NIST)
- Vérification contre les bases de données de fuites (API Have I Been Pwned)
- Pas de rotation périodique forcée (NIST 800-63B)
- Verrouillage du compte après des échecs répétés (5 tentatives, verrouillage de 15 à 30 min)

### Hachage des mots de passe {#password-hashing}
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

## Authentification multifacteur (MFA) {#multi-factor-authentication-mfa}

| Méthode | Sécurité | UX | Notes |
|--------|----------|-----|-------|
| FIDO2/WebAuthn | Maximale | Bonne | Clés matérielles (YubiKey), résistantes au phishing |
| TOTP | Élevée | Correcte | Google Authenticator, Authy : codes basés sur le temps |
| Notifications push | Élevée | Bonne | Validation via application mobile |
| Codes SMS | Faible | Facile | SIM swapping, interception SS7 |

## JWT (JSON Web Tokens) {#jwt-json-web-tokens}

### Structure {#structure}
Trois parties encodées en Base64 et séparées par des points : `header.payload.signature`

### Implémentation (Node.js) {#implementation-nodejs}
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

### Stratégie JWT pour NestJS {#nestjs-jwt-strategy}
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

- **OAuth 2.0** - cadre d'autorisation (délivre des jetons d'accès)
- **OIDC** (OpenID Connect) - couche d'authentification au-dessus d'OAuth 2.0 (jetons ID)
- Flux : Authorization Code (applications serveur, le plus sûr), Client Credentials (service à service), Implicit (obsolète)

## Kerberos (Active Directory) {#kerberos-active-directory}

Authentification par tickets, sans envoi de mots de passe sur le réseau :
1. Le client s'authentifie auprès du KDC (Key Distribution Center)
2. Le KDC délivre un TGT (Ticket Granting Ticket)
3. Le client utilise le TGT pour demander des tickets de service pour des services spécifiques
4. Le service valide le ticket sans contacter le KDC

Attaques Kerberos : Kerberoasting, AS-REP Roasting, Golden/Silver Tickets (voir [[active-directory-attacks]]).

## LDAP {#ldap}
Protocole de service d'annuaire pour interroger et modifier les bases d'utilisateurs. Utilisé avec Active Directory. Port 389 (en clair), 636 (LDAPS).

## SSO (Single Sign-On) {#sso-single-sign-on}
Une seule authentification donne accès à plusieurs services. Réduit la fatigue liée aux mots de passe et centralise le contrôle d'accès. Risque : la compromission du SSO donne accès à tout.

## Modèles {#patterns}

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
- Coffre-fort de mots de passe : stockage chiffré des identifiants
- Enregistrement des sessions : audit des sessions d'administration
- Accès just-in-time : élévation temporaire de privilèges avec approbation
- Rotation des identifiants : changement automatique des mots de passe
- Procédures de bris de glace : accès d'urgence avec piste d'audit complète

### Rotation des jetons de rafraîchissement JWT {#jwt-refresh-token-rotation}

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

Authentification moderne sans mot de passe reposant sur la cryptographie à clé publique :
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
- Résistante au phishing : liaison cryptographique à l'origine (RP ID)
- Aucun secret partagé à voler sur le serveur
- Prise en charge : Chrome, Safari, Firefox, toutes les grandes plateformes

### ABAC et RBAC {#abac-vs-rbac}

| Caractéristique | RBAC | ABAC |
|---------|------|------|
| Granularité | Basée sur les rôles | Basée sur les attributs (utilisateur, ressource, environnement) |
| Complexité | Simple | Complexe mais flexible |
| Exemple | admin, editor, viewer | user.dept == resource.dept AND time < 17:00 |
| Idéal pour | Rôles bien définis | Accès dynamiques et sensibles au contexte |

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

## Pièges à éviter {#gotchas}
- Un jeton JWT ne peut pas être révoqué une fois émis : utilisez une expiration courte et des jetons de rafraîchissement
- Stocker un JWT dans localStorage le rend vulnérable au XSS ; les cookies HttpOnly sont plus sûrs mais nécessitent une protection CSRF
- Le flux implicite d'OAuth est obsolète : utilisez toujours Authorization Code avec PKCE
- Un décalage d'horloge Kerberos supérieur à 5 minutes provoque des échecs d'authentification
- Les cookies « Se souvenir de moi » doivent aussi être invalidés lors d'un changement de mot de passe
- Attaque JWT `alg: none` : validez toujours l'algorithme côté serveur, ne faites jamais confiance à l'en-tête du jeton
- La rotation des jetons de rafraîchissement sans suivi des révocations permet le rejeu de jetons : conservez un identifiant de famille de jetons et révoquez toute la famille en cas de réutilisation détectée
- Les passkeys éliminent le phishing mais nécessitent une solution de repli pour la récupération de compte : planifiez soigneusement les procédures de récupération
- bcrypt est limité à 72 octets en entrée : pour les mots de passe longs, pré-hachez-les avec SHA-256 puis appliquez bcrypt

## Voir aussi {#see-also}
- [[cryptography-and-pki]] - mécanismes cryptographiques sous-jacents
- [[web-application-security-fundamentals]] - gestion des sessions, CSRF
- [[active-directory-attacks]] - Kerberoasting, Golden Ticket
- [[windows-security-and-powershell]] - fonctionnement interne de l'authentification Windows, SAM, LSASS
