---
title: ComfyUI Sol-Attn — Blackwell and Triton implementations
category: projects
date: 2026-08-07
tags: [blackwell-and-triton-implementations, comfyui-sol-attn, project]
aliases: ["ComfyUI Sol-Attn"]
---

# ComfyUI Sol-Attn — Blackwell and Triton implementations

**Development line:** `project:comfyui-sol-attn` · thread `blackwell-and-triton-implementations`  
**Last event:** 2026-08-07 · 1 dated since 2026-08-07 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ComfyUI Sol-Attn — общее имя для двух community-расширений ComfyUI, которые подменяют attention в MiniMax H3 разреженным вариантом Sol-Attn. — Kijai: экспериментальный Triton-вариант, заявленно проверенный с MiniMax H3 на RTX 4090 и RTX 5090. — KingGore: вариант для RTX 5090 (SM120), использующий PyTorch flex_attention. Ограничение: измерение KingGore — 1,46× на 4K и 9,00× на 32K токенов против SDPA после прогрева, только для его MiniMax H3/RTX 5090 конфигурации. Вердикт: это инструмент для A/B-проверки длинных H3-рендеров, не универсальный ускоритель ComfyUI.

## Development line

- **2026-08-07 — ComfyUI Sol-Attn implementations for Blackwell and Triton were linked.** Triton-вариант Kijai и Blackwell-вариант KingGore.

## What changed

2026-07-27 — опубликована первая версия работы Sol-Attn: training-free разреженный attention с коррекцией пропущенных блоков. 2026-07-28 — NVIDIA выпустила upstream-ядра Sol-Attn для SM89/SM90/SM100/SM120 и интеграции HunyuanVideo-13B и Wan2.1-T2V-14B. 2026-08-04 — KingGore добавил v2 с точным attention для conditioning-префикса и плотными финальными шагами; Kijai принял исправление импорта для pre-SM90 GPU. 2026-08-06 — upstream Sol-Engine добавил MiniMax H3 на GB10 и RTX 5090; это не выпуск ComfyUI-ноды. 2026-08-07 — ComfyUI-ветка зафиксировала две самостоятельные реализации: Triton-вариант Kijai и Blackwell-вариант KingGore. 2026-08-17 — upstream Sol-Engine добавил оптимизированное SM89-ядро для RTX 4090; совместимость конкретной ноды Kijai остаётся её собственным вопросом.

## How to use this

As of 2026-08-07, practitioners evaluating ComfyUI Sol-Attn should distinguish the Blackwell-targeted implementation from the Triton-targeted implementation and verify environment compatibility before adopting either.

1. Для MiniMax H3 на RTX 5090 установите Blackwell-вариант в ComfyUI/custom_nodes и перезапустите ComfyUI; ему требуется PyTorch 2.6+ и CUDA 12.x или 13.x.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
2. Вставьте Sol-Attn MiniMax H3 Patcher между Load Diffusion Model и KSampler.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
3. Начните с tau=1.0; для Blackwell-варианта документирован диапазон 0.8–1.5. При артефактах включите dense_steps или step_off для плотного финала и exact_kv для точного conditioning-префикса.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>
4. Для Triton-варианта Kijai ограничьте первый тест MiniMax H3 на RTX 4090 или RTX 5090 и подберите start_percent, end_percent и tau на одинаковом seed.
  — <https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md>

## Best practices

- Не измеряйте первый запуск: Triton-компиляция происходит при первом использовании и делает его медленнее.
  — <https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md>
- Сравнивайте скорость и изображение на одной модели, seed, разрешении, числе шагов и GPU: даже upstream-измерения фиксируют все эти условия.
  — <https://github.com/NVlabs/Sana/tree/sol-engine>
- На MiniMax H3 сохраняйте финальные denoise-шаги плотными, если разреженный attention оставляет заметную ошибку; exact_kv даёт точный attention для conditioning-префикса примерно за 3% дополнительной стоимости.
  — <https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md>

## Superseded by this

- 2026-08-04 — для KingGore устарел исходный sparse-only режим: v2 добавил dense_steps/step_off и exact_kv/exact_kv_and_rows для сохранения качества MiniMax H3.
- 2026-08-04 — для Kijai устарела необходимость терпеть ModuleNotFoundError TensorDescriptor на pre-SM90 Triton-сборках: исправление принято, но подтверждение ограничено RTX 3060 и не является гарантией для RTX 20/10.

## Still unknown

- ComfyUI Sol-Attn не является единым проектом: Kijai и KingGore — отдельные репозитории с разными backend, поддержкой GPU и параметрами. Их совместимость друг с другом не документирована.
- В тексте события от 2026-08-07 нет доступного содержимого, поэтому event_findings намеренно пуст: ни одно дополнительное датированное утверждение нельзя честно привязать именно к этому дню.
- Kijai называет проект work in progress и документирует тесты только на RTX 4090 и RTX 5090; merge для RTX 3060 не доказывает поддержку всех pre-SM90 GPU.
- Ни один использованный upstream-источник NVIDIA не объявляет официальную ComfyUI-ноду; Sol-Engine и community-ноды следует считать разными путями интеграции.
- Китайский поисковый проход не дал первичного китайскоязычного источника, относящегося именно к этим двум репозиториям.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/kijai/ComfyUI-SolAttn_triton | kijai/ComfyUI-SolAttn_triton | 2026-09-05 |
| https://github.com/kijai/ComfyUI-SolAttn_triton/blob/main/readme.md | ComfyUI-SolAttn README | 2026-09-05 |
| https://github.com/kijai/ComfyUI-SolAttn_triton/pull/1 | Kijai pull request #1: pre-SM90 TensorDescriptor import fix | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell | KingGore/ComfyUI_sol-attn_Blackwell | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/blob/main/README.md | KingGore Blackwell README | 2026-09-05 |
| https://github.com/KingGore/ComfyUI_sol-attn_Blackwell/commits/main | KingGore Blackwell commit history | 2026-09-05 |
| https://arxiv.org/abs/2607.24027 | Sol-Attn: Accelerating Video Generation Inference via On-the-Fly Attention Sparsification | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Attn/ | NVIDIA Sol-Attn project page | 2026-09-05 |
| https://github.com/NVlabs/Sana/tree/sol-engine | NVlabs/Sana sol-engine branch | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-sol-attn`, thread `blackwell-and-triton-implementations`, 1 dated events 2026-08-07 → 2026-08-07.
- **Practical note:** As of 2026-08-07, practitioners evaluating ComfyUI Sol-Attn should distinguish the Blackwell-targeted implementation from the Triton-targeted implementation and verify environment compatibility before adopting either.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
