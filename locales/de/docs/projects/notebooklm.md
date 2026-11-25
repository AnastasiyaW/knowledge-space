---
title: "NotebookLM"
category: projects
date: 2025-07-30
tags: [google_io_2024, notebooklm, notebooklm-development, project]
aliases: ["NotebookLM"]
level: 3
source_sha256: fa74b0873bf3b40203099e8f73ed2a87996fb9737d856701a9fdeb9ada171904
translation: machine
translated_at: '2026-10-24'
---
# NotebookLM {#notebooklm}

**Entwicklungslinie:** `project:notebooklm` · Thread `notebooklm-development`  
**Letztes Ereignis:** 2025-07-30 · 1 datiertes Ereignis seit 2025-07-30 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

NotebookLM, inzwischen Gemini Notebook genannt, ist Googles Arbeitsumgebung für Studierende, Analysten und Teams, die ausschließlich mit ausgewählten Dokumenten arbeiten.

- Chat: Antworten auf Basis ausgewählter Quellen mit Inline-Zitaten.
- Studio: erstellt Berichte, Datentabellen, Lernkarteien, Quizze, Mindmaps, Audio-/Video-Übersichten, Infografiken und Foliensätze.
- Limits: 50 Quellen pro kostenlosem Notebook, jeweils bis zu 500.000 Wörter oder 200 MB, mit rechenbasierter Nutzung, die je nach Tarif variiert.

## Entwicklungslinie {#development-line}

- **2025-07-30 — NotebookLM führte Video-Übersichten und Studio-Verbesserungen ein.** Google aktualisierte NotebookLM am 2025-07-30 mit Video-Übersichten und Studio-Verbesserungen, wodurch Notebook-Ausgaben nicht mehr auf ein Artefakt pro Typ beschränkt sind.

## Was sich geändert hat {#what-changed}

- 2023-07-12 — NotebookLM startete aus Project Tailwind als kleiner Rollout bei Google Labs in den USA, um Fragen anhand ausgewählter Dokumente mit Zitaten zu beantworten.
- 2024-05-14 — Auf der I/O wurden Audio-Übersichten vorgestellt, die Gemini nutzen, um hochgeladene Quellen in eine interaktive verbale Diskussion zu verwandeln.
- 2025-05-19 — iOS- und Android-Apps erhielten Audio-Übersichten für den Offline-Betrieb, Interaktion mit dem Host und Quellenerfassung über das Teilen-Menü.
- 2025-07-30 — Video-Übersichten und ein überarbeitetes Studio ermöglichten es, mehrere Ausgaben statt eines Artefakts pro Typ zu speichern.
- 2025-08-25 — Video-Übersichten wurden auf über 80 Sprachen erweitert, mit längeren Audio-Übersichten in diesen Sprachen.
- 2026-03-04 — Cinematic Video Overviews kamen als englischsprachiges Format für Nutzer von Google AI Ultra ab 18 Jahren hinzu, gebaut mit Gemini 3, Nano Banana Pro und Veo 3.
- 2026-04-08 — Notebooks wurden zwischen Gemini und NotebookLM synchronisiert, wodurch Projektstruktur und Chat-Kontext über beide Apps hinweg verknüpft werden.
- 2026-07-03 — Short Video Overviews wurden als etwa 60-sekündige vertikale Quellenerklärungen angekündigt, wobei die zugrunde liegende Ankündigung auf 2026-06-30 datiert ist.
- 2026-07-16 — Das Produkt wurde in Gemini Notebook umbenannt, erhielt für berechtigte Tarife einen sicheren Cloud-Computer für die native Ausführung von Code und erweiterte seine Rolle im Google-Ökosystem.
- 2026-09-02 — Die Nutzung wurde auf rechenbasierte Limits umgestellt, die Komplexität von Prompts und Funktionen, Modell, Chat-Länge und Kontingent berücksichtigen.

## So wird es eingesetzt {#how-to-use-this}

