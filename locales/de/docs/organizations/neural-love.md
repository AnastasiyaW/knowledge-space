---
title: "neural.love — KI-Erstellung und Modelltraining"
category: organizations
date: 2022-11-15
tags: [ai-creation-and-model-training, neural-love, neural_love, organization]
aliases: ["Neural.love", "neural.love"]
level: 3
source_sha256: bd99f44ea59b755ec2c80f34ee1e2bf50003f515578dba761cd572fac0bbec3c
translation: machine
translated_at: '2026-10-24'
---
# neural.love — KI-Erstellung und Modelltraining {#neurallove-ai-creation-and-model-training}

**Entwicklungslinie:** `organization:neural-love` · Thema `ai-creation-and-model-training`  
**Letztes Ereignis:** 2022-11-15 · 2 datierte seit 2022-08-17 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

neural.love ist eine Browser- und API-Plattform für Kreative, die KI-Bildgenerierung, Bildverbesserung bzw. -restaurierung, videobezogene Werkzeuge und Fototransformationen benötigen.

- AI Art Generator: Generierung mit Modell, Stil, Prompt, Layout, HD- und Bildeingabe-Optionen.
- AI Photo Studio: Transformationen einzelner Fotos.
- Custom-Model-Training-API: Workflow zum Training eigener KI-Kunstgenerierungsmodelle.

Der dokumentierte API-Standard beträgt 300 Anfragen pro fünf Minuten, und die Generierung verbraucht Credits.

Die Plattform unterstützt aktuelle kreative Arbeit und begrenzte Integrationen. Vor einer Entscheidung für eine neue langfristige Produktionsabhängigkeit sollten jedoch Eigentumsverhältnisse und Support geprüft werden.

## Entwicklungslinie {#development-line}

- **2022-08-17 — neural.love markierte einen Meilenstein beim KI-Kunstgenerator.** Am 2022-08-17 verlinkte neural.love auf seinen AI Art Generator und setzte damit einen öffentlichen Produktentwicklungsmeilenstein für sein Angebot zur KI-Bilderstellung.
- **2022-11-15 — neural.love markierte einen Meilenstein beim Modelltraining.** Am 2022-11-15 verlinkte neural.love auf seine Seite zum Modelltraining und erweiterte damit seine öffentliche Produktlinie von der KI-Kunstgenerierung um einen Workflow für Modelltraining.

## Was sich geändert hat {#what-changed}

neural.love — die datierten Links belegen Produktrouten, nicht verifizierte Launch-Ankündigungen.

2022-08-17 — die Route AI Art Generator war vorhanden.

2022-11-15 — die Route Train a Model war vorhanden; die verfügbaren Belege lassen weder die historischen Eingaben, den Modelltyp noch die Ausgabe erkennen.

Heute gefunden (2026-09-04) — die Route AI Art Generator ist weiterhin online. Train a Model leitet auf AI Photo Studio weiter, während das Training eigener Modelle weiterhin über die API dokumentiert ist. Ein Hinweis vom 12. März 2026 besagt, dass die Assets zum Verkauf stehen und der Eigentümer keine wesentlichen neuen Investitionen plant.

Die beiden Daten aus 2022 sollten nicht als zwei bestätigte Feature-Launches gelesen werden.

## Anwendung {#how-to-use-this}

Stand 2022-08-17 sollten Praktiker den AI Art Generator von neural.love als Teil der Produktlinie erkennen. Stand 2022-11-15 sollten sie bei der Bewertung der Erstellungsfähigkeiten der Organisation zusätzlich den Modelltraining-Workflow prüfen.

1. AI Art Generator öffnen, Modell und Stil wählen, den Prompt verfeinern und im Browser ein Bild generieren.
  — <https://neural.love/ai-art-generator>
2. AI Photo Studio verwenden, wenn es um die Transformation eines einzelnen Fotos geht und nicht um einen Workflow mit eigenem Modell.
  — <https://neural.love/ai-photostudio>
3. Für Automatisierung anmelden, unter Einstellungen den API-Token erzeugen und ihn im Header Authorization Bearer senden.
  — <https://docs.neural.love/>
4. Eine Bestellung mit Prompt, Stil, Layout, Anzahl sowie HD- oder Sichtbarkeitsoptionen aufbauen; Credits vor dem Absenden der Generierungsanfrage abschätzen und die Order-ID aufbewahren.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
5. Die Bestellung in zunehmenden Intervallen abfragen, bis status.isReady erreicht ist, und danach die Ausgabe abrufen.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
6. Für ein eigenes KI-Kunstmodell /ai-art/custom-model/create aufrufen, auf das Ende des Trainings warten und das Modell dann in /ai-art/generate verwenden.
  — <https://docs.neural.love/reference/ai-custom-model-generate>

