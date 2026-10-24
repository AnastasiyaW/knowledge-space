---
title: "Feinabstimmung und LoRA"
description: "Feinabstimmung über evaluationsorientierte Verträge, reproduzierbare Datensätze und parameter-effizientes Training auswählen, durchführen und freigeben."
tags: [llm-agents, fine-tuning, lora, qlora, peft, evaluation]
level: 3
source_sha256: 4e2c8baa683a3421ea6b233c29dcdd966a3ccd004a1f0efd92f6d25d072edbbc
translation: machine
translated_at: '2026-10-24'
---
# Feinabstimmung und LoRA (September 2026) {#fine-tuning-and-lora-september-2026}

Versionskontext: Modellverfügbarkeit, verwaltete Feinabstimmungszugänge, Trainer-APIs und Hardwareunterstützung ändern sich schnell. Erfassen Sie für jeden Lauf die genaue Revision des Basismodells, Tokenizer/Chat-Template, Bibliotheksversionen, Datensatzrevision und Evaluationssuite. Leiten Sie die aktuelle Verfügbarkeit bei Anbietern nicht aus einem alten Code-Beispiel ab.

Feinabstimmung verändert das Verhalten eines Modells. Sie ersetzt weder aktuelle Fakten, Autorisierung, Retrieval-Qualität, Tool-Sicherheit noch ein Release-Gate. Beginnen Sie mit einem messbaren Problem und bewahren Sie vor dem Training ein unberührtes Evaluationsset auf.

## Vor dem Training entscheiden {#decide-before-you-train}

| Bedarf | Erster Kandidat | Warum |
|---|---|---|
| Aktuelle oder private Fakten | Retrieval oder ein kontrolliertes Datenwerkzeug | Fakten lassen sich ohne Neutraining aktualisieren |
| Klareres Verhalten für Einzelfälle | Überarbeitung von Prompt/Instruktion | Geringste betriebliche Kosten |
| Stabile Formatierung, Stil, Klassifikation oder wiederholbares Aufgabenverhalten | Feinabstimmung nach einer Baseline | Training kann die Prompt-Länge verringern und die Konsistenz verbessern |
| Präferenz zwischen gültigen Ausgaben | Preference Optimization, sofern unterstützt | Labels können ausdrücken, welche Antwort bevorzugt wird |
| Reasoning mit hohem Risiko | Evaluation plus Workflow-/Tool-Design | Training macht ein ungeprüftes Ergebnis nicht sicher |

Die Entscheidung ist empirisch. Eine Feinabstimmung ist nur gerechtfertigt, wenn sie ein repräsentatives Held-out-Evaluationsset gegenüber einer dokumentierten Baseline verbessert und ihre Betriebskosten akzeptabel sind.

## Den Experimentvertrag festlegen {#freeze-the-experiment-contract}

Erfassen Sie vor dem Anlegen eines Jobs das Problem und die Freigaberegel:

```json
{
  "run_id": "sft-2026-09-003",
  "base_model_revision": "approved-model-revision",
  "tokenizer_and_template_revision": "chat-template@42",
  "train_dataset_revision": "data:sha256:...",
  "eval_dataset_revision": "data:sha256:...",
  "baseline": "prompt-v7",
  "primary_metric": "schema_valid_and_human_approved",
  "promotion_rule": "beats baseline without safety regression"
}
```

Halten Sie Trainings-, Validierungs- und Release-Testbeispiele disjunkt. Der Release-Test muss Produktionseingaben ähneln, einschließlich schwieriger und richtlinienrelevanter Fälle, darf aber nicht zur Abstimmung von Hyperparametern verwendet werden.

## Die Trainingsdaten sind das Produkt {#training-data-is-the-product}

Jedes Beispiel muss das Verhalten vermitteln, das zur Inferenzzeit erwartet wird. Verwenden Sie dieselben Rollen, denselben Ausgabevertrag, dieselbe Darstellung von Tools und Tool-Ergebnissen, dieselbe Sprache und denselben Detailgrad, die die Produktion verwenden wird.

```json
{"messages":[{"role":"system","content":"Return a JSON support triage record."},{"role":"user","content":"My order arrived damaged."},{"role":"assistant","content":"{\"category\":\"damage\",\"needs_human\":true}"}]}
```

