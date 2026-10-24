---
title: "SAM2Matting"
category: projects
date: 2026-07-15
tags: [project, sam2matting, sam2matting-public-release]
aliases: ["SAM2Matting"]
level: 3
source_sha256: 68ab791325f52efeb45f14a0a0884361b19e97c825c8983001f4ae38d217bf03
translation: machine
translated_at: '2026-10-24'
---
# SAM2Matting {#sam2matting}

**Entwicklungslinie:** `project:sam2matting` · Thread `sam2matting-public-release`  
**Letztes Ereignis:** 2026-07-15 · 1 datiertes seit 2026-07-15 · **Recherchiert:** 2026-09-08 · Konfidenz: mittel

## Was es ist {#what-it-is}

SAM2Matting ist ein Inferenz-Framework, das Vordergrund-Prompts in Alpha-Mattes für die Bild- und Videokomposition umwandelt.

- Matte-Verfeinerung: wandelt Masken, Punkte, Boxen und SAM3-Text-Prompts in Mattes mit feinen Kanten um.
- Video-Matting: kombiniert zeitliches Tracking mit dedizierten Matting-Heads.

Die veröffentlichten Gewichte umfassen 216 MB Tiny, 383 MB Base+ und 3,51 GB SAM3. Der Trainingscode ist nicht veröffentlicht, und CC BY-NC-SA 4.0 ist nicht kommerziell. Daher sollte das Projekt zur Evaluation der Inferenz genutzt werden und nicht als veröffentlichter Trainings- oder kommerzieller Deployment-Stack.

## Entwicklungslinie {#development-line}

- **2026-07-15 — Öffentliche Projektressourcen zu SAM2Matting wurden verfügbar.** Am 2026-07-15 wurde SAM2Matting über verlinkte offizielle Projekt-, Quellcode-, Modell-Hosting- und interaktive Demo-Ressourcen präsentiert. Dies markiert einen wesentlichen Schritt des öffentlichen Zugangs zum Projekt, da Leser die Implementierung finden und über die verlinkten Ressourcen evaluieren konnten.

## Was sich geändert hat {#what-changed}

- 2026-06-22 — Das SAM2Matting-Quellcode-Repository wurde initialisiert.
- 2026-06-25 — SAM2Matting arXiv v1 wurde eingereicht, und seine drei Inferenz-Checkpoints wurden hochgeladen.
- 2026-06-30 — SAM2Matting entfernte `pip install -e .` und korrigierte Abhängigkeiten; dies ist weiterhin die neueste Änderung im Upstream-GitHub-Repository.
- 2026-07-09 — SAM2Matting erhielt eine Hugging-Face-Modellkarte und das Tag `image-segmentation`; dies änderte die Dokumentation, nicht die Gewichte oder den Code.
- 2026-07-15 — SAM2Matting war als Bundle aus Projekt, Code, Checkpoints und Demo verfügbar; primäre Verläufe belegen an diesem Datum kein neues Upstream-Release.

## So wird es verwendet {#how-to-use-this}

1. Klonen Sie das Upstream-Repository, erstellen Sie seine Python-3.10-Conda-Umgebung und führen Sie anschließend `pip install -r requirements.txt` aus.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>
2. Laden Sie einen offiziellen Checkpoint nach `checkpoints/` herunter und ordnen Sie ihn der Skriptfamilie SAM2 oder SAM3 zu.
  — <https://huggingface.co/FudanCVL/SAM2Matting>
3. Für Video stellen Sie eine Vordergrundmaske des ersten Frames bereit und passen dann die fest codierten Pfade für Variante, Eingabe, Maske und Ausgabe im Demo-Skript an – oder kapseln es – bevor Sie eigene Medien verwenden.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py>
4. Für interaktive Prompts verwenden Sie `interactive_sam2.py` für Punkte oder Boxen und `interactive_sam3.py` für Text.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>
5. Für einen Test im Browser verwenden Sie den offiziellen Space mit einem Bild und einer groben Vordergrundmaske; er liefert eine Alpha-Matte, eine Kompositions-Vorschau und ein transparentes PNG.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>

## Bewährte Praktiken {#best-practices}

- Verwenden Sie eine Maske, die den Vordergrund grob abdeckt, wobei Weiß den Vordergrund markiert; weiche Graustufenmasken werden empfohlen.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- Verwenden Sie SAM2.1-Tiny, wenn Geschwindigkeit wichtig ist; reservieren Sie SAM3 für Fälle, in denen die Prompt-Unterstützung den höheren VRAM- und Zeitbedarf rechtfertigt.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- Für Video im Space initialisieren Sie den ersten Frame und halten die Frame-Anzahl moderat; diese Begrenzung gilt speziell für die ZeroGPU-Demo.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- Automatisieren Sie den Befehl `--save_mp4` aus der README nicht unverändert: Der aktuelle Code definiert ihn als `store_false`, während das Speichern der Standard ist.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py>
- Beschränken Sie die Nutzung auf nicht-kommerzielle Zwecke oder holen Sie für andere Anwendungsfälle eine Genehmigung gemäß der angegebenen Lizenz ein.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>

## Hiermit ersetzt {#superseded-by-this}

- 2026-06-30 — Die frühere Setup-Anweisung, `pip install -e .` hinzuzufügen, ist veraltet; der Upstream hat sie zugunsten der Installation der aufgelisteten Anforderungen entfernt.

## Weiterhin unbekannt {#still-unknown}

- Im chinesischsprachigen Suchbereich wurde keine Seite des Projektteams in chinesischer Sprache und kein unabhängig reproduzierbarer Praxisbericht eines chinesischsprachigen Anwenders gefunden; daher wird kein chinesisches Praxisrezept behauptet.
- Es wurde kein eigener lokaler Lauf und keine unabhängige aktuelle Qualitäts- oder Durchsatz-Benchmark gefunden; Ergebnisse aus dem Paper werden nicht als Produktionserwartungen verwendet.
- Der offizielle Space stellt keinen stabilen absoluten Zeitstempel für seinen aktuellen Deploy bereit, daher wird sein aktueller App-Stand nicht als datiertes Entwicklungsereignis erfasst.
- README und aktueller Code widersprechen sich bezüglich `--save_mp4`; ein Wrapper oder eine Code-Korrektur muss vor wiederholbarer Automatisierung getestet werden.
- Offizieller Trainingscode, ein Feinabstimmungsverfahren, eine Matrix unterstützter GPUs und eine minimale VRAM-Anforderung wurden nicht gefunden.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://henghuiding.com/SAM2Matting/ | SAM2Matting-Projektseite | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting | FudanCVL/SAM2Matting-Repository | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting | FudanCVL/SAM2Matting-Modell-Repository | 2026-09-08 |
| https://huggingface.co/spaces/FudanCVL/sam2matting | FudanCVL/sam2matting-Space | 2026-09-08 |
| https://arxiv.org/abs/2606.27339 | SAM2Matting: Generalized Image and Video Matting — arXiv | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/commits/main | Commits — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting/commit/6f92789a2a16ae899e81470a1b4dc47e08f40db3 | Upload checkpoints — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/commit/73dd721d77b56749248aefe5e8824d7f61b9d13c | update install and requirements — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting/discussions/1 | Model-card and pipeline-tag pull request — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/releases | Releases — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/blob/main/README.md | SAM2Matting-README — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py | inference_video_sam2.py — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py | app.py — FudanCVL/sam2matting-Space | 2026-09-08 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:sam2matting`, Thread `sam2matting-public-release`, 1 datiertes Ereignis 2026-07-15 → 2026-07-15.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
