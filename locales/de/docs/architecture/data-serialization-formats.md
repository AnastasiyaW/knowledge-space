---
title: "Datenserialisierungsformate - XML, JSON, Protobuf"
category: reference
tags: [json, xml, xsd, json-schema, protobuf, serialization, data-formats]
level: 3
source_sha256: e7042f265b6f1c77b1b401654a72a84c653ffb933a53f164e5b341787c3a6fd8
translation: machine
translated_at: '2026-10-24'
---
# Datenserialisierungsformate - XML, JSON, Protobuf {#data-serialization-formats-xml-json-protobuf}

Serialisierung wandelt In-Memory-Objekte in Byteformate für die Übertragung über das Netzwerk um. Die Wahl des Formats beeinflusst Performance, Lesbarkeit und Tooling.

## Formatvergleich {#format-comparison}

| Merkmal | XML | JSON | Protobuf | Avro |
|---------|-----|------|----------|------|
| Syntax | Ausführlich, Tags | Kompakt, Schlüssel-Wert | Binär, Feldnummern | Binär, Schema |
| Lesbarkeit | Mittel | Hoch | Keine | Keine |
| Native Typen | Nur Text | string, number, boolean, null, array, object | Typisierte Felder | Typisiert |
| Schema | XSD, DTD, RelaxNG | JSON Schema | `.proto`-Dateien | Avro-Schema |
| Namespaces | Vollständige Unterstützung | Keine | Paketbasiert | Namespace |
| Größe | Am größten | Groß | Am kleinsten | Klein |
| Parse-Geschwindigkeit | Langsam | Schnell | Am schnellsten | Schnell |
| Evolution | Versioniert | Flexibel | Vorwärts/rückwärts | Vollständig |
| Am besten geeignet für | SOAP, Enterprise | REST, Web, NoSQL | gRPC, Microservices | Kafka-Events |

## JSON Schema {#json-schema}

Validiert JSON-Struktur, Typen und Constraints. Wird in OpenAPI zur Validierung von Request und Response verwendet.

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

**Zentrale Schlüsselwörter:** `type`, `properties`, `required`, `items`, `$ref`, `additionalProperties`

**Zeichenkettenvalidierungen:** `minLength`, `maxLength`, `pattern` (Regex), `format` ("email", "date-time", "uri", "uuid")

**Zahlenvalidierungen:** `minimum`, `maximum`, `exclusiveMinimum`, `multipleOf`

**Komposition:** `allOf` (alle treffen zu), `anyOf` (mindestens eines), `oneOf` (genau eines), `not`

**Bedingungen:** `if`/`then`/`else`

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

**Elementkomposition:** `xs:sequence` (geordnet), `xs:all` (beliebige Reihenfolge), `xs:choice` (eines von)

**Einschränkungen/Facetten:** `minInclusive`, `maxInclusive`, `minLength`, `maxLength`, `pattern`, `enumeration`, `totalDigits`, `fractionDigits`

**Vorkommen:** `minOccurs`, `maxOccurs`, `maxOccurs="unbounded"`

**Verknüpfung:** `xs:import` (unterschiedliche Namespaces), `xs:include` (gleicher Namespace)

**Namespace-Hinweis:** Die URI von `xmlns:xs` ist ein Bezeichner, keine URL, die der Parser abruft.

## Protobuf Schema-Evolution {#protobuf-schema-evolution}

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

## Auswahl des Formats für Message Broker {#message-broker-format-selection}

| Format | Lesbarkeit | Größe | Geschwindigkeit | Schema-Evolution |
|--------|------------|-------|-----------------|------------------|
| JSON | Menschenlesbar | Groß | Mäßig | Flexibel |
| Avro | Nicht lesbar | Kompakt | Schnell | Vollständige Unterstützung |
| Protobuf | Nicht lesbar | Am kompaktesten | Am schnellsten | Vorwärts/rückwärts |

## Praktische Hinweise {#practical-guidance}

**Wann XML:** SOAP, Enterprise-Integration (ESB), XSD-Validierung vertraglich vorgeschrieben, Namespace-Unterstützung erforderlich, dokumentenzentrierte Daten mit gemischtem Inhalt.

**Wann JSON:** REST-APIs (de facto Standard), Web/Mobile, Konfigurationsdateien, NoSQL-Datenbanken (MongoDB, CouchDB). Für alle neuen APIs zu bevorzugen, sofern nicht unternehmensintern XML vorgegeben ist.

**Wann Protobuf:** gRPC, leistungskritische interne Services, bandbreitensensitive Mobile-Apps.

**Content Negotiation:** `Accept`- und `Content-Type`-Header. Manche APIs unterstützen beide (`application/json`, `application/xml`).

## Fallstricke {#gotchas}

- **Große JSON-Zahlen** - Die Genauigkeitsgrenze von JavaScript-Number liegt bei 2^53. Für große IDs Strings verwenden
- **JSON ohne Datumstyp** - Kein nativer Datentyp für Datum. ISO-8601-Strings verwenden (`"2024-01-15T10:30:00Z"`)
- **JSON ohne Kommentare** - Nicht Teil der Spezifikation. Für kommentierte Konfigurationen JSONC oder YAML verwenden
- **XML-Validierung abgelehnt** - XSD ist strenger als erwartet (`xs:integer` erlaubt keine Nachkommastellen, `xs:decimal` verwenden)
- **Protobuf-Nachrichten nicht lesbar** - Eine geänderte Feldnummer bricht alles. Nummern nie ändern, nur neue Felder hinzufügen
- **Base64-Aufblähung** - Binärdaten in XML/JSON zu speichern vergrößert die Größe um ca. 33 %. In Object Storage ablegen und per URL referenzieren
- **JSON-Payloads 5x größer als Protobuf** - Für die Lesbarkeit akzeptieren oder bei JSON-APIs gzip-Komprimierung verwenden

## Siehe auch {#see-also}

- [[api-documentation-specs]] - OpenAPI (JSON Schema), WSDL (XSD), Proto-Spezifikationen
- [[grpc-api]] - Protobuf im gRPC-Kontext
- [[soap-api]] - XML/XSD im SOAP-Kontext
- [[message-broker-patterns]] - Serialisierung für Messaging
