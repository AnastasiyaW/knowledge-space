---
title: Krea2 Filter Bypass
category: projects
date: 2026-07-02
tags: [krea2-filter-bypass, project]
aliases: ["Krea2 Filter Bypass"]
---

# Krea2 Filter Bypass

**Development line:** `project:krea2-filter-bypass` · thread `krea2-filter-bypass`  
**Last event:** 2026-07-02 · 1 dated since 2026-07-02 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Krea2 Filter Bypass — LoRA `fedor_bypass.safetensors` для Krea 2: заявлены изменение двух компонентов `txtfusion.projector`, сохранение остальных десяти нулевыми и работа вместе с другими LoRA; предел — файл 1,024 байта, а утверждения о снятии ограничений и отсутствии дрейфа стиля не подтверждены независимым воспроизводимым тестом. Вердикт: это узкий community-эксперимент, а не официальный режим Krea или замена проверки правил платформы.

## Development line

- **2026-07-02 — Krea2 Filter Bypass public model and discussion links recorded.** On 2026-07-02, the dated record linked Krea2 Filter Bypass to a Civitai model page and a Reddit discussion. Together, these public links mark a material public-facing development point for the project, although the underlying posts have not been independently researched.

## What changed

2026-07-02 — опубликован Krea2 Filter Bypass [Fedor], FP32-файл `fedor_bypass.safetensors` для Krea 2 с дельтами только для столбцов 9 и 10.

## How to use this

From 2026-07-02, practitioners should treat Krea2 Filter Bypass as having a public model-and-discussion record, while independently verifying the linked pages before relying on any claimed behavior or compatibility.

1. Проверьте, разрешено ли использование такого изменения в вашем локальном, лицензированном пайплайне и по правилам модели; не переносите его в сервисы, где оно обходило бы обязательные ограничения.
  — <https://civitai.red/models/2746817/krea2-filter-bypass-fedor?modelVersionId=3089754>
2. Для исследовательского воспроизведения зафиксируйте файл, хеш, базовую модель, seed, prompt и параметры генерации; исходник задаёт целевой ключ `diffusion_model.txtfusion.projector.diff` и две дельты.
  — <https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py>
3. Сравните базовый и изменённый запуск на одинаковом seed и полном наборе настроек; не переносите выводы о качестве с единичного изображения на рабочий пайплайн.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/>

## Best practices

- Относитесь к заявлению об отсутствии дрейфа стиля как к гипотезе и проводите A/B-проверку на одинаковых seed и настройках: участники сравнения описывают варианты как близкие, но не идентичные.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ul38ei/made_yet_another_bypass_filter_for_krea_2_this/>
- Проверяйте содержимое и происхождение маленьких weight-файлов, а не только название: опубликованный генератор создаёт тензор `[1,12]` и заполняет лишь позиции 9 и 10.
  — <https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py>
- Не складывайте неизвестные bypass-изменения с checkpoint или LoRA, где аналогичное изменение уже встроено: community-анализ отмечает, что сила и эффект зависят от prompt и стека.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/>

## Superseded by this

- 2026-07-18 — представление Fedor как функционально нового bypass относительно FilterBypass2 устарело: позднее описание сводит различие к точности значений, а не к новому механизму.
- 2026-07-18 — рекомендация считать отсутствие влияния на стиль математически гарантированным не должна использоваться как эксплуатационное правило без независимого A/B-теста.

## Still unknown

- Нет первичного источника от Krea, подтверждающего, что столбцы 9 и 10 являются именно механизмом safety filter или что изменение допустимо по лицензии и правилам использования.
- Нет независимого воспроизводимого бенчмарка, подтверждающего заявленное отсутствие дрейфа стиля, улучшение prompt adherence либо превосходство FP32-варианта над FilterBypass2.
- Дата 2026-07-18 является датой обновления страницы Civitai; точный журнал изменений, отдельный от текущего описания, недоступен.
- Источники описывают один и тот же двухвекторный вариант и соседние bypass-файлы, а не две разные одноимённые разработки.

## Sources

| source | title | read |
|---|---|---|
| https://civitai.red/models/2746817/krea2-filter-bypass-fedor?modelVersionId=3089754 | Krea2 Filter Bypass [Fedor] - Krea2 Bypass [Fedor] | Krea 2 LoRA | Civitai | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ul38ei/made_yet_another_bypass_filter_for_krea_2_this/ | Made yet another bypass filter for Krea 2 -- this one seems to work well at just defeating the filters and preventing any type of warping | 2026-09-05 |
| https://github.com/CliffNodes/fedor_bypass | CliffNodes/fedor_bypass | 2026-09-05 |
| https://github.com/CliffNodes/fedor_bypass/blob/main/build_fedor_bypass.py | fedor_bypass/build_fedor_bypass.py at main | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ukh334/i_extracted_the_values_of_krea_2_safery_filters/ | I extracted the values of Krea 2 Safety Filters Bypass Files, so you don't have to | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:krea2-filter-bypass`, thread `krea2-filter-bypass`, 1 dated events 2026-07-02 → 2026-07-02.
- **Practical note:** From 2026-07-02, practitioners should treat Krea2 Filter Bypass as having a public model-and-discussion record, while independently verifying the linked pages before relying on any claimed behavior or compatibility.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
