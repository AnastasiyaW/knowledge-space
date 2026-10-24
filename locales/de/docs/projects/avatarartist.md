---
title: "AvatarArtist"
category: projects
date: 2025-04-09
tags: [avatarartist, avatarartist-public-release-and-space, project]
aliases: ["AvatarArtist"]
level: 3
source_sha256: 55308cb8fe0e13d176ff3f046768ba2c552f55e61e8c8e9610bb81205d394c8f
translation: machine
translated_at: '2026-10-24'
---
# AvatarArtist {#avatarartist}

**Entwicklungslinie:** `project:avatarartist` · Thread `avatarartist-public-release-and-space`  
**Letztes Ereignis:** 2025-04-09 · 2 datierte seit 2025-03-27 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

AvatarArtist ist eine Pipeline für offene Domänen, die ein Porträt in einen 4D-Avatar umwandelt. Sie richtet sich an Kreative und Forschende, die bewegungsgesteuerte Ergebnisse benötigen.

- Porträtkonvertierung: wandelt ein Porträt in eine parametrische 4D-Repräsentation um
- Frame-Rendering: rendert Zielframes aus dem Referenzbild und den Steuersignalen
- Pipeline-Zugang: umfasst veröffentlichte Inferenz- und Eingabeverarbeitungspfade

## Entwicklungslinie {#development-line}

- **2025-03-27 — AvatarArtist veröffentlichte seine öffentliche Projektseite und das offizielle Repository.** Damit wurde der lokale Workflow aus Code und Gewichten etabliert.
- **2025-04-09 — AvatarArtist verlinkte auf einen Hugging-Face-Space.** Kein geprüfter Erstanbieter-Release-Hinweis belegt an diesem Datum eine Modellrevision.

## Was sich geändert hat {#what-changed}

AvatarArtist ging von einem lokalen Inferenz-Release zu lokalen und Online-Demos über. Ein Trainings-Release ist bislang nicht dokumentiert.

- 2025-03-26: Das offizielle Repository kündigte Inferenzcode und vortrainierte Modelle an.
- 2025-03-27: Die öffentliche Projektseite und das offizielle Repository etablierten den lokalen Workflow aus Code und Gewichten.
- 2025-03-30: Das offizielle Repository listete ein Gradio-Demo-Release auf.
- 2025-04-02: Das offizielle Repository listete ein Online-Demo-Release auf.
- 2025-04-09: Der Hugging-Face-Space erschien; kein geprüfter Erstanbieter-Release-Hinweis belegt an diesem Datum eine Modellrevision.
- 2026-09-04: Die frühere GitHub-URL von ant-research leitet nun auf robbyant-research weiter; das Repository führt Trainingscode weiterhin als ausstehend auf.

## So wird es verwendet {#how-to-use-this}

Stand 2025-04-09: Zuerst die Projektseite und das Repository von AvatarArtist konsultieren und anschließend den verlinkten Hugging-Face-Space für eine gehostete Auswertung testen.

1. Mit einer Porträt-Referenz und einer Quelle für Bewegungssteuerung beginnen; AvatarArtist erzeugt aus dem Porträt eine 4D-Repräsentation und rendert Frames unter den Steuersignalen.
  — <https://kumapowerliu.github.io/AvatarArtist/>
2. Das Repository klonen, die dokumentierte Conda-Umgebung mit Python 3.9 anlegen und die Abhängigkeiten installieren.
  — <https://github.com/robbyant-research/AvatarArtist>
3. Die Gewichte von KumaPower/AvatarArtist in `pretrained_model` herunterladen; `faceverse_v3_1.npy` separat beschaffen und in beide dokumentierten FaceVerse-Pfade kopieren.
  — <https://github.com/robbyant-research/AvatarArtist>
4. Zuerst `python3 app.py` mit den Demodaten ausführen; für kontrollierte Ergebnisse `inference.py` mit Bild, FaceVerse-Koeffizienten, Bewegungseingaben, Ausgabepfad und optional `--select_img` starten.
  — <https://github.com/robbyant-research/AvatarArtist>
