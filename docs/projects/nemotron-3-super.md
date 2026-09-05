---
title: Nemotron 3 Super
category: projects
date: 2026-03-12
tags: [llm_releases, nemotron-3-super, project]
aliases: ["Nemotron 3 Super"]
---

# Nemotron 3 Super

**Development line:** `project:nemotron-3-super` · thread `nemotron-3-super`  
**Last event:** 2026-03-12 · 1 dated since 2026-03-12 · **Researched:** 2026-09-05 · confidence: high

## What it is

Nemotron 3 Super — открытая гибридная Mamba-Transformer MoE-модель NVIDIA для команд, строящих агентные системы, программирование и длинный контекст. Способности: reasoning, tool calling, код, контекст до 1 млн токенов. Мера: 120B параметров всего, 12B активных; BF16-веса занимают 247 GB. Вердикт: подходит для сервинга или API-интеграции крупных агентных задач, но не для типичной одиночной локальной GPU.

## Development line

- **2026-03-12 — NVIDIA announced Nemotron 3 Super.** 120B/12B-active, гибридный Mamba-Transformer Latent MoE с MTP, окном 1M токенов, открытыми весами, датасетами и рецептами; первичный анонс датирован 2026-03-11, поэтому дата события фиксирует появление ссылки, а не дату публикации NVIDIA. Дополнение к этому шагу: NVIDIA указывает RL в 21 конфигурации сред и более 1,2 млн rollout-ов.

## What changed

2026-03-12 — выпущен NVIDIA-Nemotron-3-Super-120B-A12B: 120B/12B-active, гибридный Mamba-Transformer Latent MoE с MTP, окном 1M токенов, открытыми весами, датасетами и рецептами; первичный анонс датирован 2026-03-11, поэтому дата события фиксирует появление ссылки, а не дату публикации NVIDIA. Дополнение к этому шагу: NVIDIA указывает RL в 21 конфигурации сред и более 1,2 млн rollout-ов. 2026-03-25 — NVIDIA сообщила об исправлениях стримингового force_nonempty_content и tool calling с qwen3coder parser в vLLM и TensorRT-LLM; для anyOf tool call должен возвращаться объект, а не строка. Это отдельное последующее изменение, не часть запуска 12 марта.

## How to use this

Starting 2026-03-12, practitioners evaluating agentic-reasoning models should add Nemotron 3 Super to their evaluation shortlist and consult the linked model and cookbook resources to assess deployment fit; this unresearched branch does not establish benchmark or licensing conclusions.

1. Для локального прототипа загрузите BF16-чекпойнт через Transformers с trust_remote_code=True либо запустите vLLM-сервер с именем модели; обращайтесь к нему через OpenAI-совместимый /v1/chat/completions API.
  — <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/tree/main>
2. Для агентного кодинга через OpenRouter задайте модель nvidia/nemotron-3-super-120b-a12b:free и ограничьте контекст и output в конфигурации агента.
  — <https://docs.nvidia.com/nemotron/latest/usage-cookbook/Nemotron-3-Super/OpenScaffoldingResources/README.html>
3. Для воспроизводимого обучения или адаптации используйте репозиторий Nemotron, uv sync и поэтапный пайплайн pretrain, SFT, RL и eval на Slurm-кластере.
  — <https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/README.md>

## Best practices

- Для Hopper выбирайте опубликованный FP8 checkpoint, а для Blackwell — NVFP4; не переносите ожидания производительности между ними без измерения на своём железе.
  — <https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/quantization.md>
- Если используете qwen3coder tool parser или streaming, закрепите версии с исправлениями: vLLM 0.18.0 либо совместимый TensorRT-LLM/NIM-релиз, затем проверьте структуру anyOf tool call в интеграционном тесте.
  — <https://github.com/NVIDIA-NeMo/Nemotron/discussions/124>

## Superseded by this

- 2026-03-25 — прежнее предположение, что streaming force_nonempty_content работает и qwen3coder anyOf tool calls всегда имеют объектную структуру, устарело: требуются исправленные серверные версии.
- 2026-03-12 — прежний Nemotron Super заменён как ориентир производительности новым Nemotron 3 Super; NVIDIA заявляет более чем 5× throughput, но это не универсальная гарантия для иной конфигурации.

## Still unknown

- Схема ответа не содержит обязательные в задании поля event_findings и new_events; их факты сохранены соответственно в what_changed как дополнение к событию 2026-03-12 и как отдельная дата 2026-03-25.
- Не проверялись доступность, лимиты и условия бесплатного маршрута OpenRouter на момент использования; они могут измениться.
- Показатель PinchBench 85,6% — заявление NVIDIA о конкретном бенчмарке, а не независимая гарантия качества в вашей агентной среде.

## Sources

| source | title | read |
|---|---|---|
| https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/ | Introducing Nemotron 3 Super: An Open Hybrid Mamba-Transformer MoE for Agentic Reasoning | 2026-09-05 |
| https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/tree/main | nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 | 2026-09-05 |
| https://docs.nvidia.com/nemotron/latest/usage-cookbook/Nemotron-3-Super/OpenScaffoldingResources/README.html | Nemotron 3 Super with Agentic Coding Tools | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/README.md | Nemotron 3 Super Training Recipe | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/super3/quantization.md | Nemotron 3 Super Quantization | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Nemotron/discussions/124 | Nemotron 3 Super Improvements and Fixes | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:nemotron-3-super`, thread `nemotron-3-super`, 1 dated events 2026-03-12 → 2026-03-12.
- **Practical note:** Starting 2026-03-12, practitioners evaluating agentic-reasoning models should add Nemotron 3 Super to their evaluation shortlist and consult the linked model and cookbook resources to assess deployment fit; this unresearched branch does not establish benchmark or licensing conclusions.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
