---
title: "Disney Research — Interaktive generative Bewegungsbearbeitung"
category: organizations
tags: [disney-research, disney_research, interactive-generative-motion-editing, organization]
aliases: ["Disney Research"]
level: 2
source_sha256: 30f6ca9c687d9a5dafc4bb6310fc4806fb4d2ade079ef0c9331e1138e2fb5bf5
translation: machine
translated_at: '2026-10-24'
---
# Disney Research — Interaktive generative Bewegungsbearbeitung {#disney-research-interactive-generative-motion-editing}

**Entwicklungslinie:** `organization:disney-research` · Strang `interactive-generative-motion-editing`  
**Ereignisse:** 1 datiert, 2026-08-01 → 2026-08-01 · **Recherchiert:** 2026-09-03 · Konfidenz: mittel

## Worum es geht {#what-it-is}

Disney Research — DisneyResearch|Studios veröffentlicht Forschung zu maschinellem Lernen und visueller Datenverarbeitung für Animation, VFX und Forschungsteams. — öffentliche Paper und technische Demonstrationen; — Arbeit von 2022 zur Verjüngung und Alterung von Gesichtern in Videos; — Arbeit von 2026 zur editierbaren skelettbasierten Bewegung. Einschränkung: Die geprüften offiziellen Seiten nennen Paper und Videos, aber kein öffentliches Installationspaket, keine API und keine Quellcode-Veröffentlichung. Fazit: Als F&E-Referenz oder Reproduktionsziel verwenden, nicht als fertiges Werkzeug.

## Entwicklungslinie {#development-line}

- **2026-08-01 — Disney Research dokumentierte interaktive generative Bewegungsbearbeitung über Scheduled Inpainting.** Am 2026-08-01 verzeichnete diese Linie die Arbeit von Disney Research mit dem Titel „Interactive Generative Motion Editing via Scheduled Inpainting“, verlinkt von der Studios-Website. Der beigefügte Videolink deutet darauf hin, dass die Arbeit eine visuelle Demonstration des Bearbeitungsansatzes enthielt.

## Was sich geändert hat {#what-changed}

Disney Research — die datierten Einträge sind Forschungspublikationen, keine Versionen eines einzelnen Produkts. — 2022-12-02: Das verlinkte Video dokumentiert FRAN, veröffentlicht von Disney Research am 2022-11-30: ein U-Net-Ansatz zur videobasierten Gesichtsverjüngung mit lokalisierter künstlerischer Steuerung, der darauf abzielt, die Bild-für-Bild-Retusche in 2D zu verringern und dabei Identität und zeitliche Stabilität zu erhalten. — 2026-08-01: Die verlinkte Publikation, von Disney auf 2026-07-30 datiert und auf arXiv auf 2026-07-31, führt Scheduled Inpainting ein: eine Methode zur Inferenzzeit, mit der vortrainierte generative Modelle für skelettbasierte Bewegung über einen Erhaltungsplan und eine raumzeitliche Maske bearbeitet werden; sie unterstützt Verlängerung, Zusammenfügen und Compositing ohne zusätzliches Training. — Heute gefunden (2026-09-04): DisneyResearch|Studios stellt sich weiterhin als Organisation für Forschung zu maschinellem Lernen und visueller Datenverarbeitung mit laufenden Veröffentlichungen dar. Einschränkung: Die spätere Arbeit behandelt Körperbewegung, nicht die Verjüngung von Gesichtern. Fazit: Scheduled Inpainting ersetzt FRAN nicht; es handelt sich um getrennte Forschungsstränge.

## Anwendung {#how-to-use-this}

Stand 2026-08-01 sollten Praktiker, die generative Workflows zur Bewegungsbearbeitung evaluieren, den Scheduled-Inpainting-Ansatz von Disney Research als dokumentierte Forschungsrichtung betrachten und die verlinkte Demonstration prüfen, bevor sie eine Implementierung auswählen.

1. Ein konkretes Forschungsergebnis aus dem aktuellen Katalog auswählen; Disney Research ist ein Veröffentlicher von Arbeiten zu maschinellem Lernen und visueller Datenverarbeitung und kein Software-Endpunkt.
  — <https://studios.disneyresearch.com/research/>
2. Scheduled Inpainting als internes Reproduktions- oder Prototypziel behandeln: Die offizielle Seite liefert ein Paper und eine Demonstration, aber keine benannte öffentliche Installation, API oder Code-Repository.
  — <https://studios.disneyresearch.com/2026/07/30/interactive-generative-motion-editing-via-scheduled-inpainting/>
