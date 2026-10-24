---
title: "Krea 2 Anygles Kamera-Ansichtsadapter"
description: "Krea 2 Anygles rendert eine klar erkennbare Person aus einer neuen Kamera-Gierung (Yaw), Elevation oder Distanz neu, über ein Control-LoRA, das von einer SAM-3D-Body-Normal-Map gesteuert wird; es benötigt einen eigenen Loader und einen gesperrten, pickle-basierten Vorbereitungsschritt. Enthält unseren 80-Frame-Orbit-Test mit einem offenen Image-to-3D-Mesh anstelle von SAM 3D Body."
category: models
tags: [krea-2, anygles, camera-control, novel-view, control-lora, comfyui, sam-3d-body, normal-map]
aliases: ["krea2-anygles", "Anygles", "Krea 2 camera angle LoRA"]
level: 4
source_sha256: c5bcc7f604686a662d18d9f5521d5e9dfa8d8a16024299af8399ab681ee51e2f
translation: machine
translated_at: '2026-10-24'
---
# Krea 2 Anygles Kamera-Ansichtsadapter {#krea-2-anygles-camera-view-adapter}

Krea 2 Anygles ist ein Community-Adapter für Krea 2 Turbo. Aus einem Bild einer Person erzeugt er dieselbe Person und Szene aus einem neuen Kamerawinkel. Er kombiniert ein Control-LoRA mit Rang 32 mit 4 ComfyUI-Nodes. Die Zielansicht wird durch eine gerenderte Normal-Map definiert und nicht allein durch Text-Prompts. Wir haben ihn am 2026-09-30 anhand der Modellkarte, des Node-READMEs und des Node-Codes geprüft.

