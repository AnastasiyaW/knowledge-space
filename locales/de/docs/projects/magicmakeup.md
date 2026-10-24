---
title: "MagicMakeup Transfer"
category: projects
date: 2026-07-28
tags: [magicmakeup, magicmakeup-transfer, project]
aliases: ["MagicMakeup Transfer"]
level: 2
source_sha256: 5abe2ac4b1d843ac8bbc1d6d3d0a33fb1d9398fa466f6de43af7b337dee3a233
translation: machine
translated_at: '2026-10-24'
---
Wait — I must produce the translation, not placeholders. The input contains no @@CODE_n@@ placeholders, so I translate the full document directly.

---
title: MagicMakeup Transfer
category: projects
date: 2026-07-28
tags: [magicmakeup, magicmakeup-transfer, project]
aliases: ["MagicMakeup Transfer"]
---

# MagicMakeup Transfer {#magicmakeup-transfer}

**Entwicklungslinie:** `project:magicmakeup` · Thread `magicmakeup-transfer`  
**Letztes Ereignis:** 2026-07-28 · 1 datiertes Ereignis seit 2026-07-28 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

MagicMakeup Transfer ist ein Bild-zu-Bild-System für die Übertragung von Make-up mit Regionssteuerung, gedacht für Forschungsanwender, die Gesichtsausschnitte und Masken vorbereiten.

- Referenzübertragung: überträgt das Erscheinungsbild von Gesamtgesicht, Augen und Lippen aus einem Referenzporträt.
- Modell-Checkpoint: verwendet einen MagicMakeup-Checkpoint auf FLUX.1-Kontext-dev.
- Ausgabeauflösung: erzeugt 1024 × 1024 Ausschnitte und unterstützt Inferenz für einzelne Paare oder Batch-Inferenz im All-to-All-Modus.

## Entwicklungslinie {#development-line}

- **2026-07-28 — Öffentliche Projektressourcen zu MagicMakeup Transfer verlinkt.** Eine regionssteuerbare Diffusion-Transformer-Pipeline mit Übertragung von Gesicht, Augen und Lippen, aufgebaut auf FLUX.1-Kontext-dev.

## Was sich geändert hat {#what-changed}

2026-07-28 — Die offizielle Veröffentlichung von Code und Checkpoint erschien. MagicMakeup ist seitdem als regionssteuerbare Diffusion-Transformer-Pipeline mit Übertragung von Gesicht, Augen und Lippen nutzbar, aufgebaut auf FLUX.1-Kontext-dev.

## So wird es verwendet {#how-to-use-this}

Beginnen Sie mit der Projektseite, dem Repository und der gehosteten Modellressource, Stand 2026-07-28. Prüfen Sie diese primären Materialien, damit exakte Versionen und Nutzungsdetails verifiziert bleiben.

1. Klonen Sie das offizielle Repository und erstellen Sie die empfohlene Python-3.10-Umgebung mit PyTorch 2.6.0/CUDA 12.4 und den aufgelisteten Abhängigkeiten.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
2. Akzeptieren Sie die Lizenz von FLUX.1-Kontext-dev, laden Sie dieses Basismodell herunter und laden Sie anschließend den Checkpoint Anyou/MagicMakeup herunter.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
3. Legen Sie Quell- und Make-up-Referenzporträts in getrennte Verzeichnisse. Schneiden Sie die Hauptgesichter auf zentrierte 1024 × 1024 Bilder zu und bewahren Sie das Vorverarbeitungsprotokoll auf.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
4. Erzeugen Sie passende Gesichts-, Augen- oder Lippenmasken für beide Bilder. Führen Sie test_single.py mit dem gewünschten Wert für --label aus: eyes, lip oder eyes,lip,face.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
5. Bestätigen Sie vor dem Ausführen von test_dir.py, dass die Dateinamen-Stämme aller Bilder und Masken übereinstimmen. Das Skript kombiniert jede Quelle mit jeder Referenz und überspringt nicht zugeordnete Masken.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>

## Bewährte Vorgehensweisen {#best-practices}

- Beginnen Sie mit einem einzelnen Paar und prüfen Sie das Vergleichsfenster, bevor Sie einen All-to-All-Batch ausführen. Der Batch-Modus überspringt Paare, wenn Abweichungen bei Ausschnitten oder Masken auftreten.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
- Verwenden Sie zunächst den Standard-Modus für das Modell-Offloading. Wählen Sie sequenzielles CPU-Offloading nur, wenn der GPU-Speicher knapp ist, da es die Inferenz verlangsamt.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
- Halten Sie die Nutzung im angegebenen nicht-kommerziellen akademischen Forschungsbereich für Kosmetik. Verwenden Sie es nicht für Gesichtstausch, Identitätserkennung, Identitätsimitation oder täuschende Bearbeitungen.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>

## Hierdurch abgelöst {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Wir haben keine versionierte GitHub-Veröffentlichung und keine datierte Checkpoint-Veröffentlichung gefunden. Daher lässt sich der genaue Veröffentlichungszeitpunkt von Code und Checkpoint nicht vom Veröffentlichungsereignis am 2026-07-28 trennen.
- Die Hugging-Face-Seite zeigt ein generisches Diffusers-Beispiel, das die maskenkonditionierte Pipeline von MagicMakeup nicht enthält. Das offizielle Repository bleibt der maßgebliche Inferenzweg.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://vivocameraresearch.github.io/magicmakeup/ | MagicMakeup: A Region-Controllable Diffusion Transformer for High-Fidelity Makeup-Transfer | 2026-09-05 |
| https://github.com/vivoCameraResearch/Magic-Makeup | vivoCameraResearch/Magic-Makeup | 2026-09-05 |
| https://huggingface.co/Anyou/MagicMakeup | Anyou/MagicMakeup model card | 2026-09-05 |
| https://arxiv.org/abs/2607.20924 | MagicMakeup: A Region-Controllable Diffusion Transformer for High-Fidelity Makeup-Transfer | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:magicmakeup`, Thread `magicmakeup-transfer`, 1 datiertes Ereignis 2026-07-28 → 2026-07-28.
- **Praktischer Hinweis:** Beginnen Sie mit der Projektseite, dem Repository und der gehosteten Modellressource, Stand 2026-07-28. Verifizieren Sie exakte Versionen und Nutzungsdetails anhand dieser primären Materialien.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
