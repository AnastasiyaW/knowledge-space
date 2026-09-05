---
title: img2threejs
category: projects
date: 2026-07-24
tags: [img2threejs, project]
aliases: ["img2threejs"]
---

# img2threejs

**Development line:** `project:img2threejs` · thread `img2threejs`  
**Last event:** 2026-07-24 · 1 dated since 2026-07-24 · **Researched:** 2026-09-05 · confidence: high

## What it is

img2threejs — Apache-2.0 skill для Claude Code, Codex и OpenCode: из одного изображения он строит TypeScript-фабрику `THREE.Group`, а не GLB или извлечённую сетку. — разбирает объект на компоненты, материалы, сокеты и коллайдеры; — генерирует модель проходами и сравнивает рендер с референсом; — для персонажей умеет строить риг и проверять анимацию. Ограничение: один кадр не показывает скрытые стороны; для точного подобия проект прямо помечает неуверенные области и запрашивает дополнительные виды. Вердикт: подходит, когда нужен читаемый и анимируемый Three.js-код; не заменяет фотограмметрию и ручное моделирование для невидимой геометрии.

## Development line

- **2026-07-24 — img2threejs GitHub repository was publicly linked.** On 2026-07-24, the img2threejs development line included a direct link to its GitHub repository. This records a public source-reference milestone for the project; the sealed evidence does not establish its features, release status, or any specific code change.

## What changed

2026-07-15 — v1.0 выпустил исходный объектный pipeline: staged sculpt, side-by-side review и runtime-иерархию; v1.1 добавил обязательный inventory мелких деталей и strict-quality gate. 2026-07-21 — v1.2 вывел гуманоидных персонажей и гибридные объекты в отдельный маршрут с пропорциями и диагностикой. 2026-07-22 — v1.3 добавил детерминированный review harness Divine Eye, проверки геометрии и reference-grounded материалы. 2026-07-24 — проект был представлен как Python-инструмент для процедурной, готовой к анимации реконструкции Three.js по одному референсу. 2026-07-25 — v1.4.0 добавил специализированный CS2 weapon pipeline с provenance, семействами геометрии и review gates. 2026-07-26 — v1.4.1 ужесточил CS2-проверки: coverage компонентов, контракт Glock-18 и доказательства реальной геометрии вместо убедительной текстуры. 2026-07-30 — v1.4.3 закрепил 1.4.x как принятую release line; публикация релиза стала возможна только из утверждённого annotated tag. 2026-08-12 — v1.5.0 заменил beta-линию: добавил валидируемый риг, skinning, hair pipeline, проверку левости/правости и per-feature review gates. 2026-08-22 — v1.5.1 добавил GLB-reference route: GLB служит измерительным инструментом, а итог всё ещё остаётся TypeScript-кодом. 2026-08-25 — v1.5.2 добавил измеряемые animation/rigging gates; отсутствие данных теперь означает `unevaluated`, а не PASS.

## How to use this

As of 2026-07-24, practitioners can use the linked GitHub repository as the project's public source reference, while verifying its current functionality and version status directly before relying on it.

1. Клонируйте репозиторий в каталог skills; ядру нужны Python 3.10+ и стандартная библиотека.
  — <https://github.com/img2threejs/img2threejs>
2. Передайте агенту изображение и вызовите `/img2threejs`; pipeline сам классифицирует субъект и создаст assessment/spec.
  — <https://github.com/img2threejs/img2threejs>
3. Запустите strict-quality validation и генерируйте TypeScript factory только после прохождения gate.
  — <https://github.com/img2threejs/img2threejs>
4. Для долгой работы и персонажа создайте state index, затем возобновляйте следующий разрешённый проход через `forge/next.py`.
  — <https://github.com/img2threejs/img2threejs>
5. Если есть GLB персонажа, используйте отдельный GLB-reference маршрут; без него оставайтесь на image-driven core pipeline.
  — <https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1>

## Best practices

- Начинайте с изолированного hard-surface объекта с читаемым силуэтом; скрытые поверхности не выдавайте за измеренные.
  — <https://github.com/img2threejs/img2threejs>
- Сначала перечислите identity-defining details и привяжите каждый к компоненту или материалу; не обходите `--strict-quality`.
  — <https://github.com/img2threejs/img2threejs>
- Проверяйте каждый проход по одной comparison sheet «референс рядом с рендером» и не переходите дальше без PASS.
  — <https://github.com/img2threejs/img2threejs>
- Для персонажей не считайте существующий `AnimationClip` работающей анимацией: прогоняйте rig/animation gates и трактуйте `unevaluated` как незавершённую проверку.
  — <https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md>

## Superseded by this

- 2026-07-30: автоматическая публикация после merge PR устарела; релиз требует approved annotated version tag.
- 2026-08-12: `1.4.4-beta.1`, `1.4.4-beta.2` и `v1.5-beta` заменены стабильным v1.5.0; 1.4.4 не публиковался как stable.
- 2026-08-25: правило «клип без travel/rise можно повторять» заменено измерением возврата позы и положения таза; непроверенный loop больше не должен неявно считаться `false`.

## Still unknown

- Репозиторий, на который указывала исходная ссылка, сейчас перенаправляет из `hoainho/img2threejs` в `img2threejs/img2threejs`; дата и причина переноса не установлены.
- Текущий changelog содержит раздел Unreleased после v1.5.2; он не является опубликованным релизом и не должен считаться доступной стабильной версией.
- event_findings:[{"event_date":"2026-07-24","source_date":"2026-07-24","finding":"На ту же дату независимый каталог уточняет практическую рамку: это Python-инструмент, который строит процедурную, готовую к анимации Three.js-модель по референсу; это не отдельный mesh/image-to-3D сервис.","source_url":"https://buttondown.com/surfaced/archive/surfaced-friday-july-24-2026/"}]
- new_events:[{"date":"2026-07-15","finding":"v1.0 и v1.1: объектный staged pipeline и обязательная инвентаризация мелких деталей со strict-quality gate.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-21","finding":"v1.2: отдельный маршрут для гуманоидных персонажей и гибридных субъектов.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-22","finding":"v1.3: Divine Eye и детерминированные проверки геометрии, материалов и входных данных.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-25","finding":"v1.4.0: CS2 weapon pipeline с provenance и family-specific reconstruction.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-26","finding":"v1.4.1: component-coverage gate и Glock-18 contract.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-30","finding":"v1.4.3: принятая release line 1.4.x и выпуск только из утверждённого annotated tag.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-08-12","finding":"v1.5.0: валидируемый риг, skinning, hair subsystem и review gates для персонажей.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-08-22","finding":"v1.5.1: GLB-reference route с измерением параметров и кодовым итогом.","source_url":"https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1"},{"date":"2026-08-25","finding":"v1.5.2: исполнимые animation/rigging gates, где непроверенный вход не может стать PASS.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"}]

## Sources

| source | title | read |
|---|---|---|
| https://github.com/hoainho/img2threejs | img2threejs repository redirect to canonical organization repository | 2026-09-05 |
| https://github.com/img2threejs/img2threejs | img2threejs README | 2026-09-05 |
| https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md | img2threejs changelog | 2026-09-05 |
| https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1 | Release 1.5.1: add the GLB-reference route | 2026-09-05 |
| https://buttondown.com/surfaced/archive/surfaced-friday-july-24-2026/ | Surfaced — Friday, July 24, 2026 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:img2threejs`, thread `img2threejs`, 1 dated events 2026-07-24 → 2026-07-24.
- **Practical note:** As of 2026-07-24, practitioners can use the linked GitHub repository as the project's public source reference, while verifying its current functionality and version status directly before relying on it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
