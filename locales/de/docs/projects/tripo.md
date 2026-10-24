---
title: "Tripo"
category: projects
date: 2026-06-23
tags: [project, tripo, tripo-development, triposg_triposf]
aliases: ["Tripo", "Tripo 2.0", "Tripo 3.0"]
level: 3
source_sha256: 7990bc3128e26285de5771f5cc4bbc7c1e2f54ee0f952ba70d7e558182ee096d
translation: machine
translated_at: '2026-10-24'
---
# Tripo {#tripo}

**Entwicklungslinie:** `project:tripo` · Thread `tripo-development`  
**Letztes Ereignis:** 2026-06-23 · 4 datierte seit 2024-09-20 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Tripo ist eine Suite zur Erzeugung von 3D-Assets für Künstler, Spielestudios und Produktteams.

- Studio: vereint Generierung, Segmentierung, Retopologie, Texturierung und Rigging in einem webbasierten Workspace.
- API: stellt Generierungsjobs für Text-zu-Modell, Bild-zu-Modell und Multiview-zu-Modell in eine Warteschlange.

Die API bedient die Modellfamilien H2, H3 und P1; Preise und Parameter hängen vom Modell und der Aufgabe ab. Wir nutzen sie, um Assets schnell zu entwerfen und zu verfeinern, prüfen Topologie, Skalierung und Materialien aber im Ziel-DCC-Tool oder in der Game Engine.

## Entwicklungslinie {#development-line}

- **2024-09-20 — Einstiegspunkt der Tripo-Webanwendung.** Am 20. September 2024 verlinkte Tripo direkt auf die Tripo-3D-Webanwendung. Die Quelle nennt weder ihr Startdatum, ihre Version noch ihre Funktionen.
- **2025-03-31 — Öffentliche Projekt- und Distributionslinks zu TripoSG.** Gewichte und Inferenzcode für das Bild-zu-3D-Modell wurden separat veröffentlicht.
- **2025-08-20 — Tripo-Studio-Generierungsworkspace.** Am 20. August 2025 eröffnete Tripo den gehosteten Tripo-Studio-Workspace und verwies auf die TripoSG-Veröffentlichung vom März 2025. Die Notizen bestätigen weder ein neues Modell, eine neue Funktion noch eine Preisänderung.
- **2026-06-23 — Tripo-Produktupdate vom Mai.** Am 23. Juni 2026 veröffentlichte Tripo den offiziellen Beitrag „May Update on Tripo“. Der Beitrag listet die konkreten Änderungen nicht auf und das genaue Veröffentlichungsdatum ist nicht verifiziert.

## Was sich geändert hat {#what-changed}

- 2024-09-20 — Tripo 2.0 stellte das kommerzielle Angebot auf eine neue Generation der 3D-Synthese um.
- 2025-03-31 — TripoSG trennte offene Forschung von Studio, indem Gewichte für Bild-zu-3D und Inferenzcode separat veröffentlicht wurden.
- 2025-08-20 — Algorithm 3.0 ging mit detaillierterer Geometrie, Texturen und Segmentierung öffentlich in Betrieb.
- 2026-06-23 — Studio ergänzte 8K Texture, Segmentation v2, eine DCC Bridge für ZBrush und Team-Preisstufen.

## So verwenden Sie das {#how-to-use-this}

Behandeln Sie ab 2025-03-31 die öffentlichen GitHub- und Hugging-Face-Ressourcen von TripoSG getrennt von der gehosteten App und Studio von Tripo. Prüfen Sie ab 2026-06-23 die offizielle Update-Seite, bevor Sie den aktuellen gehosteten Workflow oder Funktionsumfang voraussetzen.

1. Erstellen Sie einen API-Schlüssel und übergeben Sie ihn für Automatisierungen im Bearer-Authorization-Header.
  — <https://docs.tripo3d.ai/get-started/quick-start.html>
2. Senden Sie eine Aufgabe an POST /v2/openapi/task mit text_to_model, image_to_model oder multiview_to_model.
  — <https://docs.tripo3d.ai/get-started/quick-start.html>
3. Speichern Sie task_id und fragen Sie GET /v2/openapi/task/{task_id} ab, bis status success ist; Ergebnis-URLs laufen standardmäßig nach fünf Minuten ab.
  — <https://docs.tripo3d.ai/task-query/get-your-task-result.html>
4. Prüfen Sie die Credit-Kosten vor Batch-Läufen: image-to-model kostet 20–50 Credits, während Segmentierung, Low-Poly und Rigging separat abgerechnet werden.
  — <https://docs.tripo3d.ai/get-started/pricing.html>

## Best Practices {#best-practices}

