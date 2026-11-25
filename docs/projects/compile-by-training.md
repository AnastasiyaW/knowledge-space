---
title: "Compile By Training: compile-by-training — Compile By Training"
category: "projects"
date: 2026-09-05
tags: ["compile-by-training", "project"]
aliases: ["Compile By Training: compile-by-training"]
---

# Compile by Training

**Development line:** project:compile-by-training · thread compile-by-training  
**Last event:** 2026-09-05 · 1 dated since 2026-09-05 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Compile by Training is an open-source (MIT) compiler from the Program-as-Weights (PAW) project for building reusable .paw programs from text.

- Program generation: teacher models turn a natural-language function description into task-specific input-output examples.
- Interpreter finetuning: finetunes a small shared PAW interpreter (0.6B) on the examples and packages it as a .paw function.
- Local inference: runs locally without further teacher calls.

The repository cites an EMNLP 2026 System Demonstrations paper for the compiler.

## Development line

- **2026-09-05 — Compile-by-Training: Text-to-LoRA Neural Network Compiler.** Announces PAW (Program-as-Weights) technology to convert text descriptions into small local neural networks. Reports 83.6% semantic accuracy on FuzzyBench-Hard and integrations with a multi-site assistant, a 3D avatar, and a Claudish translator.
  - The repository confirms the pipeline. The fast PAW compiler initializes the program from the specification. Teacher models generate input-output pairs. The system finetunes the shared 0.6B interpreter on those examples and outputs a .paw function. Users download the interpreter once, and it runs locally. Command-line flags configure the teacher models and training settings. The repository links to a hosted playground. It lists the paper as 'Compile by Training: Turning Natural-Language Specifications into Local Neural Functions' (Deng, Nie, Shieber; EMNLP 2026 System Demonstrations). The repository page excerpt does not state the 83.6% FuzzyBench-Hard figure. (undated page) — <https://github.com/programasweights/compile-by-training>

## What changed

The compile-by-training repository and a hosted playground are now public. Users can build a local neural function from a text specification with one command (compile.py) and call it from the programasweights Python package.

## How to use this

1. Install Python 3.10+, uv, and set an OpenAI API key (export OPENAI_API_KEY=...). The default recipe targets an accelerator with about 40 GB of available memory.
  — <https://github.com/programasweights/compile-by-training>
2. Compile a description into a program: uv run compile.py "Classify sentiment. Return only positive, negative, or neutral." -o sentiment.paw. The script saves the .paw file, installs it in the local PAW cache, and prints its program ID.
  — <https://github.com/programasweights/compile-by-training>
3. Install the runtime with pip install programasweights --extra-index-url https://pypi.programasweights.com/simple/, then load the program with paw.function("<program-id>") and call it on an input string.
  — <https://github.com/programasweights/compile-by-training>
4. Optionally tune the recipe with flags like --teacher gpt-5.4-mini=800, --steps, --batch-size, --micro-batch-size, and --learning-rate. Run --print-config to inspect the defaults.
  — <https://github.com/programasweights/compile-by-training>

## Best practices

- On devices with less memory than the roughly 40 GB the default recipe assumes, lower --micro-batch-size or enable --gradient-checkpointing.
  — <https://github.com/programasweights/compile-by-training>
- Write the specification as an explicit input-to-output function with the exact output format, like 'Return only positive, negative, or neutral', as shown in the repository example.
  — <https://github.com/programasweights/compile-by-training>
- Rerun the same specification and recipe without penalty: mapper assets and completed teacher synthesis are cached, so the build reuses finished work. Setting PAW_API_KEY is optional and raises the hosted compile limits.
  — <https://github.com/programasweights/compile-by-training>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The 83.6% semantic accuracy on FuzzyBench-Hard is absent from the repository text, leaving the benchmark setup unverified.
- The linked pages do not confirm the roughly one-minute build time.
- The linked pages do not describe the multi-site assistant, the voice-controlled 3D avatar, or the English-to-Claudish translator integrations.
- The playground page content was unavailable beyond its title, leaving hosted demo behavior undocumented.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/programasweights/compile-by-training | GitHub - programasweights/compile-by-training: Compile natural-language function descriptions into reusable local PAW programs | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** project:compile-by-training, thread compile-by-training, 1 dated events 2026-09-05 → 2026-09-05.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
