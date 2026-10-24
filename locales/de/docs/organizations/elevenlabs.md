---
title: "ElevenLabs — Voice-Platform-Entwicklung"
category: organizations
tags: [elevenlabs, organization, voice-platform-development]
aliases: ["ElevenLabs"]
level: 3
source_sha256: dca8b2dc3ee4e62ab593892e4e576c7576f58276eb3c2fe2253534018169d0db
translation: machine
translated_at: '2026-10-24'
---
# ElevenLabs — Voice-Platform-Entwicklung {#elevenlabs-voice-platform-development}

**Entwicklungslinie:** `organization:elevenlabs` · Thread `voice-platform-development`  
**Ereignisse:** 1 datiert, 2025-11-12 → 2025-11-12 · **Recherchiert:** 2026-09-03 · Konfidenz: hoch

## Was es ist {#what-it-is}

ElevenLabs ist eine KI-Audioplattform für Produktteams und Kreative, die generierte Sprache, Transkription, Stimmklonen, Synchronisation (Dubbing) oder eine Sprachschicht für ein LLM benötigen. Funktionen: - Text-to-Speech, Speech-to-Text, Stimmklonen, Dubbing und Voice Agents. - Gehostete ElevenAgents oder Speech Engine, wenn ein Team das LLM und die Gesprächslogik auf dem eigenen Server betreibt. Einschränkung: Eleven v3 unterstützt mehr als 70 Sprachen, aber keine SSML-Break-Tags; generiertes Audio ist nicht deterministisch. Fazit: eine praktische Einzelplattform für Voice-Produktarbeit, sofern jede ausgewählte Stimme, Sprache und jeder Rechtepfad vor der Veröffentlichung getestet wird.

## Entwicklungslinie {#development-line}

- **2025-11-12 — ElevenLabs verknüpfte sein Iconic-Voices-Programm mit Partnerschaften für KI-Stimmen von Prominenten.** Am 2025-11-12 verbanden die datierten Links das Iconic-Voices-Angebot von ElevenLabs mit einem Bericht von Variety über KI-Stimmen-Partnerschaften, an denen Matthew McConaughey und Michael Caine beteiligt sind. Dies ist eine wesentliche Entwicklung, weil sie ein offizielles Programm für Promi-Stimmen innerhalb der Voice-Plattform von ElevenLabs dokumentiert.

## Was sich geändert hat {#what-changed}

2023-01-30 — In der Beta-Phase bot ElevenLabs Long-Form-Text-to-Speech, Stimmklonen, Stimmgestaltung und API-Zugang; KI-Dubbing wurde noch als künftige Version beschrieben. 2024-02-13 — Die Voice Library wurde von entworfenen synthetischen Stimmen auf verifizierte Professional Voice Clones erweitert, die geteilt werden konnten und Auszahlungen aus der Nutzung durch zahlende Abonnenten ermöglichten; dazu kamen Verifizierung, Prüfung, Auszahlung und Moderationskontrollen. 2024-02-19 — Keine Produktänderung wird zugeordnet: Die verlinkte Typeform-Seite lässt sich anhand ihres derzeit abrufbaren Inhalts nicht identifizieren. 2025-11-12 — Der Iconic Marketplace führte einen Anfrage- und Lizenzierungsweg für Unternehmen ein, die genehmigte Iconic Voices suchen; es handelt sich nicht um einen gewöhnlichen Self-Service-Klonpfad. Heute gefunden, 2026-09-04 — Die aktuelle Dokumentation beschreibt eine breitere Plattform: TTS, STT, geklonte oder gestaltete Stimmen, Dubbing und zwei Agent-Wege: gehostete ElevenAgents oder Speech Engine mit eigenem LLM (Bring-your-own-LLM).

## So wird es genutzt {#how-to-use-this}

Ab 2025-11-12 sollten Praktiker offiziell lizenzierte Stimmen aus dem Iconic-Voices-Programm von ElevenLabs von unlizenzierter Imitation prominenter Stimmen unterscheiden und die jeweils geltenden Rechte vor der Nutzung prüfen.

1. Für Narration öffnen Sie Text to Speech, geben das Skript ein oder fügen es ein, wählen eine Stimme, passen bei Bedarf Modell und Einstellungen an und erzeugen anschließend das Audio und laden es herunter.
  — <https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech>
2. Für Transkription senden Sie Audio an die Speech-to-Text-API und verwenden den zurückgegebenen Text, die Zeitstempel und die Sprecherinformationen, die das gewählte Scribe-Modell unterstützt.
  — <https://elevenlabs.io/docs/overview/capabilities/speech-to-text/>
