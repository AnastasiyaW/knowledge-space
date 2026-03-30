---
title: Data Serialization Formats
category: reference
tags: [json, xml, protobuf, xsd, openapi, serialization]
---
# Data Serialization Formats

Data serialization formats define how structured data is encoded for storage, transmission, and API contracts. Format choice impacts performance, interoperability, and developer experience.

## Key Facts

- JSON is the default for REST APIs and web: human-readable, widely supported, flexible schema
- XML is required in enterprise/government/financial integrations: strict schema validation via XSD, namespace support, transformation via XSLT
- Protobuf (Protocol Buffers) is the default for gRPC: binary, compact, strongly typed, backward-compatible evolution
- XSD (XML Schema Definition) enforces data types, structure, and constraints on XML documents - validation is built into the format
- JSON Schema provides similar validation for JSON, but adoption is less universal than XSD for XML
- OpenAPI/Swagger combines API documentation with JSON schema for request/response validation
- See [[api-design-process]] for choosing format based on API requirements
- See [[message-queues]] for serialization in event payloads

## Patterns

### Format comparison

| Criterion | JSON | XML | Protobuf | Avro |
|-----------|------|-----|----------|------|
| Readability | High | Medium | None (binary) | None |
| Schema | Optional (JSON Schema) | Built-in (XSD) | Required (.proto) | Required |
| Size | Large | Largest | Smallest | Small |
| Parse speed | Fast | Slow | Fastest | Fast |
| Type safety | Weak | Strong (XSD) | Strong | Strong |
| Evolution | Flexible | Versioned | Forward/backward | Full |
| Browser | Native | Native | Needs lib | Needs lib |
| Best for | REST APIs | Enterprise | gRPC/internal | Kafka events |

### XML with XSD validation

```xml
<!-- XSD Schema defining order structure -->
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="order">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="id" type="xs:integer"/>
        <xs:element name="total" type="xs:decimal"/>
        <xs:element name="currency" type="currencyType"/>
        <xs:element name="items" type="itemListType"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <!-- restriction base: decimal must have exactly 2 decimals -->
  <xs:simpleType name="priceType">
    <xs:restriction base="xs:decimal">
      <xs:fractionDigits value="2"/>
      <xs:minInclusive value="0"/>
    </xs:restriction>
  </xs:simpleType>

  <!-- enumeration restriction -->
  <xs:simpleType name="currencyType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="USD"/>
      <xs:enumeration value="EUR"/>
      <xs:enumeration value="GBP"/>
    </xs:restriction>
  </xs:simpleType>
</xs:schema>
```

### XSD restriction types

```
Restriction base types:
  xs:string      - text values
  xs:decimal     - decimal numbers
  xs:integer     - whole numbers
  xs:boolean     - true/false
  xs:date        - YYYY-MM-DD
  xs:dateTime    - ISO 8601

Facets (constraints):
  minInclusive / maxInclusive  - value range
  minLength / maxLength        - string length
  pattern                      - regex validation
  enumeration                  - allowed values
  fractionDigits               - decimal places
  totalDigits                  - total digit count
```

### Protobuf schema evolution

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
  string currency = 4;        // new field: old readers ignore
  repeated Item items = 5;    // new field: old readers ignore
  // field 6 reserved for future use
}

// Rules for backward compatibility:
//   - Never change field numbers
//   - Never reuse field numbers
//   - New fields must be optional
//   - Use 'reserved' for removed fields
```

### JSON Schema example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "total", "currency"],
  "properties": {
    "id": { "type": "integer" },
    "total": { "type": "number", "minimum": 0 },
    "currency": {
      "type": "string",
      "enum": ["USD", "EUR", "GBP"]
    },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "quantity"],
        "properties": {
          "name": { "type": "string" },
          "quantity": { "type": "integer", "minimum": 1 }
        }
      }
    }
  }
}
```

## Gotchas

- **Symptom**: Storing images/BLOBs in XML/JSON -> **Cause**: Base64 encoding increases size by ~33% -> **Fix**: Store binary data in object storage, reference by URL in the document. Do not try to index binary content
- **Symptom**: XML validation rejects valid-looking data -> **Cause**: XSD restriction is stricter than expected (e.g., integer instead of decimal for prices) -> **Fix**: Review XSD type hierarchy. `xs:decimal` allows fractions; `xs:integer` does not. Use `restriction base` to constrain the correct base type
- **Symptom**: Protobuf message cannot be read by old consumer -> **Cause**: Changed field number or type of existing field -> **Fix**: Never change field numbers or types. Add new fields only. Use `reserved` keyword for removed fields to prevent accidental reuse
- **Symptom**: JSON payloads 5x larger than Protobuf for same data -> **Cause**: JSON's text format includes field names in every message -> **Fix**: Accept if readability is more important. Otherwise use Protobuf for internal service-to-service, JSON for external/browser APIs. Consider gzip compression for JSON

## See Also

- [[api-design-process]] - Format choice is part of API design
- [[message-queues]] - Event payload serialization (Avro popular with Kafka)
- [[quality-attributes]] - Performance requirements influencing format choice
- [JSON Schema](https://json-schema.org/)
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/)
- [W3C XML Schema](https://www.w3.org/XML/Schema)