Die Datenprüfung sollte Folgendes kontrollieren:

- Einwilligung, Lizenzierung, Datenschutz, Aufbewahrung und Mandantengrenzen;
- doppelte oder nahezu doppelte Beispiele;
- widersprüchliche Labels und unbelegte Aussagen;
- vergiftete Anweisungen oder von Modellen erzeugte Fehler, die als Wahrheit dargestellt werden;
- Überrepräsentation einfacher Fälle;
- Leckagen von Tests, Zugangsdaten, internen Kennungen oder zukünftigen Daten.

Legen Sie keine geheimen Produktions-Prompts oder rohen Kundendatensätze in eine Trainingsdatei, nur weil ein Anbieter JSONL akzeptiert.

## Evaluation vor und nach dem Training {#evaluation-comes-before-and-after-training}

Messen Sie zuerst die Baseline. Führen Sie dann dasselbe eingefrorene Testset für jeden Kandidaten aus. Erfassen Sie mindestens eine Metrik für die Aufgabenqualität, eine Sicherheits-/Richtlinienmetrik und eine Betriebsmetrik.

| Kategorie | Beispielsignal |
|---|---|
| Aufgabenqualität | Exact Match, Schema-Gültigkeit, bewertete Bewertung durch freigegebene Prüfer oder domänenspezifische Rubrik |
| Sicherheit | Einhaltung von Ablehnung/Richtlinien, Widerstandsfähigkeit gegen Injection, Leckage sensibler Daten |
| Betrieb | Latenz, Token-Verbrauch, Fehlerrate, Speicherbedarf im Deployment, Kosten |
| Regression | Eingaben, bei denen die Baseline erfolgreich ist, der Kandidat aber scheitert |

Prüfen Sie Fehlerhäufungen, nicht nur einen einzelnen Durchschnitt. Ein Modell, das die Formatierung verbessert, aber die Sicherheit in Randfällen verschlechtert, besteht kein Release-Gate.

## Verwaltete Feinabstimmung ist eine bewegliche Oberfläche {#managed-fine-tuning-is-a-moving-surface}

Der aktuelle Leitfaden des Anbieters OpenAI zur Modelloptimierung beschreibt einen Zyklus aus Evals, Prompting, Verfeinerung der Trainingsdaten und erneuter Evaluation. Dort heißt es außerdem, dass die bisherige Feinabstimmungsplattform abgekündigt wird und neuen Nutzern nicht mehr zur Verfügung steht. Bestehende Verfügbarkeit, unterstützte Basismodelle und Abkündigungstermine müssen vor der Planung von Arbeiten in der aktuellen Dokumentation des Anbieters geprüft werden.

Speichern Sie für jede verwaltete Plattform die Job-ID, den Snapshot des Basismodells, den Hash des hochgeladenen Datensatzes, Methode, Hyperparameter, Validierungsergebnis sowie den Abkündigungs- und Ersatzplan. Treffen Sie niemals eine Deployment-Entscheidung allein auf Grundlage eines Modellalias.

## Parameter-effizientes Feintuning {#parameter-efficient-fine-tuning}

LoRA und verwandte PEFT-Methoden trainieren Adapter, während der größte Teil der Basisgewichte fixiert bleibt. Dies kann den Speicherbedarf für Optimierer und Gradienten gegenüber vollständiger Feinabstimmung senken, hebt aber die Notwendigkeit einer Evaluation nicht auf und ermöglicht keine Reproduktion eines Ergebnisses ohne fixierte Eingaben.

Eine minimale Form des überwachten Trainings mit aktuellen Hugging-Face-Bibliotheken:

```python
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

adapter_config = LoraConfig(
    task_type="CAUSAL_LM",
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules="all-linear",
)

trainer = SFTTrainer(
    model=model_id,
    train_dataset=train_dataset,
    args=SFTConfig(
        output_dir="runs/sft-2026-09-003",
        max_length=1024,
        num_train_epochs=1,
    ),
    peft_config=adapter_config,
)

trainer.train()
```

