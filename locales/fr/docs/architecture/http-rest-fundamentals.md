---
title: "Fondamentaux de HTTP et des API REST"
category: reference
tags: [http, rest, api, web-services, protocol]
level: 2
source_sha256: f90ebbe43261a72beddd0205bab71e1e58ba4f970a48e8298b79d4f2a1f27fc7
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de HTTP et des API REST {#http-and-rest-api-fundamentals}

REST (Representational State Transfer) est un style d'architecture pour les systèmes distribués, et non un protocole. Il s'aligne sur l'architecture de l'Internet et utilise l'infrastructure HTTP existante. REST est le style d'API le plus largement utilisé pour les API publiques.

## Protocole HTTP {#http-protocol}

### Structure requête/réponse {#requestresponse-structure}

```html
# Request
<METHOD> <URI> HTTP/<VERSION>
<Headers>
<Empty line>
<Body>

# Response
HTTP/<VERSION> <STATUS_CODE> <REASON>
<Headers>
<Empty line>
<Body>
```

### Méthodes HTTP {#http-methods}

| Méthode | CRUD | Idempotente | Sûre | Corps de requête |
|---------|------|-------------|------|------------------|
| GET | Lecture | Oui | Oui | Non |
| POST | Création | Non | Non | Oui |
| PUT | Mise à jour complète / Création | Oui | Non | Oui |
| PATCH | Mise à jour partielle | Non* | Non | Oui |
| DELETE | Suppression | Oui | Non | Optionnel |
| HEAD | Lecture des en-têtes | Oui | Oui | Non |
| OPTIONS | Obtention des capacités | Oui | Oui | Non |

*PATCH peut être rendue idempotente avec une implémentation appropriée.

**Idempotente** = plusieurs requêtes identiques produisent le même résultat. **Sûre** = ne modifie pas l'état du serveur.

### Codes de statut {#status-codes}

| Plage | Signification | Codes principaux |
|-------|---------------|------------------|
| 2xx | Succès | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 304 Not Modified |
| 4xx | Erreur client | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| 5xx | Erreur serveur | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

### En-têtes principaux {#key-headers}

**Requête :** `Host` (obligatoire en HTTP/1.1), `Content-Type`, `Accept`, `Authorization`, `Cache-Control`, `User-Agent`

**Réponse :** `Content-Type`, `Content-Length`, `Cache-Control`, `ETag`, `Last-Modified`, `Set-Cookie`

### Versions de HTTP {#http-versions}

| Version | Principales caractéristiques |
|---------|------------------------------|
| HTTP/1.0 | Une requête par connexion TCP |
| HTTP/1.1 | Connexions persistantes, en-tête Host, transfert en morceaux (chunked), pipelining |
| HTTP/2 | Trames binaires, multiplexage, compression d'en-têtes (HPACK), server push |
| HTTP/3 | Basé sur QUIC (UDP), latence réduite, meilleures performances sur mobile |

## Les six contraintes de REST {#rest-six-constraints}

1. **Client-serveur** - séparation des préoccupations de l'interface utilisateur et du stockage des données
2. **Sans état (Stateless)** - chaque requête contient toutes les informations nécessaires à son traitement
3. **Cacheable** - les réponses déclarent si elles sont cacheables ou non
4. **Interface uniforme** - identification des ressources via des URI, manipulation par des représentations, messages auto-descriptifs, HATEOAS
5. **Système en couches** - le client ne peut pas savoir s'il est connecté directement au serveur ou via un intermédiaire
6. **Code à la demande** (optionnel) - le serveur peut envoyer du code exécutable (JavaScript)

## Conception d'URL orientée ressources {#resource-based-url-design}

```sql
# Resources are nouns, not verbs
/users            # collection
/users/123        # specific resource
/users/123/orders # nested resource

# Actions via HTTP methods, not URL
DELETE /users/123          # correct
POST /users/123/delete     # wrong

# Naming conventions
/order-items     # hyphens for multi-word
/users/123       # plurals
                 # lowercase, no trailing slashes, no file extensions
```

## Types de ressources REST {#rest-resource-types}

| Type | Description | Source de l'ID |
|------|-------------|----------------|
| **Objet** | Ressource unique avec un ID unique | - |
| **Collection** | Catalogue géré par le serveur | Le serveur génère les ID |
| **Store** | Stockage géré par le client | Le client attribue les ID |
| **Contrôleur** | Action/fonction (de type RPC) | Basé sur POST |

## Filtrage, pagination, recherche {#filtering-pagination-search}

### Approches de pagination {#pagination-approaches}

| Approche | Exemple | Avantages/Inconvénients |
|----------|---------|-------------------------|
| **Par décalage (offset)** | `?offset=20&limit=10` | Simple, permet de sauter directement à une page ; incohérent avec les données en temps réel |
| **Par curseur (cursor)** | `?cursor=abc123&limit=10` | Stable avec les données en temps réel ; impossible de sauter à une page arbitraire |
| **Par clé (keyset)** | `?after_id=100&limit=20` | Très performant avec des colonnes indexées |

### Filtrage et tri {#filtering-and-sorting}

```bash
?status=active&created_after=2024-01-01    # filtering
?sort=created_at&order=desc                # sorting
?q=search+term                             # full-text search
```

## Transfert de fichiers {#file-transfer}

```yaml
# Client request
Accept: image/png

# Server response
Content-Type: image/png
Content-Disposition: attachment; filename="file.png"
Content-Length: 12345

# Large files
Transfer-Encoding: chunked
```

## CORS (Cross-Origin Resource Sharing) {#cors-cross-origin-resource-sharing}

Mécanisme de sécurité du navigateur. Le serveur déclare les origines autorisées :
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`

Les requêtes de pré-vérification (preflight, OPTIONS) sont envoyées pour les requêtes non simples. Essentiel pour l'intégration frontend-backend.

## Comparaison des styles d'API {#api-style-comparison}

| Aspect | REST | JSON-RPC | GraphQL | gRPC |
|--------|------|----------|---------|------|
| Paradigme | Orienté ressources | Orienté fonctions | Orienté requêtes | Orienté fonctions |
| Transport | HTTP | HTTP/TCP/WS | HTTP | HTTP/2 |
| Format | JSON/XML | JSON | Proche de JSON | Protobuf (binaire) |
| Mise en cache | Native (HTTP) | Difficile | Difficile | Difficile |
| Typage | Faible (OpenAPI) | Faible | Fort (schéma) | Fort (proto) |
| Idéal pour | API publiques, CRUD | API internes simples | Requêtes complexes | Microservices |

## Pièges courants {#gotchas}

- **PUT remplace tout** - il faut envoyer la ressource entière, et non une partie. Utiliser PATCH pour les mises à jour partielles
- **POST n'est pas idempotente** - plusieurs appels identiques créent des doublons, sauf si une déduplication est implémentée
- **HTTP 200 pour les erreurs SOAP** - SOAP renvoie 200 pour les erreurs métier, et seulement des 4xx pour les erreurs de protocole
- **HATEOAS** fait partie de la spécification REST mais est rarement implémenté en pratique
- **Versionnement dans l'URL** (`/api/v1/users`) est le plus courant ; il est recommandé de garder au maximum 2 versions actives

## Voir aussi {#see-also}

- [[rest-api-advanced]] - Limitation de débit, stratégies de cache, requêtes par lots, schémas de nouvelle tentative
- [[api-authentication-security]] - OAuth 2.0, JWT, mTLS, détails sur CORS
- [[graphql-api]] - Langage de requête pour la récupération flexible de données
- [[grpc-api]] - Framework RPC binaire haute performance