3. Für einen Voice Agent wählen Sie gehostete ElevenAgents, wenn die Plattform LLM, Wissensdatenbank und Werkzeuge bereitstellen soll; wählen Sie Speech Engine, wenn Ihr Backend LLM und Gesprächsablauf verantwortet.
  — <https://elevenlabs.io/docs/overview/capabilities/speech-engine>
4. Für einen hochwertigen Klon Ihrer eigenen Stimme erstellen Sie einen Professional Voice Clone, laden saubere Aufnahmen hoch, schließen die Stimmverifizierung ab, warten auf das Feintuning und wählen die Stimme anschließend unter My Voices aus.
  — <https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning>
5. Um einen genehmigten Professional Voice Clone zu teilen und zu monetarisieren, aktivieren Sie das Teilen in der Voice Library, schließen die Stripe-Connect-Einrichtung ab und prüfen die Nutzung unter My Voices und Payouts.
  — <https://elevenlabs.io/docs/eleven-creative/voices/payouts>
6. Für eine Ikonen- oder nachlassverwaltete Stimme nutzen Sie den Iconic Marketplace und senden eine Request Voice; der Zugang ist ein Lizenzierungsantrag.
  — <https://elevenlabs.io/iconic-voices>

## Bewährte Praktiken {#best-practices}

- Wählen Sie die Stimme vor dem Feintuning der Einstellungen und passen Sie ihre Sprache, ihren Akzent und ihre Grundartikulation an das tatsächliche Skript an.
  — <https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech>
- Schreiben Sie Zahlen und mehrdeutige Symbole als Wörter aus und setzen Sie Satzzeichen gezielt ein, damit das Modell ein eindeutiges Skript erhält.
  — <https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech>
- Bei Eleven v3 passen Sie die Basisstimme an die beabsichtigte Vortragsweise an; für das Tempo verwenden Sie Audio-Tags, Satzzeichen und Textstruktur statt SSML-Break-Tags, und testen anschließend die gewählte Kombination aus Stimme und Tags.
  — <https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices>
- Behandeln Sie die Ausgabe als probabilistisch: Nutzen Sie Stability, um Ausdruckskraft gegen Wiederholbarkeit abzuwägen, und genehmigen Sie die tatsächlich erzeugte Aufnahme, statt identische Wiederholungen vorauszusetzen.
  — <https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech>
- Klonen Sie nur eine Stimme, für die Sie das Recht und die Einwilligung zur Nutzung besitzen. Für einen Professional Voice Clone verwenden Sie saubere Aufnahmen mit einem einzelnen Sprecher in der vorgesehenen Sprache und Vortragsweise; PVC ist auf die verifizierte eigene Stimme des Kontoinhabers beschränkt.
  — <https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning>

## Hiermit ersetzt {#superseded-by-this}

- 2023-01-30 — Die Empfehlung, ElevenLabs nur als Beta-Werkzeug für Long-Form-TTS und Narration zu behandeln, ist veraltet; die aktuelle Plattform dokumentiert zusätzlich STT, Dubbing, Stimmen und Agent-Workflows.
- 2024-02-13 — Die Empfehlung, die Voice Library nur als Katalog entworfener synthetischer Stimmen zu betrachten, ist veraltet; verifizierte Professional Voice Clones können inzwischen über den Auszahlungsweg geteilt und monetarisiert werden.
- 2025-11-12 — Die Empfehlung, eine berühmte oder nachlassverwaltete Stimme über gewöhnliches Self-Service-Klonen zu beschaffen, ist veraltet; der aktuelle Weg ist ein Lizenzierungsantrag über den Iconic Marketplace.
- 2026-09-04, heute gefunden — Die Empfehlung, SSML-Break-Tags für Pausen in Eleven v3 zu verwenden, ist veraltet; v3 nutzt stattdessen Audio-Tags, Satzzeichen und Textstruktur.

## Weiterhin unbekannt {#still-unknown}

