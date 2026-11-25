---
title: Wan2.2-NVFP4-Sparse
category: projects
date: 2026-06-05
tags: [project, wan, wan2-2-nvfp4-sparse, wan2-2-nvfp4-sparse-development]
aliases: ["Wan2.2-NVFP4-Sparse"]
---

# Wan2.2-NVFP4-Sparse

**Development line:** `project:wan2-2-nvfp4-sparse` · thread `wan2-2-nvfp4-sparse-development`  
**Last event:** 2026-06-05 · 1 dated since 2026-06-05 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Wan2.2-NVFP4-Sparse, с 27 июля в карточке именуемый LightWan2.2-A14B, — версия Wan2.2-T2V/I2V-A14B для владельцев Blackwell, которым нужен четырёхшаговый локальный видеогенератор. Возможности: T2V; I2V; NVFP4-пары high/low; dynamic sparse attention. Мера и предел: авторская таблица на RTX 5090 даёт 9,1–26,7 с при 4 шагах для 480p/720p, но путь требует RTX 50/Blackwell, T5/VAE, а I2V — image encoder. Вердикт: имеет смысл как специализированный LightX2V-пайплайн; на другом железе его заявленные преимущества не подтверждены.

## Development line

- **2026-06-05 — Hugging Face reference for Wan2.2-NVFP4-Sparse.** Wan2.2-NVFP4-Sparse — появились и были переупорядочены именованные T2V/I2V high/low NVFP4-веса, включая Comfy-варианты; из корня удалили два неоднозначных дубликата.

## What changed

2026-05-28: Wan2.2-NVFP4-Sparse — репозиторий модели был инициализирован на Hugging Face. 2026-05-29: Wan2.2-NVFP4-Sparse — LightX2V объявил вариант Wan 2.2 14B для T2V и I2V с NVFP4 quantization-aware step distillation и sparse attention для Blackwell; заявлено свыше 50× на одной RTX 5090. 2026-06-05: Wan2.2-NVFP4-Sparse — появились и были переупорядочены именованные T2V/I2V high/low NVFP4-веса, включая Comfy-варианты; из корня удалили два неоднозначных дубликата. 2026-06-09: Wan2.2-NVFP4-Sparse — карточка формализовала I2V как базовую модель и добавила отдельный путь запуска с image encoder и входным изображением. 2026-07-18: Wan2.2-NVFP4-Sparse — инструкции перенесли с устаревшего каталога distill на текущие скрипты wan22/extreme и добавили варианты sequence parallel для нескольких GPU. 2026-07-27: Wan2.2-NVFP4-Sparse — карточка переименована в LightWan2.2-A14B; старый адрес теперь перенаправляет на новый.

## How to use this

From 2026-06-05, practitioners should treat the linked Hugging Face repository as a candidate source for Wan2.2-NVFP4-Sparse and verify its model card, files, license, and compatibility before use.

1. Проверьте платформу: этот путь требует NVIDIA RTX 50-series или другую Blackwell-архитектуру; на иной GPU не рассчитывайте на заявленный NVFP4-режим.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
2. Поднимите рекомендованный контейнер lightx2v/lightx2v:26052801-cu130-5090 либо соберите LightX2V и NVFP4 kernel с CUTLASS по инструкции карточки.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
3. Скачайте соответствующую задаче пару high/low NVFP4-весов T2V или I2V, подготовьте Wan2.2 T5 и VAE; для I2V дополнительно подготовьте image encoder и исходное изображение.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
4. В конфигурации пропишите пути к обоим checkpoint files, high_noise_quantized_ckpt и low_noise_quantized_ckpt; стартовая T2V-конфигурация задаёт 4 шага, 81 кадр, 480×832 и sparse-attention ratio 0.9.
  — <https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json>
5. Для T2V задайте lightx2v_path и model_path в текущем run_wan22_moe_t2v_extreme.sh, затем запускайте его; скрипт вызывает model_cls wan2.2_moe с T2V extreme config.
  — <https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_t2v_extreme.sh>
6. Для I2V задайте те же пути и image_path в run_wan22_moe_i2v_extreme.sh; скрипт использует I2V extreme config и сохраняет MP4-результат.
  — <https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_i2v_extreme.sh>

