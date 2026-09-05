---
title: ComfyUI-PuLID-Flux2 — PuLID-Flux2 ComfyUI integration
category: projects
date: 2026-03-16
tags: [comfyui-pulid-flux2, project, pulid, pulid-flux2-comfyui-integration]
aliases: ["ComfyUI-PuLID-Flux2"]
---

# ComfyUI-PuLID-Flux2 — PuLID-Flux2 ComfyUI integration

**Development line:** `project:comfyui-pulid-flux2` · thread `pulid-flux2-comfyui-integration`  
**Last event:** 2026-03-16 · 1 dated since 2026-03-16 · **Researched:** 2026-09-05 · confidence: high

## What it is

ComfyUI-PuLID-Flux2 — адаптация PuLID для ComfyUI и FLUX.2: загружает InsightFace AntelopeV2, EVA-CLIP и PuLID-веса, затем применяет идентичность к модели перед семплингом. Возможности: Klein 4B/9B и Dev, выбор лица по индексу, отладочный просмотр, готовый Klein workflow. Ограничение: EVA-CLIP автоматически загружает около 800 MB, а training scripts удалены как нестабильные. Вердикт: применим для identity-preserving portrait workflows, но используйте нативные Flux.2-веса и проверяйте совместимость конкретной модели.

## Development line

- **2026-03-16 — ComfyUI-PuLID-Flux2 setup resources were linked.** On 2026-03-16, the ComfyUI-PuLID-Flux2 repository was linked together with its workflow directory and external PuLID and antelopev2 model resources. This records a practical integration reference point for the project, but the available evidence does not establish a release, version, or specific implementation change.

## What changed

2026-03-16 — v0.2.1 исправил dimension mismatch при переключении между Flux.2 Klein и Dev; в тот же день были исправлены связь и имена в example workflow. 2026-03-17 — исправлен конфликт dtype FP16/BF16. 2026-03-20 — v0.3.0 исправил single blocks, half/bfloat16, sigma range и EVA-CLIP 3D; добавлен training pipeline для Vast.ai. 2026-03-21 — v0.4.0 добавил safetensors, веса на Hugging Face и обновлённые настройки. 2026-03-25—2026-03-28 — v0.5.0 добавил новые веса; v0.6.0 добавил нативные v1/v2; v0.6.2 вернул поддержку Dev32. 2026-03-30 и 2026-04-24 — внесены обход детекции через model_function_wrapper и защита от накопительного monkey-patching block.forward.

## How to use this

From 2026-03-16, practitioners should use the linked project workflows together with the referenced PuLID and antelopev2 model sources when preparing a ComfyUI-PuLID-Flux2 setup, while verifying exact version and installation requirements separately.

1. Клонируйте custom node в ComfyUI/custom_nodes и установите указанные зависимости; не запускайте полный requirements.txt в уже работающей установке ComfyUI.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>
2. Скачайте нативный PuLID-Flux2 checkpoint и поместите его в ComfyUI/models/pulid/.
  — <https://huggingface.co/Fayens/Pulid-Flux2>
3. Поместите файлы AntelopeV2 в ComfyUI/models/insightface/models/antelopev2/.
  — <https://huggingface.co/MonsterMMORPG/InstantID_Models/tree/main/models/antelopev2>
4. Импортируйте Klein workflow, подключите референсное фото, Flux.2 model, PuLID model, EVA-CLIP и InsightFace к Apply PuLID Flux.2.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2/tree/main/workflows>

## Best practices

- Начинайте со strength 1.0; документация автора указывает 1.4 как рекомендуемую настройку, но повышайте значение только после визуальной проверки идентичности и артефактов.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>
- Для Flux.2 используйте нативные checkpoint-веса v1/v2, а не исходные PuLID-FLUX v0.9.x: последние относятся к более ранней линии FLUX.
  — <https://huggingface.co/Fayens/Pulid-Flux2>
- Не устанавливайте eva_clip напрямую из GitHub; загрузчик проекта получает EVA-CLIP автоматически.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>

## Superseded by this

- 2026-03-16: guidance for workflows that assumed Klein and Dev could be switched without rebuilding PuLID module is obsolete; v0.2.1 fixed the dimension mismatch.
- 2026-03-17: hard assumptions about a single FP16/BF16 path are obsolete; the dtype mismatch was fixed.
- 2026-03-26: pre-native-weight guidance is superseded for Flux.2 by native PuLID-Flux2 v1/v2 weights.

## Still unknown

- Требуемые поля event_findings и new_events отсутствуют в предоставленной выходной схеме; их проверяемая хронология включена в what_changed. Для события 2026-03-16 GitHub history даёт собственную дату и точную коррекцию: v0.2.1 устранил dimension mismatch Klein↔Dev, а workflow получил исправление соединения.
- Репозиторий сообщает о поддержке Klein и Dev, но не предоставляет независимый benchmark идентичности, VRAM-профиль или гарантию стабильности для всех вариантов FLUX.2.
- Исходный guozinan/PuLID публикует PuLID-FLUX-v0.9.0/v0.9.1 для ранней линии FLUX; это не тот же checkpoint, что нативные PuLID-Flux2 v1/v2.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/iFayens/ComfyUI-PuLID-Flux2 | iFayens/ComfyUI-PuLID-Flux2 README | 2026-09-05 |
| https://github.com/iFayens/ComfyUI-PuLID-Flux2/commits/main | iFayens/ComfyUI-PuLID-Flux2 commit history | 2026-09-05 |
| https://github.com/iFayens/ComfyUI-PuLID-Flux2/tree/main/workflows | ComfyUI-PuLID-Flux2 workflows | 2026-09-05 |
| https://huggingface.co/Fayens/Pulid-Flux2 | Fayens/Pulid-Flux2 model repository | 2026-09-05 |
| https://huggingface.co/MonsterMMORPG/InstantID_Models/tree/main/models/antelopev2 | MonsterMMORPG/InstantID_Models AntelopeV2 files | 2026-09-05 |
| https://huggingface.co/guozinan/PuLID | guozinan/PuLID model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-pulid-flux2`, thread `pulid-flux2-comfyui-integration`, 1 dated events 2026-03-16 → 2026-03-16.
- **Practical note:** From 2026-03-16, practitioners should use the linked project workflows together with the referenced PuLID and antelopev2 model sources when preparing a ComfyUI-PuLID-Flux2 setup, while verifying exact version and installation requirements separately.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
