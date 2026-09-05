---
title: OrbitQuant
category: projects

tags: [orbitquant, orbitquant-development, project]
aliases: ["OrbitQuant"]
---

# OrbitQuant

**Development line:** `project:orbitquant` · thread `orbitquant-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

OrbitQuant — Python-библиотека и метод постобучающей квантизации для image/video diffusion transformers. Возможности: RPBH-поворот, общие Lloyd–Max codebook, W2A4–W4A6 recipes, интеграции Transformers/Diffusers/PyTorch и packed CUDA, Triton и Metal execution. Ограничение: для неизвестной архитектуры покрытие модулей не доказывает сохранение качества, поэтому результат нужно измерять до публикации артефакта. Вердикт: это практический путь к data-free low-bit inference, но не универсальная замена проверки качества конкретной модели.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-07 — опубликована страница метода OrbitQuant для calibration-free weight-and-activation quantization image и video diffusion transformers. 2026-07-09 — в PyPI вышла первоначальная серия пакетов OrbitQuant 0.1.0–0.1.6. 2026-07-10 — выпущены версии 0.2.0–0.3.1. 2026-07-11 — выпущена версия 0.4.0. 2026-07-12 — выпущена версия 0.5.0. 2026-07-14 — выпущены версии 0.6.0–0.9.0. 2026-08-04 — опубликована текущая по проверенному реестру версия 0.9.2.

## How to use this

As of 2026-07-07, treat OrbitQuant as an unresearched project reference and verify its purpose, capabilities, and status before using it in practice.

1. Установите интеграцию для Hugging Face: `pip install "orbitquant[hf]"`.
  — <https://github.com/iamwavecut/OrbitQuant>
2. До конвертации загрузите модель и проверьте machine-readable coverage через `inspect_linear_module_policy()`; отдельно изучите skipped и unsupported modules.
  — <https://github.com/iamwavecut/OrbitQuant>
3. Для Transformers передайте `OrbitQuantConfig(target_policy="auto")` в `from_pretrained()`, затем сохраните packed artifact через `save_pretrained()`.
  — <https://github.com/iamwavecut/OrbitQuant>
4. Для Diffusers создайте `build_diffusers_pipeline_quantization_config(...)`, квантуйте компонент `transformer` и загрузите pipeline в BF16.
  — <https://github.com/iamwavecut/OrbitQuant>
5. В ComfyUI подключите соответствующий OrbitQuant loader к исходному Diffusers pipeline, укажите локальный `artifact_path` и используйте возвращённый pipeline дальше по графу.
  — <https://pypi.org/project/comfyui-orbitquant/>

## Best practices

- Не обновляйте Triton отдельно от PyTorch: пакет использует Triton из Linux wheels PyTorch как CUDA fallback.
  — <https://github.com/iamwavecut/OrbitQuant>
- Для неизвестных архитектур сначала проверьте policy coverage и измерьте качество генерации; автоматическое обнаружение модулей не является гарантией качества.
  — <https://github.com/iamwavecut/OrbitQuant>
- Используйте `auto_fused` для packed runtime, а `dequant_bf16` — только как явный compatibility/debug путь.
  — <https://pypi.org/project/comfyui-orbitquant/>
- Перед загрузкой ComfyUI-артефакта проверяйте manifest, checksums, source metadata, bit settings и target policy.
  — <https://pypi.org/project/comfyui-orbitquant/>

## Superseded by this

- 2026-08-04 — версии OrbitQuant до 0.9.2 не являются текущим релизом в проверенном PyPI release history.
- 2026-07-09 — ранняя серия 0.1.0–0.1.6 заменена последующими релизами; для новой установки следует сверять актуальную версию в PyPI.

## Still unknown

- Страница метода и статья описывают исследовательский OrbitQuant, а PyPI/GitHub-реализация заявлена как clean-room implementation; их практические интерфейсы и поздние release notes не следует приписывать исходной публикации 2026-07-07.
- Не найден первичный датированный changelog, который объясняет содержательные различия между всеми пакетными версиями 0.1.0–0.9.2; подтверждены даты и номера релизов, но не полный change-by-change scope.

## Sources

| source | title | read |
|---|---|---|
| https://saurabhcantina.github.io/orbitquant/ | OrbitQuant: Data-Agnostic Quantization for Image and Video Diffusion Transformers | 2026-09-05 |
| https://arxiv.org/abs/2607.02461 | OrbitQuant: Data-Agnostic Quantization for Image and Video Diffusion Transformers | 2026-09-05 |
| https://github.com/iamwavecut/OrbitQuant | iamwavecut/OrbitQuant | 2026-09-05 |
| https://pypi.org/project/orbitquant/ | orbitquant · PyPI | 2026-09-05 |
| https://pypi.org/project/comfyui-orbitquant/ | comfyui-orbitquant · PyPI | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:orbitquant`, thread `orbitquant-development`, 0 dated events - → -.
- **Practical note:** As of 2026-07-07, treat OrbitQuant as an unresearched project reference and verify its purpose, capabilities, and status before using it in practice.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
