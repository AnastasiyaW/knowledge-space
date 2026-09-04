---
title: GalaxyAce LoRA — GalaxyAce LoRA development
category: projects
tags: [galaxyace-lora, project]
aliases: ["GalaxyAce LoRA"]
---

# GalaxyAce LoRA — GalaxyAce LoRA development

**Development line:** `project:galaxyace-lora` · thread `galaxyace-lora`  
**Events:** 1 dated, 2026-03-30 → 2026-03-30 · **Researched:** 2026-09-04 · confidence: medium

## What it is

GalaxyAce LoRA — это отдельные style-LoRA для автора фото и видео, которому нужна съёмка с признаками недорогой Android-камеры начала 2010-х. — цветопередача, экспозиция и мягкость объектива; — для LTX-вариантов — шум сенсора, компрессия и ручная дрожь; — для H3 — тот же визуальный эффект на видео с нативным аудио. Один файл привязан к своей базовой модели: LTX-2/2.3, Z-Image-Turbo, Krea 2 и MiniMax H3 не используют взаимозаменяемые веса. Вывод: это адаптер под конкретный workflow, а не универсальный фильтр для любого checkpoint.

## Development line

- **2026-03-30 — GalaxyAce LoRA version-specific Civitai reference recorded.** On 2026-03-30, this development line recorded a version-specific Civitai URL for GalaxyAce LoRA, identifying model 2200329 and version 2808759. It provides a dated identity anchor for that model version, while its release context, training details, and compatibility remain unverified.

## What changed

GalaxyAce LoRA — линия перешла от LTX-2.3 к отдельным вариантам для Krea 2 и MiniMax H3. 2026-03-30 — ссылка на версию 2808759 фиксирует вариант LTXV 2.3; публичное обновление описывает силу 1.0, отсутствие trigger word и подключение после checkpoint внутри ComfyUI T2V/I2V subgraph. 2026-06-25 (найдено сегодня, обновление автора) — добавлен отдельный вариант для Krea 2 Raw и Turbo; сила стала зависеть от близости промпта к повседневным сценам из обучения. 2026-07-06 — корневая страница модели указана без version ID; новый вес или настройку на эту дату установить нельзя. 2026-08-05 (найдено сегодня, обновление автора) — добавлен MiniMax H3-вариант 3201619 для видео с нативным звуком и другой формой промпта. По состоянию на 2026-09-04 доступная карточка названа MiniMax H3, но её содержимое требует входа.

## How to use this

As of 2026-03-30, practitioners can retain Civitai model 2200329, version 2808759 as the dated provenance reference for GalaxyAce LoRA, but should not infer its training method, contents, compatibility, or later updates from this line alone.

1. Откройте карточку, войдите в Civitai и выберите именно MiniMax H3-вариант; не загружайте LTX- или Krea-вес в H3 workflow.
  — <https://civitai.red/models/2200329/galaxyace-lora>
2. Разверните MiniMax H3 Base по официальной инструкции и начните с рекомендованного ComfyUI T2V или R2V template.
  — <https://github.com/MiniMax-AI/MiniMax-H3>
3. Подключите H3-совместимый GalaxyAce LoRA в LoRA-слот H3 workflow; в зеркале текущей версии указаны стартовые значения strength 1.0, guidance_scale 1, 768p/24 fps, число кадров 17n+5 и размеры, кратные 32.
  — <https://fastsdmodel.com/models/2200329?lang=zh>
4. Пишите связный промпт в порядке «сцена → биты с таймкодами → поведение камеры → аудио → без текста и логотипов».
  — <https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/>

## Best practices

- Для MiniMax H3 описывайте нужный звук явно и не используйте tag tails или весовые скобки как в CLIP-пайплайнах; структура и положительные формулировки работают надёжнее.
  — <https://fastsdmodel.com/models/2200329?lang=zh>
- Не смешивайте с эффектом дешёвой камеры слова вроде cinematic, anamorphic, depth of field, iPhone и именованные colour grades: они противоречат фиксированному маленькому объективу и автоэкспозиции.
  — <https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/>
- Только для Krea 2-варианта: начинайте с 1.0 на бытовых сценах, используйте 1.25–1.45 как Realism Detailer и 1.7–2.0 для полного эффекта либо необычного сюжета; это не параметры H3.
  — <https://www.reddit.com/r/comfyui/comments/1ufksvg/galaxyace_lora_update_now_supports_krea_2/>
- Если в H3 речь теряет синхрон, зеркальная инструкция советует сначала снизить силу LoRA до 0.7, а не переписывать промпт; отрицательный промпт там не является рабочим способом исключения.
  — <https://fastsdmodel.com/models/2200329?lang=zh>

## Superseded by this

- 2026-03-30 — инструкция LTX-2.3 подключать LoRA после checkpoint не является универсальной инструкцией после появления H3-варианта; она остаётся применима только к LTXV 2.3-весу.
- 2026-06-25 — шкала силы Krea 2 от 1.0 до 2.0 устарела как общая рекомендация для GalaxyAce LoRA: она относится только к Krea-2 Raw/Turbo.
- 2026-07-06 — корневая ссылка без version ID не может считаться указанием на актуальный вес; позже опубликован H3-вариант 3201619.

## Still unknown

- Прямая карточка Civitai требует входа: список файлов, SHA-256, лицензия, авторский аккаунт и доступность прежних версий не подтверждены.
- Параметры H3 из Fast SD Model взяты из стороннего зеркала и не сверены с загружаемым файлом на Civitai.
- Две датированные ссылки имеют один model ID 2200329, поэтому признаков двух разных предметов нет; LTX, Krea и H3 выглядят как разные base-specific версии одной серии.
- Существует одноимённый Hugging Face-репозиторий, но его происхождение не связано проверяемым источником с Civitai-моделью; он исключён из инструкций.

## Sources

| source | title | read |
|---|---|---|
| https://civitai.red/models/2200329/galaxyace-lora | GalaxyAce LoRA - MiniMax H3 GalaxyAce LoRA | Hailuo H3 by MiniMax LoRA | Civitai | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1vgkbej/sora_2_vibes_on_minimax_h3_galaxyace_lora_update/ | Sora 2 vibes on MiniMax H3 — GalaxyAce LoRA Update | 2026-09-04 |
| https://github.com/MiniMax-AI/MiniMax-H3 | MiniMax H3 | 2026-09-04 |
| https://fastsdmodel.com/models/2200329?lang=zh | GalaxyAce LoRA | Fast SD Model | 2026-09-04 |
| https://civitai.com/models/2200329/galaxyace-lora?modelVersionId=2808759 | GalaxyAce LoRA model URL (version 2808759) | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1s5g11w/galaxyace_lora_update_now_supports_ltx23/ | GalaxyAce LoRA Update — Now Supports LTX-2.3 | 2026-09-04 |
| https://www.reddit.com/r/comfyui/comments/1ufksvg/galaxyace_lora_update_now_supports_krea_2/ | GalaxyAce LoRA Update — Now Supports Krea 2 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:galaxyace-lora`, thread `galaxyace-lora`, 1 dated events 2026-03-30 → 2026-03-30.
- **Practical note:** As of 2026-03-30, practitioners can retain Civitai model 2200329, version 2808759 as the dated provenance reference for GalaxyAce LoRA, but should not infer its training method, contents, compatibility, or later updates from this line alone.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
