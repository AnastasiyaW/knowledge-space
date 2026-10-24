---
title: "API-Dokumentation und Spezifikationen"
category: reference
tags: [openapi, swagger, wsdl, asyncapi, openrpc, api-first, documentation]
level: 3
source_sha256: c1de1c06459e6f5f3e50de556bff9742b477fd935c633a292f3f2a8f43cf6d51
translation: machine
translated_at: '2026-10-24'
---
__CODE_0__ hmm, I need to reproduce exactly. Let me write the translation carefully.

---
title: API-Dokumentation und Spezifikationen
category: reference
tags: [openapi, swagger, wsdl, asyncapi, openrpc, api-first, documentation]
---

# API-Dokumentation und Spezifikationen {#api-documentation-and-specifications}

Die API ist nur eine Komponente eines Webservice. Vollständige Dokumentation umfasst Architektur, Datenmodelle, Geschäftsprozesse, Autorisierung und Diagramme zu den Beziehungen zwischen Komponenten.

## API First vs. Code First {#api-first-vs-code-first}

| Ansatz | Vorgehen | Geeignet für |
|--------|----------|--------------|
| **API First** | Spezifikation vor der Implementierung entwerfen | Große Projekte, öffentliche APIs, mehrere Teams |
| **Code First** | Code schreiben, Dokumentation generieren | Schnelle Prototypen, kleine Teams, interne APIs |

**Vorteile von API First:** bessere Zusammenarbeit über ein zentrales Dokument, Generierung von Stubs/SDKs/Dokumentation aus der Spezifikation, Konsistenz. **Nachteil:** zeitaufwendiger Entwurf im Vorfeld.

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

**Werkzeuge:** editor.swagger.io (Editor), Swagger UI (interaktive Dokumentation).

### REST-API-Entwurfsalgorithmus {#rest-api-design-algorithm}
1. Benötigte Daten für jede Aktion/Methode ermitteln
2. Parametersätze pro Entität definieren
3. Reduzieren: unnötige Parameter und Entitäten entfernen, Endpunkte zusammenführen
4. Anfrage und Antwort entwerfen – weniger Parameter bedeuten bessere Benutzbarkeit

## WSDL (SOAP) {#wsdl-soap}

XML-basierte Spezifikation. Struktur: `types` (XSD-Schemas), `message` (Anfrage- und Antwortstrukturen), `portType` (Operationen), `binding` (Protokoll), `service` (Endpunktadresse).

Wichtige Namespaces: `xmlns:soap`, `xmlns:tns`, `xmlns:xsd`.

## OpenRPC (JSON-RPC) {#openrpc-json-rpc}

Standard zur Dokumentation von JSON-RPC-APIs (spec.open-rpc.org):
- `openrpc`: Spezifikationsversion
- `info`: Version, Titel
- `servers`: Name, URL mit Variablen
- `methods[]`: Name, Parameter, Ergebnis, Fehler, Beispiele

**Parameterübergabe:** positionell (Array – der Server muss die Reihenfolge kennen) vs. benannt (Objekt – beliebige Reihenfolge, besser lesbar).

## AsyncAPI (ereignisgesteuert) {#asyncapi-event-driven}

Für Kafka, RabbitMQ, WebSocket, MQTT:
- Definiert Channels (Topics/Queues)
- Nachrichtenschemas
- Server-Bindings pro Protokoll

## Protocol Buffers / Proto (gRPC) {#protocol-buffers-proto-grpc}

IDL für gRPC-Services:
```protobuf
service Hello {
  rpc SayHi (HiRequest) returns (HiReply);
}
message HiRequest {
  string name = 1;
}
```

## Vorlage für die Webservice-Dokumentation {#web-service-documentation-template}

Vollständige Dokumentation sollte enthalten: Servicename, Ansprechpartner (Maintainer), Beschreibung, Link zum Repository, Link zur API-Dokumentation, Host-URLs (Test/Produktion), Monitoring-URLs, Deployment-Anleitung, Changelog, Architekturdiagramme, Entitäts-/Datenmodell, Geschäftsprozessdiagramme, Zugriffskontrolle.

### Format der Endpunktspezifikation {#endpoint-specification-format}
- Pfad, HTTP-Methode, Authentifizierungsverfahren, Ratenbegrenzungen
- Parametertabelle: Name, Ort (body/header/path/query), erforderlich, Format, Beispiel
- Anfragebeispiel (JSON)
- Antwort-Statuscodes mit Beschreibungen
- Beispiele für Erfolgs- und Fehlerantworten

## MIME-Typen {#mime-types}

Format: `type/subtype` – `text/html`, `application/json`, `image/png`. Der Client sendet einen `Accept`-Header; der Server antwortet mit `Content-Type`. Unverzichtbar für die korrekte Interpretation der Daten.

## Stolperfallen {#gotchas}

- **OpenAPI 3.0 vs. 2.0 (Swagger)** – unterschiedlicher Aufbau, auf die richtige Version achten
- **`$ref` zur Wiederverwendung** – Schemas einmal in `components/schemas` definieren und überall referenzieren
- **WSDL ist selbstdokumentierend** – wer die Datei hat, versteht die API
- **AsyncAPI ist jung** – weniger Tooling als bei OpenAPI, wächst aber schnell
- **Dokumentationsdrift** – API First verhindert dies; Code First erfordert Disziplin, um die Dokumentation aktuell zu halten

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] – REST-Protokoll und Konventionen
- [[soap-api]] – SOAP-Protokoll und WSDL-Details
- [[graphql-api]] – Schema als Dokumentation
- [[data-serialization-formats]] – JSON Schema, XSD, Protobuf
- [[api-testing-tools]] – Postman, cURL, DevTools
