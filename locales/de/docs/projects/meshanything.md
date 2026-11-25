---
title: "MeshAnything"
category: projects
date: 2024-08-06
tags: [meshanything, meshanything-development, project]
aliases: ["MeshAnything", "MeshAnything V2"]
level: 4
source_sha256: 33570e5dd2edac2d4399ea50472df30d1bb88e36d76e28ffa56823d8e0492eb4
translation: machine
translated_at: '2026-10-24'
---
# MeshAnything {#meshanything}

**Entwicklungslinie:** `project:meshanything` · Thread `meshanything-development`  
**Letztes Ereignis:** 2024-08-06 · 2 datierte Einträge seit 2024-06-17 · **Recherchiert:** 2026-09-04 · Vertrauensgrad: mittel

## Was es ist {#what-it-is}

MeshAnything V2 ist ein lokales Nachbearbeitungsmodell für Technical Artists und Ingenieure in 3D-Pipelines, die aus einer dichten 3D-Form ein kompaktes Dreiecksnetz benötigen, und zwar nicht als Prompt-zu-3D-Asset-Generator.

- Nimmt ein vorhandenes Mesh oder eine Punktwolke mit Normalen entgegen und sagt ein artist-artiges Mesh voraus, das auf diese Form ausgerichtet ist.
- Setzt nach Rekonstruktion, Scanning, SDS oder einem anderen Generator für dichte Meshes an; V2 stellt außerdem lokalen Gradio-, CLI-, Tokenisierungs- und Trainingscode bereit.

## Entwicklungslinie {#development-line}

- **2024-06-17 — Öffentliche Projektressourcen von MeshAnything wurden verlinkt.** Ein VQ-VAE-Mesh-Vokabular plus ein reiner Decoder-Transformer machte aus einer gelieferten 3D-Form ein artist-artiges Dreiecksnetz mit wenigen Flächen.
- **2024-08-06 — Öffentliche Ressourcen von MeshAnything V2 wurden verlinkt.** Am 2024-08-06 verlinkte der MeshAnything-Thread eine V2-Projektseite, ein eigenständiges V2-Quellcode-Repository und einen Hugging-Face-Space, mit Verweis auf den früheren Thread-Eintrag. Dies markiert einen späteren Entwicklungspunkt der V2-Ära, doch die Links nennen keine genauen Änderungen, kein Modellverhalten und keinen Verfügbarkeitsstatus.

## Was sich geändert hat {#what-changed}

- 2024-06-17 — MeshAnything ermöglichte formbedingtes autoregressives Remeshing: Ein VQ-VAE-Mesh-Vokabular plus ein reiner Decoder-Transformer machte aus einer gelieferten 3D-Form ein artist-artiges Dreiecksnetz mit wenigen Flächen.
- 2024-08-06 — MeshAnything V2 ersetzte die Tokenisierung Fläche für Fläche durch Adjacent Mesh Tokenization, verkürzte die Sequenzen etwa um die Hälfte und verdoppelte die dokumentierte Obergrenze von 800 auf 1600 Flächen.
- 2025-04-28 — Das offizielle V2-Repository erhielt einen Trainings-Commit; die aktuelle Dokumentation umfasst verarbeitete Objaverse-Daten, einen Michelangelo-Punktencoder sowie Training und Evaluation auf mehreren GPUs.

## So wird es verwendet {#how-to-use-this}

Ab dem 2024-08-06 behandeln wir MeshAnything V2 als eigenständige, versionierte Ressourcenlinie. Konsultieren Sie die zugehörige Projektseite, das Repository und den Hugging-Face-Space, statt anzunehmen, dass die Ressourcen vom 2024-06-17 V2 beschreiben.

1. Klonen Sie das offizielle V2-Repository und richten Sie die getestete lokale Umgebung ein: Ubuntu 22.04, CUDA 11.8, Python 3.10.13, PyTorch 2.1.1, FlashAttention und Gradio.
  — <https://github.com/buaacyw/MeshAnythingV2>
2. Laden Sie die offiziellen Modellgewichte Yiwen-ntu/MeshAnythingV2 für die lokale Inferenz herunter; die Modellkarte nennt das Bibliotheks-Repository und führt ein Modell mit 0,5 Mrd. Parametern auf.
  — <https://huggingface.co/Yiwen-ntu/MeshAnythingV2>
3. Stellen Sie entweder ein dichtes Eingabemesh oder eine N×6-.npy-Punktwolke mit Koordinaten und Normalen bereit. Für eine Text- oder Bildanfrage erzeugen Sie zuerst mit einem vorgelagerten System das dichte Mesh und übergeben dann dessen OBJ-Datei an MeshAnything.
  — <https://github.com/buaacyw/MeshAnythingV2>
4. Für ein Mesh, das nicht aus Marching Cubes stammt, führen Sie main.py mit --mc aus; beginnen Sie mit der Standardauflösung 128 und verwenden Sie --mc_level 8 nur dann, wenn feine Geometrie eine Vorverarbeitung mit 256er-Auflösung erfordert.
  — <https://github.com/buaacyw/MeshAnythingV2>
5. Starten Sie die CLI-Inferenz mit main.py oder eine lokale Oberfläche mit app.py und prüfen Sie das Ergebnis anschließend gegen die Obergrenze von 1600 Flächen und die Topologieanforderungen der nachgelagerten Schritte.
  — <https://github.com/buaacyw/MeshAnythingV2>
6. Für das Training beschaffen Sie den verarbeiteten Objaverse-Split und den Checkpoint des Michelangelo-Punktencoders und verwenden dann die dokumentierten accelerate-Befehle für Training und Evaluation mit acht Prozessen.
  — <https://github.com/buaacyw/MeshAnythingV2>

