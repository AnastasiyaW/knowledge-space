---
title: "Praktisches LLM-Fine-Tuning"
description: "Ein auf Releases ausgerichteter Fine-Tuning-Workflow für überwachte Anpassung, PEFT, Evaluation und reproduzierbare Artefakte"
level: 3
source_sha256: a78afadae6fbf566c63c878b039285c543763f282c10cf24a7f7809e89b7ae46
translation: machine
translated_at: '2026-10-24'
---
# Praktisches LLM-Fine-Tuning (September 2026) {#practical-llm-fine-tuning-september-2026}

Versionskontext: Die Fine-Tuning-Berechtigung bei Anbietern und die Request-Strukturen der SDKs ändern sich häufig. Behandeln Sie die aktuell dokumentierte Anbieterfunktion, die Modellrevision, den Dataset-Digest und die Evaluation-Suite als ein versioniertes Experiment.

Fine-Tuning passt Verhalten anhand von Beispielen an. Es ist nicht der Standardweg, um sich schnell ändernde Fakten hinzuzufügen; verwenden Sie Retrieval oder eine gepflegte Datenquelle, wenn die Aktualität von Fakten die Anforderung ist.

## Entscheidungskriterium {#decision-gate}

Führen Sie Fine-Tuning erst durch, nachdem eine Baseline ein messbares Defizit nachgewiesen hat.

| Signal | Typischerweise wählen |
|---|---|
| Ausgabeformat, Tonalität, Routing oder wiederholte domänenspezifische Transformation | Fine-Tuning kann helfen |
| Häufig wechselndes Wissen oder dokumentbasierte Antworten | Retrieval / Tools |
| Unzureichendes Schlussfolgern bei einer breiten Aufgabe | Aufgabendesign verbessern oder ein stärkeres Basismodell wählen |
| Spärliche, inkonsistente oder ungeprüfte Beispiele | Daten vor dem Training verbessern |
| Keine Held-out-Evaluation und kein Release-Schwellenwert | Noch nicht trainieren |

Das erforderliche Entscheidungsartefakt ist ein Baseline-Bericht: Modellrevision, Prompt-Policy, Digest der Testmenge, Metriken, Kosten, Latenz und Fehlerkategorien.

## Dataset-Vertrag {#dataset-contract}

Jedes Beispiel muss auf seine Quelle, die Lizenz- bzw. Einwilligungsgrundlage, den Split und die Revision der Transformation rückführbar sein. Halten Sie Trainings- und Evaluationsdatensätze getrennt, bevor eine manuelle Bereinigung erfolgt.

```json
{
  "experiment_id": "support-routing-sft-2026-09-03",
  "base_model": {"id": "provider-or-model-id", "revision": "immutable-revision"},
  "dataset": {
    "train_digest": "sha256:...",
    "eval_digest": "sha256:...",
    "schema": "messages-v1",
    "redaction_policy": "pii-redaction-v2"
  },
  "acceptance": {
    "primary_metric": "validated_route_accuracy",
    "minimum_delta": 0.03,
    "safety_regressions": 0
  }
}
```

Für konversationelles überwachtes Fine-Tuning erleichtert ein stabiles `messages`-Schema sowohl beim anbietergesteuerten als auch beim Open-Stack-Training die Validierung:

```json
{
  "messages": [
    {"role": "user", "content": "Cancel my subscription."},
    {"role": "assistant", "content": "{\"route\":\"retention\",\"priority\":\"normal\"}"}
  ]
}
```

## Datenprüfungen vor dem Training {#data-checks-before-training}

- Entfernen Sie nahezu identische Datensätze über Trainings- und Evaluationspartitionen hinweg.
- Prüfen Sie, ob die Zielantwort autorisiert, sicher und mit der aktuellen Policy konsistent ist.
- Bewahren Sie schwierige Fehlerfälle und Negativbeispiele; trainieren Sie nicht nur auf geschliffenen Idealfällen.
- Validieren Sie das Inferenz-Chat-Template gegen die Trainingsrepräsentation.
- Erstellen Sie Slice-Labels für kritische Kohorten, Sprachen, Quellen und sicherheitsrelevante Intents.

Ein niedrigerer Trainingsverlust ist kein Release-Nachweis. Nachweisend ist die Held-out-Aufgabensuite.

## Überwachtes Fine-Tuning mit PEFT {#supervised-fine-tuning-with-peft}

Der aktuelle TRL-`SFTTrainer` akzeptiert Daten für Sprachmodellierung oder Prompt-Completion und kann einen PEFT-Adapter aus `LoraConfig` initialisieren. Das Beispiel verwendet einen kleinen, dokumentierten Modellbezeichner; Anforderungen an Hardware, Pakete und Modellzugriff gelten weiterhin.

