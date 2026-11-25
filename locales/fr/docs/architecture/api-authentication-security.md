---
title: "Authentification et sécurité des API"
category: reference
tags: [security, authentication, authorization, oauth, jwt, tls, encryption]
level: 3
source_sha256: 0acb61926e8038ae186c13d84ad1c7f8d8a1afeb8b75cb9752c9d3a66073bef5
translation: machine
translated_at: '2026-10-24'
---
# Authentification et sécurité des API {#api-authentication-and-security}

L'authentification prouve l'identité, l'autorisation détermine les accès. L'architecture de sécurité couvre la cryptographie, les protocoles et les pratiques organisationnelles. L'architecte identifie les points faibles et les communique aux personnes concernées.

## Authentification vs autorisation {#authentication-vs-authorization}

| Concept | Question | Exemple |
|---------|----------|---------|
| **Identification** | Qui êtes-vous ? | Nom d'utilisateur/login |
| **Authentification** | Prouvez-le | Mot de passe, jeton, biométrie |
| **Autorisation** | À quoi pouvez-vous accéder ? | Permissions, rôles |

## Méthodes d'authentification {#authentication-methods}

### 1. Clé API {#1-api-key}
Clé simple dans un en-tête : `X-API-Key: abc123`. Facile à mettre en œuvre mais limitée : généralement destinée aux communications serveur à serveur, et non à l'authentification au niveau utilisateur.

### 2. Basic Auth {#2-basic-auth}
`username:password` encodé en Base64 dans l'en-tête `Authorization`. HTTPS obligatoire. Les identifiants sont envoyés à chaque requête.

