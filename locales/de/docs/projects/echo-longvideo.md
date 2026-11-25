---
title: "Echo LongVideo"
category: projects
date: 2026-06-05
tags: [echo-longvideo, echo-longvideo-public-release, echo_longvideo, project]
aliases: ["Echo LongVideo"]
level: 2
source_sha256: 013b181b2644d3b426639d2f815de4a669c6c527e3a7c82c4eada7a54e81a871
translation: machine
translated_at: '2026-10-24'
---
# Echo LongVideo {#echo-longvideo}

**Entwicklungslinie:** `project:echo-longvideo` · Thread `echo-longvideo-public-release`  
**Letztes Ereignis:** 2026-06-05 · 1 datiertes Ereignis seit 2026-06-05 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Echo LongVideo ist das Long-Video-Teilprojekt von JoyAI-Echo 1.5 für Multi-Shot-Audio und -Video mit Übertragung von Identität, Stimme und Szene über bearbeitbare Shots hinweg.
- R2V mit Text, optionalem ersten Frame und bis zu 7 geordneten Audio-Video-Speicherplätzen.
- Gemeinsame Audio- und Videogenerierung, Inferenz in BF16/FP8/FP4 sowie ein lokaler Director Agent.
FP4-Gewichte benötigen 22,81 GB; das 24-GiB-Profil erfordert vorberechnete Konditionierung.
Dies ist ein lokaler Inferenz-Stack zum Testen, kein etablierter Produktionsdienst.

## Entwicklungslinie {#development-line}

- **2026-06-05 — Öffentliche Projektressourcen von Echo LongVideo wurden verlinkt.** Am 2026-06-05 wurde Echo LongVideo über eine öffentliche Projektseite, ein GitHub-Repository und eine Hugging-Face-Modellseite referenziert. Dieser datierte Ressourcensatz benennt die Orte der öffentlichen Dokumentation, des Quellcodes und der Modellverteilung; die Belege belegen nicht die konkreten Inhalte des Releases.

## Was sich geändert hat {#what-changed}

2026-06-05 — Hugging Face erhielt ein README-Update; die Projektseite beschrieb einen technischen Bericht, der kohärente 5-Minuten-Geschichten, A/V-Speicher und eine 7,5-fache Beschleunigung beansprucht, während Code und Gewichte als künftige Open-Source-Veröffentlichung dargestellt wurden. 2026-06-22 — Das Root-README datiert das Release von JoyAI-Echo 1.0 und führt es im Branch `echo1.0`; die ursprüngliche Pipeline war T2V/Multi-Shot ohne I2V. 2026-08-24 — arXiv v1 stellte JoyAI-Echo 1.5 vor; die Long-Video-Variante ergänzte komponierbaren Cross-Shot-A/V-Speicher, um Text-, Bild- und Speicherkonditionierung zu kombinieren. 2026-08-27 — Ein Git-Commit veröffentlichte das Long-Video-Release von JoyAI-Echo 1.5. 2026-08-28 — Die Dokumentation kündigte JoyAI-Echo 1.5 / Echo-LongVideo an: Code, Gewichte, R2V-Inferenz, Profile für Consumer-GPUs und Director Agent. 2026-08-31 — Die Dokumentation aktualisierte die beanspruchte Videolänge auf 10+ Minuten; dies ist eine Aktualisierung der Behauptung, kein eigenständiger Nachweis eines neuen Checkpoints oder Benchmarks.

## So wird es verwendet {#how-to-use-this}

Stand 2026-06-05 sollten Praktiker bei der Bewertung oder beim Einsatz von Echo LongVideo die verlinkte Projektseite, das Quell-Repository und die Hugging-Face-Seite des Projekts heranziehen, statt sich auf eine ungeprüfte Sekundärbeschreibung zu verlassen.