```python
from datasets import Dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

train = Dataset.from_list([
    {
        "messages": [
            {"role": "user", "content": "Classify: refund requested twice"},
            {"role": "assistant", "content": "{\"route\":\"billing\",\"priority\":\"high\"}"},
        ]
    }
])

args = SFTConfig(
    output_dir="artifacts/support-routing-sft",
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    logging_steps=1,
    save_strategy="no",
)

trainer = SFTTrainer(
    model="Qwen/Qwen3-0.6B",
    args=args,
    train_dataset=train,
    peft_config=LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    ),
)
trainer.train()
```

QLoRA kombiniert eine quantisierte Ladung des Basismodells mit einem trainierbaren PEFT-Adapter. Die genaue Quantisierungskonfiguration und die unterstützte Hardware müssen im Experiment-Manifest festgehalten werden und dürfen nicht unbesehen zwischen Modellfamilien übernommen werden.

## Evaluation und Release-Gate {#evaluation-and-release-gate}

Vergleichen Sie den Kandidaten mit der Baseline anhand desselben eingefrorenen Evaluationssatzes.

| Prüfung | Erforderlicher Nachweis |
|---|---|
| Primäre Aufgabenqualität | Aggregierte Metrik und gelabelte Fehlerprüfung |
| Kritische Slices | Ergebnisse pro Slice, nicht nur ein Durchschnitt |
| Sicherheit und Policy | Regressionssuite und Ablehnungsverhalten |
| Formateinhaltung | Schemavalidierung der Ausgaben |
| Kosten und Latenz | Gemessenes Serving-Protokoll |
| Reproduzierbarkeit | Basisrevision, Adapter-Digest, Daten-Digests, Konfiguration, Seed |

Veröffentlichen Sie einen Adapter nur zusammen mit einer Model Card oder einem gleichwertigen Nachweis, der das kompatible Basismodell benennt. Ein Adapter ohne seine Basismodellrevision ist kein deploybares Artefakt.

## Verwaltete Fine-Tuning-Dienste {#managed-fine-tuning-services}

Für einen anbietergesteuerten Job verwenden Sie den aktuellen Optimierungsleitfaden des Anbieters, um ein unterstütztes Modell und Verfahren auszuwählen. Halten Sie Job-ID des Anbieters, Digest der hochgeladenen Datei, Evaluationskonfiguration, Ergebnis-Modell-ID und Abnahmeurteil im selben unveränderlichen Release-Datensatz fest.

Legen Sie keine Anbieter-Tokens, Kundeninhalte oder rohen Produktionsunterhaltungen in Trainingsdateien ab, ohne eine ausdrückliche Datenrichtlinie und Prüfung.

## Stolperfallen {#gotchas}

- **Eine gute Trainingskurve kann ein schlechtes Release verbergen.** Die Optimierung sieht Trainingsbeispiele; Nutzer sehen neue Eingaben. **Lösung:** Halten Sie realistische, versionierte Evaluationsdaten zurück und blockieren Sie das Release bei Regressionen in einzelnen Slices.
- **Das Chat-Template ist Teil des Modellvertrags.** Wenn man mit einem Rollenformat trainiert und mit einem anderen bedient, verschieben sich Token-Grenzen und das Verhalten ändert sich. **Lösung:** Validieren Sie das exakt serialisierte Inferenzformat vor dem Training.
- **Loss-Masking ist nicht universell verfügbar.** Loss nur auf Assistentenantworten hängt in der aktuellen TRL-Version von der Unterstützung durch das Chat-Template ab. **Lösung:** Prüfen Sie das gerenderte Template und testen Sie die beabsichtigte Loss-Maske an einem repräsentativen Batch.
- **Ein LoRA-Adapter ist nicht eigenständig.** Er hängt von einem exakten Basismodell und mitunter von einer Quantisierungs- bzw. Laufzeitkonfiguration ab. **Lösung:** Veröffentlichen Sie Basisrevision, Adapter-Digest, Loader-Konfiguration und Evaluationsnachweis gemeinsam.

## Quellen {#sources}

- [OpenAI model optimization guide](https://developers.openai.com/api/docs/guides/model-optimization)
- [Hugging Face TRL SFTTrainer documentation](https://huggingface.co/docs/trl/sft_trainer)
- [Hugging Face TRL PEFT integration](https://huggingface.co/docs/trl/peft_integration)
- [Hugging Face PEFT quicktour](https://huggingface.co/docs/peft/quicktour)

## Siehe auch {#see-also}

- [[fine-tuning]]
- [[model-optimization]]
- [[rag-pipeline]]
- [[agent-evaluation]]
