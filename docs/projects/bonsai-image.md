---
title: Bonsai Image 4B — Bonsai Image development
category: projects
date: 2026-05-29
tags: [bonsai-image, project]
aliases: ["Bonsai Image 4B"]
---

# Bonsai Image 4B — Bonsai Image development

**Development line:** `project:bonsai-image` · thread `bonsai-image`  
**Last event:** 2026-05-29 · 1 dated since 2026-05-29 · **Researched:** 2026-09-05 · confidence: high

## What it is

Bonsai Image 4B: семейство text-to-image diffusion-моделей для локального запуска; Binary 1-bit — для минимального размера, Ternary — для лучшего качества; WebGPU-вариант остаётся экспериментальным. Предел: ternary-трансформер занимает 1,21 GB, а полный Apple Silicon payload — 3,88 GB. Вердикт: для локальной генерации следует начинать с ternary low-bit pack, а не с FP16-версии.

## Development line

- **2026-05-29 — Bonsai Image 4B was surfaced through Hugging Face resources.** On 2026-05-29, a dated record pointed readers to a Hugging Face collection for Bonsai Image and to a WebGPU Space associated with the project. This is treated as a material distribution and evaluation-access event because it identifies concrete public project resources. The links alone do not establish whether a model release, update, or benchmark occurred on that date.

## What changed

2026-05-26 — PrismML выпустила Bonsai Image 4B в двух вариантах: Binary 1-bit и Ternary. 2026-05-29 — ссылки на коллекцию весов и WebGPU-демо отражали доступность модели; первичный релиз уточняет базу FLUX.2 Klein 4B, размер 0,93 GB для Binary и 1,21 GB для Ternary diffusion transformer, а также локальные Apple Silicon и CUDA пути. 2026-06-01 — в коллекции появились платформенные low-bit packs и FP16 unpacked варианты; FP16 предназначен для совместимости с обычным Diffusers, не для экономии памяти или ускорения.

## How to use this

From 2026-05-29, practitioners can use the linked Hugging Face collection and WebGPU Space as starting points for locating and evaluating Bonsai Image 4B; they should not infer release status, capabilities, or usage guidance from these links alone.

1. Клонируйте Bonsai Image Demo и выполните setup для своей платформы: MLX на macOS либо gemlite/HQQ на Linux или Windows.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
2. Загрузите Ternary-вариант по умолчанию; выберите Binary, если важнее минимальный размер, чем качество.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
3. Запустите studio через scripts/serve или отправляйте запросы в уже запущенный backend через send_request, чтобы не оплачивать cold start на каждом изображении.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
4. Для экспериментального браузерного запуска откройте WebGPU-демо, загрузите Ternary model, укажите prompt и параметры; страница запрашивает Hugging Face access token.
  — <https://huggingface.co/spaces/webml-community/bonsai-image-webgpu>

## Best practices

- Используйте Ternary как стандартный вариант: официальный demo рекомендует его за лучшее качество при умеренном росте размера.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
- Не выбирайте unpacked FP16 safetensors ради локальной эффективности: они нужны как fallback для stock Diffusers и не сохраняют преимущества low-bit pack.
  — <https://huggingface.co/prism-ml/bonsai-image-ternary-4B-unpacked>
- Для браузерного демо рассматривайте совместимость как непроверенную вне Apple M4 Max и M5 Max; Chrome/Edge предлагает unsafe WebGPU flag только для производительности.
  — <https://webml-community-bonsai-image-webgpu.static.hf.space/index.html>

## Superseded by this

- 2026-06-01 — рекомендация использовать unpacked FP16 как основной путь устарела: официальные карточки рекомендуют optimized MLX или gemlite low-bit packs.

## Still unknown

- Первичный релиз датирован 2026-05-26, тогда как зафиксированный шаг — 2026-05-29; точная дата создания коллекции и WebGPU Space в просмотренных источниках не подтверждена.
- Требуемые поля event_findings и new_events отсутствуют в предоставленной выходной схеме; относящееся к событию уточнение и более ранний релиз отражены в what_changed.

## Sources

| source | title | read |
|---|---|---|
| https://prismml.com/news/bonsai-image-4b | Introducing 1-bit and Ternary Bonsai Image 4B: Image Generation for Local Devices | 2026-09-05 |
| https://huggingface.co/collections/prism-ml/bonsai-image | Bonsai Image - a prism-ml Collection | 2026-09-05 |
| https://huggingface.co/spaces/webml-community/bonsai-image-webgpu | Bonsai Image WebGPU - a Hugging Face Space by webml-community | 2026-09-05 |
| https://webml-community-bonsai-image-webgpu.static.hf.space/index.html | Bonsai image generation WebGPU demo | 2026-09-05 |
| https://huggingface.co/prism-ml/bonsai-image-ternary-4B-mlx-2bit | prism-ml/bonsai-image-ternary-4B-mlx-2bit | 2026-09-05 |
| https://huggingface.co/prism-ml/bonsai-image-ternary-4B-unpacked | Bonsai Image Ternary 4B — Unpacked FP16 Safetensors | 2026-09-05 |
| https://github.com/PrismML-Eng/Bonsai-image-demo | PrismML-Eng/Bonsai-Image-Demo | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:bonsai-image`, thread `bonsai-image`, 1 dated events 2026-05-29 → 2026-05-29.
- **Practical note:** From 2026-05-29, practitioners can use the linked Hugging Face collection and WebGPU Space as starting points for locating and evaluating Bonsai Image 4B; they should not infer release status, capabilities, or usage guidance from these links alone.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
