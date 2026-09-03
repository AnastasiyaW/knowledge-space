---
title: "Practical LLM Fine-Tuning"
description: "A release-oriented fine-tuning workflow for supervised adaptation, PEFT, evaluation, and reproducible artifacts"
---

# Practical LLM Fine-Tuning (September 2026)

Version context: provider fine-tuning eligibility and SDK request shapes change frequently. Treat the currently documented provider capability, model revision, dataset digest, and evaluation suite as one versioned experiment.

Fine-tuning adapts behavior from examples. It is not the default way to add fast-changing facts; use retrieval or a maintained data source when factual freshness is the requirement.

## Decision Gate

Fine-tune only after a baseline establishes a measurable shortfall.

| Signal | Usually choose |
|---|---|
| Output format, tone, routing, or repeated domain transformation | Fine-tuning may help |
| Frequently changing knowledge or document-grounded answers | Retrieval / tools |
| Insufficient reasoning on a broad task | Improve task design or choose a stronger base model |
| Sparse, inconsistent, or unreviewed examples | Improve data before training |
| No held-out evaluation or release threshold | Do not train yet |

The required decision artifact is a baseline report: model revision, prompt policy, test set digest, metrics, cost, latency, and failure slices.

## Dataset Contract

Each example must be traceable to its source, license/consent basis, split, and transformation revision. Keep training and evaluation records separate before any manual cleanup.

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

For conversational supervised fine-tuning, a stable `messages` schema makes both provider-managed and open-stack training easier to validate:

```json
{
  "messages": [
    {"role": "user", "content": "Cancel my subscription."},
    {"role": "assistant", "content": "{\"route\":\"retention\",\"priority\":\"normal\"}"}
  ]
}
```

## Data Checks Before Training

- Deduplicate near-identical records across train and evaluation partitions.
- Verify that the target answer is authorized, safe, and consistent with the current policy.
- Preserve difficult failures and negative cases; do not train only on polished happy paths.
- Validate the inference chat template against the training representation.
- Create slice labels for critical cohorts, languages, sources, and safety-sensitive intents.

A lower training loss is not release evidence. The held-out task suite is.

## Supervised Fine-Tuning with PEFT

The current TRL `SFTTrainer` accepts language-modeling or prompt-completion data and can initialize a PEFT adapter from `LoraConfig`. The example uses a small documented model identifier; hardware, package, and model-access requirements still apply.

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

QLoRA combines a quantized base-model load with a trainable PEFT adapter. Its exact quantization configuration and supported hardware must be recorded in the experiment manifest, not copied blindly between model families.

## Evaluation and Release Gate

Compare the candidate with the baseline using the same frozen evaluation set.

| Check | Required evidence |
|---|---|
| Primary task quality | Aggregate metric and labeled error review |
| Critical slices | Per-slice results, not only an average |
| Safety and policy | Regression suite and refusal behavior |
| Format compliance | Schema validation on outputs |
| Cost and latency | Measured serving record |
| Reproducibility | Base revision, adapter digest, data digests, config, seed |

Publish an adapter only with a model card or equivalent receipt that identifies the compatible base model. An adapter without its base-model revision is not a deployable artifact.

## Managed Fine-Tuning Services

For a provider-managed job, use the provider's current optimization guide to select a supported model and method. Keep the provider job ID, uploaded file digest, evaluation configuration, result model ID, and acceptance verdict in the same immutable release record.

Do not put provider tokens, customer content, or raw production conversations into training files without an explicit data policy and review.

## Gotchas

- **A good training curve can hide a bad release.** Optimization sees training examples; users see new inputs. **Fix:** hold out realistic, versioned evaluation data and block release on regression slices.
- **The chat template is part of the model contract.** Training one role format and serving another changes token boundaries and behavior. **Fix:** validate the exact serialized inference format before training.
- **Loss masking is not universal.** Assistant-only loss depends on chat-template support in current TRL. **Fix:** inspect the rendered template and test the intended loss mask on a representative batch.
- **A LoRA adapter is not self-contained.** It depends on an exact base model and sometimes a quantization/runtime configuration. **Fix:** publish the base revision, adapter digest, loader configuration, and evaluation receipt together.

## Sources

- [OpenAI model optimization guide](https://developers.openai.com/api/docs/guides/model-optimization)
- [Hugging Face TRL SFTTrainer documentation](https://huggingface.co/docs/trl/sft_trainer)
- [Hugging Face TRL PEFT integration](https://huggingface.co/docs/trl/peft_integration)
- [Hugging Face PEFT quicktour](https://huggingface.co/docs/peft/quicktour)

## See Also

- [[fine-tuning]]
- [[model-optimization]]
- [[rag-pipeline]]
- [[agent-evaluation]]