### 3. Basée sur les sessions (cookies) {#3-session-based-cookies}
Le serveur crée une session à la connexion et stocke l'identifiant de session dans un cookie. Le navigateur envoie le cookie automatiquement.
- Attributs du cookie : `Secure` (HTTPS uniquement), `HttpOnly` (pas d'accès par JS), `SameSite` (protection CSRF)
- Nécessite un stockage des sessions (Keycloak, Redis)

### 4. JWT (JSON Web Token) {#4-jwt-json-web-token}
Jeton autonome : `header.payload.signature` (encodé en Base64).

```yaml
Header:    {"alg": "HS256", "typ": "JWT"}
Payload:   {"user_id": 123, "roles": ["admin"], "exp": 1700000000}
Signature: HMAC-SHA256(base64(header) + "." + base64(payload), secret)
```

- **Sans état (stateless)** - le serveur ne stocke pas les sessions
- **Paire de jetons** - jeton d'accès (courte durée de vie, 15 à 30 min) + jeton de rafraîchissement (longue durée de vie)

### 5. OAuth 2.0 {#5-oauth-20}
Framework d'autorisation déléguée. Quatre rôles : propriétaire de la ressource (Resource Owner), client, serveur d'autorisation (Authorization Server), serveur de ressources (Resource Server).

**Types de grant :**

| Type | Cas d'usage |
|------|-------------|
| Authorization Code | Applications serveur (le plus sûr) |
| Client Credentials | Machine à machine |
| PKCE | Applications mobiles/SPA |

**Flux Authorization Code :**
```text
1. Client redirects user to authorization server
2. User authenticates and grants permission
3. Auth server returns authorization code
4. Client exchanges code for access token (server-side)
5. Client uses access token to access resources
```

### 6. mTLS (TLS mutuel) {#6-mtls-mutual-tls}
Le client et le serveur présentent tous deux un certificat. Utilisé dans les scénarios à haute sécurité : API financières, communications inter-services.

## Bases de la cryptographie {#cryptography-fundamentals}

### Chiffrement symétrique {#symmetric-encryption}
Une seule clé secrète partagée pour le chiffrement et le déchiffrement. Rapide, mais la clé doit être transmise de manière sécurisée.
- Avantage : rapide, adapté aux gros volumes de données
- Inconvénient : la transmission de la clé constitue la vulnérabilité

### Chiffrement asymétrique {#asymmetric-encryption}
Deux clés : publique (chiffre) et privée (déchiffre). Le destinataire diffuse librement sa clé publique.
- Avantage : haut niveau de sécurité, aucun risque lié à la transmission de clé, permet les signatures numériques
- Inconvénient : beaucoup plus lent, coût de calcul plus élevé

### Chiffrement hybride (HTTPS) {#hybrid-encryption-https}
Chiffrement asymétrique pour échanger de manière sécurisée la clé symétrique, puis chiffrement symétrique pour le transfert effectif des données. Le meilleur des deux mondes.

### Handshake TLS {#tls-handshake}
```hcl
1. Client sends supported cipher suites
2. Server selects cipher, sends certificate with public key
3. Client verifies certificate against CA
4. Key exchange (Diffie-Hellman or RSA)
5. Symmetric key established for session
6. All subsequent data encrypted symmetrically
```

## Signatures numériques {#digital-signatures}

1. L'expéditeur calcule le hash du document
2. Le hash est chiffré avec la **clé privée** de l'expéditeur = signature numérique
3. Le destinataire déchiffre la signature avec la **clé publique** de l'expéditeur pour obtenir le hash
4. Le destinataire calcule indépendamment le hash du document
5. Si les hash correspondent : le document est authentique et n'a pas été modifié

Le système des **autorités de certification (CA)** vérifie les identités. La CA tient un registre des certificats valides et révoqués.

## Hachage {#hashing}

Transformation à sens unique produisant une sortie de longueur fixe. Toute modification d'un seul caractère produit un hash complètement différent. Utilisé pour : le stockage des mots de passe, la vérification de l'intégrité des données, les signatures numériques.

## Liste de contrôle de la sécurité applicative {#application-security-checklist}

| Domaine | Menaces | Mesures d'atténuation |
|---------|---------|-----------------------|
| Validation des entrées | Injection SQL, XSS | Requêtes paramétrées, assainissement |
| Gestion des sessions | Détournement de session | Identifiants uniques, cookies Secure/HttpOnly |
| Chiffrement des données | Interception | AES au repos, TLS en transit |
| Sécurité des API | Injection de code | API Gateway, validation des entrées |
| Journalisation | Attaques non détectées | ELK Stack, Grafana, piste d'audit |
| Analyse de code | Vulnérabilités | OWASP ZAP, SonarQube |
| Gestion des erreurs | Fuite d'informations | Pages d'erreur personnalisées, détails réservés à l'interne |
| Limitation de débit | DoS/DDoS | Limites par utilisateur/IP |

## Sécurité au niveau des données {#data-level-security}

- **Chiffrement au repos** - AES, TDE. Rotation régulière des clés
- **Chiffrement en transit** - TLS/SSL pour toutes les transmissions
- **Masquage des données** - valeurs masquées pour les environnements hors production
- **Contrôle d'accès** - RBAC, principe du moindre privilège
- **DLP** - surveillance et blocage des transferts de données non autorisés
- **Sauvegardes immuables (WORM)** - Write Once, Read Many
- **Zero Trust** - vérifier chaque requête, quelle que soit sa source

## Pièges courants {#gotchas}

- **JWT dans le local storage** - vulnérable au XSS. Privilégier les cookies HttpOnly pour les applications web
- **Clés API dans les URL** - visibles dans les journaux et l'historique du navigateur. Utiliser les en-têtes
- **Flux implicite OAuth** - déprécié. Utiliser Authorization Code + PKCE à la place
- **Certificats auto-signés** - désactiver la vérification SSL uniquement en développement, jamais en production
- **Messages d'erreur** - « Nom d'utilisateur invalide » vs « Mot de passe invalide » révèle lequel est correct. Utiliser un message générique « Identifiants invalides »

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - bases du protocole HTTP, CORS
- [[security-architecture]] - workflow de sécurité de l'architecte
- [[authentication-and-authorization]] - modèles SSO, SAML, OpenID Connect
