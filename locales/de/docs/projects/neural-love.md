---
title: "neural.love"
category: projects
date: 2022-12-23
tags: [neural-love, neural-love-image-tools, neural_love, project]
aliases: ["neural.love"]
level: 2
source_sha256: 2b80f2b536c39377748de8467c7c52670c00f669b3cfae4c6f9b7a07a154f7bb
translation: machine
translated_at: '2026-10-24'
---
# neural.love {#neurallove}

**Entwicklungslinie:** `project:neural-love` · Thread `neural-love-image-tools`  
**Letztes Ereignis:** 2022-12-23 · 2 datierte seit 2022-09-09 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

neural.love ist eine Browser- und API-Plattform für Kreative, die KI-Bildgenerierung, Bildverarbeitung und Medien-Workflows benötigen.

- Text-zu-Bild-Generierung mit Optionen für Modell, Stil, Prompt, Layout, HD und Bildeingabe.
- Bildverarbeitung zum Hochskalieren, Schärfen, Colorieren, Restaurieren und Uncropping.
- Videobezogene Workflows für Kreative.

Das dokumentierte API-Standardlimit beträgt 300 Anfragen pro fünf Minuten, und kostenpflichtige Aufträge verbrauchen Credits. Wir nutzen den Dienst für begrenzte, aktuelle Aufgaben, machen ihn jedoch nicht zu einer neuen langfristigen Produktionsabhängigkeit, solange Eigentümerschaft und Support-Kontinuität nicht bestätigt sind.

## Entwicklungslinie {#development-line}

- **2022-09-09 — neural.love verlinkte eine Route und Dokumentation für KI-Kunstgenerierung.** Die Route AI Art Generator war vorhanden; eine frühere öffentliche Auflistung macht dies zu einem Sichtbarkeitsmeilenstein und nicht zu einem bestätigten Erststart.
- **2022-12-23 — neural.love verlinkte eine eigene Route für Bild-Uncropping.** Die Route Uncrop war vorhanden; ihr ursprüngliches Modell, ihre Einstellungen, ihr Preis und ihre Limits sind nicht verifiziert.

## Was sich geändert hat {#what-changed}

- 2022-09-09: Die Route AI Art Generator war vorhanden; eine frühere öffentliche Auflistung macht dies zu einem Sichtbarkeitsmeilenstein und nicht zu einem bestätigten Erststart.
- 2022-12-23: Die Route Uncrop war vorhanden; ihr ursprüngliches Modell, ihre Einstellungen, ihr Preis und ihre Limits sind nicht verifiziert.
- 2023-08-28: NL 1.01 Text-zu-Bild und ein aktualisierter HD-Modus gingen live, zusammen mit Updates für Bild-zu-Bild-Remix, Kategorien, Suche und Dark Theme.
- 2023-10-16: Uncrop 2.0 zielte auf Glitches und die Konvertierung von Seitenverhältnissen.
- 2024-09-11: Uncrop 4 fügte drei Varianten pro Eingabe hinzu und behielt Outpainting mit einem oder zwei Durchgängen bei.
- 2024-11-11: MiniMax Video 01 brachte Bild-zu-Video- und Text-zu-Video-Generierung in das Produkt.
- 2025-03-22: Die Suite erhielt Bildbearbeitung per Textbefehl, agentische Bildgeschichten, Text-zu-Video mit Motivreferenz, Imgen 3 und einen Schalter zum Deaktivieren der Prompt-Erweiterung.
- 2026-03-12: Der Eigentümer stellte Produkt, Marke, Domain, Codebasis und Betriebsunterlagen zum Verkauf und erklärte, dass nicht mehr nennenswert investiert werde.

## Anwendung {#how-to-use-this}

Stand 2022-12-23 sollten Praktiker die sichtbare Bildwerkzeug-Linie von neural.love so verstehen, dass sie sowohl die KI-Kunstgenerierung als auch eine eigene Uncropping-Route umfasst. Vor dem Einsatz eines der beiden Workflows sollte der damalige Funktionsumfang überprüft werden.

1. Für die Bildgenerierung im Browser öffnen Sie AI Art Generator, wählen ein Modell und einen Stil, verfeinern den Prompt und generieren.
  — <https://neural.love/ai-art-generator>
2. Für den API-Zugang melden Sie sich an, öffnen die Einstellungen, erzeugen ein API-Token und senden es als Bearer-Token.
  — <https://docs.neural.love/>
3. Für die API-Bildgenerierung senden Sie einen POST an /v1/ai-art/generate mit expliziten Werten für prompt, style, layout, amount, isHd und isPublic; speichern Sie orderId und fragen Sie den Abschluss ab.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
4. Für die API-Verarbeitung holen Sie sich eine vorsignierte Upload-URL, laden die Quelle hoch und erstellen dann einen Bildverarbeitungsauftrag; verwenden Sie image_uncrop allein mit outpainting oder aspect_ratio und fragen Sie den zurückgegebenen Auftrag ab.
  — <https://docs.neural.love/ai-images-processing-api>
