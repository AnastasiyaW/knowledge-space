---
title: "Formats de sérialisation de données - XML, JSON, Protobuf"
category: reference
tags: [json, xml, xsd, json-schema, protobuf, serialization, data-formats]
level: 3
source_sha256: e7042f265b6f1c77b1b401654a72a84c653ffb933a53f164e5b341787c3a6fd8
translation: machine
translated_at: '2026-10-24'
---
# Formats de sérialisation de données - XML, JSON, Protobuf {#data-serialization-formats-xml-json-protobuf}

La sérialisation convertit les objets en mémoire en formats binaires ou textuels destinés à la transmission réseau. Le choix du format influe sur les performances, la lisibilité et l'outillage.

## Comparaison des formats {#format-comparison}

| Fonctionnalité | XML | JSON | Protobuf | Avro |
|---------|-----|------|----------|------|
| Syntaxe | Verbeuse, balises | Compacte, clé-valeur | Binaire, numéros de champs | Binaire, schéma |
| Lisibilité | Moyenne | Élevée | Aucune | Aucune |
| Types natifs | Texte uniquement | string, number, boolean, null, array, object | Champs typés | Typés |
| Schéma | XSD, DTD, RelaxNG | JSON Schema | Fichiers `.proto` | Schéma Avro |
| Espaces de noms | Prise en charge complète | Aucun | Basés sur le package | Namespace |
| Taille | La plus importante | Importante | La plus petite | Petite |
| Vitesse d'analyse | Lente | Rapide | La plus rapide | Rapide |
| Évolution | Versionnée | Souple | Ascendante/descendante | Complète |
| Idéal pour | SOAP, entreprise | REST, web, NoSQL | gRPC, microservices | Événements Kafka |

## JSON Schema {#json-schema}

Valide la structure JSON, les types et les contraintes. Utilisé dans OpenAPI pour la validation des requêtes et des réponses.

```json
{
  "type": "object",
  "required": ["id", "title", "author"],
  "properties": {
    "id": {"type": "integer"},
    "title": {"type": "string", "minLength": 1, "maxLength": 200},
    "author": {"$ref": "#/definitions/Author"},
    "tags": {"type": "array", "items": {"type": "string"}},
    "published": {"type": "boolean"}
  },
  "if": {"properties": {"published": {"const": true}}},
  "then": {"required": ["publishedDate"]},
  "definitions": {
    "Author": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
      }
    }
  }
}
```

**Mots-clés principaux :** `type`, `properties`, `required`, `items`, `$ref`, `additionalProperties`

**Validations de chaînes :** `minLength`, `maxLength`, `pattern` (regex), `format` (« email », « date-time », « uri », « uuid »)

**Validations numériques :** `minimum`, `maximum`, `exclusiveMinimum`, `multipleOf`

**Composition :** `allOf` (toutes correspondent), `anyOf` (au moins une), `oneOf` (exactement une), `not`

**Conditionnel :** `if`/`then`/`else`

## XSD (XML Schema Definition) {#xsd-xml-schema-definition}

```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="book">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="title" type="xs:string"/>
        <xs:element name="pages" type="xs:integer" minOccurs="0"/>
      </xs:sequence>
      <xs:attribute name="id" type="xs:string" use="required"/>
    </xs:complexType>
  </xs:element>

  <xs:simpleType name="currencyType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="USD"/>
      <xs:enumeration value="EUR"/>
    </xs:restriction>
  </xs:simpleType>
</xs:schema>
```

**Composition des éléments :** `xs:sequence` (ordonnée), `xs:all` (ordre quelconque), `xs:choice` (l'un des éléments)

**Restrictions et facettes :** `minInclusive`, `maxInclusive`, `minLength`, `maxLength`, `pattern`, `enumeration`, `totalDigits`, `fractionDigits`

**Occurrences :** `minOccurs`, `maxOccurs`, `maxOccurs="unbounded"`

**Liaison :** `xs:import` (espaces de noms différents), `xs:include` (même espace de noms)

**Remarque sur les espaces de noms :** l'URI `xmlns:xs` est un identifiant, et non une URL que le parseur récupère.

## Évolution du schéma Protobuf {#protobuf-schema-evolution}

```protobuf
// Version 1
message Order {
  int64 id = 1;
  string customer_name = 2;
  double total = 3;
}

// Version 2 (backward compatible)
message Order {
  int64 id = 1;
  string customer_name = 2;
  double total = 3;
  string currency = 4;        // new: old readers ignore
  repeated Item items = 5;    // new: old readers ignore
  // field 6 reserved for future
}

// Rules: never change field numbers, never reuse deleted numbers,
// new fields must be optional, use 'reserved' for removed fields
```

## Choix du format pour les brokers de messages {#message-broker-format-selection}

| Format | Lisibilité | Taille | Vitesse | Évolution du schéma |
|--------|------------|------|-------|-----------------|
| JSON | Lisible par un humain | Importante | Modérée | Souple |
| Avro | Non lisible | Compacte | Rapide | Prise en charge complète |
| Protobuf | Non lisible | La plus compacte | La plus rapide | Ascendante/descendante |

## Recommandations pratiques {#practical-guidance}

**Quand XML :** SOAP, intégration d'entreprise (ESB), validation XSD imposée par contrat, besoin de prise en charge des espaces de noms, données orientées document avec contenu mixte.

**Quand JSON :** APIs REST (standard de fait), web/mobile, fichiers de configuration, bases NoSQL (MongoDB, CouchDB). À privilégier pour toutes les nouvelles APIs, sauf si l'entreprise impose XML.

**Quand Protobuf :** gRPC, services internes à haute performance, applications mobiles sensibles à la bande passante.

**Négociation de contenu :** en-têtes `Accept` et `Content-Type`. Certaines APIs prennent en charge les deux (`application/json`, `application/xml`).

## Pièges courants {#gotchas}

- **Grands nombres en JSON** - limite de précision de Number en JavaScript à 2^53. Utiliser des chaînes pour les identifiants volumineux
- **JSON sans dates** - pas de type date natif. Utiliser des chaînes ISO 8601 (`"2024-01-15T10:30:00Z"`)
- **JSON sans commentaires** - non prévu par la spécification. Utiliser JSONC ou YAML pour les configurations commentées
- **Validation XML rejetée** - XSD plus strict que prévu (`xs:integer` n'accepte pas les fractions, utiliser `xs:decimal`)
- **Messages Protobuf illisibles** - modifier un numéro de champ casse tout. Ne jamais changer les numéros, seulement ajouter de nouveaux champs
- **Surcoût du Base64** - stocker du binaire dans XML/JSON augmente la taille d'environ 33 %. Stocker dans un stockage objet et référencer par URL
- **Charges utiles JSON 5 fois plus volumineuses qu'en Protobuf** - à accepter pour la lisibilité, ou utiliser la compression gzip pour les APIs JSON

## Voir aussi {#see-also}

- [[api-documentation-specs]] - OpenAPI (JSON Schema), WSDL (XSD), spécifications Proto
- [[grpc-api]] - Protobuf dans le contexte gRPC
- [[soap-api]] - XML/XSD dans le contexte SOAP
- [[message-broker-patterns]] - Sérialisation pour la messagerie