## Best practices

- Используйте рекомендованный Docker-образ и официальные extreme-скрипты: они являются документированным маршрутом для этой модели, а не только общим Hub-виджетом Diffusers.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
- Храните high- и low-noise веса парой и задавайте оба явных пути в конфигурации; не возвращайтесь к удалённым generic high_nvfp4/low_nvfp4 filenames.
  — <https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json>
- Применяйте sparse attention прежде всего на высоком разрешении; CPU offload включайте только при нехватке памяти, потому что карточка предупреждает о падении throughput.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
- Перед рабочим применением сравните собственный набор prompts с FP8-базой по prompt adherence: один открытый, но не закрытый issue сообщил о худшем следовании промпту у FP4, и это не равно подтверждённому общему регрессу качества.
  — <https://github.com/ModelTC/LightX2V/issues/1147>

## Superseded by this

- {"claim":"Инструкции, ссылающиеся на generic high_nvfp4.safetensors и low_nvfp4.safetensors, устарели: оба файла были удалены из репозитория.","obsolete_since":"2026-06-05","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/0191e9d9499dfc0bc7fcfbc24b678e94b918c405"}
- {"claim":"Инструкции с путями scripts/wan22/distill/run_wan22_moe_*_extreme.sh устарели: карточка перевела запуск на scripts/wan22/extreme и добавила sequence-parallel варианты.","obsolete_since":"2026-07-18","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/3eef5caddabe719c0a96fd8f3f703f5f1f235f8b"}
- {"claim":"Wan2.2-NVFP4-Sparse как текущее имя карточки устарело: в карточке оно заменено на LightWan2.2-A14B; старый URL сохраняется как redirect.","obsolete_since":"2026-07-27","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/27213d1d4a6cfb1ecd9c60d214764c917d0f6c45"}

## Still unknown

- The July 19, 2026 LightX2V blog entry named in the project README returned 404 during verification, so it is not used as evidence of a model or runtime update.
- The RTX 5090 timings and 50×-plus claim are author-reported; no independent Blackwell reproduction was run here.
- Issue #1147 reports weaker prompt adherence than an FP8 comparison, but it is unassigned and has no maintainer response or reproducible benchmark, so it does not prove a general quality regression.
- The Hub shows generic Diffusers sample code, but no execution was found proving that it replaces the documented LightX2V setup with explicit high/low checkpoint paths and NVFP4 kernels.
- July 27 proves the model-card rename and the old URL currently redirects, but the exact timestamp of the Hugging Face repository redirect was not exposed.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/lightx2v/Wan2.2-NVFP4-Sparse | Historical Wan2.2-NVFP4-Sparse URL, redirecting to LightWan2.2-A14B | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B | LightWan2.2-A14B model card | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commits/main | LightWan2.2-A14B commit history | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/0191e9d9499dfc0bc7fcfbc24b678e94b918c405 | Remove extra NVFP4 safetensors files | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/4dbf88dc61135c02943f3f54c99acee05ed856db | Model-card update adding the I2V route | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/3eef5caddabe719c0a96fd8f3f703f5f1f235f8b | Model-card update moving to extreme and sequence-parallel scripts | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/27213d1d4a6cfb1ecd9c60d214764c917d0f6c45 | Model-card update renaming LightWan2.2-A14B | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/README.md | LightX2V English README and dated release log | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/README_zh.md | LightX2V Simplified Chinese README and dated release log | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json | T2V NVFP4 sparse-attention configuration | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_t2v_extreme.sh | T2V extreme launch script | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_i2v_extreme.sh | I2V extreme launch script | 2026-09-06 |
| https://lightx2v-en.readthedocs.io/en/latest/getting_started/model_structure.html | LightX2V model format and loading guide | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/issues/1147 | Open community report on NVFP4 prompt adherence | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:wan2-2-nvfp4-sparse`, thread `wan2-2-nvfp4-sparse-development`, 1 dated events 2026-06-05 → 2026-06-05.
- **Practical note:** From 2026-06-05, practitioners should treat the linked Hugging Face repository as a candidate source for Wan2.2-NVFP4-Sparse and verify its model card, files, license, and compatibility before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
