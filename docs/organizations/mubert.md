---
title: Mubert — Mubert Text-to-Music
category: organizations
tags: [mubert, mubert-text-to-music, organization]
aliases: ["Mubert"]
---

# Mubert — Mubert Text-to-Music

**Development line:** `organization:mubert` · thread `mubert-text-to-music`  
**Events:** 1 dated, 2022-10-20 → 2022-10-20 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Mubert — сервис генерации и лицензирования музыки для авторов видео и команд, которым нужен веб-инструмент Render или API вместо самостоятельной музыкальной системы. Возможности: - Render: текст или изображение → трек, выбор типа и длительности; - API v3: генерация треков и потоков, параметры и webhook-статусы; - Track Editor: секции, слои, BPM, тональность и длительность уже сгенерированного трека. Лимит: Text-to-Music в API принимает английскую подсказку до 200 символов; Text-to-Music и Image-to-Music должны быть включены договором. Вердикт: для ручной работы подходит Render, для интеграции в продукт — API v3.

## Development line

- **2022-10-20 — Mubert published a text-to-music GitHub and Colab workflow.** On 2022-10-20, Mubert's development line included a public GitHub repository and linked Google Colab notebook for a text-to-music workflow. The dated links establish the availability of those implementation resources, but do not establish their underlying model, support status, or performance.

## What changed

Mubert — путь от демонстрации prompt-to-music к отдельным интерфейсам для авторов и интеграций. - 2022-10-20: GitHub-репозиторий и Colab-ноутбук показали генерацию по текстовой подсказке и длительности через Mubert API, включая режимы loop и track. - 2022-10-28: доступна только ссылка на прежний The source-пост; отдельное изменение продукта из неё не подтверждено. - Найдено сегодня, 2026-09-04: Mubert Render принимает текст или изображение для создания трека, а API v3 документирует генерацию треков, потоков, пользовательские учётные данные и webhook-уведомления. - Найдено сегодня, 2026-09-04: Track Editor в Render меняет секции и слои созданного в Mubert трека; Remix создаёт новую версию и сохраняет исходную. Ограничение: первичные текущие страницы не называют даты запуска API v3 или Track Editor. Вердикт: исторический Colab остаётся примером ранней интеграции, но не текущим рабочим интерфейсом.

## How to use this

From 2022-10-20, practitioners could use Mubert's linked GitHub repository and Colab notebook as a starting point for evaluating a text-to-music workflow; the dated links alone do not justify assumptions about current availability or capabilities.

1. Mubert Render — откройте Generate, введите текст на английском или загрузите изображение, выберите Track и длительность, затем запустите генерацию.
  — <https://mubert.com/render>
2. Mubert Render — откройте созданный трек в Track Editor, измените секции, слои, BPM, тональность или длительность, затем нажмите Remix и сохраните новую версию.
  — <https://mubert.com/render/track-editor>
3. Mubert Render — до публикации выберите подходящий тип лицензии для конкретного сценария и скачайте трек в рамках выбранного плана.
  — <https://mubert.com/documents/mubert_render_license.pdf>
4. Mubert API — запросите API-ключи и перед интеграцией проверьте разрешённые возможности и лимиты лицензии.
  — <https://mubert.com/api/docs>
5. Mubert API — создайте запись customer для каждого конечного пользователя и используйте выданные customer-id и access-token в публичных запросах.
  — <https://mubert.com/api/docs>
6. Mubert API — отправьте запрос в public/tracks с prompt либо playlist_index, длительностью и параметрами; затем получите статус трека или настройте webhook на лицензии.
  — <https://mubert.com/api/docs>

## Best practices

- Mubert API — пишите явную английскую подсказку не длиннее 200 символов, всегда задавайте длительность и выбирайте track для композиции с началом и концом либо loop для зацикливания.
  — <https://mubert.com/api/docs>
- Mubert API — до запуска Text-to-Music или Image-to-Music проверяйте, что возможность включена договором, а лимит лицензии достаточен для нагрузки.
  — <https://mubert.com/api/docs>
- Mubert API — для асинхронной генерации обрабатывайте webhook-статусы либо опрашивайте модель трека, а не считайте файл готовым сразу после отправки запроса.
  — <https://mubert.com/api/docs>
- Mubert Render — сохраняйте исходный трек и работайте итерациями: Remix не перезаписывает оригинал; редактор не принимает загруженное внешнее аудио и не экспортирует слои отдельно.
  — <https://mubert.com/render/track-editor>
- Mubert Render — согласуйте лицензию до релиза: не распространяйте трек отдельно или через стоковую площадку, если это не разрешено конкретным договором.
  — <https://mubert.com/documents/mubert_render_license.pdf>

## Superseded by this

- 2022-10-20: начинать новую работу с Colab-ноутбука Mubert-Text-to-Music — устаревшая практика по умолчанию; для новых задач использовать Render или API v3. Это смена рабочего маршрута по текущим первичным endpoints, а не официальное уведомление о закрытии репозитория.
- 2022-10-20: воспринимать указанную в ноутбуке бесплатную attribution-лицензию как актуальное правило публикации — устаревшее руководство; права определяются текущей лицензией Render либо отдельным договором API.

## Still unknown

- Содержимое источника для события 2022-10-28 недоступно: URL The source вернул ошибку, поэтому нельзя установить, был ли это репост, комментарий или отдельный релиз.
- Поиск в упрощённо-китайском направлении не нашёл актуальной первичной страницы Mubert на китайском; найдены только английская, корейская и японская локализации.
- На странице Track Editor планы Pro и Business заявляют «App & Services», но лицензия Mubert Render запрещает использование трека в мобильном приложении или ПО; перед таким использованием нужно получить письменное разъяснение или работать по отдельному API-договору.
- Не найдено подтверждение, что два события относятся к разным объектам: оба указывают на Mubert, но второе событие недостаточно содержательно для построения самостоятельной линии развития.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/MubertAI/Mubert-Text-to-Music | GitHub — MubertAI/Mubert-Text-to-Music | 2026-09-04 |
| https://colab.research.google.com/github/ferluht/Mubert-Text-to-Music/blob/main/Mubert_Text_to_Music.ipynb | Google Colab — Mubert_Text_to_Music.ipynb | 2026-09-04 |
| https://mubert.com/render | Mubert Music Rendering — Render Music | 2026-09-04 |
| https://mubert.com/render/track-editor | AI Track Editor by Mubert — Edit AI Music | 2026-09-04 |
| https://mubert.com/api/docs | Mubert API Docs — AI Music Generation API Documentation | 2026-09-04 |
| https://mubert.com/documents/mubert_render_license.pdf | Mubert Render License | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:mubert`, thread `mubert-text-to-music`, 1 dated events 2022-10-20 → 2022-10-20.
- **Practical note:** From 2022-10-20, practitioners could use Mubert's linked GitHub repository and Colab notebook as a starting point for evaluating a text-to-music workflow; the dated links alone do not justify assumptions about current availability or capabilities.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