- Geben Sie für Text-zu-3D Objekt, Material, Form und Zweck an und fügen Sie einen Negativ-Prompt hinzu, um unerwünschte Merkmale auszuschließen.
  — <https://www.tripo3d.ai/blog/text-to-3d-prompt-engineering>
- Prüfen Sie ein importiertes Asset auf Skalierung, Ausrichtung, Pivot und Polygonbudget, bevor Sie es in der Szene vervielfältigen.
  — <https://www.tripo3d.ai/zh-Hant/blog/ai-environment-creator>
- Akzeptieren Sie automatische Retopologie für Animation nicht ungeprüft, sondern kontrollieren Sie die Deformationen. Nicht standardisierte Anatomie, Gesichts-Edge-Loops und proprietäre Rigs können manuelle Nacharbeit erfordern.
  — <https://www.tripo3d.ai/blog/retopo-an-ai-character-model-for-animation>

## Abgelöst durch dies {#superseded-by-this}

- 2025-02-11 — Die Behauptung, Algorithm 2.5 sei das neueste kommerzielle Modell, wurde durch die öffentliche Veröffentlichung von Algorithm 3.0 im August 2025 abgelöst.
- 2025-05-22 — Der reine Generieren-und-Exportieren-Workflow wurde abgelöst, als Tripo Studio Segmentierung, Low-Poly-Werkzeuge, Textur-Bearbeitung und Uni-Rig ergänzte.
- 2024-09-20 — Tripo 2.0 ist für neue Integrationen veraltet; die API-Dokumentation verweist neue Integrationen auf H3, H2, P1 oder Turbo-v1.0.

## Noch unbekannt {#still-unknown}

- TripoSG ist ein offenes Forschungsmodell von VAST, während Tripo Studio und die API kommerzielle Produkte im selben Ökosystem sind. Wir können sie nicht als austauschbare Releases behandeln.
- Das genaue Startdatum von Tripo 2.0 innerhalb von September 2024 ist durch keine primäre datierte Ankündigung belegt; bestätigt sind nur Monat und Jahr.
- Die öffentliche API-Dokumentation verwendet H2, H3 und P1, das Marketing dagegen 2.0, 2.5 und 3.0; eine direkte Zuordnung zwischen diesen Bezeichnungen ist nicht bestätigt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.tripo3d.ai/blog/vast-open-source-month | VAST Open Source Month | TripoSG & TripoSF, Setting a New SOTA in 3D Generation | 2026-09-05 |
| https://github.com/VAST-AI-Research/TripoSG/blob/main/README.md | TripoSG README | 2026-09-05 |
| https://www.tripo3d.ai/blog/tripo-2-5-and-plugins | Tripo's Latest Releases & Updates: Algorithm 2.5, Blender & Unity Plugins | 2026-09-05 |
| https://www.tripo3d.ai/blog/introducing-tripo-studio | Introducing Tripo Studio: Your Next 3D Workspace with AI | 2026-09-05 |
| https://www.accessnewswire.com/newsroom/en/business-and-professional-services/tripo-the-frontrunner-of-3d-ai-boom-supercharges-new-era-in-cont-1066689 | Tripo 3.0 Upgrade announcement | 2026-09-05 |
| https://www.tripo3d.ai/blog/may-update-on-tripo | What's New on Tripo | May | 2026-09-05 |
| https://docs.tripo3d.ai/get-started/quick-start.html | Tripo OpenAPI Schnellstart und Authentifizierung | 2026-09-05 |
| https://docs.tripo3d.ai/task-query/get-your-task-result.html | Ergebnis einer Aufgabe abrufen | 2026-09-05 |
| https://docs.tripo3d.ai/get-started/pricing.html | Tripo OpenAPI Preise | 2026-09-05 |
| https://docs.tripo3d.ai/model-generation/image-to-model-v1-4-20240625.html | Image to model v1.4 API-Referenz | 2026-09-05 |
| https://www.tripo3d.ai/blog/text-to-3d-prompt-engineering | How to Master Prompt Engineering for Text to 3D Models | 2026-09-05 |
| https://www.tripo3d.ai/zh-Hant/blog/ai-environment-creator | AI Environment Creator | 2026-09-05 |
| https://www.tripo3d.ai/blog/retopo-an-ai-character-model-for-animation | How to Retopo an AI Character Model for Animation | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:tripo`, Thread `tripo-development`, 4 datierte Ereignisse 2024-09-20 → 2026-06-23.
- **Praktischer Hinweis:** Behandeln Sie ab 2025-03-31 die öffentlichen GitHub- und Hugging-Face-Ressourcen von TripoSG als eigenen Forschungs- und Distributionsweg, getrennt von der gehosteten Anwendung und Studio von Tripo; konsultieren Sie ab 2026-06-23 die offizielle Update-Seite, bevor Sie den aktuellen gehosteten Workflow oder Funktionsumfang voraussetzen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.

