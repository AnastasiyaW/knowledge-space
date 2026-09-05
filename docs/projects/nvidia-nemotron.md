---
title: Nemotron 3.5 Lightning
category: projects
date: 2026-08-12
tags: [nemotron-3-5-lightning, nvidia-nemotron, nvidia_nemotron, project]
aliases: ["Nemotron 3.5 Lightning"]
---

# Nemotron 3.5 Lightning

**Development line:** `project:nvidia-nemotron` · thread `nemotron-3-5-lightning`  
**Last event:** 2026-08-12 · 1 dated since 2026-08-12 · **Researched:** 2026-09-05 · confidence: high

## What it is

Nemotron 3.5 Lightning — текстовая гибридная MoE-модель с 30B общих и 3B активных параметров для разработчиков агентных систем, чат-ботов и RAG. Возможности: рассуждение с переключателем thinking, tool use, код, длинный контекст до 1M токенов, speculative decoding; доступны NVFP4 и BF16 варианты. Практический предел: NVFP4 checkpoint занимает около 22 GB; NVIDIA указывает запуск на одной DGX Spark или H100. Вердикт: это исполнительная модель для частых агентных вызовов, а не замена более крупной модели для сложного планирования.

## Development line

- **2026-08-12 — Nemotron 3.5 Lightning public model and playground resources surfaced.** Вышла NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 — коммерчески применимый 30B/3B-active гибрид Mamba-2/MoE/attention с контекстом до 1M токенов; вместе с ним представлены BF16, NVFP4, DSpark/DFlash для speculative decoding и маршрутизация через NeMo Switchyard. Первичная карточка модели датирует релиз 2026-08-11, поэтому событие 12 августа отражает следующий день публикации/распространения, а не отдельную модель.

## What changed

2026-08-12: вышла NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 — коммерчески применимый 30B/3B-active гибрид Mamba-2/MoE/attention с контекстом до 1M токенов; вместе с ним представлены BF16, NVFP4, DSpark/DFlash для speculative decoding и маршрутизация через NeMo Switchyard. Первичная карточка модели датирует релиз 2026-08-11, поэтому событие 12 августа отражает следующий день публикации/распространения, а не отдельную модель. 2026-08-17: NVIDIA опубликовала разбор QAD-рецепта NVFP4: checkpoint сжат примерно с 66 GB BF16 до 22 GB; это документация к уже вышедшему checkpoint, не новый базовый релиз.

## How to use this

From 2026-08-12, practitioners should treat Nemotron 3.5 Lightning as a line with public model artifacts, a hosted playground, and related Switchyard tooling; select the specific published model or deployment path from those resources rather than relying on an unverified repost.

1. Для быстрого прототипа вызовите NVIDIA Build API через OpenAI-совместимый клиент с именем модели `nvidia/nemotron-3.5-lightning-30b-a3b`; задайте `enable_thinking` и ограничьте reasoning budget под задачу.
  — <https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b>
2. Для self-hosting запустите NVFP4 checkpoint через vLLM или SGLang и используйте возвращаемое `/v1/models` имя в OpenAI-совместимом клиенте.
  — <https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4>
3. В агентной системе направляйте в Lightning массовые действия — вызовы инструментов, проверку результатов и форматирование — а сложное планирование оставляйте более сильной модели.
  — <https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/>

## Best practices

- Сначала измерьте базовый NVFP4/BF16 путь на собственных задачах; speculative decoding выбирайте по concurrency: DSpark рекомендован для DGX Spark и низкой concurrency, а MTP — для средней и высокой.
  — <https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/>
- Не используйте маршрутизацию как неявный fallback: задайте явные правила, какой класс задач идёт в Lightning, и проверяйте качество и стоимость маршрутов через Switchyard.
  — <https://github.com/NVIDIA-NeMo/Switchyard>
- Для жёсткого лимита памяти рассматривайте NVFP4; QAD-рецепт NVIDIA предназначен для восстановления качества после агрессивной квантизации и требует отдельной проверки на целевых agentic benchmarks.
  — <https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/>

## Superseded by this

- 2026-08-17: представление, что NVFP4 — только обычная post-training quantization, устарело для официального Lightning NVFP4 checkpoint: NVIDIA описывает QAD-дистилляцию поверх PTQ.
- 2026-08-12: для исполнения рутинных высокочастотных агентных шагов прежняя рекомендация назначать ту же крупную reasoning-модель на каждый вызов заменена архитектурой «планирование — сильная модель, исполнение — Lightning».

## Still unknown

- Нельзя по доступным первичным материалам установить точное время публикации всех пяти ссылок 12 августа; модельная карточка указывает release date 2026-08-11, поэтому расхождение в один день может быть следствием времени публикации или часового пояса.
- Заявления NVIDIA о скорости и бенчмарках не заменяют измерение на конкретном железе, версии сервера, concurrency и агентном harness.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 | NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 model card | 2026-09-05 |
| https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/ | NVIDIA Nemotron 3.5 Lightning Delivers Fast, Accurate Specialized Task Execution for Long-Running Agents | 2026-09-05 |
| https://build.nvidia.com/nvidia/nemotron-3.5-lightning-30b-a3b | nvidia/nemotron-3.5-lightning-30b-a3b on NVIDIA Build | 2026-09-05 |
| https://github.com/NVIDIA-NeMo/Switchyard | NVIDIA-NeMo/Switchyard | 2026-09-05 |
| https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/ | Developing Nemotron 3.5 Lightning NVFP4 with QAD Using NVIDIA Model Optimizer | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:nvidia-nemotron`, thread `nemotron-3-5-lightning`, 1 dated events 2026-08-12 → 2026-08-12.
- **Practical note:** From 2026-08-12, practitioners should treat Nemotron 3.5 Lightning as a line with public model artifacts, a hosted playground, and related Switchyard tooling; select the specific published model or deployment path from those resources rather than relying on an unverified repost.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
