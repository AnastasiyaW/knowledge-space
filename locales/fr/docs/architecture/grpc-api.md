---
title: "Conception d'API gRPC"
category: reference
tags: [grpc, protobuf, http2, rpc, binary-protocol, microservices]
level: 3
source_sha256: c26f060f315038b43570449fbd88f985cddbaca5890016e38d65ba5fb77f1051
translation: machine
translated_at: '2026-10-24'
---
# Conception d'API gRPC {#grpc-api-design}

gRPC est un framework RPC open source créé par Google (2016). Il utilise Protocol Buffers comme format d'échange de données sur HTTP/2. Il est idéal pour la communication haute performance entre microservices, lorsque la surcharge de JSON est inacceptable.

## Architecture {#architecture}

Le client appelle une méthode du serveur comme s'il s'agissait d'une fonction locale. Le fichier `.proto` définit l'interface du service. Des générateurs de code produisent à partir de la définition proto les stubs client et les squelettes serveur.

```sql
[Client Stub] --binary over HTTP/2--> [Server Skeleton]
     |                                       |
  generated from .proto              generated from .proto
```

## Protocol Buffers (Protobuf) {#protocol-buffers-protobuf}

Format de sérialisation binaire. Plus compact et plus rapide que JSON/XML. Ce sont les numéros de champs (et non leurs noms) qui sont transmis.

```protobuf
syntax = "proto3";

service Hello {
  rpc SayHi (HiRequest) returns (HiReply);
}

message HiRequest {
  string name = 1;
}

message HiReply {
  string message = 1;
}

message Client {
  string name = 1;
  int32 id = 2;
  bool has_car = 3;
}
```

Le fichier proto doit exister à la fois côté client et côté serveur. Types de champs : `string`, `int32`, `int64`, `bool`, `float`, `double`, `bytes`, messages imbriqués.

## Quatre modes de communication {#four-communication-patterns}

| Mode | Description |
|------|-------------|
| **Unary** | Une requête, une réponse (comme REST) |
| **Server streaming** | Une requête, un flux de réponses |
| **Client streaming** | Un flux de requêtes, une seule réponse |
| **Bidirectional streaming** | Les deux côtés émettent un flux simultanément |

## Fondations HTTP/2 {#http2-foundation}

gRPC repose sur les fonctionnalités de HTTP/2 :
- **Multiplexage** - plusieurs requêtes sur une même connexion
- **Compression des en-têtes** (HPACK) - réduit la surcharge
- **Découpage binaire** - plus efficace que HTTP/1.1 basé sur du texte
- **Server push** - envoi proactif de données
- **Priorisation des flux** - requêtes importantes traitées en premier

## Avantages {#advantages}

- **Haute performance** - protocole binaire léger, plus rapide que REST basé sur JSON
- **Interopérabilité** - prise en charge de plusieurs langages grâce à la génération de code
- **Contrats fortement typés** - les schémas protobuf fournissent des interfaces claires et typées
- **Streaming bidirectionnel** - données en temps réel dans les deux sens
- **Génération de code** - code client/serveur généré automatiquement à partir des fichiers proto

## Inconvénients {#disadvantages}

- **Support limité par les navigateurs** - nécessite un proxy gRPC-Web pour les navigateurs
- **Difficulté de débogage** - format binaire plus difficile à inspecter que JSON
- **Complexité de versionnement** - les modifications de schéma proto exigent une gestion rigoureuse
- **Écosystème plus restreint** - moins d'outillage et de communauté que REST
- **Gestion des erreurs spécifique** - utilise ses propres codes d'erreur, peu familiers à certains développeurs

## Quand l'utiliser {#when-to-use}

- Communication haute performance entre microservices (API internes)
- Streaming bidirectionnel (données en temps réel, chat, supervision)
- Environnements polyglottes (services écrits dans différents langages)
- Applications sensibles à la latence

## Quand ne pas l'utiliser {#when-not-to-use}

- API exposées publiquement (clients navigateurs)
- Opérations CRUD simples
- Petits projets avec peu de services
- Lorsque des charges utiles lisibles par un humain sont nécessaires pour le débogage

## Points de vigilance {#gotchas}

- **Seuls ~45 % des sites web** prennent en charge HTTP/2, malgré sa sortie en 2015 - vérifiez la compatibilité de votre infrastructure
- **Évolution du schéma proto** - ne réutilisez jamais un numéro de champ (champs supprimés) ; ajoutez uniquement de nouveaux champs avec de nouveaux numéros
- **gRPC-Web** ajoute une couche de proxy entre le navigateur et le serveur gRPC, ce qui augmente la latence et la complexité
- **Répartition de charge** - gRPC utilise des connexions HTTP/2 de longue durée, si bien que les load balancers L4 ne répartissent pas bien la charge. Utilisez L7 ou une répartition côté client
- **Outil :** json-to-proto.github.io pour la conversion de fichiers proto

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - comparaison avec REST, protocole HTTP
- [[graphql-api]] - style d'API alternatif basé sur les requêtes
- [[data-serialization-formats]] - comparaison JSON, XML, Protobuf
- [[microservices-communication]] - modèles de communication inter-services