<!-- live-update:9a22698ca8b1d44c45b9878f61fb75f78790f49dd7737df4a921e79e94e2a88d -->
## 2026-10-17 — Tripo startet Early Access für UV-Unwrap und Retopologie {#2026-10-17-tripo-launches-early-access-to-uv-unwrap-and-retopology}

Tripo hat den Early Access für automatisches UV-Unwrapping und Retopologie eröffnet. Die Konvertierung in Low-Poly-Meshes und die Erzeugung von UV-Layouts sind nun direkt in den 3D-Modellierungsworkflow integriert.

### Verwendung und Praktiken {#usage-and-practices}

- Erzeugen Sie ein 3D-Asset in Tripo aus einer Textbeschreibung oder einem 2D-Bild-Prompt. [Quelle](https://customuse.com/)
- Führen Sie eine automatische Retopologie aus, um das dichte generierte Mesh in eine optimierte Quad- oder Dreiecksstruktur zu überführen, innerhalb der von Ihnen festgelegten Polygongrenzen. [Quelle](https://customuse.com/)
- Wenden Sie automatisches UV-Unwrapping an: Es berechnet Nähte, packt 2D-UV-Inseln und bäckt Texturkarten erneut auf das entfaltete Mesh. [Quelle](https://customuse.com/)
- Exportieren Sie das optimierte Asset als FBX, OBJ oder USD für eine Game Engine oder ein Werkzeug zur digitalen Inhaltserstellung. [Quelle](https://customuse.com/)
- Legen Sie die Ziel-Polygonzahl vor der Retopologie fest, damit die Asset-Dichte zum Performancebudget der Engine passt. [Quelle](https://customuse.com/)
- Prüfen Sie das Layout der 2D-UV-Inseln und die Nähte in stark gekrümmten Bereichen, bevor Sie die finalen Texturkarten backen. [Quelle](https://customuse.com/)

### Zusätzliche Belege {#additional-evidence}

- 2026-10-17: Die Retopologie erzeugt Low-Poly-Ausgaben als Quads oder Dreiecke, mit der von Tripo so genannten intelligenten Dichteverteilung. Die Berechnung der UV-Nähte und das Packen der Inseln laufen in derselben Pipeline zur 3D-Asset-Erzeugung. [Quelle](https://customuse.com/)

### Überholte Anleitung (zur Dokumentation beibehalten) {#superseded-guidance-retained-for-history}

- 2026-10-17: KI-generierte 3D-Meshes benötigten manuelle Retopologie und UV-Unwrapping in externer Software, bevor Texturierung oder Einsatz in einer Game Engine möglich waren. [Quelle](https://customuse.com/)

### Grenzen und offene Fragen {#limits-and-open-questions}

- Direkte Pfade zur Dokumentation von Tripo auf tripo3d.ai konnten nicht verifiziert werden, da Suchergebnisse sie hinter Weiterleitungen verbargen. Eine direkte Erstquellen-Angabe liegt daher noch nicht vor.
- Langfristige Preise und Tarifbeschränkungen für die Early-Access-Retopologie und das UV-Unwrapping sind nicht angekündigt.

<!-- Retained base: 694331793733b8221866d9072af7e45999930387; article blob: 11d856f6dc8c75d0fae16ee7b15ee410955295d4 -->

<!-- live-update:9bcb91cd3e2d7094b7f6c1e8ebd6eb64e2fe47fe3bfc2d61e36252d582e1a65e -->
## 2026-10-23 — Tripo Studio ergänzt automatisches Skelett-Rigging und textgesteuerte Animation {#2026-10-23-tripo-studio-adds-skeletal-auto-rigging-and-text-driven-animation}

Tripo Studio rigged Charaktere nun automatisch und animiert sie aus Text. Das automatische Rigging kommt mit fünf humanoiden Skelett-Presets: UE5 Mannequin, Mixamo, VRM 1.0, Unity Humanoid und ActorCore. Text to Motion macht aus einem Prompt einen Clip von 1–10 Sekunden und kann Clips zu mehrstufigen Sequenzen verketten. Das humanoide automatische Rigging akzeptiert nur Meshes mit weniger als 100.000 Dreiecken. Skin Weights müssen unter Umständen noch in einem externen DCC-Tool korrigiert werden.

## 2026-10-23 — Tripo Studio führt Auto-Rigging und einen Workflow zur Bewegungserzeugung ein {#2026-10-23-tripo-studio-introduces-auto-rigging-and-motion-generation-workflow}

Rigging und Animation sind nun in Tripo Studio integriert. Knochen werden für fünf Standard-Presets von Game Engines automatisch platziert. Animationen entstehen aus Text-Prompts, und bis zu fünf Bewegungssegmente lassen sich verketten. All das funktioniert bei Modellen mit bis zu 100.000 Dreiecken.

### Verwendung und Praktiken {#usage-and-practices_1}

- Besorgen Sie sich ein Mesh: Erzeugen Sie einen 3D-Charakter in Tripo Studio aus einem Text-Prompt oder aus Referenzbildern oder importieren Sie ein bestehendes 3D-Mesh. [Quelle](https://studio.tripo3d.ai/)
- Rigging anwenden: Öffnen Sie das Modul Auto-Rigging und wählen Sie eines der fünf Presets (UE5 Mannequin, Mixamo, Unity Humanoid, VRM 1.0 oder ActorCore). Prüfen Sie vorab, ob das Mesh unter 100.000 Dreiecken liegt. [Quelle](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Animieren Sie es: Wählen Sie eine fertige Bewegung aus der Motion-Bibliothek oder geben Sie einen Prompt in Text to Motion ein, für einen individuellen Clip von 1–10 Sekunden oder eine mehrstufige Sequenz. [Quelle](https://www.tripo3d.ai/blog/rigging-animation)
- Exportieren Sie es: Prüfen Sie die Deformation im 3D-Viewport, passen Sie bei mehrstufigen Sequenzen die Zeitabschnitte an und exportieren Sie anschließend als FBX oder GLB mit eingebetteter Skelettanimation. [Quelle](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Retopologisieren Sie zuerst: Halten Sie das Basis-Mesh vor dem Auto-Rigging unter 100.000 Dreiecken, damit Vertex-Gewichte und Gelenkdeformationen konsistent bleiben. [Quelle](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Prüfen Sie die kritischen Gelenke: Schultern, Hüften und Finger müssen oft ihre automatischen Skin Weights in Blender oder Maya korrigiert bekommen, bevor der Charakter in eine Game Engine geht. [Quelle](https://www.tripo3d.ai/blog/rigging-animation)
- Blocken Sie mit kostenlosen Presets vor: Testen Sie zuerst mit der kostenlosen Motion-Bibliothek, damit Credits nur dann für individuelles Text to Motion anfallen, wenn es nötig ist. [Quelle](https://www.tripo3d.ai/blog/rigging-animation)

### Zusätzliche Belege {#additional-evidence_1}

- 2026-10-23: Die Versionshinweise zur Nachbearbeitung besagen, dass exportierte Rigs und Text-to-Motion-Sequenzen als standardmäßig bearbeitbare Skelettanimationsspuren in FBX und GLB vorliegen. Sie können in Unreal Engine, Unity, Blender und WebGL-Viewern neu zugeordnet (retargeted) werden. [Quelle](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- 2026-10-23: Die technische Dokumentation besagt, dass Auto-Rigging Gelenke positioniert und initiale Heatmap-Skin-Weights über fünf Skeletthierarchien anwendet (UE5 Mannequin, Mixamo, VRM 1.0, Unity Humanoid, ActorCore). Prompt-Verkettung erlaubt bis zu fünf aufeinanderfolgende Bewegungssegmente, jeweils mit einer eigenen Dauer von bis zu 10 Sekunden. [Quelle](https://www.tripo3d.ai/blog/rigging-animation)

### Überholte Anleitung (zur Dokumentation beibehalten) {#superseded-guidance-retained-for-history_1}

- 2026-10-23: Einen Tripo-Charakter zu riggen bedeutete, das statische Mesh in Mixamo, Blender oder ein ähnliches Werkzeug zu exportieren und das Skelett von Hand zu platzieren und zu gewichten. [Quelle](https://www.tripo3d.ai/blog/rigging-animation)
- 2026-10-23: Tripo-Assets zu animieren bedeutete, Motion-Capture-Bibliotheken von Drittanbietern oder manuelles Keyframing außerhalb von Tripo Studio zu verwenden. [Quelle](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)

### Grenzen und offene Fragen {#limits-and-open-questions_1}

- Wie gut die Deformation bei textgesteuerter Animation über die Zeit auf nicht-humanoiden oder vierbeinigen Modellen hält.
- Unabhängige Community-Benchmarks der Skin-Weighting-Funktion von Tripo Studio gegenüber dem Auto-Rigging, das in DCC-Tools integriert ist.
- Die neuronale Netzarchitektur und die Trainingsdaten hinter Text to Motion.

<!-- Retained base: d42a348223e0670592e2f1b683c46992af48130e; article blob: 990e6d08d55ddbad4d5d0b851ef0456aa73dd67f -->
