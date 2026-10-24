---
title: "Conception d'API JSON-RPC"
category: reference
tags: [json-rpc, rpc, api, protocol]
level: 3
source_sha256: 08af5358e15b92b0d38a80f07f33b2c3de5a6960d368075824a7063eb3e29318
translation: machine
translated_at: '2026-10-24'
---
# Conception d'API JSON-RPC {#json-rpc-api-design}

JSON-RPC est un protocole RPC léger encodé en JSON. Le client envoie le nom de la fonction et ses paramètres ; le serveur l'exécute et renvoie le résultat. Toutes les requêtes sont envoyées à un seul point de terminaison. Version actuelle : 2.0.

## Format des requêtes et des réponses {#requestresponse-format}

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getMenu",
  "params": {"category": "pizza"}
}

// Success response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {"items": ["Margherita", "Pepperoni"]}
}

// Error response
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {"code": -32601, "message": "Method not found"}
}
```

Champs : `jsonrpc` (obligatoire, "2.0"), `id` (identifiant unique de la requête), `method` (nom de la fonction), `params` (facultatif).

## Codes d'erreur standard {#standard-error-codes}

| HTTP | Code JSON-RPC | Signification |
|------|--------------|---------|
| 500 | -32700 | Erreur d'analyse |
| 400 | -32600 | Requête invalide |
| 404 | -32601 | Méthode introuvable |
| 500 | -32602 | Paramètres invalides |
| 500 | -32603 | Erreur interne |
| 500 | -32099..-32000 | Erreurs serveur personnalisées |

Spécification : https://www.jsonrpc.org/specification

## Requêtes par lot {#batch-requests}

JSON-RPC prend nativement en charge les requêtes par lot : plusieurs opérations dans une seule requête HTTP. C'est plus élégant que REST, où chaque opération nécessite généralement une requête distincte.

## Avantages {#advantages}

- **Léger et performant** - JSON compact, rapide pour les petites données
- **Implémentation simple** - structure directe, paramètres uniquement dans le corps
- **Indépendance vis-à-vis du transport** - HTTP, TCP, WebSocket
- **Prise en charge native des lots** - plusieurs opérations par requête

## Inconvénients {#disadvantages}

- **Pas de mise en cache intégrée** - afficher deux fois les mêmes données nécessite une nouvelle requête
- **Gestion des erreurs limitée** - le serveur renvoie HTTP 200 pour les erreurs métier
- **Pas de standard pour les schémas complexes** - moins mature que REST ou GraphQL

## Quand l'utiliser {#when-to-use}

- Communication interne entre services
- Projets blockchain (JSON-RPC d'Ethereum)
- API IoT (capteur -> contrôleur)
- API ouvertes simples (messageries instantanées)
- Opérations complexes à haute performance

## Points de vigilance {#gotchas}

- **HTTP 200 pour les erreurs** - le client doit inspecter le corps de la réponse, et pas seulement le code de statut
- **Absence de cache** : charge serveur plus élevée pour les requêtes répétées
- **Passage des paramètres** - positionnels (tableau) ou nommés (objet). Les paramètres nommés sont plus lisibles ; les paramètres positionnels demandent moins de code

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - comparaison REST et JSON-RPC
- [[async-event-apis]] - transport WebSocket pour JSON-RPC
