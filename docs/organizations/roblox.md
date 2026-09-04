---
title: Roblox — Roblox AI Creation
category: organizations
tags: [model_releases, organization, roblox, roblox-ai, roblox-ai-creation]
aliases: ["Roblox"]
---

# Roblox — Roblox AI Creation

**Development line:** `organization:roblox` · thread `roblox-ai-creation`  
**Events:** 2 dated, 2023-02-18 → 2026-02-05 · **Researched:** 2026-09-04 · confidence: high

## What it is

Roblox — игровая платформа и Roblox Studio для разработчиков; в этой линии Cube даёт: — локальный Cube 3D v0.5 для генерации OBJ по тексту; — GenerationService для статического Body1 или составного Car5 прямо в опыте; — CubePart для именованных частей под игровой код. Локальный fast-inference требует 24 ГБ VRAM, обычный — 16 ГБ; 4D Generation остаётся beta, а в текущих документах явно описаны Car5 и Body1. Вывод: берите GenerationService для Roblox-объектов с заранее спроектированной схемой, а Cube 3D v0.5 — для локальных прототипов, не для обещанного, но ещё не доказанного генератора произвольных сцен.

## Development line

- **2023-02-18 — Wired Reports on Roblox's Generative-AI Direction.** On 2023-02-18, Wired published a report connecting Roblox with generative AI and its gaming universe. The dated linked source marks an early public milestone in Roblox's generative-AI development direction, although the supplied evidence does not establish a specific released product or capability.
- **2026-02-05 — Roblox Advances Creation with the Cube Foundation Model.** On 2026-02-05, Roblox published a newsroom update on accelerating creation with its Cube foundation model. The supplied links also identify an earlier Cube announcement plus public GitHub and Hugging Face resources, making this a concrete public development step in Roblox's AI-creation tooling.

## What changed

2023-02-18 — Roblox тестировал ввод на естественном языке для создания и изменения кода, внешнего вида и поведения игровых объектов; это была ранняя экспериментальная линия. 2025-03-17 — Roblox представил и открыл Cube 3D v0.1: модель и стартовый код для text-to-shape, а также beta Mesh Generation в Studio и Lua API. 2025-07 (найдено сегодня) — Cube 3D v0.5 стал текущим дефолтом репозитория: улучшены текстовое соответствие и управление bounding box. 2026-02-05 — 4D Generation beta перенесла акцент со статического меша на функциональную многокомпонентную модель: схема задаёт части, а скрипты подстраиваются под её размер и форму. 2026-05-28 (найдено сегодня) — CubePart добавил генерацию и сегментацию именованных частей по открытой пользовательской схеме; прямой доступ в Studio ещё заявлен как будущий.

## How to use this

As of 2026-02-05, practitioners evaluating Roblox creation tooling should treat Roblox Cube as a separately documented foundation-model route and consult the linked official, GitHub, and Hugging Face resources for current access and usage details.

1. Для объекта внутри Roblox используйте `GenerationService:GenerateModelAsync` с `TextPrompt` и схемой; начните с документированных `Car5` либо `Body1`.
  — <https://create.roblox.com/docs/reference/engine/classes/GenerationService>
2. Обработайте результат через `pcall`, затем масштабируйте и позиционируйте модель, закрепите её части и только после этого подключайте игровое поведение.
  — <https://create.roblox.com/docs/reference/engine/classes/GenerationService>
3. Для локального text-to-3D клонируйте `Roblox/cube`, установите зависимости в виртуальное окружение, скачайте веса `Roblox/cube3d-v0.5` и запустите `cube3d.generate`; результат сохраняется как OBJ.
  — <https://github.com/Roblox/cube>
4. Если объект должен подходить под заданный габарит, передайте `--bounding-box-xyz`; для проверки визуального результата используйте примеры репозитория или turntable-рендер.
  — <https://github.com/Roblox/cube>

## Best practices

- Сначала проектируйте схему из имён частей, от которых зависит игровой код; для машины это кузов и отдельные колёса, а не один монолитный меш.
  — <https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator>
- Новые локальные интеграции начинайте с Cube 3D v0.5, а v0.1 оставьте только для воспроизведения старого результата.
  — <https://github.com/Roblox/cube>
- Планируйте минимум 16 ГБ VRAM либо 24 ГБ для `--fast-inference`; при медленном декодировании снижайте `resolution-base` в диапазоне 4.0–9.0.
  — <https://github.com/Roblox/cube>
- Не задавайте экстремальные bounding box без проверки: v0.5 может вернуть разъединённые или диагональные компоненты.
  — <https://github.com/Roblox/cube>
- Не публикуйте результат CubePart без проверки пересечений и пространственных отношений частей: Roblox прямо указывает, что overlap и различение направлений ещё требуют улучшения.
  — <https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator>

## Superseded by this

- 2023-02-18 — ориентироваться на ранний эксперимент natural-language code/object generation как на рабочий контракт устарело; его сменили документированные Cube и GenerationService.
- 2025-03-17 — использовать Cube 3D v0.1 как текущий дефолт устарело с выходом Cube 3D v0.5 в июле 2025.
- 2025-03-17 — предполагать только статический single-mesh workflow устарело для Roblox-интеграции: 4D beta добавила Car5 и Body1, но не доказала общий произвольный schema workflow.
- 2026-09-04 — `GenerationService:GenerateMeshAsync` помечен deprecated; новая интеграция должна использовать `GenerateModelAsync`.

## Still unknown

- 4D Generation обозначен как beta; текущие источники не подтверждают доступность по регионам, аккаунтам, квоты или стоимость для конкретного опыта.
- Компания-level AI Assistant и модельно-API линия Cube связаны, но это не полный список AI-функций Roblox; практические шаги выше относятся только к Cube, CubePart и GenerationService.
- CubePart заявлен как будущая функция Roblox Studio, однако найденные источники не дают даты публичного Studio-релиза или отдельного Studio API.

## Sources

| source | title | read |
|---|---|---|
| https://www.wired.com/story/roblox-generative-ai-gaming-universe/ | Roblox Is Bringing Generative AI to Its Gaming Universe | WIRED | 2026-09-04 |
| https://about.roblox.com/newsroom/2025/03/introducing-roblox-cube | Introducing Roblox Cube: Our Core Generative AI System for 3D and 4D | Roblox | 2026-09-04 |
| https://about.roblox.com/newsroom/2026/02/accelerating-creation-powered-roblox-cube-foundation-model | Accelerating Creation, Powered by Roblox’s Cube Foundation Model | Roblox | 2026-09-04 |
| https://github.com/Roblox/cube | Cube: Generative AI System for 3D | 2026-09-04 |
| https://huggingface.co/Roblox/cube3d-v0.1 | Roblox/cube3d-v0.1 · Hugging Face | 2026-09-04 |
| https://about.roblox.com/newsroom/2026/05/cubepart-roblox-open-vocabulary-part-controllable-3d-generator | CubePart: An Open-Vocabulary Part-Controllable 3D Generator | Roblox | 2026-09-04 |
| https://create.roblox.com/docs/reference/engine/classes/GenerationService | GenerationService | Documentation - Roblox Creator Hub | 2026-09-04 |
| https://create.roblox.com/docs/zh-cn/parts/model-generation | 模型生成 | 文档 - Roblox 创作者中心 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:roblox`, thread `roblox-ai-creation`, 2 dated events 2023-02-18 → 2026-02-05.
- **Practical note:** As of 2026-02-05, practitioners evaluating Roblox creation tooling should treat Roblox Cube as a separately documented foundation-model route and consult the linked official, GitHub, and Hugging Face resources for current access and usage details.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