5. Für Outpainting im Browser verwenden Sie die aktive Route Uncrop, um Ränder zu erweitern oder ein Bildseitenverhältnis zu ändern, und prüfen das erzeugte Ergebnis, bevor Sie es verwenden.
  — <https://neural.love/uncrop>

## Bewährte Praktiken {#best-practices}

- Schätzen Sie die Credits mit denselben Generierungsparametern ab, bevor Sie einen kostenpflichtigen Auftrag absenden.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
- Fragen Sie Aufträge in steigenden Intervallen ab, etwa 30, 45, 60, 90 und 150 Sekunden, statt in engen Schleifen zu pollen.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
- Setzen Sie isPublic explizit und führen Sie einen Test mit unkritischem Material durch, bevor Sie privates Material verarbeiten; die aktuelle Dokumentation nennt widersprüchliche Standardwerte.
  — <https://docs.neural.love/faq>
- Belassen Sie image_uncrop in einem eigenen Verarbeitungsauftrag; laut API kann es nicht mit anderen Bildparametern kombiniert werden.
  — <https://docs.neural.love/ai-images-processing-api>
- Behandeln Sie Uncrop als kreative Erweiterung und nicht als historische Rekonstruktion: Das Produkt warnt, dass Eingaben verkleinert werden, Ergebnisse variieren und historische Genauigkeit nicht sein Ziel ist.
  — <https://neural.love/blog/uncrop-4-image-expansion>
- Ersetzen Sie eingesetzte Zugangsdaten, bevor Sie ein neues API-Token erzeugen, da pro Konto nur ein Token aktiv ist und ein neues das alte deaktiviert.
  — <https://docs.neural.love/>

## Abgelöst durch diesen Stand {#superseded-by-this}

- 2022-09-09 als erste öffentliche Verfügbarkeit von AI Art Generator — seit 2022-08-23 überholt.
- Anleitungen vor Uncrop 4 als aktuelle Richtlinie — seit 2024-09-11 überholt.
- Die Annahme, dass der heutige Eigentümer weiterhin nennenswert in das Produkt investiert — seit 2026-03-12 überholt.

## Weiterhin unbekannt {#still-unknown}

- Für den Link AI Art Generator vom 2022-09-09 und den Link Uncrop vom 2022-12-23 wurde keine datierte Ankündigung des Anbieters gefunden; ihr ursprüngliches Modell, ihre Eingaben, ihr Preis und ihre Limits sind nicht verifiziert.
- Die historische Route https://docs.neural.love/docs konnte heute nicht abgerufen werden; ihr Inhalt aus 2022 könnte verschoben worden sein, ist hier aber nicht verifiziert.
- Die aktuelle API-Dokumentation widerspricht sich bei der Standardsichtbarkeit generierter Bilder: Das Tutorial besagt, dass alle Generierungen standardmäßig öffentlich sind, die FAQ, dass API-Generierungen standardmäßig privat sind.
- Die Mitteilung zum Verkauf der Vermögenswerte nennt weder einen Abschlusstermin, einen Käufer, einen Übergangsplan, eine Support-Zusage noch ein API-SLA.
- Eine Suche in vereinfachtem Chinesisch fand keine datierte Bestätigung des Anbieters für die beiden Routen von 2022.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://neural.love/ai-art-generator | AI Art Generator & AI Image Generator | neural.love | 2026-09-04 |
| https://neural.love/uncrop | Uncrop Image Online – Extend Photos for Free | neural.love | 2026-09-04 |
| https://docs.neural.love/ | Getting Started | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api | How to generate AI art with neural.love API | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/ai-images-processing-api | AI Images Processing API | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/faq | neural.love API - Frequently Asked Questions | The neural.love API Developer Hub | 2026-09-04 |
| https://akinix.com/forums/topic/209-curated-ai-art-generator-by-neurallove/ | Curated AI art generator by neural.love - General discussions - Akinix | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/xev8ds | Free stable diffusion generation website – neural.love | 2026-09-04 |
| https://neural.love/blog/new-text-to-image-model-and-future-roadmap | New text-to-image model is here & Future Roadmap | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/uncrop-2-0-feature-update | Feature Update: Uncrop 2.0 – Less Glitches | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/uncrop-4-image-expansion | Introducing Uncrop 4: Expand Your Images Like Never Before | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/video-generation-launch | Introducing Video Generation: Transform Images into Motion with neural.love | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/march-2025-release-notes | Product Updates: March 2025 Release Notes | neural.love blog about AI stuff | 2026-09-04 |
| https://neural.love/blog/neural-love-is-for-sale | neural.love assets are for sale | neural.love blog about AI stuff | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:neural-love`, Thread `neural-love-image-tools`, 2 datierte Ereignisse vom 2022-09-09 bis 2022-12-23.
- **Praktischer Hinweis:** Stand 2022-12-23 sollten Praktiker die sichtbare Bildwerkzeug-Linie von neural.love so verstehen, dass sie sowohl die KI-Kunstgenerierung als auch eine eigene Uncropping-Route umfasst. Vor dem Einsatz eines der beiden Workflows sollte der damalige Funktionsumfang überprüft werden.
- **Konfidenz:** mittel. Für die Frage, was überholt ist, gelten die datierten Angaben unter „Abgelöst durch diesen Stand“.
