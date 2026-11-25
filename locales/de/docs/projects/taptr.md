---
title: "TAPTR"
category: projects
date: 2024-12-13
tags: [project, taptr, taptr-public-availability]
aliases: ["TAPTR"]
level: 2
source_sha256: 99641a2dd85ca9c57142055db335cf230f0c90f3e710da4c883d57e0231ad7d8
translation: machine
translated_at: '2026-10-24'
---
# TAPTR {#taptr}

**Entwicklungslinie:** `project:taptr` · Thread `taptr-public-availability`  
**Letztes Ereignis:** 2024-12-13 · 2 datierte Einträge seit 2024-08-01 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

TAPTR ist ein Transformer-Ansatz für Tracking Any Point, gedacht für Entwickler von Videowerkzeugen, 3D-Rekonstruktion und Mask-Tracking.

- Punkt- und Regioneingabe: akzeptiert Punkte oder einen Begrenzungsbereich in einem Frame.
- Trajektorien-Tracking: liefert Punkttrajektorien und Sichtbarkeitsflags über das gesamte Video.
- Raumzeitlicher Kontext: TAPTRv3 ergänzt räumlichen und zeitlichen Kontext mit Wiederherstellung über Schnittgrenzen hinweg.

Die ältere Demo-Space aus der ursprünglichen Auswahl ist gestoppt.
Verwende für die benötigte Version den offiziellen Code statt dieser Demo-Space.

## Entwicklungslinie {#development-line}

- **2024-08-01 — TAPTR-Projektressourcen und aufgabenspezifische Demos wurden verlinkt.** Am 2024-08-01 verlinkte ein Update die Projektwebsite, das Quellcode-Repository und Online-Demonstrationen für Videobearbeitung und Trajektorien-Tracking.
- **2024-12-13 — Eine TAPTR-Hugging-Face-Space wurde verlinkt.** Am 2024-12-13 verlinkte ein Update eine Hugging-Face-Space namens TAPTR zusammen mit einer Quellenangabe als gehosteten Zugangspunkt.

## Was sich geändert hat {#what-changed}

- 2024-08-01 — TAPTRv1 war als offene DETR-ähnliche Implementierung für Point-Tracking verfügbar; der offizielle Code wurde am 2024-07-16 veröffentlicht.
- 2024-12-13 — Für TAPTR erschien eine Hugging-Face-Space eines Drittanbieters statt einer offiziellen Modellveröffentlichung; zum Zeitpunkt der Prüfung ist die Space gestoppt.
- 2026-02-10 — Code für TAPTRv3 wurde als aktuelle Version für lange Videos veröffentlicht.

## So nutzt du es {#how-to-use-this}

Ab 2024-08-01 konnten Praktiker die öffentlichen Quellen von TAPTR und die aufgabenspezifischen Demos über die Projektlinks finden; ab 2024-12-13 konnten sie zusätzlich die verlinkte Hugging-Face-Space evaluieren, nachdem sie deren Eigentümerschaft und Version geprüft hatten.

1. Öffne das offizielle Repository und wähle v1, v2 oder v3; für neue Aufgaben mit langen Videos beginne mit v3.
  — <https://github.com/IDEA-Research/TAPTR>
2. Folge der README für deine Version, übergib Punkte oder eine abgetastete Region im ersten Frame und speichere die vorhergesagten Koordinaten zusammen mit den Sichtbarkeitsflags.
  — <https://github.com/IDEA-Research/TAPTR>
3. Für Videobearbeitung tastest du Punkte innerhalb der Bearbeitungsregion ab und verwendest deren Trajektorien, um die Region über Frames hinweg zu übertragen.
  — <https://arxiv.org/abs/2407.16291>

## Best Practices {#best-practices}

- Wähle TAPTRv3 für lange Clips und Schnittgrenzen: Es verwendet Visibility-aware Long-Temporal Attention, Context-aware Cross Attention und globales Matching bei der Erkennung von Schnitten.
  — <https://taptr.github.io/>
- Baue keine Workflows auf der HYeungLee/TAPTR-Space auf: Sie ist zum Zeitpunkt der Prüfung gestoppt.
  — <https://huggingface.co/spaces/HYeungLee/TAPTR>
- Verwende TAPTRv2 nicht als Standard für lange Videos: Die Autoren vermerken eine unbefriedigende Leistung von v2 bei großer Länge.
  — <https://github.com/IDEA-Research/TAPTR>

## Hiermit überholt {#superseded-by-this}

- 2024-07-24 — TAPTRv2 ersetzte das Cost Volume in TAPTRv1 durch Attention-based Position Update; die Wahl von v1 für maximale Qualität ist damit veraltet.
- 2024-11-27 / 2026-02-10 — TAPTRv3 ersetzt v2 für lange Videos: v2 nutzte RNN-ähnliche Modellierung und hatte Schwierigkeiten mit der Merkmalsextraktion über lange Sequenzen; der Code für v3 wurde am 2026-02-10 veröffentlicht.

## Noch unbekannt {#still-unknown}

- Genaue Installationsbefehle und Versions-Tag-Namen im offiziellen Repository sind auf GitHub noch nicht bestätigt; prüfe vor dem Deployment die README für deine Version.
- Die Hugging-Face-Space aus dem Ereignis vom 2024-12-13 ist eine Demonstration eines Drittanbieters und keine verifizierte offizielle TAPTR-Schnittstelle.
- Zwei Einträge gehören zur TAPTR-Familie, aber der erste betrifft die v1-Veröffentlichung und Demos, während der zweite eine Space eines Drittanbieters ist; es handelt sich um verschiedene Ereignistypen, nicht um zwei Modellveröffentlichungen.
- Ursprüngliche Quellenlinks wurden nicht als Beleg verwendet, da der Nachrichtentext nicht verfügbar ist.
- Das TAPTRv3-Paper erschien am 2024-11-27, der offizielle Code wurde jedoch erst am 2026-02-10 veröffentlicht; davor war es keine zugängliche Implementierung.
- Aktuelle Benchmark-Metriken für v3 wurden nicht zusammengefasst: Quellen behaupten eine konkurrenzfähige Spitzenleistung, die Datensatzauswahl erfordert jedoch eine reproduzierbare Evaluation.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/IDEA-Research/TAPTR | IDEA-Research/TAPTR — offizielle Implementierung und Veröffentlichungszeitplan | 2026-09-05 |
| https://taptr.github.io/ | TAPTR-Projektseite — Überblick v1 bis v3 | 2026-09-05 |
| https://huggingface.co/spaces/HYeungLee/TAPTR | HYeungLee/TAPTR Hugging-Face-Space | 2026-09-05 |
| https://arxiv.org/abs/2407.16291 | TAPTRv2: Attention-based Position Update Improves Tracking Any Point | 2026-09-05 |
| https://arxiv.org/abs/2411.18671 | TAPTRv3: Spatial and Temporal Context Foster Robust Tracking of Any Point in Long Video | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:taptr`, Thread `taptr-public-availability`, 2 datierte Ereignisse 2024-08-01 → 2024-12-13.
- **Praktischer Hinweis:** Ab 2024-08-01 konnten Praktiker TAPTRs öffentliche Quellen und aufgabenspezifische Demos über die Projektlinks finden; ab 2024-12-13 konnten sie zusätzlich die verlinkte Hugging-Face-Space evaluieren, wobei zuvor deren Eigentümerschaft und Version zu prüfen waren.
- **Konfidenz:** hoch. Die datierten Überholungsvermerke sind maßgeblich dafür, was veraltet ist.
