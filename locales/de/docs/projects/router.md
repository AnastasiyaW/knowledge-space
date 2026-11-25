---
title: "Cursor Router"
category: projects
date: 2026-07-25
tags: [cursor, project, router]
aliases: ["Cursor Router"]
level: 2
source_sha256: 89adf4b8478602b37f2839c8c43f69453a86335b0b1210c8b868a5e6b1496358
translation: machine
translated_at: '2026-10-24'
---
# Cursor Router {#cursor-router}

**Entwicklungslinie:** `project:router` · Thread `router`  
**Letztes Ereignis:** 2026-07-25 · 1 datiert seit 2026-07-25 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Cursor Router leitet jede Agent-Anfrage über den sich verändernden Modellpool von Cursor, anstatt dass ein Entwickler für jede Anfrage ein Modell auswählen muss. Für Teams und Enterprise stehen die Modi Cost, Balance und Intelligence zur Verfügung. Balance und Intelligence verbrauchen Nutzungslimits schneller als Cost, daher sollte ein expliziter Modus gewählt werden, statt Auto als festes Modell zu behandeln. Der Router eignet sich für die Kosten- und Qualitätssteuerung auf Teamebene, nicht aber für Workloads, die ein fest vorgegebenes zugrunde liegendes Modell erfordern.

## Entwicklungslinie {#development-line}

- **2026-07-25 — Cursor veröffentlichte ein öffentliches Update zu Router.** Am 2026-07-25 veröffentlichte Cursor einen öffentlichen Blogbeitrag im Zusammenhang mit Router. Der Beitrag markiert einen öffentlichen Meilenstein der Entwicklungslinie Cursor Router, Cursor hat jedoch weder seine Funktionsweise, den Rollout-Status noch die Auswirkungen auf Nutzer näher beschrieben.

## Was sich geändert hat {#what-changed}

- 2026-07-25 — Cursor Router ersetzte das feste Routing von Auto durch eine Klassifizierung pro Anfrage und führte für Teams und Enterprise die Steuerungsoptionen Cost, Balance und Intelligence ein.
- 2026-08-06 — Cursor dokumentierte den gelernten zweistufigen Routing-Ansatz und berichtete von Verbesserungen nach dem Launch, die auf mehr Produktionsverkehr zurückgehen.
- 2026-08-12 — Cursor veröffentlichte Empfehlungen für den Rollout: zuerst für ein stark ausgelastetes Team aktivieren, die Kosten pro Commit überwachen und den Einsatz erst dann ausweiten, wenn das gemessene Ergebnis Bestand hat.

## So verwenden Sie es {#how-to-use-this}

Ab dem 2026-07-25 sollte die Router-Ankündigung von Cursor konsultiert werden, bevor man sich auf Router verlässt oder ihn konfiguriert.

1. Wählen Sie im Modell-Picker von Cursor Auto aus und anschließend Cost für Kostenkontrolle, Balance für den Standardkompromiss oder Intelligence für anspruchsvolle mehrstufige Aufgaben.
  — <https://prod.cursor.com/docs/cursor-router>
2. Aktivieren Sie für ein Enterprise-Team Router im Team-Dashboard und konfigurieren Sie erlaubte Modi, Modellzugriff, Sichtbarkeit des gerouteten Modells sowie optional die weiche oder harte Durchsetzung von Auto.
  — <https://prod.cursor.com/docs/cursor-router>
3. Verwenden Sie im TypeScript- oder Python-Agent-SDK die Modell-ID `auto-smart` und setzen Sie `optimize_for` auf `cost`, `balanced` oder `intelligence`; rufen Sie `Cursor.models.list()` auf, bevor Sie sich für ein Team darauf verlassen.
  — <https://prod.cursor.com/docs/cursor-router>

## Best Practices {#best-practices}

- Testen Sie Router zunächst mit einem aktiven Team und messen Sie eine Woche lang die Kosten pro Commit, bevor Sie den Rollout ausweiten.
  — <https://cursor.com/guides/model-routing>
- Halten Sie eine preiseffiziente Routing-Option aktiviert. Laut der Enterprise-Dokumentation von Cursor kann das Blockieren zu vieler Modelle die Qualität mindern oder Router deaktivieren; außerdem wird Cursor Grok 4.5 als Voraussetzung dafür genannt, dass Router funktioniert.
  — <https://prod.cursor.com/docs/cursor-router>
- Leiten Sie nicht allein aus der Ausgabe ab, welches Modell geantwortet hat: Das geroutete Modell ist standardmäßig verborgen, und der Pool kann sich ändern, sobald neue Modelle veröffentlicht werden.
  — <https://prod.cursor.com/docs/cursor-router>

## Hiermit überholt {#superseded-by-this}

- 2026-07-22 — Auto als eine stabile, manuell vorhersagbare Modellwahl zu behandeln, ist für gerouteete Balance- und Intelligence-Anfragen veraltet; Cursor wählt nun das zugrunde liegende Modell pro Anfrage aus.
- 2026-07-22 — Laut aktueller Dokumentation existiert das frühere Auto-Verhalten nur noch als Cost-Modus.

## Weiterhin unbekannt {#still-unknown}

- Cursor veröffentlicht keine stabile, vollständige Zuordnung von Anfragetypen zu zugrunde liegenden Modellnamen; der Modellpool ändert sich im Laufe der Zeit.
- Die veröffentlichten Einspar- und Zufriedenheitswerte sind Messungen des Anbieters selbst, kein unabhängig reproduzierbarer Benchmark.
- Konkrete Änderungen an Arbeitsabläufen bleiben ungeprüft, bis der Ankündigungsartikel recherchiert wurde.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://cursor.com/blog/router | Introducing Cursor Router | 2026-09-05 |
| https://cursor.com/changelog/router | Cursor Router changelog | 2026-09-05 |
| https://prod.cursor.com/blog/how-cursor-router-works | How Cursor Router chooses the right model for the task | 2026-09-05 |
| https://cursor.com/guides/model-routing | Model routing: right model, right job, right price | 2026-09-05 |
| https://prod.cursor.com/docs/cursor-router | Cursor Router documentation | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:router`, Thread `router`, 1 datiertes Ereignis 2026-07-25 → 2026-07-25.
- **Praktischer Hinweis:** Ab dem 2026-07-25 sollte die Router-Ankündigung von Cursor konsultiert werden, bevor man sich auf Router verlässt oder ihn konfiguriert.
- **Konfidenz:** hoch. Die datierten Überholungsvermerke oben sind maßgeblich dafür, was veraltet ist.
