---
title: Diffusion LoRA Training: Evidence and Compatibility Contract
description: "Diffusion LoRA training is a version-bound adapter experiment; bind the exact base checkpoint, architecture, runtime, adapter format, authorized data, and evaluation split, and select rank, schedule, targets, and optimizer only from measured held-out behavior rather than copied recipes."
category: techniques
tags: [lora, fine-tuning, diffusion, adapters, provenance, evaluation, training]
aliases: ["LoRA Training Pipeline", "Diffusion Fine-Tuning"]
---

# Diffusion LoRA Training: Evidence and Compatibility Contract

A LoRA is not a portable style file or a recipe defined by a number of images,
rank, learning rate, or steps. It is an adapter trained against a specific
base architecture and runtime. Training parameters are experimental inputs
whose value must be judged on held-out behavior for the named task.

## Pin the adapter contract

Before training, record:

- base model/checkpoint and component digests, architecture revision, VAE or
  image encoder, tokenizer/text encoder, and image-conditioning path;
- trainer/runtime, dependency versions, target modules, adapter method,
  precision, preprocessing, and checkpoint serialization format;
- intended inference runtime and loader, including its supported adapter
  format and loading order; and
- license, authorized use, output policy, and revision of every upstream
  artifact.

[PEFT checkpoint guidance](https://huggingface.co/docs/peft/developer_guides/checkpoint)
requires adapter weights and adapter configuration when converting into its
format. That illustrates why an adapter file alone is not a compatibility
claim. Test loading and a known baseline output with the exact production
runtime before interpreting a training result.

## Define the data authority

Keep source rights, consent where a person is depicted, caption/annotation
provenance, and the intended task for every sample. A style/domain collection,
a source-to-target edit pair, and a reference-conditioned task provide
different supervision; do not relabel one as another to make an experiment
look paired.

Split data by original asset, capture session, subject/product, and derivative
chain. Near-duplicate crops, multiple edits of one source, and generated
derivatives belong in the same split. Retain uncertainty and exclusion labels
instead of treating all internet imagery or synthetic images as authorized
ground truth.

## Select parameters by measurement

Rank, target layers, learning rate, optimizer, batch/accumulation, resolution,
caption policy, and stopping point depend on the pinned model and task. Start
from the named trainer/model documentation, establish a reproducible baseline,
and vary a bounded configuration with a retained experiment receipt.

[Diffusers training documentation](https://huggingface.co/docs/diffusers/training/overview)
provides example scripts, each with its own requirements. It does not
establish a universal parameter recipe for every diffusion architecture.
Similarly, BFL documents [klein Base models](https://docs.bfl.ai/flux_2/flux2_klein_training)
as appropriate starting points for fine-tuning; that does not certify a
community trainer, rank, optimizer, or adapter as compatible without an
artifact-level test.

## Bind precision and data loading separately

PyTorch 2.14 documentation distinguishes autocast from gradient scaling.
Scaling addresses FP16 gradient underflow; it is not a generic switch for every
reduced-precision run. For a trainer's supported CUDA path, enable its scaler
for FP16, not automatically for BF16. A full-precision CPU fallback must not
enter a CUDA autocast context. CPU BF16 is a separate supported-op choice,
not an assumption made when CUDA is absent.
[AMP reference](https://docs.pytorch.org/docs/2.14/amp.html).

Start an unverified iterable input pipeline with `num_workers=0`. Before adding
workers, prove that replicas partition the intended samples and that throughput
improves without unacceptable host-memory growth. Record sample IDs/counts as
well as batches: a faster duplicated stream is not a training improvement.
Use worker-aware partitioning through `get_worker_info()` or `worker_init_fn`
where appropriate; configure prefetching and persistent workers only for a
multi-process loader. [DataLoader reference](https://docs.pytorch.org/docs/2.14/data.html).

## Evaluate the requested change and preservation

Use source-disjoint prompts/images that were not used to choose parameters.
Review separately:

| Question | Evidence |
|---|---|
| Does the requested concept or edit occur? | task-specific held-out evaluation and approved visual review |
| What should stay unchanged? | identity, product geometry, text, masks, background, color, or other declared protected regions |
| Does the adapter load correctly? | exact base/runtime load receipt and deterministic or reviewed smoke examples |
| Is it stable? | repeated seeds/inputs, failure capture, and comparison with the pinned base baseline |

High apparent style strength is not evidence of correct editing, factual
recovery, identity preservation, or license compliance.

## Release boundary

Publish an adapter only with its base/runtime contract, data authority,
adapter/configuration files, evaluation receipt, known failure modes, and
license/distribution evidence. If compatibility, rights, or preservation
cannot be shown, keep it private for evaluation or mark it as a reviewed
visual experiment rather than a reusable production adapter.

## Gotchas

- **A green CPU smoke test is called a GPU training result:** retain its CPU-only
  boundary; verify the selected accelerator, dtype and optimizer path in the
  actual training run before making that claim.
- **More loader workers repeat examples:** check per-worker sample ownership
  before interpreting throughput or epoch counters.
- **BF16 inherited an FP16 scaler setting:** bind the scaler to the trainer's
  actual dtype contract rather than copying a mixed-precision recipe.

## Related pages

- [[lora-fine-tuning-for-editing-models]]
- [[flux-klein-9b-architecture]]
- [[flux-klein-character-lora]]
- [[paired-training-for-restoration]]