Ab 2025-07-30 sollten Praktiker bei der Auswahl von NotebookLM-Ausgaben und Arbeitsabläufen im Workspace Video-Übersichten und Studio in Betracht ziehen, abhängig von der Verfügbarkeit in ihrem Konto.

1. Öffnen Sie notebook.google.com, legen Sie pro Projekt ein Notebook an und fügen Sie das Quellenset hinzu, das die Antworten bestimmt.
  — <https://support.google.com/gemininotebook/answer/16206563>
2. Importieren Sie nur Material, das Sie verwenden dürfen: unterstützte Dateien, Google-Inhalte, Web-URLs, öffentlich untertitelte YouTube-Videos oder ausgewählte Gemini-Chats.
  — <https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-GB>
3. Wählen Sie im Chat die relevanten Quellen aus, stellen Sie eine konkrete Frage und öffnen Sie jedes Inline-Zitat, um die zitierte Textstelle im Kontext zu lesen.
  — <https://support.google.com/gemininotebook/answer/16179559?hl=en&ref_topic=16164070>
4. Erstellen Sie im Studio aus dem Quellenset einen Bericht oder eine Datentabelle und exportieren Sie sie bei Bedarf nach Docs oder Sheets.
  — <https://support.google.com/gemininotebook/answer/16206563>
5. Für die visuelle Prüfung erstellen Sie eine Video-Übersicht und legen Format, Sprache und Steuerungs-Prompt vor der Generierung fest.
  — <https://support.google.com/gemininotebook/answer/16454555?hl=en&ref_topic=16164070>
6. Wenn Sie auch in Gemini arbeiten, nutzen Sie dessen appübergreifende Notebook-Ansicht für die Kontinuität, behalten Sie streng quellengestützte Schlussfolgerungen aber in Gemini Notebook.
  — <https://support.google.com/gemininotebook/answer/17003757?hl=en&ref_topic=16164070>

## Bewährte Vorgehensweisen {#best-practices}

- Behalten Sie pro Notebook ein klar abgegrenztes Projekt bei: Notebooks sind voneinander unabhängig und können nicht auf die Informationen des jeweils anderen zugreifen.
  — <https://support.google.com/gemininotebook/answer/16206563>
- Wählen Sie relevante Quellen aus und stellen Sie eng gefasste Fragen; prüfen Sie die zitierten Textstellen im Kontext, statt glatten Antworten blind zu vertrauen.
  — <https://support.google.com/gemininotebook/answer/16179559?hl=en&ref_topic=16164070>
- Behandeln Sie generierte Videos als Lernhilfe, nicht als endgültigen Beleg: Stimmen und Bilder können Fehler aufweisen oder Fakten falsch wiedergeben.
  — <https://support.google.com/gemininotebook/answer/16454555?hl=en&ref_topic=16164070>
- Betrachten Sie die Freigabe als Zugriff auf Quelldaten: Betrachter können geteilte Quellen lesen, und die Chat-Ansicht entzieht diesen Zugriff nicht vollständig.
  — <https://support.google.com/gemininotebook/answer/16206563>
- Halten Sie die Fundierung von Gemini und Gemini Notebook getrennt: Gemini Notebook stützt sich streng auf Quellen, während Gemini auf Suche und Werkzeuge zugreifen kann.
  — <https://support.google.com/gemininotebook/answer/17003757?hl=en&ref_topic=16164070>
- Planen Sie mit schwankenden, rechenbasierten Kontingenten: Aktuelle Limits können alle fünf Stunden erneuert werden, bis das Wochenlimit erreicht ist.
  — <https://support.google.com/gemininotebook/answer/17670842?hl=en&ref_topic=16164070>
- Lassen Sie Video-Übersichten asynchron laufen und später abholen: Die Generierung kann mehr als 30 Minuten dauern.
  — <https://support.google.com/gemininotebook/answer/16454555?hl=en&ref_topic=16164070>

## Hierdurch abgelöst {#superseded-by-this}

