---
title: "LTX-2.3 IC-LoRA Ingredients — LTX-2.3"
category: projects
date: 2026-06-19
tags: [ltx-2-3, ltx-2-3-ic-lora-ingredients, ltx_2_3, project]
aliases: ["LTX-2.3 IC-LoRA Ingredients"]
level: 2
source_sha256: ecffa62cd24e01f93b402c8a894f3c6db7b5d3a19e40ad5fba95cc54c0632c07
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.3 IC-LoRA Ingredients — LTX-2.3 {#ltx-23-ic-lora-ingredients-ltx-23}

**Entwicklungslinie:** `project:ltx-2-3-ic-lora-ingredients` · Thread `ltx-2-3`  
**Letztes Ereignis:** 2026-06-19 · 1 datiertes Ereignis seit 2026-06-19 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

LTX-2.3 IC-LoRA Ingredients ist ein IC-LoRA für Praktiker mit LTX-2.3-22B: Es nimmt ein zusammengesetztes Reference Sheet als statisches Video entgegen und erzeugt daraus einen neuen Clip anhand einer Textbeschreibung der Aktion. Funktionen: Konsistenz von Figuren, Kostümen, Requisiten und Schauplatz; Trennung von Sheet-Beschreibung und Aktion; Betrieb über den spezialisierten IC-LoRA-Workflow. Trainingsbucket: 768×448, 121 Frames, 24 fps. Fazit: Dies ist kein allgemeines T2V-Modul und kein Werkzeug zur Bearbeitung fertiger Videos, sondern ein eng gefasster Weg, wiederkehrende Szenenelemente konsistent zu halten.

## Entwicklungslinie {#development-line}

- **2026-06-19 — Lightricks veröffentlichte eine Modellseite für LTX-2.3 IC-LoRA Ingredients.** Am 2026-06-19 wurde in dieser Entwicklungslinie eine Hugging-Face-Modellseite für Lightricks' LTX-2.3-22B IC-LoRA Ingredients erfasst. Der datierte Link belegt ein eigenständiges LTX-2.3-Modellartefakt, die vorliegenden Belege klären jedoch weder Release Notes, Funktionen noch den empfohlenen Workflow.

## Was sich geändert hat {#what-changed}

2026-06-19 — Das Modell erschien im Zweig als LTX-2.3-22b-IC-LoRA-Ingredients; die Modellkarte präzisiert, dass es sich um eine Reference-Sheet-Steuerung für die Dev-Version von LTX-2.3-22B handelt, mit der Datei `ltx-2.3-22b-ic-lora-ingredients-0.9.safetensors`, Rank 128 und einem empfohlenen Checkpoint bei Schritt 12 000.

2026-06-17 — Ein Drittanbieter-Index datiert den offiziellen Release auf den 17. Juni, nicht auf den 19. Juni; der 19. Juni bleibt das Datum des erfassten Ereignisses, nicht ein bestätigtes Release-Datum.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-06-19 sollten Praktiker LTX-2.3-22B IC-LoRA Ingredients als eigenständig verfolgtes LTX-2.3-Modellartefakt behandeln und vor der Auswahl für einen Ingredients-bezogenen Workflow die Hugging-Face-Seite konsultieren.

1. Verschaffen Sie sich Zugang zum gated Repository, laden Sie das Ingredients LoRA sowie die kompatible LTX-2.3-22B-Basis herunter.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
2. Erstellen Sie ein einzelnes Reference Sheet auf schwarzem Hintergrund: getrennte, saubere Panels für Figuren, Requisiten und Schauplatz; wandeln Sie das Sheet in ein statisches Video um, dessen Auflösung und fps dem Ausgabeformat entsprechen und dessen Länge mindestens 121 Frames beträgt.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
3. Laden Sie in ComfyUI das Basismodell LTX-2.3-22B und das Ingredients LoRA über den IC-LoRA/Reference-Workflow und führen Sie danach das statische Video des Sheets in den Control-/Reference-Eingang ein.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
4. Schreiben Sie den Prompt in zwei Abschnitten: `Reference sheet:` für den Inhalt der Panels und `Generated video:` für die Aktion oder den Shot.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
5. Für einen reproduzierbaren Start verwenden Sie den offiziellen ComfyUI-Workflow, in dem `ltx-2.3-22b-dev.safetensors` und das Ingredients LoRA festgelegt sind.
  — <https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.3/LTX-2.3_ICLoRA_Ingredients_Single_Stage_Distilled.json>

## Best Practices {#best-practices}

- Beginnen Sie zur Prüfung der Pipeline mit einer LoRA-Stärke von 1.0; die Modellkarte empfiehlt 1.4 als Arbeitswert.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- Bleiben Sie im Trainingsbucket 768×448, 121 Frames, 24 fps; andere Auflösungen, deutlich längere Clips und Läufe ohne Reference Sheet liegen außerhalb der Trainingsverteilung.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- Geben Sie kritischen Figuren und Objekten große, saubere Panels; für Gesichter fügen Sie eine frontale Nahaufnahme und eine vollständige Drehung hinzu, ohne Text auf das Panel zu setzen.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- Verwenden Sie keinen gewöhnlichen LoRA-Loader, sofern dieser den Pfad zum Reference Video nicht übergibt: Er lädt die Gewichte, wendet das Reference Conditioning aber nicht an.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>

## Hiermit ersetzt {#superseded-by-this}

- 2026-06-17 — Die Annahme, dass Ingredients ein universelles Text-to-Video-Modell oder ein Editor für bestehende Clips sei, ist falsch: Es erfordert Reference-Sheet-Conditioning und erzeugt einen neuen Clip.
- 2026-06-17 — Die Empfehlung, einen kurzen Reference-Clip einzureichen, ist veraltet: Das statische Reference-Video muss mindestens 121 Frames umfassen.

## Weiterhin unbekannt {#still-unknown}

- Die am 2026-09-05 gelesene offizielle Modellkarte nennt kein eigenes Veröffentlichungsdatum; das Datum 2026-06-17 für den Release ist nur durch einen sekundären Index belegt.
- Es wurde keine datierte Primärquelle gefunden, die den Unterschied zwischen dem Ereignisdatum 2026-06-19 und dem Indexdatum 2026-06-17 erklärt.
- Die aktuelle Kompatibilität mit LTX-2.5 ist nicht bestätigt: Die offizielle LTX-Dokumentation warnt, dass ein LoRA nur mit dem Modell funktioniert, auf dem es trainiert wurde.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients | Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients Model Card | 2026-09-05 |
| https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.3/LTX-2.3_ICLoRA_Ingredients_Single_Stage_Distilled.json | LTX-2.3 IC-LoRA Ingredients Single Stage Distilled Workflow | 2026-09-05 |
| https://github.com/NitishMamadgi/awesome-ltx2.3-ic_lora | awesome-ltx2.3-ic_lora Index | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:ltx-2-3-ic-lora-ingredients`, Thread `ltx-2-3`, 1 datiertes Ereignis 2026-06-19 → 2026-06-19.
- **Praktischer Hinweis:** Stand 2026-06-19 sollten Praktiker LTX-2.3-22B IC-LoRA Ingredients als eigenständig verfolgtes LTX-2.3-Modellartefakt behandeln und vor der Auswahl für einen Ingredients-bezogenen Workflow die Hugging-Face-Seite konsultieren.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
