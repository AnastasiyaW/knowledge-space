---
title: "Apple — Apple AI: von Forschungsveröffentlichungen zu Produktfunktionen"
category: organizations
tags: [apple, apple-ai-research-to-product, apple_gaudi, apple_intelligence, open_source_release, organization]
aliases: ["Apple"]
level: 2
source_sha256: 39e133c36ad4a05d3879f19bbd549bd750d1264d2601271c88f0c4cea7b9b7e9
translation: machine
translated_at: '2026-10-24'
---
# Apple — Apple AI: von Forschungsveröffentlichungen zu Produktfunktionen {#apple-apple-ai-research-releases-to-product-capabilities}

**Entwicklungslinie:** `organization:apple` · Thread `apple-ai-research-to-product`  
**Ereignisse:** 3 datierte, 2022-08-05 → 2026-06-09 · **Recherchiert:** 2026-09-03 · Konfidenz: mittel

## Was es ist {#what-it-is}

Apple ist ein Geräte- und Software-Plattformunternehmen, dessen nutzbare KI-Oberfläche Apple Intelligence für Personen mit unterstützter Apple-Hardware ist, sowie Swift-Teams, die systemnahe Apps entwickeln. - Auf Geräten: Funktionen für Schreiben, Bilder, Suche, Übersetzung, Benachrichtigungen und Shortcuts. - In Apps: Foundation Models für typisierte Generierung und Tool-Nutzung; App Intents für Siri, Spotlight und Shortcuts. Einschränkung: Die Unterstützung variiert nach Gerät, Betriebssystem, Sprache und Region; berechtigte iPhone-, iPad-, Mac- und Vision-Pro-Geräte benötigen 7 GB Speicher. Fazit: Apple Intelligence als eine an Voraussetzungen gebundene Plattformintegration nutzen; GAUDI und NeuMan als getrennten Forschungscode aus dem Jahr 2022 behandeln.

## Entwicklungslinie {#development-line}

- **2022-08-05 — Apple veröffentlichte das Gaudi-Machine-Learning-Repository.** Am 2022-08-05 veröffentlichte Apple das Repository ml-gaudi öffentlich auf GitHub. Dies ist eine datierte öffentliche Veröffentlichung eines Machine-Learning-Forschungsprojekts von Apple und gehört in die KI-Entwicklungshistorie der Organisation.
- **2022-08-17 — Apple veröffentlichte das Neuman-Machine-Learning-Repository.** Am 2022-08-17 veröffentlichte Apple das Repository ml-neuman öffentlich auf GitHub. Dies ist eine eigenständige, datierte öffentliche Veröffentlichung von Machine-Learning-Arbeiten Apples und belegt die fortgesetzte öffentliche KI-Forschungstätigkeit.
- **2026-06-09 — Apple kündigte neue Apple-Intelligence-Funktionen für den Alltag an.** Am 2026-06-09 kündigte Apple Apple-Intelligence-Funktionen an, die für alltägliche Erfahrungen gedacht sind. Die verlinkte Seite im Apple Newsroom und das begleitende Video machen dies zu einem wesentlichen, produktbezogenen Meilenstein in der KI-Entwicklungshistorie Apples.

## Was sich geändert hat {#what-changed}

Apple-Entwicklungslinie: - 2022-08-05 — GAUDI stellte Forschungscode von Apple für generative 3D-Szenen zur Verfügung, die als Radiance Fields dargestellt werden, einschließlich Konditionierung durch Text oder RGB-Bilder. Es handelte sich um eine Forschungsimplementierung, nicht um eine Plattform-API. - 2022-08-17 — NeuMan stellte eine Referenzimplementierung zur Verfügung, mit der ein Hintergrund und eine animierbare Person aus einem einzigen Video rekonstruiert werden können. Die dokumentierte Umgebung mit Python 3.7, PyTorch 1.8 und CUDA macht daraus einen Reproduktions-Workflow, keine Laufzeitumgebung für Apple-Geräte. - 2026-06-09 — Apples Veröffentlichung vom 8. Juni kündigte die nächste Apple-Intelligence-Architektur an, einschließlich neuer Systemfunktionen und der Erstellung von Shortcuts per natürlicher Sprache. Die Veröffentlichung beschrieb Funktionen der iOS-27-Ära als Entwicklertests, öffentliche Beta oder Verfügbarkeit im Herbst, nicht als abgeschlossene weltweite Einführung. - Heute geprüft (2026-09-03) — Apples aktueller Entwicklerweg besteht aus Foundation Models plus App Intents; der Apple Support dokumentiert Hardware-, Speicher-, Sprach- und regionale Voraussetzungen für verfügbare Funktionen.

## Verwendung {#how-to-use-this}

Stand 2026-06-09 sollten Praktiker, die Apple beobachten, öffentliche Machine-Learning-Forschungsveröffentlichungen von produktbezogenen Apple-Intelligence-Ankündigungen unterscheiden und beide als zusammenhängende Belege für die KI-Entwicklung des Unternehmens verfolgen.

1. Prüfen Sie Hardware, Betriebssystem, freien Speicher, Geräte- und Siri-Sprache sowie die regionale Verfügbarkeit. Aktualisieren Sie das Gerät, aktivieren Sie Apple Intelligence unter Einstellungen > Apple Intelligence & Siri und lassen Sie das Gerät während des Herunterladens der On-Device-Modelle mit WLAN und am Stromnetz.
  — <https://support.apple.com/en-ie/121115>