- 2025-07-29 — Der Studio-Workflow mit einer Ausgabe pro Typ.
- 2025-08-25 — Video-Übersichten nur auf Englisch.
- 2026-07-16 — NotebookLM als aktueller offizieller Produktname.
- 2026-09-02 — Feste numerische Kontingenttabellen als stabile Grundlage für die Nutzungsplanung.

## Weiterhin unbekannt {#still-unknown}

- Eine verlinkte Statusseite vom 2026-07-03 konnte nicht abgerufen werden. Ihre Status-ID kodiert einen Zeitstempel vom 2026-06-30, doch die Zuordnung aus Sekundärquellen bestätigt den Originalwortlaut nicht.
- Für die Angaben von 2024 zu Modellversion, Länderanzahl oder Erhöhung des Quellenlimits wurde keine datierte Erstveröffentlichung von NotebookLM gefunden.
- Die genaue Verfügbarkeit variiert je nach Konto, Abonnement, Region und Alter; Google weist darauf hin, dass sich Funktionszugang und Limits ändern können.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://blog.google/innovation-and-ai/technology/ai/notebooklm-google-ai/ | NotebookLM vorgestellt | 2026-09-04 |
| https://blog.google/intl/en-africa/products/explore-get-answers/google-io-2024-an-io-for-a-new-generation/ | Google I/O 2024: Eine I/O für eine neue Generation | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/google-io-2024-100-announcements/ | 100 Neuerungen, die wir auf der I/O 2024 angekündigt haben | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/notebooklm-app/ | Mit der neuen NotebookLM-App alles überall verstehen | 2026-09-04 |
| https://blog.google/technology/google-labs/notebooklm-video-overviews-studio-upgrades/ | Neues in NotebookLM: Video-Übersichten und ein überarbeitetes Studio | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-labs/notebook-lm-audio-video-overviews-more-languages-longer-content/ | NotebookLMs Video-Übersichten sind jetzt in 80 Sprachen verfügbar | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/notebooklm/generate-your-own-cinematic-video-overviews-in-notebooklm/ | Eigene Cinematic Video Overviews in NotebookLM erstellen. | 2026-09-04 |
| https://blog.google/intl/en-ie/products/notebooks-gemini-notebooklm/ | Notebooks in Gemini ausprobieren, um Projekte leicht im Blick zu behalten | 2026-09-04 |
| https://9to5google.com/2026/06/30/notebooklm-short-video-overviews/ | NotebookLM ergänzt Short Video Overviews mit Nano Banana 2 Lite | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/ | Mit Nano Banana 2 Lite und Gemini Omni Flash loslegen | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/ | NotebookLM heißt jetzt Gemini Notebook | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16164461?hl=en | Informationen zu Gemini Notebook | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16206563 | Ein Notebook in Gemini Notebook erstellen | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-GB | Quellen zu Ihrem Notebook hinzufügen oder neue entdecken | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16179559?hl=en&ref_topic=16164070 | Chat in Gemini Notebook verwenden | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/16454555?hl=en&ref_topic=16164070 | Video-Übersichten in Gemini Notebook generieren | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/17670842?hl=en&ref_topic=16164070 | Nutzungslimits von Gemini Notebook verwalten | 2026-09-04 |
| https://support.google.com/gemininotebook/answer/17003757?hl=en&ref_topic=16164070 | Notebooks in Gemini-Apps | 2026-09-04 |
| https://notebooklm.google/ | Gemini Notebook | AI Research Tool & Thinking Partner | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:notebooklm`, Thread `notebooklm-development`, 1 datiertes Ereignis vom 2025-07-30 bis 2025-07-30.
- **Praxishinweis:** Ab 2025-07-30 sollten Praktiker bei der Auswahl von NotebookLM-Ausgaben und Workspace-Arbeitsabläufen Video-Übersichten und Studio in Betracht ziehen, abhängig von der Verfügbarkeit in ihrem Konto.
- **Konfidenz:** mittel. Die datierten „Hierdurch abgelöst“-Einträge sind maßgeblich dafür, was veraltet ist.