- Die Typeform-URL vom 2024-02-19, https://form.typeform.com/to/gg0xzZW4, konnte nicht abgerufen oder unabhängig identifiziert werden; sie wird daher nicht als Nachweis einer Produktänderung verwendet.
- Preise, regionale Verfügbarkeit und die Genehmigung einer einzelnen Marketplace- oder Iconic-Voice-Anfrage hängen vom Konto, vom Tarif und der Prüfung durch den Rechteinhaber ab; sie wurden hier nicht verglichen.
- Dies ist Nachweis aus erster Hand zu Produkt und Workflow, kein unabhängiger Benchmark zu Ausgabequalität, Verfügbarkeit oder kommerzieller Eignung.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://elevenlabs.io/docs/overview | Dokumentation | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech | Text to Speech (Produktleitfaden) | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/overview/capabilities/speech-to-text/ | Transkription | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/overview/capabilities/speech-engine | Speech Engine | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning | Professional Voice Cloning | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/eleven-creative/voices/payouts | Payouts | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices | Best practices | ElevenLabs Documentation | 2026-09-04 |
| https://elevenlabs.io/blog/elevenlabs-raises-2m-pre-seed-and-announces-ai-speech-platform-promising-to-revolutionize-audio-storytelling | ElevenLabs Raises $2M and Announces AI Speech Platform | 2026-09-04 |
| https://elevenlabs.io/blog/introducing-voice-actor-payouts | Introducing Voice Actor Payouts | 2026-09-04 |
| https://elevenlabs.io/blog/announcing-partnership-with-sir-michael-caine-to-newly-launched-iconic-marketplace | Sir Michael Caine partners with ElevenLabs and joins new Iconic Marketplace | 2026-09-04 |
| https://elevenlabs.io/iconic-voices | ElevenLabs — License Legendary Voices - Iconic Marketplace | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `organization:elevenlabs`, Thread `voice-platform-development`, 1 datiertes Ereignis 2025-11-12 → 2025-11-12.
- **Praxishinweis:** Ab 2025-11-12 sollten Praktiker offiziell lizenzierte Stimmen aus dem Iconic-Voices-Programm von ElevenLabs von unlizenzierter Imitation prominenter Stimmen unterscheiden und die jeweils geltenden Rechte vor der Nutzung prüfen.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.

<!-- live-update:463d2c76338193a3159f2c71777af49ca92383d8f02ad28090db53d1eafdb2b7 -->
## 2026-10-17 — ElevenLabs ergänzt Instant Soundtracks für hochgeladene Videos {#2026-10-17-elevenlabs-adds-instant-soundtracks-for-uploaded-video}

Instant Soundtracks erstellt aus hochgeladenen Videos eine Vertonung und zeitgestempelte Soundeffekte. Die Effekte bleiben als bearbeitbare Ebenen erhalten, und über die API können Musik und Soundeffekte als getrennte Dateien zurückgegeben werden.

### Nutzung und Praktiken {#usage-and-practices}

