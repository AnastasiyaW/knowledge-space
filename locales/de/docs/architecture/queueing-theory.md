---
title: "Warteschlangentheorie für Ingenieure"
category: concepts
tags: [queueing-theory, performance, capacity-planning, latency, utilization]
level: 3
source_sha256: 455dbd3f94d5e00fe39256aa340b36a9aa5b5958daf557dc49ed54c69fe6ed0f
translation: machine
translated_at: '2026-10-24'
---
# Warteschlangentheorie für Ingenieure {#queueing-theory-for-engineers}

Die Warteschlangentheorie untersucht, wie sich Warteschlangen verhalten. Die Ergebnisse werden stark vom Warten beeinflusst, und Warten ist Verschwendung. Diese Verschwendung zu minimieren ist einer der größten Performance-Hebel für Systeme und Teams.

## Kontraintuitive Kernwahrheit {#core-counterintuitive-truth}

**Warteschlangen entstehen auch dann, wenn mehr als ausreichend Kapazität vorhanden ist.** Ein Kassierer, der Kunden im Schnitt in 45 s abfertigt, bei einer Ankunft von einem Kunden pro Minute (75 % Auslastung) – die Intuition sagt: keine Wartezeit. Die Realität: Es bilden sich deutliche Warteschlangen.

**Drei Ursachen für Warteschlangen:**
1. **Unregelmäßige Ankünfte** – Kunden überlappen sich
2. **Unregelmäßige Jobgrößen** – einige Jobs blockieren die Schlange
3. **Verschwendung** – ungenutzte Zeit lässt sich nie zurückgewinnen

**Verschlechtert sich bei:** hoher Auslastung, hoher Variabilität, wenigen Servern.

## Die Hockey-Stick-Kurve {#the-hockey-stick-curve}

Die wichtigste Visualisierung: Antwortzeit gegenüber Auslastung. Bei niedriger Auslastung steigt sie nur allmählich an, nähert sich bei 100 % jedoch dem Unendlichen.

```text
Response |                          /
Time     |                        /
         |                      /
         |                   /
         |               ../
         |          ...
         |     ....
         |....
         +-------------------------
         0%    50%    80%  95% 100%
                Utilization
```

**Die menschliche Intuition ist linear; Warteschlangensysteme sind nichtlinear.** Übergänge können plötzlich und überraschend erfolgen.

## Wichtige Formeln {#key-formulas}

### Kendall-Notation: A/S/c {#kendall-notation-asc}
- **A** = Ankunftsverteilung (M=zufällig, D=deterministisch, G=allgemein)
- **S** = Verteilung der Servicezeit
- **c** = Anzahl der Server

Gängige Modelle: M/M/1, M/M/c, M/D/1, M/G/1

### M/M/1 (einfachstes, gebräuchlichstes Modell) {#mm1-simplest-most-common}

```yaml
Utilization:    rho = arrival_rate / service_rate     (must be < 1)
Residence time: R = S / (1 - rho)                    (S = avg service time)
Queue length:   N = rho / (1 - rho)
```

| Auslastung | Wartezeit-Multiplikator | Warteschlangenlänge |
|------------|-------------------------|---------------------|
| 50 % | 2-fache Servicezeit | 1 Element |
| 75 % | 4-fache Servicezeit | 3 Elemente |
| 90 % | 10-fache Servicezeit | 9 Elemente |
| 99 % | 100-fache Servicezeit | 99 Elemente |

### Mehrere Server (M/M/c) {#multi-server-mmc}
Das Hinzufügen von Servern reduziert die Wartezeiten dramatisch, selbst bei gleicher Gesamtauslastung. Die Erlang-C-Formel liefert die Wahrscheinlichkeit, warten zu müssen.

## Eine Warteschlange > mehrere Warteschlangen {#single-queue-multiple-queues}

**Eine gemeinsame Warteschlange, die mehrere Server bedient, ist IMMER besser als getrennte Warteschlangen pro Server.**

Vier getrennte Schlangen bei vier Kassierern gegenüber einer gemeinsamen Schlange für vier Kassierer – die gemeinsame Variante führt zu deutlich kürzeren und besser vorhersagbaren Wartezeiten.

**Warum:** Sie beseitigt das Problem „hinter einem langsamen Kunden feststecken“. Bei einer gemeinsamen Warteschlange übernimmt der nächste freie Server sofort den nächsten Kunden.

**Anwendungen:** Bankabsperrungen, Flughafensicherheit, Routing in Call-Centern, Connection Pooling, Load Balancing.

## Praktische Anwendungen {#practical-applications}

| Szenario | Erkenntnis aus der Warteschlangentheorie |
|----------|------------------------------------------|
| **Kapazitätsplanung** | Ein Traffic-Anstieg um 30 % führt zu einem weitaus stärkeren Anstieg der Antwortzeit (nichtlinear) |
| **Skalierung** | Mehrere langsamere Festplatten > eine schnelle Festplatte (fügt Server zur Warteschlange hinzu) |
| **Teamdesign** | Spezialisierung erzeugt Übergaben = neue Warteschlangen. Generalisten reduzieren Warteschlangen |
| **Connection Pooling** | Pool-Größe = Anzahl der Server im Warteschlangenmodell |
| **Load Balancing** | Eine Warteschlange + mehrere Backends > Warteschlangen pro Backend |
| **Kanban/WIP-Limits** | Die Begrenzung von WIP verkürzt die Warteschlangen |

## Zentrale Erkenntnisse {#key-takeaways}

1. **Auslastung über 70–80 %** verursacht unverhältnismäßig starke Anstiege der Antwortzeit
2. **Variabilität reduzieren** bei Ankünften und Jobgrößen, wann immer möglich
3. **Warteschlangen zusammenlegen**, wann immer möglich (eine Schlange, mehrere Server)
4. **Zusätzliche Kapazität** bringt bei niedriger Auslastung abnehmende Erträge, bei hoher Auslastung dagegen enorme Gewinne
5. **Auslastung UND Antwortzeit gemeinsam überwachen** – die Auslastung allein ist irreführend
6. **Warteschlangen tauchen überall auf** – CPUs, Festplatten, Netzwerke, Teams, Prozesse

## Stolperfallen {#gotchas}

- **Die durchschnittliche Auslastung ist irreführend** – eine mittlere Auslastung von 70 % kann Spitzen von 95 % und mehr enthalten, die zu schwerer Verschlechterung führen
- **Little-Gesetz** (L = λ * W) – durchschnittliche Anzahl der Elemente im System = Ankunftsrate * durchschnittliche Verweildauer im System. Nützlicher Plausibilitätscheck
- **Verzögerung der Auto-Skalierung** – bis die Skalierung greift, ist die Hockey-Stick-Kurve unter Umständen bereits wirksam
- **Datenbank-Connection-Pools** zu klein = Warteschlangen auf Pool-Ebene; zu groß = Warteschlangen auf Datenbankebene

## Siehe auch {#see-also}

- [[distributed-systems-fundamentals]] – Latenzzahlen, Systemperformance
- [[caching-and-performance]] – Last reduzieren, um Warteschlangen zu vermeiden
- [[quality-attributes-reliability]] – SLA, Verfügbarkeitsrechnung