## Bewährte Praktiken {#best-practices}

- Verwenden Sie ein scharfes, hochwertiges Mesh aus Rekonstruktion, Scanning, SDS oder einem Generator für dichte Meshes; die offiziellen Hinweise warnen, dass schwache Feed-Forward-Geometrie bei dem Flächenbudget möglicherweise zu wenig Formdetail enthält.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Normalisieren Sie die Eingabe auf eine Einheits-Bounding-Box und behalten Sie die Up-Richtung +Y bei, bevor Sie die Inferenz starten.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Verwenden Sie Marching-Cubes-Vorverarbeitung für Meshes, die nicht aus Marching Cubes stammen; erhöhen Sie die Auflösung erst, nachdem Sie die zusätzliche Vorverarbeitungszeit mit dem Topologiegewinn verglichen haben.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Halten Sie die Aufgabe innerhalb der dokumentierten Obergrenze von 1600 Flächen, statt ein detailliertes High-Poly-Ergebnis zu erwarten.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Automatisieren Sie keine Abläufe gegen den offiziellen V2-Space: Er ist pausiert. Verwenden Sie für einen reproduzierbaren lokalen Weg das Repository und die heruntergeladenen Gewichte.
  — <https://huggingface.co/spaces/Yiwen-ntu/MeshAnythingV2>
- Behandeln Sie die Nutzung unter der S-Lab-License des offiziellen Repositorys als nicht kommerziell, bis die Autoren die widersprüchliche Lizenzangabe auf der Modellkarte klären.
  — <https://raw.githubusercontent.com/buaacyw/MeshAnythingV2/main/LICENSE.txt>
- Prüfen Sie vor dem Training den Dateinamen im ausgecheckten Stand: Die README verweist auf training_requirements.txt, während die Dateiliste des Repositorys training_requirement.txt zeigt.
  — <https://github.com/buaacyw/MeshAnythingV2>

## Dadurch überholt {#superseded-by-this}

- 2024-08-06 — Die Hinweise zu MeshAnything V1 begrenzten generierte Meshes auf unter 800 Flächen; das offizielle 1600-Flächen-Modell von V2 hebt diese Kapazitätsgrenze für neue V2-Läufe auf.
- 2025-04-28 — Die Behauptung, V2 besitze keinen offiziellen Trainingsweg, ist veraltet: Der Trainings-Commit des Repositorys und die aktuellen Anleitungen bieten einen solchen Weg.
- 2026-09-04 — Den gehosteten V2-Gradio-Space als aktuellen Zugangsweg zu nutzen, ist veraltet: Der offizielle Space ist pausiert.

## Weiterhin unbekannt {#still-unknown}

- Das offizielle V2-Repository erlaubt nichtkommerzielle Nutzung, während die offizielle Hugging-Face-Modellkarte das Modell als MIT kennzeichnet; welche Lizenz die kommerzielle Nutzung der Gewichte regelt, ist uns nicht bekannt.
- Die offizielle Dokumentation ist auf Ubuntu 22.04 und CUDA 11.8 getestet, doch die Kompatibilität mit aktuellen Treiberversionen und ein erfolgreicher Inferenzlauf wurden hier nicht unabhängig nachvollzogen.
- Die Dokumentation belegt nicht, dass UVs, Materialien, Rigs, Wasserdichtheit oder Animationstauglichkeit erhalten bleiben; diese Anforderungen sollten vor dem Einsatz an repräsentativen Assets geprüft werden.
- In den geprüften offiziellen Endpunkten wurde keine V3 oder kein funktionales Release nach 2025 gefunden; das ist kein Beleg dafür, dass ein unveröffentlichter Nachfolger nicht existiert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://buaacyw.github.io/mesh-anything/ | MeshAnything-Projektseite | 2026-09-04 |
| https://github.com/buaacyw/MeshAnything | MeshAnything offizielles Repository | 2026-09-04 |
| https://arxiv.org/abs/2406.10163 | MeshAnything: Artist-Created Mesh Generation with Autoregressive Transformers | 2026-09-04 |
| https://buaacyw.github.io/meshanything-v2/ | MeshAnything-V2-Projektseite | 2026-09-04 |
| https://github.com/buaacyw/MeshAnythingV2 | MeshAnything-V2 offizielles Repository | 2026-09-04 |
| https://github.com/buaacyw/MeshAnythingV2/commits/main | MeshAnything-V2-Commit-Verlauf | 2026-09-04 |
| https://arxiv.org/abs/2408.02555 | MeshAnything V2: Artist-Created Mesh Generation With Adjacent Mesh Tokenization | 2026-09-04 |
| https://huggingface.co/Yiwen-ntu/MeshAnythingV2 | Yiwen-ntu/MeshAnythingV2 Modellkarte | 2026-09-04 |
| https://huggingface.co/spaces/Yiwen-ntu/MeshAnythingV2 | Yiwen-ntu/MeshAnythingV2 Space | 2026-09-04 |
| https://raw.githubusercontent.com/buaacyw/MeshAnythingV2/main/LICENSE.txt | S-Lab License 1.0 für MeshAnything V2 | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:meshanything`, Thread `meshanything-development`, 2 datierte Ereignisse 2024-06-17 → 2024-08-06.
- **Praktischer Hinweis:** Ab dem 2024-08-06 sollten Praktiker MeshAnything V2 als eigenständige, versionierte Ressourcenlinie behandeln und dessen eigene Projektseite, das Repository und den Hugging-Face-Space konsultieren, statt anzunehmen, dass die Ressourcen vom 2024-06-17 V2 beschreiben.
- **Vertrauensgrad:** mittel. Für die Frage, was überholt ist, gelten die datierten Abschnitte „Dadurch überholt“ als maßgeblich.
