---
title: "Documentation et spécifications d'API"
category: reference
tags: [openapi, swagger, wsdl, asyncapi, openrpc, api-first, documentation]
level: 3
source_sha256: c1de1c06459e6f5f3e50de556bff9742b477fd935c633a292f3f2a8f43cf6d51
translation: machine
translated_at: '2026-10-24'
---
# Documentation et spécifications d'API {#api-documentation-and-specifications}

L'API n'est qu'un composant d'un service web. Une documentation complète couvre l'architecture, les modèles de données, les processus métier, l'autorisation et les diagrammes de relations entre composants.

## API First vs Code First {#api-first-vs-code-first}

| Approche | Processus | Idéal pour |
|----------|-----------|------------|
| **API First** | Concevoir la spécification avant l'implémentation | Grands projets, API publiques, équipes multiples |
| **Code First** | Écrire le code, générer la documentation | Prototypes rapides, petites équipes, API internes |

**Avantages de l'API First :** meilleure collaboration grâce à un document central, génération de stubs/SDK/documentation à partir de la spécification, cohérence. **Inconvénient :** conception initiale chronophage.

## OpenAPI / Swagger (REST) {#openapi-swagger-rest}

```yaml
openapi: "3.0.0"
info:
  title: "Task API"
  version: "1.0.0"
paths:
  /tasks/{id}:
    get:
      summary: "Get task by ID"
      operationId: "getTask"
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Task"
components:
  schemas:
    Task:
      type: object
      required: [id, title]
      properties:
        id:
          type: integer
        title:
          type: string
```

**Outils :** editor.swagger.io (éditeur), Swagger UI (documentation interactive).

### Algorithme de conception d'API REST {#rest-api-design-algorithm}
1. Déterminer les données nécessaires à chaque action/méthode
2. Définir les ensembles de paramètres par entité
3. Élaguer : supprimer les paramètres et entités inutiles, fusionner les endpoints
4. Concevoir à la fois la requête et la réponse - moins de paramètres = meilleure ergonomie

## WSDL (SOAP) {#wsdl-soap}

Spécification basée sur XML. Structure : `types` (schémas XSD), `message` (structures de requête/réponse), `portType` (opérations), `binding` (protocole), `service` (adresse de l'endpoint).

Espaces de noms principaux : `xmlns:soap`, `xmlns:tns`, `xmlns:xsd`.

## OpenRPC (JSON-RPC) {#openrpc-json-rpc}

Standard de documentation des API JSON-RPC (spec.open-rpc.org) :
- `openrpc` : version de la spécification
- `info` : version, titre
- `servers` : nom, URL avec variables
- `methods[]` : nom, params, result, errors, examples

**Passage des paramètres :** positionnel (tableau - le serveur doit connaître l'ordre) vs nommé (objet - ordre quelconque, plus lisible).

## AsyncAPI (événementiel) {#asyncapi-event-driven}

Pour Kafka, RabbitMQ, WebSocket, MQTT :
- Définit les canaux (topics/queues)
- Schémas de messages
- Liaisons serveur par protocole

## Protocol Buffers / Proto (gRPC) {#protocol-buffers-proto-grpc}

IDL pour les services gRPC :
```protobuf
service Hello {
  rpc SayHi (HiRequest) returns (HiReply);
}
message HiRequest {
  string name = 1;
}
```

## Modèle de documentation d'un service web {#web-service-documentation-template}

Une documentation complète doit inclure : le nom du service, les contacts du mainteneur, la description, le lien vers le dépôt, le lien vers la documentation de l'API, les URL d'hôtes (test/prod), les URL de supervision, les instructions de déploiement, le journal des modifications, les diagrammes d'architecture, le modèle d'entités/données, les diagrammes de processus métier, le contrôle d'accès.

### Format de spécification d'un endpoint {#endpoint-specification-format}
- Chemin, méthode HTTP, méthode d'authentification, limites de débit
- Tableau des paramètres : nom, emplacement (body/header/path/query), obligatoire, format, exemple
- Exemple de requête (JSON)
- Codes de statut de réponse avec descriptions
- Exemples de réponses de succès et d'erreur

## Types MIME {#mime-types}

Format : `type/subtype` - `text/html`, `application/json`, `image/png`. Le client envoie un en-tête `Accept` ; le serveur répond avec `Content-Type`. Indispensable pour une interprétation correcte des données.

## Pièges à éviter {#gotchas}

- **OpenAPI 3.0 vs 2.0 (Swagger)** - structures différentes, vérifier la bonne version
- **`$ref` pour la réutilisation** - définir les schémas une seule fois dans `components/schemas`, puis les référencer partout
- **WSDL est auto-documenté** - fournir le fichier aux développeurs suffit à leur faire comprendre l'API
- **AsyncAPI est jeune** - moins d'outillage qu'OpenAPI, mais en croissance rapide
- **Dérive de la documentation** - l'API First l'empêche ; le Code First exige de la rigueur pour maintenir la documentation à jour

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - protocole REST et conventions
- [[soap-api]] - protocole SOAP et détails de WSDL
- [[graphql-api]] - le schéma comme documentation
- [[data-serialization-formats]] - JSON Schema, XSD, Protobuf
- [[api-testing-tools]] - Postman, cURL, DevTools