- Öffnen Sie den ElevenCreative Music Video Editor, laden Sie ein Video hoch und erzeugen Sie einen Soundtrack mit Soundeffekten. Die vorhandene Tonspur des Videos kann als Referenz für die Vertonung dienen. [Quelle](https://elevenlabs.io/blog/introducing-instant-soundtracks)
- Prüfen Sie die Soundeffekte auf separaten Timeline-Ebenen. Passen Sie das Timing an oder ersetzen Sie die Musik und exportieren Sie anschließend das Ergebnis. [Quelle](https://elevenlabs.io/blog/introducing-instant-soundtracks)
- Für Musik außerhalb des Video-Workflows beschreiben Sie Genre, Stimmung, Instrumentierung, Struktur und Verwendungszweck in einem Prompt in natürlicher Sprache. Anschließend bearbeiten Sie einzelne Abschnitte oder generieren sie neu. [Quelle](https://elevenlabs.io/docs/eleven-creative/products/music)
- Kombinieren Sie Genre, Stimmung, Instrumentierung, Tempo und Verwendungszweck in einem detaillierten Prompt, statt eine grobe Genrebezeichnung zu verwenden. [Quelle](https://elevenlabs.io/docs/eleven-creative/products/music)
- Bei längeren Kompositionen erzeugen und genehmigen Sie zuerst das Intro. Bauen Sie die nächsten Abschnitte nacheinander auf und verfeinern Sie die Prompts, statt den gesamten Track neu zu starten. [Quelle](https://elevenlabs.io/docs/eleven-creative/products/music)
- Nutzen Sie separate Soundeffekt-Ebenen, um das Timing der Einsätze zu prüfen und einzelne Momente vor dem Export zu überarbeiten. [Quelle](https://elevenlabs.io/blog/introducing-instant-soundtracks)

### Zusätzliche Belege {#additional-evidence}

- 2026-10-17: Die Veröffentlichung dokumentiert die API-Steuerungen add\_sfx, separate\_tracks und use\_audio\_as\_reference. Mit separate\_tracks=true liefert die API ein ZIP mit getrennten Musik- und Soundeffektdateien. Anfragen unterstützen bis zu 10 Videos mit insgesamt 200 MB und 10 Minuten. [Quelle](https://elevenlabs.io/blog/introducing-instant-soundtracks)

### Grenzen und offene Fragen {#limits-and-open-questions}

- Das geprüfte öffentliche Material nennt keine Mindeststufe des Abonnements für den vollständigen Instant-Soundtracks-Workflow.
- Die öffentliche Veröffentlichung nennt kein eigenes Modell für Instant Soundtracks.
- In den geprüften Ergebnissen wurde keine qualifizierte unabhängige Diskussion von Praktikern speziell zu Instant Soundtracks gefunden.

<!-- Retained base: fa3cccdfbdd5ddca7a3b01f3b752c0fa59966afe; article blob: fe6aa94482f605160178e07ded1bc76ca5ad03de -->

<!-- live-update:c8ce4024a7948cdb529aa05d26690a24bbae6d3aad2f4a65d8d0503d6ce199ef -->
## 2026-10-22 — ElevenLabs Chimera in ElevenCreative {#2026-10-22-elevenlabs-chimera-in-elevencreative}

ElevenLabs hat Chimera vorgestellt, ein Charaktersystem innerhalb von ElevenCreative. Es kombiniert die emotionale Sprachsynthese Eleven v4 mit dem Videogenerierungsmodell Seedance 2.5. Aus einem Textskript, Emotions-Tags und einem Referenzbild entsteht ein sprechender Charakter, bei dem Sprache und Gesicht synchron sind.

### Nutzung und Praktiken {#usage-and-practices_1}

- Öffnen Sie ElevenCreative und wählen Sie das Studio zur Charaktererzeugung. [Quelle](https://elevenlabs.io/creative)
- Laden Sie ein Referenzbild des Charakters hoch oder erzeugen Sie eines aus einem Textprompt. [Quelle](https://elevenlabs.io/creative)
- Wählen Sie eine Eleven-v4-Stimme oder weisen Sie ein geklontes Stimmprofil zu. [Quelle](https://elevenlabs.io/creative)
- Tippen Sie den Dialog im Skripteditor ein. Fügen Sie in eckigen Klammern Emotions-Tags wie \[whispers\] oder \[laughs\] hinzu, um Stimme und Gesichtsausdruck zu steuern. [Quelle](https://elevenlabs.io/creative)
- Rendern Sie den Generierungsdurchlauf, um das lippensynchrone Video zu exportieren. [Quelle](https://elevenlabs.io/creative)
- Setzen Sie jeden Emotions-Tag direkt vor den Satz oder das Wort, auf das er sich bezieht, damit Sprachmodell und Videomodell den Ausdruck auf die Tonlage abstimmen. [Quelle](https://elevenlabs.io/creative)
- Verwenden Sie ein hochauflösendes, frontal ausgerichtetes Porträt mit klaren Gesichtszügen, damit die Lippensynchronisation bei emotional komplexen Passagen nicht verzerrt. [Quelle](https://elevenlabs.io/creative)
- Halten Sie jedes Dialogsegment kurz, damit das Gesicht konsistent bleibt und bei langen Renderings nicht abdriftet. [Quelle](https://elevenlabs.io/creative)

### Zusätzliche Belege {#additional-evidence_1}

- 2026-10-22: Chimera kombiniert innerhalb von ElevenCreative die Video-Architektur Seedance 2.5 von ByteDance mit der Sprachsynthese Eleven v4. Ziel ist laut Angabe, die Verzögerung beim Synchronisieren (Dubbing) zu beseitigen und die Gesichtsbewegung aus der Emotion abzuleiten, und zwar in mehr als neunzig Sprachen. [Quelle](https://elevenlabs.io/creative)

### Bisheriger Ablauf (zur Dokumentation beibehalten) {#superseded-guidance-retained-for-history}

- 2026-10-22: Der bisherige Workflow teilte die Aufgabe in zwei Schritte: Zuerst wurde das Voiceover synthetisiert, danach mit einem separaten Nachbearbeitungswerkzeug lippensynchron gemacht. [Quelle](https://elevenlabs.io/creative)

### Grenzen und offene Fragen {#limits-and-open-questions_1}

- „Voice Platform Development“ ist eine allgemeine Kategorie und kein Produktname. Dieser Eintrag behandelt nur ElevenLabs Chimera innerhalb von ElevenCreative.
- Drittanbieter-Benchmarks und Diskussionen in der Community auf Reddit, YouTube und Medium wurden gefunden, jedoch ohne überprüfbare direkte Seitenlinks, weshalb hier nichts davon zitiert wird.
- Kosten pro Rendering in Credits, Batch-API-Endpunkte und Obergrenzen der Exportauflösung für Chimera werden auf der Hauptseite von ElevenCreative nicht angegeben.

<!-- Retained base: dfb3de9ab54eb4b0ebd0dce739bcda6b6bd59c78; article blob: 52948543a1ace86d5aefeb5f2fb50994000b8d6c -->
