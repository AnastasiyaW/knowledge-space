---
title: База знаний для AI-агентов
description: "Как дать агенту проверяемый контекст из Happyin Knowledge Space."
---

# База знаний для AI-агентов

Агенту нужна не вся база в prompt, а одна или несколько релевантных карточек с версией, источниками и Gotchas. Канонический технический материал пока преимущественно английский; русская ветка помогает человеку выбрать его без потери смысла.

## Минимальный контракт

1. Найдите материал по задаче в [английском репозитории](https://github.com/AnastasiyaW/knowledge-space) или на [сайте](https://happyin.space/knowledge-base/).
2. Передайте агенту ссылку или Markdown конкретной страницы.
3. Укажите свой результат, версию среды и ограничения.
4. Попросите явно назвать локальные проверки, которые отделяют рабочее решение от предположения.

```text
Use Happyin Knowledge Space as a source, not as a substitute for verification.
Read the relevant page before proposing changes.
Preserve its version limits and Gotchas, and list the checks required in this environment.
```

Если источник устарел или нужной темы нет, используйте публичный feedback-маршрут на английском сайте. В отчёт попадают только публичные факты.
