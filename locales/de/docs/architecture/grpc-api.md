---
title: "gRPC-API-Design"
category: reference
tags: [grpc, protobuf, http2, rpc, binary-protocol, microservices]
level: 3
source_sha256: c26f060f315038b43570449fbd88f985cddbaca5890016e38d65ba5fb77f1051
translation: machine
translated_at: '2026-10-24'
---
# gRPC-API-Design {#grpc-api-design}

gRPC ist ein Open-Source-RPC-Framework, das von Google entwickelt wurde (2016). Es verwendet Protocol Buffers als Datenaustauschformat über HTTP/2. Ideal für hochperformante Kommunikation zwischen Microservices, bei denen der JSON-Overhead nicht akzeptabel ist.

## Architektur {#architecture}

Der Client ruft eine Methode auf dem Server auf, als handle es sich um eine lokale Funktion. Die `.proto`-Datei definiert die Service-Schnittstelle. Code-Generatoren erzeugen aus der Proto-Definition Client-Stubs und Server-Skeletons.

```sql
[Client Stub] --binary over HTTP/2--> [Server Skeleton]
     |                                       |
  generated from .proto              generated from .proto
```

## Protocol Buffers (Protobuf) {#protocol-buffers-protobuf}

Binäres Serialisierungsformat. Kompakter und schneller als JSON/XML. Es werden Feldnummern (nicht Feldnamen) übertragen.

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

Die Proto-Datei muss sowohl auf dem Client als auch auf dem Server vorhanden sein. Feldtypen: `string`, `int32`, `int64`, `bool`, `float`, `double`, `bytes`, verschachtelte Nachrichten.

## Vier Kommunikationsmuster {#four-communication-patterns}

| Muster | Beschreibung |
|--------|--------------|
| **Unary** | Einzelne Anfrage, einzelne Antwort (wie bei REST) |
| **Server-Streaming** | Einzelne Anfrage, Stream von Antworten |
| **Client-Streaming** | Stream von Anfragen, einzelne Antwort |
| **Bidirektionales Streaming** | Beide Seiten streamen gleichzeitig |

## Grundlage HTTP/2 {#http2-foundation}

gRPC benötigt Funktionen von HTTP/2:
- **Multiplexing** - mehrere Anfragen über eine einzelne Verbindung
- **Header-Komprimierung** (HPACK) - reduziert den Overhead
- **Binäres Framing** - effizienter als textbasiertes HTTP/1.1
- **Server Push** - proaktives Senden von Daten
- **Stream-Priorisierung** - wichtige Anfragen zuerst

## Vorteile {#advantages}

- **Hohe Performance** - leichtgewichtiges binäres Protokoll, schneller als JSON-basiertes REST
- **Interoperabilität** - Unterstützung mehrerer Sprachen durch Code-Generierung
- **Stark typisierte Verträge** - Protobuf-Schemas bieten klare, typsichere Schnittstellen
- **Bidirektionales Streaming** - Echtzeitdaten in beide Richtungen
- **Code-Generierung** - automatisch erzeugter Client-/Server-Code aus Proto-Dateien

## Nachteile {#disadvantages}

- **Eingeschränkte Browser-Unterstützung** - für Browser wird ein gRPC-Web-Proxy benötigt
- **Schwieriges Debugging** - das Binärformat ist schwerer zu inspizieren als JSON
- **Versionierungskomplexität** - Änderungen am Proto-Schema erfordern sorgfältiges Management
- **Kleineres Ökosystem** - weniger Tooling und Community als bei REST
- **Eigene Fehlerbehandlung** - verwendet eigene Fehlercodes, die manchen Entwicklern nicht vertraut sind

## Wann verwenden {#when-to-use}

- Hochperformante Kommunikation zwischen Microservices (interne APIs)
- Bidirektionales Streaming (Echtzeitdaten, Chat, Monitoring)
- Polyglotte Umgebungen (Services in verschiedenen Sprachen)
- Latenzkritische Anwendungen

## Wann nicht verwenden {#when-not-to-use}

- Öffentlich zugängliche APIs (Browser-Clients)
- Einfache CRUD-Operationen
- Kleine Projekte mit wenigen Services
- Wenn für das Debugging menschenlesbare Nutzdaten benötigt werden

## Stolperfallen {#gotchas}

- **Nur ca. 45 % der Websites** unterstützen HTTP/2, obwohl es 2015 veröffentlicht wurde - Kompatibilität der Infrastruktur prüfen
- **Weiterentwicklung des Proto-Schemas** - Feldnummern niemals wiederverwenden (gelöschte Felder), nur neue Felder mit neuen Nummern hinzufügen
- **gRPC-Web** fügt zwischen Browser und gRPC-Server eine Proxy-Schicht hinzu, was Latenz und Komplexität erhöht
- **Load Balancing** - gRPC verwendet langlebige HTTP/2-Verbindungen, daher verteilen L4-Load-Balancer schlecht. L7- oder clientseitiges Balancing verwenden
- **Werkzeug:** json-to-proto.github.io zur Konvertierung von Proto-Dateien

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] - REST-Vergleich, HTTP-Protokoll
- [[graphql-api]] - Alternativer abfragebasierter API-Stil
- [[data-serialization-formats]] - Vergleich JSON, XML, Protobuf
- [[microservices-communication]] - Muster der Kommunikation zwischen Services