1. Prüfen Sie die [LTX-2 Community License](https://github.com/jd-opensource/JoyAI-Echo/blob/main/LICENSE) vor dem Herunterladen oder Deployen: Organisationen mit einem Jahresumsatz ab 10 Mio. US$ benötigen eine separate kommerzielle Lizenz; Lizenzbeschränkungen müssen bei einer Weitergabe beibehalten werden.
2. Klonen Sie das Repository und arbeiten Sie ausschließlich innerhalb von `echo_longvideo`; die Referenzumgebung ist Python 3.11, PyTorch 2.8, CUDA 12.8, `ffmpeg` im PATH sowie `scripts/setup_msst.py`, wie im [README](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md) beschrieben.
3. Laden Sie genau einen 1.5-Checkpoint herunter — BF16, FP8 oder FP4 — zusammen mit `gemma-3-12b`; passen Sie ihn an dieselbe Inferenzkonfiguration an und prüfen Sie das Manifest und `SHA256SUMS` auf [Hugging Face](https://huggingface.co/jdopensource/JoyAI-Echo).
4. Erstellen Sie die R2V-Anfrage mit einem Textprompt, einem optionalen ersten Frame und bis zu sieben geordneten Bild-/Audio-Speicherplätzen; führen Sie `inference.py` mit der passenden YAML-Konfiguration aus dem [Leitfaden](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md) aus.
5. Verwenden Sie für eine Ziel-GPU mit 24 GiB das FP4-Profil für Consumer-Hardware und berechnen Sie die Konditionierung vorab; der tatsächliche Spielraum hängt von GPU, Treiber und Anfrageform ab, wie im [Leitfaden](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md) dokumentiert.

## Best Practices {#best-practices}

- Mischen Sie keine Umgebungen, Checkpoint-Verzeichnisse oder Entrypoints von Echo LongVideo mit Echo-WM: Upstream behandelt sie als getrennte Projekte auf [GitHub](https://github.com/jd-opensource/JoyAI-Echo).
- Prüfen Sie `checkpoint.json` im Gewichtsverzeichnis und die Root-Datei `SHA256SUMS` vor dem ersten Inferenzlauf auf [Hugging Face](https://huggingface.co/jdopensource/JoyAI-Echo).
- Fixieren Sie den vollständigen Commit-SHA für reproduzierbare Installationen: GitHub stellt unter [releases](https://github.com/jd-opensource/JoyAI-Echo/releases) kein veröffentlichtes Release-Artefakt bereit.
- Beginnen Sie mit dem mitgelieferten Satz `examples/the_last_visa/requests/`, den die Standardkonfiguration verarbeitet, bevor Sie eigene R2V-Anfragen einsetzen, gemäß dem [README](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).

## Durch diese Angaben überholt {#superseded-by-this}

- 2026-08-28 — Der Zustand „Code und Gewichte werden später veröffentlicht“ ist veraltet: Die Dokumentation zu 1.5 kündigt Code, Gewichte und R2V-Inferenz als veröffentlicht an.
- 2026-08-28 — Für Neuinstallationen ist die Anweisung aus 1.0 „nur T2V, I2V nicht unterstützt“ veraltet: 1.5 nutzt R2V mit optionalem ersten Frame, und 1.0 bleibt im Archiv-Branch `echo1.0` erhalten.

## Weiterhin unbekannt {#still-unknown}

- Das formale Veröffentlichungsdatum von 1.0 ist uneindeutig: Die Hugging-Face-Historie zeigt einen initialen Commit, eine Lizenz und Uploads am 2026-06-02 sowie ein README-Update am 2026-06-05, während das Root-README das Release auf den 2026-06-22 datiert.
- Es gibt kein versioniertes GitHub-Release; der Release-Commit für 1.5 ist auf den 2026-08-27 datiert, die Ankündigung im README auf den 2026-08-28.
- Keine Primärbelege zeigen einen erfolgreichen lokalen End-to-End-Lauf, einen universell gültigen minimalen VRAM-/RAM-Bedarf, tatsächliche Geschwindigkeit oder Ausgabequalität; 24 GiB ist ein angestrebtes Consumer-Profil, keine Garantie.
- Die Lizenzbedingungen erfordern manuelle Prüfung: Das README nennt akademische, Forschungs- und nicht-kommerzielle Nutzung, während die beigelegte LTX-2 Community License eingeschränkte Nutzung erlaubt und für kommerzielle Einheiten mit einem Umsatz ab 10 Mio. US$ eine kostenpflichtige Lizenz verlangt.
- Das Repository enthält auch Echo-WM, doch der Upstream isoliert es als eigenständiges Projekt mit abweichender Umgebung und eigenem Checkpoint-Baum; Echo-WM-Ereignisse sind aus dieser Linie ausgeschlossen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://echo-team-joy-future-academy-jd.github.io/Echo-LongVideo-Page/ | JoyAI-Echo: Die Grenzen langer audiovisueller Generierung verschieben | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Echo/commits/main | Commits · jdopensource/JoyAI-Echo | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo | JoyAI-Echo-Repository und datierte Neuigkeiten | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md | JoyAI-Echo/echo_longvideo/README.md at main · jd-opensource/JoyAI-Echo | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Echo | jdopensource/JoyAI-Echo · Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2608.23383 | Long-Horizon Audio-Visual Generation for Persistent Stories and Interactive Worlds | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/commits/main/ | Commits · jd-opensource/JoyAI-Echo · GitHub | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/tree/echo1.0 | GitHub - jd-opensource/JoyAI-Echo at echo1.0 | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/blob/main/LICENSE | LTX-2 Community License Agreement | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/releases | Releases · jd-opensource/JoyAI-Echo | 2026-09-05 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:echo-longvideo`, Thread `echo-longvideo-public-release`, 1 datiertes Ereignis 2026-06-05 → 2026-06-05.
- **Praktischer Hinweis:** Stand 2026-06-05 sollten Praktiker bei der Bewertung oder beim Einsatz von Echo LongVideo die verlinkte Projektseite, das Quell-Repository und die Hugging-Face-Seite des Projekts heranziehen, statt sich auf eine ungeprüfte Sekundärbeschreibung zu verlassen.
- **Konfidenz:** mittel. Die datierten Überholungsangaben sind maßgeblich dafür, was veraltet ist.
