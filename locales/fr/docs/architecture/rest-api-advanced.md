---
title: "REST API avancée - Performance, versionnage, mise en cache"
category: reference
tags: [rest, api, caching, rate-limiting, versioning, retry]
level: 4
source_sha256: 790494f424d524b0887feaf883ea33ecef1ec7bc20c15dbe117686dbca3d7dc8
translation: machine
translated_at: '2026-10-24'
---
# REST API avancée - Performance, versionnage, mise en cache {#rest-api-advanced-performance-versioning-caching}

La performance d'une API dépend de la vitesse, du volume de données et de la fréquence des appels. Des facteurs comme le coût des données mobiles, la consommation de batterie des appareils et la facturation des architectures serverless rendent l'efficacité essentielle.

## Limitation de débit et throttling {#rate-limiting-and-throttling}

### Limitation de débit au niveau des requêtes {#request-level-rate-limiting}
Limitez le nombre de requêtes par fenêtre temporelle, par adresse IP, par clé d'API ou par utilisateur. En cas de dépassement :
- **HTTP 429 Too Many Requests**
- `X-Rate-Limit-Limit` - nombre de requêtes autorisées sur la période en cours
- `X-Rate-Limit-Remaining` - nombre de requêtes restantes
- `X-Rate-Limit-Reset` - nombre de secondes avant la réinitialisation de la période

### Algorithmes de limitation de débit {#rate-limiting-algorithms}
- **Fenêtre fixe** - simple compteur par fenêtre temporelle
- **Fenêtre glissante** - plus précise, évite les rafales à la frontière de la fenêtre
- **Token bucket** - autorise de courtes rafales tout en maintenant un débit moyen (le plus courant)
- **Leaky bucket** - débit de sortie régulier, quel que soit le débit d'entrée

### Throttling au niveau applicatif {#application-level-throttling}
Protection interne contre les pics de charge. Priorise les requêtes urgentes. Implémenté par des délais ou un traitement par lots.

## Stratégies de mise en cache HTTP {#http-caching-strategies}

### Quatre approches de mise en cache {#four-caching-approaches}

| Stratégie | En-tête | Cas d'usage |
|----------|--------|----------|
| **Pas de cache** | `Cache-Control: private, no-cache, no-store` | Données confidentielles ou dynamiques |
| **Basée sur le temps** | `Cache-Control: max-age=3600, must-revalidate` | Intervalle de changement connu |
| **Basée sur la validation** | `Cache-Control: no-cache` + `ETag` | Intervalle de changement inconnu |
| **Cache permanent** | `Cache-Control: max-age=31536000, public, immutable` | Contenu immuable |

### Flux de validation (ETag) {#validation-flow-etag}
```rust
1. Server responds with: ETag: "abc123"
2. Client conditional request: If-None-Match: "abc123"
3. Server responds: 304 Not Modified (use cache)
   OR sends new data with new ETag
```

### Gestion du cache {#cache-management}
- Mettez en cache les fichiers indéfiniment avec des noms versionnés (`style1a.css`)
- Lors d'une mise à jour, renommez en `style2b.css` - le navigateur le traite comme une nouvelle ressource
- Invalidation complète : `Clear-Site-Data: "cache", "cookies", "storage"`

## Compression {#compression}

Aucune modification de la conception de l'API n'est nécessaire :
```yaml
# Client
Accept-Encoding: gzip, deflate, br

# Server
Content-Encoding: gzip
```

## Requêtes par lots {#batch-requests}

Combinez plusieurs opérations de l'API en une seule. Réduit la latence et économise la bande passante. Toutes les sous-requêtes sont regroupées dans une seule requête ; les réponses sont renvoyées ensemble. Voir le format de lot de l'API Google Drive comme référence.

## Versionnage de l'API {#api-versioning}

### Pourquoi versionner {#why-version}
- Maintenir la rétrocompatibilité pour les clients existants
- Communiquer clairement les fonctionnalités disponibles
- Permettre aux clients de migrer à leur propre rythme

### Versionnage sémantique {#semantic-versioning}
- **Non cassant** (nouveaux endpoints, nouveaux champs optionnels, nouveaux champs de réponse) : incrémentation mineure (1.0 -> 1.1)
- **Cassant** (endpoints supprimés, champs obligatoires modifiés, codes d'erreur modifiés) : incrémentation majeure (1.x -> 2.0)
- Conservez au maximum 2 versions actives ; informez les clients de la dépréciation

### Approches de versionnage {#versioning-approaches}

| Approche | Exemple | Remarques |
|----------|---------|-------|
| **Chemin d'URL** | `/api/v1/users` | Le plus courant, explicite |
| **Paramètre de requête** | `/api/users?version=1` | Simple mais peu propre |
| **En-tête** | `Accept: application/vnd.api.v1+json` | URLs plus propres |

### Migration d'API sans interruption {#zero-downtime-api-migration}
- Annonces de dépréciation avec un calendrier clair
- Surveillez l'utilisation des anciennes versions avant leur suppression
- Conservez les anciennes versions de l'API plus longtemps que prévu : certains clients n'appellent l'API qu'une fois par an
- Pattern expand-contract : ajoutez le nouveau à côté de l'ancien, migrez, puis supprimez l'ancien

## Patterns de nouvelle tentative {#retry-patterns}

### Backoff exponentiel {#exponential-backoff}
Commencez par un court délai, puis augmentez-le exponentiellement : 5s -> 25s -> 125s

### Jitter {#jitter}
Ajoutez de l'aléatoire aux délais de nouvelle tentative pour éviter l'effet thundering herd lorsque plusieurs clients réessaient simultanément.

### Règles de nouvelle tentative {#retry-rules}
- Ne réessayez que sur des erreurs transitoires (5xx, timeouts réseau)
- Ne réessayez pas les erreurs client (4xx) : elles ne se résoudront pas d'elles-mêmes
- Définissez un nombre maximal de tentatives
- Envisagez un circuit breaker pour les échecs persistants

## Format des réponses d'erreur {#error-response-format}

Format standardisé pour toutes les API :
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {"field": "email", "issue": "invalid format"}
    ]
  }
}
```

N'exposez jamais de détails internes d'erreur (traces de pile, requêtes SQL) en production.

## Pièges à éviter {#gotchas}

- **Cache et authentification** - ne mettez jamais en cache les réponses contenant un en-tête `Authorization`, sauf si elles sont explicitement `public`
- **429 sans en-têtes** - incluez toujours les en-têtes de limitation de débit afin que les clients puissent se throttler eux-mêmes
- **Nouvelle tentative sur POST** - dangereux sans clés d'idempotence, peut créer des ressources en double
- **Cache stampede** - lorsqu'une clé populaire expire, de nombreuses requêtes frappent la base de données simultanément. Utilisez des verrous ou une expiration anticipée probabiliste
- **Coût CPU de la compression** - activez-la pour le contenu textuel (JSON, HTML) mais pas pour le contenu déjà compressé (images, vidéos)

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - protocole HTTP, contraintes REST, conception des ressources
- [[api-authentication-security]] - OAuth 2.0, JWT, TLS
- [[caching-and-performance]] - Patterns de mise en cache au niveau applicatif
- [[api-documentation-specs]] - OpenAPI, Swagger, AsyncAPI