## Bewährte Praktiken {#best-practices}

- Die Credit-Kosten vor jedem kostenpflichtigen Batch abschätzen; sie hängen von Bildanzahl, Sichtbarkeit und HD-Modus ab.
  — <https://docs.neural.love/>
- Die Order-ID speichern und Statusabfragen in zunehmenden Intervallen statt in engem Takt durchführen.
  — <https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api>
- API-Token sicher verwalten und koordiniert rotieren: Pro Konto ist nur ein Token aktiv, und das Erstellen eines neuen deaktiviert das bisherige.
  — <https://docs.neural.love/>
- Datenschutz als kontoweite Einstellung behandeln, die vor dem Versand sensibler Medien zu prüfen ist: Der API-Leitfaden und die FAQ beschreiben unterschiedliche Standardwerte für öffentliche und private Ergebnisse.
  — <https://docs.neural.love/faq>
- Wiederholungsversuche begrenzen und HTTP 429 als normale Rate-Limit-Antwort behandeln, im Rahmen des dokumentierten Standards von 300 Anfragen pro fünf Minuten.
  — <https://docs.neural.love/>
- Vor einer neuen Produktionsabhängigkeit aktuelle Eigentumsverhältnisse, Support und Portabilität der Ausgaben prüfen, da der Eigentümer einen Verkauf von Assets und geistigem Eigentum angekündigt hat.
  — <https://neural.love/blog/neural-love-is-for-sale>

## Hierdurch abgelöst {#superseded-by-this}

- 2022-11-15 — Die frühere Route Train a Model als aktuelle, für Nutzer sichtbare Seite für das Training eigener Modelle zu behandeln, ist veraltet: Sie leitet nun auf AI Photo Studio weiter; das aktuelle Training eigener Modelle ist über die API dokumentiert.
- Vor 2026-03-12 — Planungen mit anhaltenden wesentlichen Investitionen des Anbieters sind veraltete Empfehlungen: Der Eigentümer gibt an, stattdessen einen Verkauf von Assets und geistigem Eigentum anzustreben.

## Weiterhin unbekannt {#still-unknown}

- Der vollständige Text zu den beiden Daten aus 2022 ist nicht verfügbar; keines der beiden Daten belegt daher einen Launch, eine Preisänderung oder eine Modellveröffentlichung.
- Die Links zu KI-Kunst und Train a Model aus 2022 könnten getrennte Produktabläufe innerhalb desselben Unternehmens beschreiben; die aktuelle Weiterleitung belegt nicht, was der frühere Trainings-Workflow war.
- Der Verkaufshinweis vom 12. März 2026 belegt nicht, ob ein Verkauf abgeschlossen wurde, wer den Dienst nun betreibt oder welche aktuellen Support- und Datenspeicherbedingungen gelten.
- Die offizielle Dokumentation widerspricht sich bei der API-Standardsichtbarkeit; die tatsächlich wirksame Datenschutzeinstellung muss daher über ein kontoweites, nicht sensibles Testergebnis überprüft werden.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://neural.love/blog/neural-love-is-for-sale | neural.love assets are for sale | neural.love-Blog über KI-Themen | 2026-09-04 |
| https://docs.neural.love/ | Getting Started | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/how-to-generate-ai-art-with-neural-love-api | How to generate AI art with neural.love API | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/reference/ai-custom-model-generate | Start training custom model | The neural.love API Developer Hub | 2026-09-04 |
| https://docs.neural.love/faq | neural.love API - Frequently Asked Questions | The neural.love API Developer Hub | 2026-09-04 |
| https://neural.love/ai-art-generator | AI Art Generator & AI Image Generator | neural.love | 2026-09-04 |
| https://neural.love/train-a-model | AI Photo Studio | Create Stunning AI Photos and Videos Instantly | neural.love | 2026-09-04 |
| https://neural.love/ai-photostudio | AI Photo Studio | Create Stunning AI Photos and Videos Instantly | neural.love | 2026-09-04 |

## Kurzbrief für Agenten {#agent-brief}

- **Gegenstand:** `organization:neural-love`, Thema `ai-creation-and-model-training`, 2 datierte Ereignisse 2022-08-17 → 2022-11-15.
- **Praktischer Hinweis:** Stand 2022-08-17 sollten Praktiker den AI Art Generator von neural.love als Teil der Produktlinie erkennen; Stand 2022-11-15 sollten sie bei der Bewertung der Erstellungsfähigkeiten der Organisation zusätzlich den Modelltraining-Workflow prüfen.
- **Konfidenz:** mittel. Maßgeblich dafür, was veraltet ist, sind die datierten Abschnitte „Hierdurch abgelöst“.