3. Einen skelettbasierten Ausgangsbewegungsclip und räumliche Gelenkbedingungen an ein vortrainiertes generatives Bewegungsmodell übergeben, das direkte Manipulation unterstützt.
  — <https://arxiv.org/html/2607.29133>
4. Einen zeitlichen Erhaltungsplan und eine Maske pro Gelenk und pro Frame festlegen: unveränderte Bewegung beibehalten und Synthese rund um die beabsichtigte Bearbeitung zulassen; denselben Mechanismus für Verlängerung, Zusammenfügen oder Compositing verwenden.
  — <https://arxiv.org/html/2607.29133>
5. Ergebnisse auf Einhaltung der Bedingungen, Kontinuität, Fußgleiten und Verhalten außerhalb der gelernten Bewegungsverteilung des Modells prüfen, bevor sie in eine Animationspipeline übernommen werden.
  — <https://arxiv.org/html/2607.29133>

## Bewährte Vorgehensweisen {#best-practices}

- Zuerst die grobe strukturelle Bearbeitung mit Ganzkörperbedingungen vornehmen und dann die Bewegungskurven mit einzelnen Positions- und Orientierungsbedingungen verfeinern.
  — <https://arxiv.org/html/2607.29133>
- Ursprung und Richtung des Clips ausrichten und die Skalierung normalisieren, bevor Bewegungen gemischt werden; das Paper bringt fehlende Ausrichtung mit Verzerrungen, Diskontinuitäten und Gleitartefakten in Verbindung.
  — <https://arxiv.org/html/2607.29133>
- Um eine Bearbeitung einen sanft abklingenden gaußschen Einflussbereich verwenden, damit benachbarte Frames teilweise an die Ausgangsbewegung gebunden bleiben und ihren Rhythmus nicht abrupt ändern.
  — <https://arxiv.org/html/2607.29133>
- Keine verlässliche Rekonstruktion weit außerhalb der gelernten Bewegungsverteilung des Modells erwarten; übertriebene oder periodische Bewegung benötigt unter Umständen zusätzliche Extremwertbedingungen und erzeugt später mehr Bedingungen, die zu verwalten sind.
  — <https://arxiv.org/html/2607.29133>

## Abgelöst durch {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Arbeit zur Gesichtsverjüngung von 2022 und die Arbeit zur skelettbasierten Bewegung von 2026 teilen eine Organisation, aber keine geprüfte Quelle belegt eine Vorgänger- oder Nachfolgebeziehung zwischen ihnen.
- Die geprüften offiziellen Projektseiten nennen kein öffentliches Code-Repository, keine Gewichte, keine API, kein Installationspaket und keine Lizenz; die öffentliche Verfügbarkeit einer Implementierung ist nicht verifiziert.
- Bei der heutigen begrenzten Suche wurde keine separate chinesischsprachige Primärquelle gefunden.
- Die geprüften Quellen geben nicht an, ob eine der beiden Methoden nach der Veröffentlichung in einer Disney-Produktion eingesetzt wurde.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://studios.disneyresearch.com/research/ | Research | Disney Research Studios | 2026-09-04 |
| https://www.youtube.com/watch?v=ZP1ApcdyAjk | Production Ready Face Re Aging for Visual Effects - YouTube | 2026-09-04 |
| https://studios.disneyresearch.com/2022/11/30/production-ready-face-re-aging-for-visual-effects/ | Production-Ready Face Re-Aging for Visual Effects | Disney Research Studios | 2026-09-04 |
| https://studios.disneyresearch.com/2026/07/30/interactive-generative-motion-editing-via-scheduled-inpainting/ | Interactive Generative Motion Editing via Scheduled Inpainting | Disney Research Studios | 2026-09-04 |
| https://arxiv.org/html/2607.29133 | Interactive Generative Motion Editing via Scheduled Inpainting | 2026-09-04 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `organization:disney-research`, Strang `interactive-generative-motion-editing`, 1 datiertes Ereignis 2026-08-01 → 2026-08-01.
- **Praktischer Hinweis:** Stand 2026-08-01 sollten Praktiker, die generative Workflows zur Bewegungsbearbeitung evaluieren, den Scheduled-Inpainting-Ansatz von Disney Research als dokumentierte Forschungsrichtung betrachten und die verlinkte Demonstration prüfen, bevor sie eine Implementierung auswählen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
