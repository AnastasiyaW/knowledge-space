---
title: "Architekturstile – Vom Monolithen zu Microservices"
category: concepts
tags: [architecture, monolith, microservices, soa, modular-monolith]
level: 4
source_sha256: 4bc8ced7702788b4cdbb33fb14e2a40aa9f59ac6a6b1653389ce617562e1e962
translation: machine
translated_at: '2026-10-24'
---
# Architekturstile – Vom Monolithen zu Microservices {#architectural-styles-monolith-to-microservices}

Die Wahl des Architekturstils ist der erste und wichtigste Entwurfsschritt. Er bestimmt Flexibilität, Skalierbarkeit und zentrale Systemeigenschaften. Architektur ist ein Spektrum und keine binäre Entscheidung.

## Entwicklung der Stile {#style-evolution}

```php
Monolith -> Modular Monolith -> SOA -> Microservices -> Microservices + Micro-Frontends
```

1. **Monolith** – einzelne Auslieferung, eng gekoppelt. Alle Komponenten in einer Codebasis
2. **Modularer Monolith** – klare Modulgrenzen innerhalb einer einzelnen Auslieferung, wohldefinierte Schnittstellen
3. **SOA** – Services über einen Enterprise Service Bus (ESB), gemeinsam genutzte Datenbank möglich
4. **Microservices** – unabhängige Services mit eigenen Datenbanken, unabhängige Auslieferung
5. **Microservices + Micro-Frontends** – sowohl Backend als auch Frontend in autonome Teile zerlegt

## Wann welcher Stil {#when-to-choose-what}

### Mit dem Monolithen beginnen, wenn {#start-with-monolith-when}
- kleines Team (< 5–7 Entwickler)
- einfache Domäne
- Geschwindigkeit der initialen Entwicklung zählt
- Domäne noch nicht gut verstanden
- geringe Änderungsfrequenz
- Team hat noch wenig DevOps-/Infrastruktur-Reife

### Umstieg auf Microservices, wenn {#migrate-to-microservices-when}
- Team wächst und unabhängige Auslieferungen benötigt
- unterschiedliche Skalierungsanforderungen pro Domäne
- Bedarf an technologischer Vielfalt
- klare Domänengrenzen identifiziert sind
- der betriebliche Mehraufwand durch den Nutzen gerechtfertigt ist

### Entscheidungsbaum {#decision-tree}

```php
Team size < 10?
  -> Monolith (or modular monolith)
Clear domain boundaries + independent deployment needed?
  -> Microservices
Unclear boundaries + fast iteration needed?
  -> Start monolith, extract later (Strangler Fig)
```

## Migration vom Monolithen zu Microservices {#monolith-to-microservices-migration}

### Strangler-Fig-Muster {#strangler-fig-pattern}
Funktionalität des Monolithen schrittweise ersetzen:
1. Neue Features werden als Microservices umgesetzt
2. Bestehende Features werden nacheinander herausgelöst
3. Der Traffic wird über eine Fassade geroutet, die zwischen Monolith und Microservice entscheidet
4. Der Monolith schrumpft mit der Zeit, bis er vollständig ersetzt ist

### Verteilter Monolith (Anti-Pattern) {#distributed-monolith-anti-pattern}
Services, die getrennt deployt werden, aber so eng gekoppelt sind, dass sie nur gemeinsam deployt werden können. Das Schlechteste aus beiden Welten: verteilte Komplexität ohne die Vorteile der Unabhängigkeit.

## Grundprinzipien von Microservices {#microservices-core-principles}

### Lose Kopplung {#low-coupling}
Service A (erstellt Bestellungen) kennt Zahlungen nicht. Service B (verarbeitet Zahlungen) kennt die Bestellerstellung nicht. Jeder Service hat minimale Abhängigkeiten, was unabhängige Auslieferung ermöglicht.

### Hohe Kohäsion {#high-cohesion}
Code für einen funktionalen Bereich gehört zusammen. Jeder Microservice ist für genau einen funktionalen Bereich verantwortlich.

### Vorteile beider Prinzipien {#benefits-of-both}
- unabhängige Skalierung pro Service
- unabhängige Auslieferung (kein vollständiger Neuaufbau)
- jeder Service bleibt einfach
- unterschiedliche Technologie-Stacks pro Service
- beschleunigte Auslieferung von Produktionscode

## Datenbankmuster für Microservices {#microservices-database-patterns}

### Datenbank pro Service {#database-per-service}
Jeder Microservice besitzt seine eigene Datenbank. Keine gemeinsam genutzten Datenbanken. Services kommunizieren über APIs, nicht über Joins. Ermöglicht technologische Vielfalt und unabhängige Skalierung.

### Gemeinsam genutzte Datenbank (Anti-Pattern) {#shared-database-anti-pattern}
Mehrere Services, die auf dieselbe Datenbank zugreifen, erzeugen enge Kopplung. Nur in der übergangsweisen Migration vom Monolithen zu Microservices vertretbar.

### Regeln zur Datenhoheit {#data-ownership-rules}
- Kleine Datenmengen aus einem anderen Service: lokaler Cache (am schnellsten, benötigt aber Invalidierung)
- Große gemeinsam genutzte Datenmengen: verteilter Cache (Redis), auf den beide zugreifen
- Wenn die gecachten Fremddaten die eigenen Daten deutlich übersteigen: Servicegrenzen überdenken

## Service Discovery {#service-discovery}

Services müssen sich in dynamischen Umgebungen (Container, Auto-Scaling) gegenseitig finden.

- **Client-seitige Discovery** – der Client fragt die Registry ab und verbindet sich direkt
- **Server-seitige Discovery** – der Client sendet an einen Load Balancer, der die Registry abfragt

Werkzeuge: Consul, Eureka, etcd, Kubernetes DNS.

## Stolperfallen {#gotchas}

- **Nicht mit Microservices beginnen** – mit einem gut strukturierten Monolithen starten und zerlegen, wenn Schmerzpunkte auftreten
- **Conway'sches Gesetz** – das Systemdesign spiegelt die Kommunikationsstruktur der Organisation wider
- **Microservices ohne DevOps-Reife** = betrieblicher Albtraum
- **Der modulare Monolith** ist oft der optimale Punkt – klare Grenzen ohne die Komplexität verteilter Systeme
- **Architekt:innen wirken mitunter wenig produktiv**, während sie organisatorische Konflikte austragen (z. B. monatelanges Warten auf Infrastruktur)

## Siehe auch {#see-also}

- [[microservices-communication]] – Sync vs. async, API-Gateway, BFF, CQRS
- [[distributed-systems-fundamentals]] – CAP-Theorem, Konsens, Replikation
- [[enterprise-integration]] – ESB, Integrationsstile, moderne Alternativen
- [[microfrontends]] – Strategien zur Frontend-Zerlegung
