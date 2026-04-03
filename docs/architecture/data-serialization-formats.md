---
title: Data Serialization Formats - XML, JSON, Protobuf
category: reference
tags: [json, xml, xsd, json-schema, protobuf, serialization, data-formats]
---

# Data Serialization Formats - XML, JSON, Protobuf

Serialization converts in-memory objects into byte formats for network transmission. The choice of format affects performance, readability, and tooling.

## Format Comparison

| Feature | XML | JSON | Protobuf | Avro |
|---------|-----|------|----------|------|
| Syntax | Verbose, tags | Compact, key-value | Binary, field numbers | Binary, schema |
| Readability | Medium | High | None | None |
| Native types | Text only | string, number, boolean, null, array, object | Typed fields | Typed |
| Schema | XSD, DTD, RelaxNG | JSON Schema | `.proto` files | Avro schema |
| Namespaces | Full support | None | Package-based | Namespace |
| Size | Largest | Large | Smallest | Small |
| Parse speed | Slow | Fast | Fastest | Fast |
| Evolution | Versioned | Flexible | Forward/backward | Full |
| Best for | SOAP, enterprise | REST, web, NoSQL | gRPC, microservices | Kafka events |

## JSON Schema

Validates JSON structure, types, and constraints. Used in OpenAPI for request/response validation.

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

**Key keywords:** `type`, `properties`, `required`, `items`, `$ref`, `additionalProperties`

**String validations:** `minLength`, `maxLength`, `pattern` (regex), `format` ("email", "date-time", "uri", "uuid")

**Number validations:** `minimum`, `maximum`, `exclusiveMinimum`, `multipleOf`

**Composition:** `allOf` (all match), `anyOf` (at least one), `oneOf` (exactly one), `not`

**Conditional:** `if`/`then`/`else`

## XSD (XML Schema Definition)

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

**Element composition:** `xs:sequence` (ordered), `xs:all` (any order), `xs:choice` (one of)

**Restrictions/facets:** `minInclusive`, `maxInclusive`, `minLength`, `maxLength`, `pattern`, `enumeration`, `totalDigits`, `fractionDigits`

**Occurrence:** `minOccurs`, `maxOccurs`, `maxOccurs="unbounded"`

**Linking:** `xs:import` (different namespaces), `xs:include` (same namespace)

**Namespace note:** `xmlns:xs` URI is an identifier, not a URL the parser fetches.

## Protobuf Schema Evolution

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

## Message Broker Format Selection

| Format | Readability | Size | Speed | Schema Evolution |
|--------|------------|------|-------|-----------------|
| JSON | Human-readable | Large | Moderate | Flexible |
| Avro | Not readable | Compact | Fast | Full support |
| Protobuf | Not readable | Most compact | Fastest | Forward/backward |

## Practical Guidance

**When XML:** SOAP, enterprise integration (ESB), XSD validation required by contract, namespace support needed, document-centric data with mixed content.

**When JSON:** REST APIs (de facto standard), web/mobile, config files, NoSQL databases (MongoDB, CouchDB). Prefer for all new APIs unless enterprise dictates XML.

**When Protobuf:** gRPC, high-performance internal services, bandwidth-sensitive mobile apps.

**Content negotiation:** `Accept` and `Content-Type` headers. Some APIs support both (`application/json`, `application/xml`).

## Gotchas

- **JSON large numbers** - JavaScript Number precision limit at 2^53. Use strings for large IDs
- **JSON no dates** - no native date type. Use ISO 8601 strings (`"2024-01-15T10:30:00Z"`)
- **JSON no comments** - not in spec. Use JSONC or YAML for commented configuration
- **XML validation rejected** - XSD stricter than expected (`xs:integer` doesn't allow fractions, use `xs:decimal`)
- **Protobuf unreadable messages** - changed field number breaks everything. Never change numbers, only add new fields
- **Base64 bloat** - storing binary in XML/JSON inflates size ~33%. Store in object storage, reference by URL
- **JSON payloads 5x larger than Protobuf** - accept for readability, or use gzip compression for JSON APIs

## See Also

- [[api-documentation-specs]] - OpenAPI (JSON Schema), WSDL (XSD), Proto specs
- [[grpc-api]] - Protobuf in gRPC context
- [[soap-api]] - XML/XSD in SOAP context
- [[message-broker-patterns]] - Serialization for messaging