2. Bei einer Swift-App beginnen Sie mit Foundation Models, wenn die Funktion Sprach- oder multimodale Generierung, strukturierte Ausgaben oder Tool-Aufrufe benötigt; wählen Sie das Modell bzw. den Anbieter für die jeweilige Aufgabe, statt anzunehmen, dass ein On-Device-Modell jede Arbeitslast abdeckt.
  — <https://developer.apple.com/apple-intelligence/>
3. Stellen Sie App-Aktionen und Inhalte über App Intents und Entitäten bereit, damit sie über Siri, Spotlight und Shortcuts auffindbar sind.
  — <https://developer.apple.com/apple-intelligence/>
4. Für eine persönliche Automatisierung verwenden Sie die Shortcuts-Aktion „Use Model“, wählen einen Ausgabetyp, den die nächste Aktion verarbeiten kann, und testen den gesamten Ablauf mit echten App-Entitäten.
  — <https://developer.apple.com/videos/play/wwdc2025/260/>

## Bewährte Praktiken {#best-practices}

- Beschränken Sie Onboarding und Funktionspfade auf die tatsächliche Hardware, das Betriebssystem, den Speicher, die Sprache und die Region; präsentieren Sie nicht unterstützte Funktionen nicht als verfügbar.
  — <https://support.apple.com/en-ie/121115>
- Verwenden Sie Guided Generation für typisierte Ausgaben, testen Sie verschiedene Prompts anhand repräsentativer Stichproben und bewerten Sie die Ergebnisse, bevor Sie sich auf eine modellgestützte Funktion verlassen.
  — <https://developer.apple.com/documentation/technologyoverviews/generative-models?changes=_2%2C_2>
- Stellen Sie Modell-Workflows nur nützliche Entitätseigenschaften zur Verfügung, bieten Sie „Find“-Aktionen oder Indexierung für die Auffindbarkeit an und liefern Sie Parameterzusammenfassungen und Vorschläge für Spotlight und Shortcuts.
  — <https://developer.apple.com/videos/play/wwdc2025/260/>
- Halten Sie die Funktionen vom Juni 2026 hinter Verfügbarkeitsprüfungen: Apple kennzeichnet sie in der Veröffentlichung als Tests, Beta oder Rollout im späteren Jahresverlauf und weist auf sprachliche und regionale Unterschiede hin.
  — <https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/>

## Dadurch ersetzt {#superseded-by-this}

- 2022-08-05/2022-08-17: GAUDI und NeuMan sind als Leitfaden für die Integration einer KI-Funktion auf Apple-Plattformen überholt. Foundation Models und App Intents sind der aktuelle Weg; die Repositories bleiben nur für ihre separaten Forschungs- und Reproduktionsfragen relevant.
- Status der Vorschau vom 2026-06-08: Die Annahme, dass jede KI-Funktion von iOS 27 oder Siri allgemein verfügbar sei, ist überholt. Apples Ankündigung kennzeichnet die neuen Funktionen als Tests, Beta oder Verfügbarkeit im späteren Jahresverlauf und behält regionale und sprachliche Einschränkungen bei.

## Weiterhin unbekannt {#still-unknown}

- GAUDI, NeuMan und Apple Intelligence bilden keine dokumentierte gemeinsame Produktlinie. Keine heute gelesene Primärquelle verbindet eines der beiden Repositories aus dem Jahr 2022 mit dem Produkt oder SDK Apple Intelligence.
- Die Seite vom Juni 2026 beschreibt Funktionen der iOS-27-Ära weiterhin als künftige Tests, Beta oder Verfügbarkeit im Herbst. Es wurde keine Versionsmitteilung nach der Ankündigung gefunden, die belegt, dass alle angekündigten Funktionen zum 2026-09-03 in jeder Region aktiv sind.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/apple/ml-gaudi | GAUDI: A Neural Architect for Immersive 3D Scene Generation — apple/ml-gaudi | 2026-09-03 |
| https://github.com/apple/ml-neuman | NeuMan: Neural Human Radiance Field from a Single Video — apple/ml-neuman | 2026-09-03 |
| https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/ | Apple Intelligence brings powerful AI capabilities into everyday experiences | 2026-09-03 |
| https://developer.apple.com/apple-intelligence/ | Apple Intelligence — Apple Developer | 2026-09-03 |
| https://support.apple.com/en-ie/121115 | How to get Apple Intelligence — Apple Support | 2026-09-03 |
| https://developer.apple.com/documentation/technologyoverviews/generative-models?changes=_2%2C_2 | Generative models and machine learning — Apple Developer Documentation | 2026-09-03 |
| https://developer.apple.com/videos/play/wwdc2025/260/ | Develop for Shortcuts and Spotlight with App Intents — WWDC25 | 2026-09-03 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `organization:apple`, Thread `apple-ai-research-to-product`, 3 datierte Ereignisse 2022-08-05 → 2026-06-09.
- **Praktischer Hinweis:** Stand 2026-06-09 sollten Praktiker, die Apple beobachten, öffentliche Machine-Learning-Forschungsveröffentlichungen von produktbezogenen Apple-Intelligence-Ankündigungen unterscheiden und beide als zusammenhängende Belege für die KI-Entwicklung des Unternehmens verfolgen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise sind maßgeblich dafür, was veraltet ist.