Wir haben den echten Adapter mit einem offenen Image-to-3D-Mesh (TripoSG) anstelle des gesperrten SAM 3D Body ausgeführt; die Ergebnisse der kleinen Stichprobe finden sich unter [Unser Orbit-Test](#our-orbit-test).

## Was er steuert {#what-it-controls}

| Steuerung | Node-Bereich | Demos des Autors | Bedeutung |
|---|---|---|---|
| Yaw | -180 bis +180 Grad | voller Orbit | negativ bewegt die Kamera nach links, positiv nach rechts |
| Elevation | -60 bis +60 Grad | -45 bis +45 | negativ bewegt die Kamera nach unten, positiv nach oben |
| Distanz | 0,6x bis 1,8x | 0,78x bis 1,35x | unter 1 näher, über 1 weiter entfernt |

- Geltungsbereich: **eine klar erkennbare menschliche Person.** Tiere, allgemeine Objekte, Menschenmengen sowie exakte 3D-Rekonstruktion werden nicht unterstützt. Das Modell erzeugt verdeckte Seiten und den Hintergrund, anstatt sie zu rekonstruieren.
- Elevation und Distanz sind nützliche Steuergrößen und keine kalibrierte Szenenrekonstruktion. Die Werte sind als Richtungen zu verstehen.

## So funktioniert es {#how-it-works}

1. **Kamera-Node.** SAM 3D Body extrahiert das Körpermesh, und MoGe schätzt das Sichtfeld der Kamera. Der Node rotiert das Mesh um das Becken und rendert eine Ziel-Normal-Map im Seitenverhältnis der Quelle. Außerdem erzeugt er den Kamera-Satz für das Training.
2. **Encode-Node.** Dieser Node leitet das Bild an Qwen3-VL und an einen sauberen Referenzpfad mit maximaler Kantenlänge von 384 px weiter. Anschließend VAE-kodiert er die Ziel-Normal für die gesamte Leinwand.
3. **Load-LoRA-Node.** Dieser Node lädt die LoRA-Paare und den Projektionstensor `transformer.first_control.weight`. Standard-Loader lassen diesen Tensor weg und verlieren die räumliche Steuerung stillschweigend.
4. **Model-Patch-Node.** Dieser Node injiziert Normal-Tokens am Eingang des verrauschten Bildes und speichert den Referenz-K/V-Cache einmal pro Durchlauf.

Die Gewichtsdatei `krea2_anygles_rank32.safetensors` ist in BF16 229 MB groß. Sie enthält 256 LoRA-Paare mit Rang 32 über die 32 Transformer-Blöcke (Attention q, k, v, out, Gate und MLP) sowie die eine Control-Projektion mit der Form [6144, 64]. Wir haben die Datei untersucht und die veröffentlichte Prüfsumme des Autors bestätigt.

### Kamera-Satz {#camera-sentence}

Das Training verwendete nur Formulierungen für Drehungen nach links. Der Node wandelt das vorzeichenbehaftete Yaw über `left_angle = (-yaw) mod 360` um. Eine Drehung nach rechts um +50 Grad wird zu:

```text
Same figure. Move the camera 310 degrees to the left relative to the input view.
```

Der Node hängt Elevation- und Distanzangaben nur an, wenn sie angefordert werden, und übernimmt benutzerdefinierten Text unverändert. Szenendetails gehören in den zusätzlichen Text („weiches Nachmittagslicht“). Schreiben Sie keine Kameraanweisungen, die der Normal-Map widersprechen.

## Einstellungen (Modellkarte und README des Autors) {#settings-authors-card-and-readme}

```yaml
inference_base: krea/Krea-2-Turbo      # ComfyUI graph validated with krea2_turbo_int8_convrot
steps: 8
sampler: euler
scheduler: simple
guidance: 0.0 in diffusers / cfg 1.0 in ComfyUI
lora_strength: 1.0                     # node allows 0-2; no other value is documented
reference_max_edge: 384                # px; Qwen3-VL image input on
reference_kv_cache: on
output: source aspect ratio, sides multiple of 16, at most 2 * 1024 * 1024 px
validated_size: 1008x1344
```

Zu den Konventionen für die Guidance (Krea 0.0 = ComfyUI 1.0) siehe [[krea-2-prompting]].

## Ausführung {#running-it}

Für ComfyUI das Repository in `custom_nodes` klonen, `requirements.txt` installieren, die Lizenz akzeptieren, um den SAM-3D-Body-Checkpoint herunterzuladen, das LoRA nach `models/loras` kopieren und `krea2_anygles_workflow.json` laden.

Die Modellkarte stellt einen eigenständigen Python-Workflow bereit:

```bash
python prepare_normal.py --source person.webp --output target_normal.png \
  --yaw 50 --elevation 0 --distance 1.0 \
  --sam3d-root ./sam-3d-body \
  --checkpoint ./checkpoints/sam-3d-body-dinov3/model.ckpt \
  --mhr-model ./checkpoints/sam-3d-body-dinov3/assets/mhr_model.pt

python example.py --source person.webp --normal target_normal.png --output result.webp \
  --yaw 50 --elevation 0 --distance 1.0 --prompt "soft afternoon light" --steps 8 --seed 42
```

### Was der Normal-Vorbereitungsschritt mitbringt {#what-the-normal-preparation-step-pulls-in}

Unser Code-Audit vor der Installation ergab, dass die Diffusion-Nodes Safetensors-Dateien direkt laden, ohne Netzwerkaufrufe, Subprozesse, `eval` oder `exec`. Die Normal-Vorbereitungspipeline bringt dagegen schwere Abhängigkeiten mit:

- zwei Pickle-Checkpoints, geladen über `torch.load(weights_only=False)` und `torch.jit.load`
- ein Pickle-MoGe-Modell
- ein Laufzeit-Download von DINOv3-Code von GitHub über `torch.hub`
- etwa 20 zusätzliche Pakete, darunter pyrender, pytorch-lightning und MoGe aus Git
- das gesperrte Repository `facebook/sam-3d-body-dinov3`.

Das gesperrte Repository lieferte uns HTTP 403, und wir entpacken Pickle-Checkpoints von Drittanbietern nicht in einer gemeinsam genutzten Laufzeitumgebung. Deshalb haben wir diesen Pfad nicht verwendet.

Führen Sie die Normal-Vorbereitung in einem dedizierten Container oder auf einer eigenen Maschine aus, die nur `target_normal.png` ausgibt. Übergeben Sie diese Datei und den Kamera-Satz an den Encode-Node, damit die ComfyUI-Hauptumgebung niemals Pickle-Dateien berührt.

## Unser Orbit-Test {#our-orbit-test}

Wir haben den Mesh-Generator ersetzt und die übrige Pipeline des Autors beibehalten:

- **Mesh:** [TripoSG](https://github.com/VAST-AI-Research/TripoSG) (MIT-Lizenz, ungesperrt, `.safetensors`-Gewichte), ausgeführt auf einem [BiRefNet](https://huggingface.co/ZhengPeng7/BiRefNet)-Personen-Matte in einer isolierten Umgebung. TripoSG lief mit 50 Schritten, Guidance 7,0 und Seed 42.
- **Normals:** Der Normal-Renderer des Autors lief unverändert auf unserem Mesh mit den Kamera-Sätzen des Autors. Wir haben die Brennweite auf 1680 px festgelegt (SAM-3D-Body-Standard ohne FOV-Schätzung), um den Pickle-basierten MoGe-Checkpoint zu vermeiden.
- **Diffusion:** Wir haben in ComfyUI nur die Encode-, Load-LoRA- und Model-Patch-Nodes ausgeführt: fp8 Turbo, 8 Schritte, euler/simple, cfg 1, Stärke 1,0, Referenzkante 384 px, Auflösung 1008x1344 und ein fester Seed.
- **Matrix:** 4 Ein-Personen-Motive (ein Motiv mit Identitäts-LoRA und drei fotorealistische Szenen) über 20 Kamerawinkel. Das deckte einen vollen Yaw-Kreis in 22,5-Grad-Schritten (16 Ansichten), Elevation ±20 sowie Distanzen 0,78 und 1,35 ab, insgesamt 80 Frames.

Die Gesichtsähnlichkeit wird als Kosinusdistanz mit OpenCV SFace gegenüber dem Quellgesicht gemessen; Werte von 0,363 oder höher zeigen dieselbe Identität an:

| Signal | Ergebnis |
|---|---|
| Silhouette der Person vs. Ziel-Normal (IoU, Median pro Motiv) | 0,83-0,91 (das sitzende Motiv passt am schlechtesten) |
| Gesichtsähnlichkeit, nahezu frontale Ansichten (Median pro Motiv) | 0,47-0,61 |
| Gesichtsähnlichkeit bei ±90 Grad (Profile) | 0,07-0,53, stark motivabhängig |
| Rückansichten (etwa ±135 bis 180 Grad) | der Detektor findet meist kein Gesicht, wie erwartet |
| Erkannte Gesichter auf oder über der Linie für dieselbe Person | 43 von 60 |

TripoSG liefert einen bekleideten Umriss. SAM 3D Body erzeugt ein nacktes parametrisches Körpermesh, das zu den Trainingsdaten des Adapters passt. Sitzende Posen passen auf unser offenes Mesh am schlechtesten. Diese Zahlen beschreiben diesen Ersatz-Aufbau und nicht die ursprüngliche SAM-3D-Body-Pipeline.

## Stolperfallen {#gotchas}

- **Laden Sie die Gewichte nicht mit einem Standard-LoRA-Loader.** Verwenden Sie den Anygles-Load-LoRA-Node. Generische Loader verwerfen `transformer.first_control.weight`, wodurch die Ansichtssteuerung stillschweigend entfällt.
- **Passen Sie die Abmessungen der Normal-Map an die Leinwand an.** Rendern Sie Normals in exakt der Ausgabeauflösung und dem Seitenverhältnis, damit die räumliche Steuerung genau bleibt.
- **Schneiden Sie auf eine klar erkennbare Person zu.** Der Adapter kann keine Gruppen oder entfernte Figuren verarbeiten; beschneiden Sie zuerst das Bild.
- **Prüfen Sie die Identität bei Rückansichten.** Das Modell erfindet nicht gesehene Winkel und Hintergründe, statt sie zu rekonstruieren. Prüfen Sie Gesicht und Kleidung über große Yaw-Drehungen hinweg auf Konsistenz.
- **Testen Sie quantisierte Checkpoints.** Der ComfyUI-Graph wurde mit einem int8-ConvRot-Turbo-Checkpoint validiert. Ob fp8 sich gleich verhält, ist ungetestet, prüfen Sie daher die Ausgabe beim Wechsel.
- **Führen Sie die Normal-Vorbereitung in einer eigenen Umgebung aus.** Die Vorbereitungsskripte entpacken Pickle-Checkpoints von Drittanbietern und laden Code zur Laufzeit herunter.

## Offene Fragen {#open-questions}

- Orbit-Ergebnisse mit nativen Normals des bloßen SAM-3D-Body-Meshes statt bekleideter Meshes.
- Verhalten des Adapters bei anderen LoRA-Stärken als 1,0.
- Parität zwischen fp8 Turbo und dem vom Autor validierten int8-ConvRot-Checkpoint.

## Siehe auch {#see-also}

- [[krea-2-prompting]] - Einstellungen, Konventionen für die Guidance und Prompt-Struktur für Krea 2
- [[krea-2]] - Meilensteine der Krea-2-Veröffentlichung
- [[flux-klein-capability-map]] - Regeln zur Variantenwahl und Laufzeitprüfung

## Quellen {#sources}

- Modellkarte (Einstellungen, Wertebereiche, portable Nutzung, Lizenz): https://huggingface.co/yijunwang2/krea2-anygles
- ComfyUI-Nodes, README und Workflow: https://github.com/alexw5702-afk/krea2-anygles
- Wertebereiche der Node-Widgets: https://github.com/alexw5702-afk/krea2-anygles/blob/main/nodes.py
- Pixelbudget (`MAX_PIXELS = 2 * 1024 * 1024`): https://github.com/alexw5702-afk/krea2-anygles/blob/main/anygles.py
- Demo-Space: https://huggingface.co/spaces/yijunwang2/krea2-anygles
- SAM-3D-Body-Repository: https://github.com/facebookresearch/sam-3d-body
- SAM-3D-Body-Checkpoint (gesperrt): https://huggingface.co/facebook/sam-3d-body-dinov3
- TripoSG (Image-to-3D, MIT): https://github.com/VAST-AI-Research/TripoSG und Gewichte https://huggingface.co/VAST-AI/TripoSG
- BiRefNet (Matting): https://huggingface.co/ZhengPeng7/BiRefNet
- OpenCV-Gesichtserkennung (SFace, Cosinus-Schwelle 0,363): https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html
