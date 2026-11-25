---
title: OpenPose Studio for ComfyUI — Project development
category: projects
date: 2026-07-28
tags: [comfyui-openpose-studio, comfyui_openpose_studio, project, project-development]
aliases: ["OpenPose Studio for ComfyUI"]
---

# OpenPose Studio for ComfyUI — Project development

**Development line:** `project:comfyui-openpose-studio` · thread `project-development`  
**Last event:** 2026-07-28 · 1 dated since 2026-07-28 · **Researched:** 2026-09-05 · confidence: high

## What it is

OpenPose Studio for ComfyUI — редактор поз внутри ComfyUI для художника, который хочет поправить скелет, руки или JSON, а не принимать результат pose-estimator как есть. Возможности: COCO-18 тело, по-точечная правка рук, галерея и объединение JSON-поз, вход DWPose и выходы IMAGE/JSON/KPS. Ограничение: точки лица сохраняются и рендерятся, но по отдельности не редактируются. Вердикт: это практичная альтернатива отдельному OpenPose-редактору, если контроль позы уже нужен в графе ComfyUI.

## Development line

- **2026-07-28 — ComfyUI-OpenPose-Studio repository referenced.** Редактор рук получил больше рабочей области, а фоновые референсы и направляющие были исправлены для увеличенного режима.

## What changed

2026-07-28 — актуальным ближайшим состоянием был OpenPose Studio 2.0.2: редактор рук получил больше рабочей области, а фоновые референсы и направляющие были исправлены для увеличенного режима. 2026-07-29 — версия 2.1.0 добавила предпросмотр выбранной позы в Gallery, 14 жестов рук и инструменты восстановления/удаления точек руки. 2026-07-30 — версия 2.1.1 добавила локализацию на хинди. 2026-08-08 — версия 2.2.0 добавила вставку отсутствующей руки перетаскиванием, выбор ориентации ладони и уведомление об обновлении. 2026-08-14 — версия 2.3.0 добавила адаптивный сенсорный интерфейс и компактную мобильную Gallery.

## How to use this

As of 2026-07-28, practitioners should treat ComfyUI-OpenPose-Studio as a project to evaluate from its linked GitHub repository; the available record does not yet support a more specific installation or workflow recommendation.

1. В ComfyUI Extension Manager откройте Nodes Manager, найдите `openpose-studio`, установите расширение и перезапустите ComfyUI.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
2. Добавьте узел `image > OpenPose Studio`, откройте редактор через предпросмотр, выберите позу из пресета или Gallery и перетащите ключевые точки.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
3. Нажмите Apply; подключите `image` к следующим image-узлам, а `kps` — к ControlNet/OpenPose-совместимому узлу.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
4. Для исправления результата детектора подключите выход DWPose Estimator к необязательному входу `pose_keypoint`, затем уточните точки в редакторе.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>

## Best practices

- Перед импортом проверяйте JSON: нужны числовые координаты и структура с `pose_keypoints_2d`; для тела ожидаются 18 ключевых точек.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Для несоответствующих размеров поз сначала масштабируйте их до целевого разрешения: Pose Merger не выравнивает разрешение коллекции автоматически.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Если редактор или предпросмотр не появился, полностью перезапустите ComfyUI, сделайте жёсткое обновление страницы и проверьте browser console и startup log.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>
- Фоновые изображения используйте как временный референс: они сохраняются в рамках сессии ComfyUI, но не записываются в workflow.
  — <https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md>

## Superseded by this

- 2026-07-29: прежняя Gallery без предпросмотра выбранной позы и 14 встроенных жестов рук заменена поведением 2.1.0.
- 2026-08-08: прежний ручной путь добавления отсутствующих рук заменён поддерживаемой вставкой drag-to-canvas в 2.2.0.
- 2026-08-14: прежняя desktop-first компоновка заменена адаптивными сенсорными представлениями 2.3.0.

## Still unknown

- Для события 2026-07-28 не найден отдельный первичный релиз или commit с этой точной датой. Подтверждённый ближайший релиз 2.0.2 датирован авторским changelog 2026-07-27; поэтому его детали приведены как уточнение к событию, а не как новый шаг на 2026-07-28.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/andreszs/ComfyUI-OpenPose-Studio | andreszs/ComfyUI-OpenPose-Studio — repository | 2026-09-05 |
| https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/CHANGELOG.md | OpenPose Studio changelog | 2026-09-05 |
| https://raw.githubusercontent.com/andreszs/ComfyUI-OpenPose-Studio/main/docs/README.md | OpenPose Studio documentation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-openpose-studio`, thread `project-development`, 1 dated events 2026-07-28 → 2026-07-28.
- **Practical note:** As of 2026-07-28, practitioners should treat ComfyUI-OpenPose-Studio as a project to evaluate from its linked GitHub repository; the available record does not yet support a more specific installation or workflow recommendation.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
