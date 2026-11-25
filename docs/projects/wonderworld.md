---
title: WonderWorld
category: projects
date: 2024-12-30
tags: [project, wonderworld, wonderworld-development]
aliases: ["WonderWorld"]
---

# WonderWorld

**Development line:** `project:wonderworld` · thread `wonderworld-development`  
**Last event:** 2024-12-30 · 2 dated since 2024-07-11 · **Researched:** 2026-09-05 · confidence: high

## What it is

WonderWorld — код исследовательского метода для разработчиков 3D-генерации: из одной стартовой картинки он строит и интерактивно достраивает связанные 3D-сцены по движению камеры и текстовым описаниям. Возможности: FLAGS-представление, послойная генерация, guided depth diffusion; ориентир производительности — 9,5 секунды на сцену на A6000. Вердикт: воспроизводимый исследовательский стек, требующий CUDA GPU с 48 GB памяти, а не готовый облачный продукт.

## Development line

- **2024-07-11 — WonderWorld project website linked.** On 2024-07-11, the record linked a public WonderWorld project website. The dated link establishes a public project reference, but does not show whether it marked a launch, update, or repost.
- **2024-12-30 — WonderWorld GitHub repository linked.** On 2024-12-30, the record linked the WonderWorld GitHub repository. This adds a code-hosting reference to the development line, but the dated links alone do not establish whether the repository was newly published or merely referenced.

## What changed

2024-07-11 — страница проекта представляла интерактивную генерацию связанных 3D-сцен из одной картинки; препринт от 2024-06-13 уточняет FLAGS и guided depth diffusion, а также заявляет время менее 10 секунд на A6000. 2024-12-30 — появился публичный код, превративший метод в воспроизводимый локальный пайплайн с конфигурациями, интерактивным просмотром и сохранением сгенерированной сцены. 2025-06-11 — работа вышла на CVPR 2025 как Highlight; это публикационный статус, а не новая версия публичного кода.

## How to use this

From 2024-12-30, practitioners evaluating WonderWorld should consult the linked project page and GitHub repository together; the dated links alone do not establish installation, reproduction, or release-readiness guidance.

1. Клонировать репозиторий, создать окружение Python 3.10 и установить зависимости по README на CUDA-совместимой машине с 48 GB GPU-памяти.
  — <https://github.com/KovenYu/WonderWorld>
2. Скачать checkpoint RepViT-SAM в корень репозитория и при необходимости задать ключ OpenAI только для автоматического создания описаний сцен.
  — <https://github.com/KovenYu/WonderWorld>
3. Настроить пример YAML, запустить run.py на сервере, открыть локальный viewer через SSH-туннель и выбрать новый ракурс клавишей R; X сохраняет результат.
  — <https://github.com/KovenYu/WonderWorld>

## Best practices

- Начинать с готового example.yaml и менять параметры по одному; README включает depth_conditioning и параметры камеры, а текущая страница проекта предупреждает, что сложные объекты могут давать holes и floaters при смене ракурса.
  — <https://github.com/KovenYu/WonderWorld>
- Использовать ручное текстовое описание сцены, если не нужен внешний LLM; use_gpt=False оставляет описание под контролем оператора.
  — <https://github.com/KovenYu/WonderWorld>
- Сохранять удачные миры и загружать их через load_gen вместо повторной генерации.
  — <https://github.com/KovenYu/WonderWorld>

## Superseded by this

- 2024-06-13 — утверждение препринта «код будет выпущен» устарело: публичный репозиторий теперь содержит инструкции по установке и запуску.
- 2024-06-13 — статус только препринта устарел: страница проекта указывает CVPR 2025 (Highlight).

## Still unknown

- Первоначальная дата и точный объём первого публичного коммита репозитория не подтверждены независимым датированным GitHub API-ответом; событие 2024-12-30 подтверждает наличие ссылки на репозиторий, но не дату конкретного коммита.
- Публичный README не фиксирует поддерживаемый статус после пяти показанных коммитов, поэтому нельзя утверждать, что проект активно сопровождается.

## Sources

| source | title | read |
|---|---|---|
| https://wonderworld-2024.github.io/ | WonderWorld 2024 project page | 2026-09-05 |
| https://github.com/KovenYu/WonderWorld | KovenYu/WonderWorld repository and README | 2026-09-05 |
| https://arxiv.org/abs/2406.09394 | WonderWorld: Interactive 3D Scene Generation from a Single Image | 2026-09-05 |
| https://kovenyu.com/wonderworld/ | WonderWorld project page | 2026-09-05 |
| https://openaccess.thecvf.com/content/CVPR2025/papers/Yu_WonderWorld_Interactive_3D_Scene_Generation_from_a_Single_Image_CVPR_2025_paper.pdf | WonderWorld CVPR 2025 paper | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:wonderworld`, thread `wonderworld-development`, 2 dated events 2024-07-11 → 2024-12-30.
- **Practical note:** From 2024-12-30, practitioners evaluating WonderWorld should consult the linked project page and GitHub repository together; the dated links alone do not establish installation, reproduction, or release-readiness guidance.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
