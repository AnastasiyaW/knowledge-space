---
title: SpatialClaw
category: projects
date: 2026-07-01
tags: [nvidia, project, spatialclaw, spatialclaw-development]
aliases: ["SpatialClaw"]
---

# SpatialClaw

**Development line:** `project:spatialclaw` · thread `spatialclaw-development`  
**Last event:** 2026-07-01 · 1 dated since 2026-07-01 · **Researched:** 2026-09-05 · confidence: high

## What it is

SpatialClaw — training-free фреймворк NVIDIA и KAIST для команд, проверяющих VLM на 3D, multi-view, video и 4D пространственных задачах; агент пишет ячейки Python в persistent Jupyter kernel, вызывает SAM3, Depth Anything 3, геометрию и NumPy/SciPy, изучает промежуточные результаты и затем возвращает ответ. Измерение: 59,9% средней точности на 20 бенчмарках, на 11,2 п.п. выше SpaceTools-Toolshed при сравнении на Gemma 4-31B. Вердикт: это воспроизводимый исследовательский runtime, а не лёгкая библиотека для обычного vision-приложения.

## Development line

- **2026-07-01 — SpatialClaw project references shared.** Training-free агент с code-as-action интерфейсом, persistent Python/Jupyter kernel, GPU-сервером восприятия и запусками как на одной GPU-машине, так и через SLURM.

## What changed

2026-07-01 — опубликованы официальный код и сайт SpatialClaw: training-free агент с code-as-action интерфейсом, persistent Python/Jupyter kernel, GPU-сервером восприятия и запусками как на одной GPU-машине, так и через SLURM.

Дополнение к событию 2026-07-01: репозиторий уточняет состав поставки — LangGraph runtime, AST-проверка ячеек, planning/reflection loops, 20 загрузчиков бенчмарков, FastAPI GPU tool server, vLLM discovery/load balancing и SLURM launch managers. Официальная статья от 2026-06-11 сообщает исходный результат: 59,9% на 20 бенчмарках и +11,2 п.п. относительно недавнего spatial agent.

## How to use this

From 2026-07-01, practitioners can use the project website and NVlabs repository as the dated primary starting points for evaluating SpatialClaw; this evidence alone supports no specific workflow change.

1. Клонировать репозиторий рекурсивно и запустить официальный setup-скрипт; он создаёт окружения агента, CUDA и vLLM.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
2. Подготовить Linux с NVIDIA GPU, CUDA 12.x, Conda и доступом к gated весам SAM3.1; для FP8-вариантов из статьи требуется Hopper/H100 или новее, а для A100/L40S документация указывает AWQ/GPTQ-варианты.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
3. Скопировать .env и выбрать backend: self-hosted vLLM либо OpenAI-compatible endpoint; задать model/dataset JSON и запустить spatial_agent.entrypoints.run.
  — <https://github.com/NVlabs/SpatialClaw>
4. Для SLURM сначала привести account, partition и memory limits в launch-конфигах к своему кластеру, затем заранее скачать VLM и perception weights на login node.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md>

## Best practices

- Всегда клонировать с --recursive либо отдельно инициализировать submodules: SAM3, Pi3, Depth-Anything-3 и map-anything закреплены конкретными ревизиями.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md>
- Перед SLURM-запуском скачать все веса заранее: compute jobs работают с HF_HUB_OFFLINE=1, и отсутствующий локальный артефакт завершит задачу ошибкой LocalEntryNotFoundError.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md>
- Не использовать HF-модельный путь как llm_model при llm_base_url=vllm: указать served_name из models.json; для внешнего OpenAI-compatible endpoint использовать его ожидаемый идентификатор модели.
  — <https://github.com/NVlabs/SpatialClaw/blob/main/docs/configuration.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Документация не указывает отдельный versioned release или tag, привязанный именно к 2026-07-01; дата относится к доступности проекта и кода в указанном событии, а не к подтверждённому GitHub Release.
- Лицензия репозитория — NVIDIA Source Code License-NC; пригодность для коммерческого использования нужно отдельно сверить с её полным текстом.

## Sources

| source | title | read |
|---|---|---|
| https://spatialclaw.github.io/ | SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw | NVlabs/SpatialClaw repository | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/installation.md | SpatialClaw Installation | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/running.md | SpatialClaw Running Experiments | 2026-09-05 |
| https://github.com/NVlabs/SpatialClaw/blob/main/docs/configuration.md | SpatialClaw Configuration & Benchmarks | 2026-09-05 |
| https://arxiv.org/abs/2606.13673 | SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:spatialclaw`, thread `spatialclaw-development`, 1 dated events 2026-07-01 → 2026-07-01.
- **Practical note:** From 2026-07-01, practitioners can use the project website and NVlabs repository as the dated primary starting points for evaluating SpatialClaw; this evidence alone supports no specific workflow change.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
