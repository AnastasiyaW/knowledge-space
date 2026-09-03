---
title: "Fine-Tuning and LoRA"
description: "Choose, run, and release fine-tuning through evaluation-first contracts, reproducible datasets, and parameter-efficient training."
tags: [llm-agents, fine-tuning, lora, qlora, peft, evaluation]
---

# Fine-Tuning and LoRA (September 2026)

Version context: model availability, managed fine-tuning access, trainer APIs, and hardware support change quickly. Record the exact base-model revision, tokenizer/chat template, library versions, dataset revision, and evaluation suite for every run. Do not infer current provider availability from an old code sample.

Fine-tuning changes model behavior. It is not a substitute for current facts, authorization, retrieval quality, tool safety, or a release gate. Start with a measurable problem and preserve an untouched evaluation set before training.

## Decide Before You Train

| Need | First candidate | Why |
|---|---|---|
| Current or private facts | Retrieval or a controlled data tool | Facts can be updated without retraining |
| Clearer one-off behavior | Prompt/instruction revision | Lowest operational cost |
| Stable formatting, style, classification, or repeatable task behavior | Fine-tuning after a baseline | Training may reduce prompt length and improve consistency |
| Preference between valid outputs | Preference optimization where supported | Labels can express which answer is preferred |
| High-stakes reasoning | Evaluation plus workflow/tool design | Training does not make an unverified result safe |

The decision is empirical. A fine-tune is justified only if it improves a representative held-out evaluation relative to a documented baseline and its operating cost is acceptable.

## Freeze the Experiment Contract

Before creating a job, record the problem and the release rule:

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

Keep train, validation, and release-test examples disjoint. The release test must resemble production inputs, including difficult and policy-relevant cases, but it must not be used to tune hyperparameters.

## Training Data Is the Product

Each example must teach the behavior that will be expected at inference time. Include the same roles, output contract, tools or tool-result representation, language, and level of detail that production will use.

```json
{"messages":[{"role":"system","content":"Return a JSON support triage record."},{"role":"user","content":"My order arrived damaged."},{"role":"assistant","content":"{\"category\":\"damage\",\"needs_human\":true}"}]}
```

Data review should check for:

- consent, licensing, privacy, retention, and tenant boundaries;
- duplicate or near-duplicate examples;
- contradictory labels and unsupported claims;
- poisoned instructions or model-generated errors presented as truth;
- over-representation of easy cases;
- leakage of tests, credentials, internal identifiers, or future data.

Do not put secret production prompts or raw customer records into a training file merely because a provider accepts JSONL.

## Evaluation Comes Before and After Training

Measure the baseline first. Then run the same frozen test set against each candidate. Track at least one task-quality metric, one safety/policy metric, and one operational metric.

| Category | Example signal |
|---|---|
| Task quality | Exact-match, schema validity, approved reviewer score, or domain rubric |
| Safety | Refusal/policy compliance, injection resistance, sensitive-data leakage |
| Operations | Latency, token use, failure rate, deployment memory, cost |
| Regression | Inputs where baseline succeeds but the candidate fails |

Review error clusters, not only a single average. A model that improves formatting but worsens edge-case safety does not pass a release gate.

## Managed Fine-Tuning Is a Moving Surface

OpenAI's current model-optimization guide describes a cycle of evals, prompting, training data refinement, and re-evaluation. It also states that its legacy fine-tuning platform is being wound down and is not available to new users. Existing availability, supported base models, and deprecation dates must be checked in the current provider documentation before scheduling work.

For any managed platform, persist the job ID, base-model snapshot, uploaded dataset hash, method, hyperparameters, validation result, and deprecation/replacement plan. Never make a deployment decision from a model alias alone.

## Parameter-Efficient Fine-Tuning

LoRA and related PEFT methods train adapters while keeping most base weights fixed. This can reduce optimizer and gradient memory compared with full fine-tuning, but it does not eliminate the need for evaluation or reproduce a result without pinned inputs.

A minimal supervised-training shape with current Hugging Face libraries:

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

The model architecture determines compatible target modules, chat formatting, precision, sequence length, and hardware behavior. Start with a smoke run that loads one batch, trains one step, evaluates one batch, and writes an artifact manifest before committing a long run.

## QLoRA and Quantization

QLoRA combines parameter-efficient adapters with low-bit loading to make a training experiment fit smaller hardware. Quantization is a memory and throughput trade-off, not a quality certificate.

Test every candidate at the precision and sequence length that will be used in deployment. Include structured-output validity, long-context behavior, safety cases, and target-task accuracy. A lower-memory training configuration can still create a worse release candidate.

## Release Artifact

A promoted adapter or managed fine-tune needs a deployable manifest:

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

Serve the base model, adapter, tokenizer, template, and policy as one compatible release unit. Preserve a rollback target and re-run the release suite after changing any member of that unit.

## Gotchas

- **Fine-tuning does not update factual knowledge.** It can make stale facts more confidently expressed. **Fix:** use retrieval or a controlled data tool for changing information.
- **Training and inference formats can drift.** A different tokenizer or chat template can erase a measured gain. **Fix:** pin and test the full serving bundle.
- **A random split can leak near-duplicates.** Scores then exaggerate generalization. **Fix:** split by source, user, document, or time where appropriate.
- **Low-memory training is not a production proof.** Quantization and adapters can change behavior by task. **Fix:** evaluate the exact deployed precision and context length.
- **A provider endpoint may be in transition.** Fine-tuning availability and eligible models can change. **Fix:** verify current account access and deprecation guidance before designing around it.

## Sources

- [OpenAI model optimization and fine-tuning guidance](https://developers.openai.com/api/docs/guides/model-optimization)
- [OpenAI working with evals](https://developers.openai.com/api/docs/guides/evals)
- [Hugging Face PEFT documentation](https://huggingface.co/docs/peft/en/index)
- [Hugging Face TRL SFTTrainer](https://huggingface.co/docs/trl/en/sft_trainer)
- [bitsandbytes quick start](https://huggingface.co/docs/bitsandbytes/main/quickstart)
- [Transformers quantization documentation](https://huggingface.co/docs/transformers/quantization/bitsandbytes)

## See Also

- [[model-optimization]]
- [[frontier-models]]
- [[ollama-local-llms]]
- [[rag-pipeline]]
- [[prompt-engineering]]
- [[agent-evaluation]]
