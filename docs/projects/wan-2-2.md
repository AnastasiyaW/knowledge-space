---
title: WAN 2.2 — WAN
category: projects
date: 2025-07-28
tags: [project, wan, wan-2-2]
aliases: ["WAN 2.2"]
---

# WAN 2.2 — WAN

**Development line:** `project:wan-2-2` · thread `wan`  
**Last event:** 2025-07-28 · 2 dated since 2025-07-28 · **Researched:** 2026-09-05 · confidence: medium

## What it is

WAN 2.2 — линейка открытых video-diffusion моделей для разработчиков и создателей: text-to-video, image-to-video, text-image-to-video, speech-to-video и анимация персонажа. Лимит: TI2V-5B заявлен для 720p при 24 fps; T2V-A14B в официальном single-GPU примере требует не менее 80 GB VRAM. Вердикт: для 720p на ограниченном железе практичнее начать с TI2V-5B, а A14B выбирать для T2V/I2V при доступе к существенно большей VRAM.

## Development line

- **2025-07-28 — Official WAN social post recorded.** T2V-A14B, I2V-A14B и TI2V-5B; в тот же день появились интеграции в ComfyUI, Diffusers и Space для TI2V-5B. Дополнение к событию: A14B — двухэкспертная MoE-серия с 27B суммарных и около 14B активных параметров на шаг; TI2V-5B совмещает T2V и I2V через VAE со сжатием 16×16×4.
- **2025-07-28 — WAN model collection reference recorded.** T2V-A14B, I2V-A14B и TI2V-5B; в тот же день появились интеграции в ComfyUI, Diffusers и Space для TI2V-5B. Дополнение к событию: A14B — двухэкспертная MoE-серия с 27B суммарных и около 14B активных параметров на шаг; TI2V-5B совмещает T2V и I2V через VAE со сжатием 16×16×4.

## What changed

2025-07-28 — опубликованы код инференса и веса WAN 2.2: T2V-A14B, I2V-A14B и TI2V-5B; в тот же день появились интеграции в ComfyUI, Diffusers и Space для TI2V-5B. Дополнение к событию: A14B — двухэкспертная MoE-серия с 27B суммарных и около 14B активных параметров на шаг; TI2V-5B совмещает T2V и I2V через VAE со сжатием 16×16×4. 2025-08-26 — добавлен Wan2.2-S2V-14B: генерация видео по изображению и аудио, с весами, кодом и техническим отчётом. 2025-09-05 — добавлена поддержка синтеза речи CosyVoice для speech-to-video. 2025-09-19 — добавлен Wan2.2-Animate-14B для анимации и замены персонажа по движению и выражению. 2025-11-13 — Wan2.2-Animate-14B интегрирован в Diffusers. Новые шаги расширяют семейство; они не являются уточнениями события 2025-07-28.

## How to use this

As of 2025-07-28, practitioners should consult the official Wan-AI Hugging Face model collection and the linked official WAN update when locating WAN 2.2 artifacts; the available dated links alone do not establish a specific model, capability, or workflow change.

1. Клонируйте официальный репозиторий, установите зависимости при PyTorch 2.4 или новее и скачайте нужный checkpoint через Hugging Face CLI.
  — <https://github.com/Wan-Video/Wan2.2>
2. Для text-to-video выберите Wan2.2-T2V-A14B; для image-to-video — I2V-A14B; для смешанного T2V/I2V при 720p — TI2V-5B.
  — <https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B>
3. Запустите generate.py с соответствующим --task, --ckpt_dir, размером и prompt; для multi-GPU используйте документированный запуск torchrun с FSDP и Ulysses.
  — <https://github.com/Wan-Video/Wan2.2>

## Best practices

- Начинайте с базового запуска без расширения промпта, затем добавляйте расширение только при необходимости; официальный проект поддерживает DashScope и локальный Qwen.
  — <https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B>
- При нехватке памяти включайте --offload_model True, --convert_model_dtype и при необходимости --t5_cpu; это официально рекомендованные меры против OOM.
  — <https://github.com/Wan-Video/Wan2.2>
- Для speech-to-video устанавливайте дополнительный requirements_s2v.txt, а не предполагаете, что базовый requirements.txt содержит CosyVoice.
  — <https://github.com/Wan-Video/Wan2.2>

## Superseded by this

- 2025-07-28 — считать Wan 2.1 текущей открытой базовой линейкой Wan стало устаревшим для задач T2V, I2V и TI2V: WAN 2.2 заменила её как следующая опубликованная основная линейка.
- 2025-11-13 — прежняя рекомендация использовать Wan2.2-Animate-14B только через собственный код устарела для пользователей Diffusers: появилась официально зафиксированная интеграция.

## Still unknown

- Тело X-поста недоступно при проверке, поэтому нельзя надёжно приписать ему более узкое утверждение, чем дату и URL исходного события.
- Страница Hugging Face с перечнем моделей отражает текущее состояние организации, но не даёт исходную дату публикации каждого checkpoint.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Wan-Video/Wan2.2 | Wan-Video/Wan2.2 — official repository and usage guide | 2026-09-05 |
| https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B | Wan-AI/Wan2.2-T2V-A14B — official model card | 2026-09-05 |
| https://huggingface.co/Wan-AI/models | Wan-AI — Hugging Face model collection | 2026-09-05 |
| https://x.com/Alibaba_Wan/status/1949332715071037862 | Alibaba Wan X post linked to the 2025-07-28 event | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:wan-2-2`, thread `wan`, 2 dated events 2025-07-28 → 2025-07-28.
- **Practical note:** As of 2025-07-28, practitioners should consult the official Wan-AI Hugging Face model collection and the linked official WAN update when locating WAN 2.2 artifacts; the available dated links alone do not establish a specific model, capability, or workflow change.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