5. Für eigene Medien den offiziellen Vorverarbeitungspfad verwenden, sodass das finale `dataset` vor der Inferenz die erforderlichen Ordner für Bild, Koeffizienten, Bewegung und Renderings enthält.
  — <https://github.com/robbyant-research/AvatarArtist>
6. Den Browser-Space nur für einen schnellen manuellen Test nutzen; der zugängliche Snapshot der Seite war als Sleeping markiert und damit kein aktiver Endpunkt.
  — <https://huggingface.co/spaces/KumaPower/AvatarArtist>

## Bewährte Vorgehensweisen {#best-practices}

- Mit den mitgelieferten Demodaten und dem dokumentierten Vorverarbeitungslayout beginnen; nur das finale Verzeichnis `dataset` ist Modelleingabe, die übrigen Ordner sind Zwischenstände.
  — <https://github.com/robbyant-research/AvatarArtist>
- `faceverse_v3_1.npy` als erforderliche Einrichtung behandeln, nicht als optionalen Zusatz: Gewichte allein machen das Projekt nicht lauffähig.
  — <https://github.com/robbyant-research/AvatarArtist>
- Die Arbeit auf veröffentlichte Inferenz und Datenverarbeitung beschränken; die offizielle To-do-Liste führt die Veröffentlichung des Trainingscodes weiterhin als ausstehend.
  — <https://github.com/robbyant-research/AvatarArtist>
- Für neue Setup-Links das umgeleitete Repository robbyant-research verwenden; die ant-research-URL nur für historische Verweise beibehalten.
  — <https://github.com/ant-research/AvatarArtist>
- Die Model Card nicht als gehostete Inferenz verstehen: Sie listet kein Deployment über einen Hugging Face Inference Provider.
  — <https://huggingface.co/KumaPower/AvatarArtist>
- Den Space als optionale Exploration behandeln und nicht als Abhängigkeit für den Produktivbetrieb, da der zugängliche Snapshot ihn als Sleeping zeigte.
  — <https://huggingface.co/spaces/KumaPower/AvatarArtist>

## Hiermit überholt {#superseded-by-this}

- 2025-03-27: Die Verwendung von `https://github.com/ant-research/AvatarArtist` als kanonische Owner-URL ist durch die beobachtete Weiterleitung auf `https://github.com/robbyant-research/AvatarArtist` am 2026-09-04 überholt.

## Noch unbekannt {#still-unknown}

- Der datierte Ereignistext zum 2025-04-09 ist nicht verfügbar; daher lässt er sich über den verlinkten Space hinaus nicht mit der Online-Demo verknüpfen.
- Während der Prüfung haben wir den Space nicht durchgehend getestet; aktueller Zustand, Kaltstartverhalten und Latenz sind daher nicht verifiziert.
- Erstanbieter-Quellen nennen keine belegte Matrix zu GPU, VRAM, CUDA oder Betriebssystemen.
- Wir haben keine Erfahrungsberichte aus der Community gefunden; diese Vorgehensweisen stammen aus offiziellen Anforderungen und dem Verbreitungsstand.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://kumapowerliu.github.io/AvatarArtist/ | AvatarArtist: Open-Domain 4D Avatarization | 2026-09-04 |
| https://github.com/ant-research/AvatarArtist | AvatarArtist official PyTorch implementation; redirects to robbyant-research | 2026-09-04 |
| https://github.com/robbyant-research/AvatarArtist | AvatarArtist official PyTorch implementation | 2026-09-04 |
| https://huggingface.co/KumaPower/AvatarArtist | KumaPower/AvatarArtist model card | 2026-09-04 |
| https://huggingface.co/spaces/KumaPower/AvatarArtist | KumaPower/AvatarArtist Hugging Face Space | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:avatarartist`, Thread `avatarartist-public-release-and-space`, 2 datierte Ereignisse vom 2025-03-27 bis 2025-04-09.
- **Praxishinweis:** Stand 2025-04-09 sollten Praktiker zuerst die Projektseite und das Quell-Repository von AvatarArtist konsultieren und danach den verlinkten Hugging-Face-Space als gehosteten öffentlichen Zugangspunkt nutzen, wenn sie das Projekt bewerten.
- **Konfidenz:** mittel. Die datierten Überholungsvermerke oben sind maßgeblich dafür, was veraltet ist.
