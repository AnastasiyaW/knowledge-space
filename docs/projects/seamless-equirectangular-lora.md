---
title: Seamless-Equirectangular LTX-2.3 LoRA — Seamless-Equirectangular LoRA release
category: projects
date: 2026-07-07
tags: [project, seamless-equirectangular-lora, seamless-equirectangular-lora-release]
aliases: ["Seamless-Equirectangular LTX-2.3 LoRA"]
---

# Seamless-Equirectangular LTX-2.3 LoRA — Seamless-Equirectangular LoRA release

**Development line:** `project:seamless-equirectangular-lora` · thread `seamless-equirectangular-lora-release`  
**Last event:** 2026-07-07 · 1 dated since 2026-07-07 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Seamless-Equirectangular LTX-2.3 LoRA — rank-128 адаптер для создания 360° equirectangular видео в LTX-2.3 через ComfyUI.

Возможности:

- text-to-video с триггером `Equirectangular`;
- устранение шва через circular VAE и per-step latent roll;
- обработка полюсов через EquiRoPE и геометрический CFG;
- outpaint обычного видео до 360° через отдельный VR-Outpaint workflow.

Ограничение: LoRA обучали 15 000 шагов; базовая LTX-2.3 без неё, по заявлению автора, не формирует equirectangular-вывод, а hosted inference provider отсутствует.

Вердикт: это практический локальный ComfyUI-пайплайн, а не самостоятельная облачная модель.

## Development line

- **2026-07-07 — Public resources linked for Seamless-Equirectangular LTX-2.3 LoRA.** Seamless-Equirectangular LTX-2.3 LoRA и ComfyUI node pack. Карточка модели уточняет параметры адаптера: rank 128, 15 000 шагов, триггер `Equirectangular`; репозиторий уточняет, что LoRA отвечает за equirectangular-представление, а circular VAE и per-step roll закрывают шов. Последующие текущие README-материалы добавляют поддержку Krea2 и MiniMax H3, но первичные страницы не дают надёжной даты этих расширений, поэтому они не отнесены к отдельному датированному событию.

## What changed

2026-07-07 — опубликован связанный комплект: Seamless-Equirectangular LTX-2.3 LoRA и ComfyUI node pack. Карточка модели уточняет параметры адаптера: rank 128, 15 000 шагов, триггер `Equirectangular`; репозиторий уточняет, что LoRA отвечает за equirectangular-представление, а circular VAE и per-step roll закрывают шов. Последующие текущие README-материалы добавляют поддержку Krea2 и MiniMax H3, но первичные страницы не дают надёжной даты этих расширений, поэтому они не отнесены к отдельному датированному событию.

## How to use this

From 2026-07-07, practitioners should treat the linked Hugging Face LoRA and ComfyUI extension as a paired starting point when evaluating seamless equirectangular LTX-2.3 workflows.

1. Установите ComfyUI-Seamless-Equirectangular в каталог custom nodes ComfyUI и перезапустите ComfyUI.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular>
2. Загрузите адаптер как обычный LTX-2.3 LoRA и добавьте в prompt слово `Equirectangular`.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>
3. Откройте приложенный T2V workflow и используйте node pack: он добавляет EquiRoPE, geometric CFG, per-step roll, circular VAE и wrapped noise.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>
4. Для превращения перспективного ролика в 360° используйте отдельный VR-Outpaint workflow и ComfyUI-VR-Outpaint-Tools; этот LoRA применяется совместно с VR-Outpaint IC-LoRA.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>

## Best practices

- Для LTX начните с LoRA + per-step roll + circular VAE: позиционные патчи являются улучшением геометрии, но не заменяют LoRA.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- При повторяющихся или зеркальных объектах не используйте `dual_average`; переключитесь на `random_per_step` либо отключите roll.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- Для быстрого панорамирования задайте `start_percent` 0.2–0.3, чтобы сначала зафиксировать структуру сцены, а затем лечить шов.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- Не считайте latent или image seam blend исправлением несовпадающих объектов: это только узкий косметический fallback для остаточного цветового шва.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Первичные страницы не дают надёжных дат для последующих Krea2 и MiniMax H3 расширений, поэтому они не оформлены как новые датированные события.
- Заявления о качестве, production-использовании и сравнении компонентов исходят от автора проекта; независимой воспроизводимой оценки в использованных источниках нет.
- The recorded link не был использован: страница не открылась через доступный веб-доступ.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA | TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA — model card | 2026-09-05 |
| https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular | Burgstall-labs/ComfyUI-Seamless-Equirectangular | 2026-09-05 |
| https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md | ComfyUI-Seamless-Equirectangular README | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:seamless-equirectangular-lora`, thread `seamless-equirectangular-lora-release`, 1 dated events 2026-07-07 → 2026-07-07.
- **Practical note:** From 2026-07-07, practitioners should treat the linked Hugging Face LoRA and ComfyUI extension as a paired starting point when evaluating seamless equirectangular LTX-2.3 workflows.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
