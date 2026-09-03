---
title: "MACRO: Structured Multi-Reference Image Data"
description: "MACRO is a structured multi-reference dataset, benchmark, and set of model-specific fine-tuning assets; validate the compatible base model and artifact terms before deployment."
category: models
tags: [multi-reference, dataset, benchmark, fine-tuning, bagel, omnigen2, qwen-image-edit]
aliases: ["MACRO-400K", "MacroData", "MacroBench"]
---

# MACRO: Structured Multi-Reference Image Data

**Scope checked: 2026-09-04.** MACRO is a research release for multi-reference image generation, not a new universal inference architecture. The authors publish structured data, a benchmark, training material, and checkpoints for selected open models so that a system can learn to use more than one reference image without relying solely on short-context training examples.

## What Is Released

The project describes a `400K`-sample data release with up to ten reference images per sample. It organizes examples across four complementary task families:

| Task family | What the references are intended to provide |
|---|---|
| Customization | subjects, identity, objects, or visual attributes |
| Illustration | multimodal context for a requested composition |
| Spatial | view, geometry, or scene relationships |
| Temporal | visual state across time |

`MacroBench` evaluates those scenarios, and the repository supplies model-specific paths for Bagel, OmniGen2, and Qwen-Image-Edit. The data and benchmark make a useful evaluation substrate; they do not establish that an arbitrary model accepts ten images or that it will preserve every reference faithfully.

## Choose a Compatible Route

Use the exact route maintained by the project:

1. choose one supported base model and its documented revision;
2. follow that model's preprocessing, resolution budget, prompt syntax, and checkpoint loading path;
3. use the matching MACRO checkpoint or training configuration rather than mixing adapter formats;
4. keep a baseline run from the unmodified base model for the same task fixture.

The reference count changes the image-token budget. MACRO's implementation dynamically reduces input-image resolution as more references are supplied. Do not apply a fixed pixel budget from an old tutorial to a different base model; inspect the current configuration and measure whether critical details survive the resize.

## Evaluate the Real Task

Multi-reference generation has several independent failure modes: subject mixing, lost small details, incorrect relationships, selective copying, and a plausible but unfaithful output. Build an acceptance fixture that names which reference controls which result attribute, then inspect the output against that mapping.

MacroBench uses an LLM-based scoring workflow. It can be a repeatable research signal, but it is not a replacement for human review, rights checks, or task-specific validators in a production workflow. Retain prompts, input ordering, model revision, random seed where applicable, and generated artifacts with each comparison.

## Data, Rights, and Release Terms

The project documents a data-construction pipeline and provides released artifacts, but the provenance and terms of every input, base model, checkpoint, and downstream output remain separate questions. In particular:

- read the license and model card for the selected base model and MACRO artifact;
- verify whether the intended deployment and redistribution are allowed;
- use only reference images that the operator is authorized to process;
- do not infer commercial permission for every component from the availability of the repository.

## References

- [MACRO official repository](https://github.com/HKU-MMLab/Macro)
- [MACRO paper](https://arxiv.org/abs/2603.25319)
- [MACRO project page](https://macro400k.github.io/)