Die Modellarchitektur bestimmt die kompatiblen Zielmodule, die Chat-Formatierung, die Präzision, die Sequenzlänge und das Hardwareverhalten. Beginnen Sie mit einem Smoke-Lauf, der einen Batch lädt, einen Schritt trainiert, einen Batch evaluiert und ein Artefakt-Manifest schreibt, bevor Sie einen langen Lauf starten.

## QLoRA und Quantisierung {#qlora-and-quantization}

QLoRA kombiniert parameter-effiziente Adapter mit niedrigbittiger Ladung, damit ein Trainingsexperiment auf kleinerer Hardware Platz findet. Quantisierung ist ein Kompromiss zwischen Speicher und Durchsatz, kein Qualitätsnachweis.

Testen Sie jeden Kandidaten mit der Präzision und Sequenzlänge, die im Deployment verwendet werden. Schließen Sie die Gültigkeit strukturierter Ausgaben, das Verhalten bei langem Kontext, Sicherheitsfälle und die Genauigkeit für die Zielaufgabe ein. Eine Trainingskonfiguration mit geringerem Speicherbedarf kann trotzdem einen schlechteren Release-Kandidaten erzeugen.

## Release-Artefakt {#release-artifact}

Ein freigegebener Adapter oder eine verwaltete Feinabstimmung benötigt ein deploybares Manifest:

```json
{
  "candidate": "adapter-or-provider-model-id",
  "base_model_revision": "immutable-revision",
  "adapter_revision": "artifact:sha256:...",
  "tokenizer_revision": "artifact:sha256:...",
  "chat_template_revision": "artifact:sha256:...",
  "eval_receipt": "eval-2026-09-003",
  "rollback_target": "baseline-v7"
}
```

Betreiben Sie Basismodell, Adapter, Tokenizer, Template und Richtlinie als eine zueinander passende Release-Einheit. Bewahren Sie ein Rollback-Ziel auf und führen Sie die Release-Suite erneut aus, sobald ein Bestandteil dieser Einheit geändert wird.

## Stolpersteine {#gotchas}

- **Feinabstimmung aktualisiert kein Faktenwissen.** Sie kann veraltete Fakten sogar selbstsicherer formulieren. **Lösung:** Verwenden Sie für sich ändernde Informationen Retrieval oder ein kontrolliertes Datenwerkzeug.
- **Trainings- und Inferenzformate können auseinanderlaufen.** Ein anderer Tokenizer oder ein anderes Chat-Template kann einen gemessenen Gewinn zunichtemachen. **Lösung:** Fixieren und testen Sie das vollständige Serving-Bündel.
- **Ein zufälliger Split kann nahezu doppelte Beispiele durchlassen.** Die Ergebnisse überzeichnen dann die Generalisierung. **Lösung:** Teilen Sie gegebenenfalls nach Quelle, Nutzer, Dokument oder Zeitpunkt auf.
- **Training mit geringem Speicherbedarf ist kein Produktionsnachweis.** Quantisierung und Adapter können das Verhalten je nach Aufgabe verändern. **Lösung:** Evaluieren Sie die exakt eingesetzte Präzision und Kontextlänge.
- **Ein Anbieter-Endpunkt befindet sich möglicherweise im Übergang.** Verfügbarkeit der Feinabstimmung und zulässige Modelle können sich ändern. **Lösung:** Prüfen Sie den aktuellen Kontozugang und die Hinweise zur Abkündigung, bevor Sie darauf aufbauen.

## Quellen {#sources}

- [OpenAI model optimization and fine-tuning guidance](https://developers.openai.com/api/docs/guides/model-optimization)
- [OpenAI working with evals](https://developers.openai.com/api/docs/guides/evals)
- [Hugging Face PEFT documentation](https://huggingface.co/docs/peft/en/index)
- [Hugging Face TRL SFTTrainer](https://huggingface.co/docs/trl/en/sft_trainer)
- [bitsandbytes quick start](https://huggingface.co/docs/bitsandbytes/main/quickstart)
- [Transformers quantization documentation](https://huggingface.co/docs/transformers/quantization/bitsandbytes)

## Siehe auch {#see-also}

- [[model-optimization]]
- [[frontier-models]]
- [[ollama-local-llms]]
- [[rag-pipeline]]
- [[prompt-engineering]]
- [[agent-evaluation]]
