---
title: "SHELLS"
category: projects

tags: [google-shells, project, shells]
aliases: ["SHELLS"]
level: 2
source_sha256: 9e608c92aa11aa41c79e197f190834063a46c456657d6a20d06833549b26b2e9
translation: machine
translated_at: '2026-10-24'
---
# SHELLS {#shells}

**Entwicklungslinie:** `project:google-shells` · Thread `shells`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was ist das {#what-it-is}

SHELLS ist eine Forschungsmethode für 3D-Capture-Teams: Aus kalibrierten Aufnahmen mehrerer Kameras rekonstruiert sie einen Kopf mit fester Topologie und dichter semantischer Korrespondenz. — DINOv2 mit LoRA extrahiert die Merkmale; — ein grobes Netz steuert die Samplingschichten entlang der Normalen; — ein gemeinsamer Transformer sagt das finale Netz voraus. Kennzahlen: 18k Vertices in 0,08 s und etwa 2,4 GB angegebener Inferenzspeicher im Vergleich zu 20 GB bei volumetrischen Baseline-Methoden. Fazit: Es handelt sich um eine Spezifikation zur Reproduktion und Bewertung des Captures, nicht um ein fertiges öffentliches SDK.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; der aktuelle Kenntnisstand steht in den folgenden Abschnitten.

## Was sich geändert hat {#what-changed}

2026-07-21 — SHELLS hat den Übergang von lokaler volumetrischer Vertex-Nachbearbeitung zu einem zweistufigen, grob geführten Oberflächen-Sampling vollzogen: zuerst ein grobes Netz, dann Punktschichten um dieses Netz herum, für eine konsistente Rekonstruktion mit 18k Vertices.

## Anwendung {#how-to-use-this}

Stand 2026-07-21 ergibt sich aus dieser Linie allein keine Änderung der Praxis: Die Links zu SHELLS und Google GNM sind als Hinweise für eine spätere Überprüfung zu behandeln, bevor man sich auf eines der Projekte oder deren Verhältnis zueinander stützt.

1. Beginnen Sie nur mit kalibriertem Multi-View-Capture: Die Methode benötigt Bilder und Kameraparameter für die projektive Merkmalsabtastung.
  — <https://arxiv.org/html/2605.31283v1>
2. Für eine eigenständige Reproduktion implementieren Sie die beschriebene Reihenfolge: DINOv2 mit LoRA, dünnbesetzter globaler Graph, grobes Netz, danach Punktschichten bei ±4 mm entlang der Normalen und ein gemeinsamer Transformer.
  — <https://arxiv.org/html/2605.31283v1>
3. Bewerten Sie die semantische V2V-Korrespondenz und die geometrische P2S-Nähe zum Scan getrennt: Diese Metriken können auseinanderlaufen.
  — <https://arxiv.org/html/2605.31283v1>
4. Planen Sie keinen Start aus dem offiziellen GitHub-Repository von SHELLS: Es enthält den Code der Projektwebsite, nicht die Modellimplementierung oder Checkpoints.
  — <https://github.com/syntec-research/SHELLS>

## Best Practices {#best-practices}

- Prüfen Sie die Kalibrierung, einschließlich Intrinsics, Extrinsics und Objektivverzerrungen; die Methode nutzt bekannte Kameraparameter und löst die Geometrie nicht aus einem Einzelbild.
  — <https://arxiv.org/html/2605.31283v1>
- Verwenden Sie kein Einzelbild als regulären Eingang: Die Autoren bezeichnen die Single-View-Rekonstruktion als schlecht gestellte Aufgabe; Stabilität wird ab zwei Ansichten gezeigt.
  — <https://arxiv.org/html/2605.31283v1>
- Geben Sie das Netz nicht als fotorealistisches finales Asset aus: Feine Falten und Poren fehlen, dafür braucht es eine eigene Schicht aus Displacement Maps und Texturen.
  — <https://arxiv.org/html/2605.31283v1>
- Testen Sie extreme Artikulationen der Sprache sowie die externe Geometrie von Haaren oder Bart separat: Diese Fälle sind in den veröffentlichten Einschränkungen nicht zuverlässig abgedeckt.
  — <https://arxiv.org/html/2605.31283v1>

## Hiermit ersetzt {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Öffentlicher Code, Gewichte, Modelllizenz und ein reproduzierbares Inferenzskript für SHELLS wurden nicht gefunden: Das offizielle SHELLS-Repository wird ausdrücklich als Website-Repository beschrieben.
- Die beiden Ausgangs-URLs führen zu unterschiedlichen Ressourcen: SHELLS zum Artikel und zur Rekonstruktions-Website, GNM zu einem parametrischen Kopfmodell. Im Text des SHELLS-Artikels wird GNM nicht erwähnt; ihr technischer Zusammenhang ist daher, abgesehen von gemeinsamen Autoren und Google, nicht belegt.
- Ein Vertrag zur Aufbereitung realer Eingangsdaten außerhalb des von den Autoren beschriebenen 13-Kamera-Captures wurde nicht veröffentlicht; die Übertragung auf beliebige Smartphone- oder unkalibrierte Aufnahmen ist daher nicht belegt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://arxiv.org/html/2605.31283v1 | Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://syntec-research.github.io/SHELLS/ | Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://github.com/syntec-research/SHELLS | GitHub - syntec-research/SHELLS: Website-Repository für das Projekt SHELLS | 2026-09-05 |
| https://arxiv.org/abs/2605.31283v1 | arXiv:2605.31283v1 — Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://github.com/google/GNM/tree/main | GitHub - google/GNM: Ein offenes Ökosystem parametrischer Menschmodelle und Perception-Stacks, beginnend mit GNM Head | 2026-09-05 |

## Agenten-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:google-shells`, Thread `shells`, 0 datierte Ereignisse - → -.
- **Praxishinweis:** Stand 2026-07-21 ergibt sich aus dieser Linie allein keine Änderung der Praxis: Die Links zu SHELLS und Google GNM sind als Hinweise für eine spätere Überprüfung zu behandeln, bevor man sich auf eines der Projekte oder deren Verhältnis zueinander stützt.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
