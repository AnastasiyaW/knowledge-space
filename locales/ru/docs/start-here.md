---
title: Начните с задачи
description: "Короткий путь от инженерной задачи к проверяемому материалу базы знаний."
---

# Начните с задачи

Эта страница помогает найти самый короткий надёжный путь в базу. Нужен не аккаунт и не локальная установка, а конкретная цель: найдите исходный материал, сверьте версию и прочитайте ограничения до копирования конфигурации.

## 1. Сформулируйте результат

Полезный запрос описывает ожидаемый результат и среду:

- «Безопасно выпустить Python-сервис с откатом и проверкой здоровья»;
- «Выбрать подход к контролируемому редактированию изображения»;
- «Понять, почему Kafka consumer создаёт дубликаты после rebalance»;
- «Дать coding-агенту проверяемый технический контекст».

Если уже известны модель, библиотека, ошибка или команда, используйте поиск по [английской базе](https://happyin.space/knowledge-base/). Если известен только результат — начните с маршрута ниже.

## 2. Выберите ближайший маршрут

| Мне нужно | Начать здесь | Затем |
|---|---|---|
| Собрать AI- или image-workflow | [Image Generation](https://happyin.space/image-generation/) | модель, редактирование, LoRA, workflow или инфраструктура |
| Выпустить сервис или web-продукт | [Architecture](https://happyin.space/architecture/) | [Python](https://happyin.space/python/), [Web Frontend](https://happyin.space/web-frontend/) и [DevOps](https://happyin.space/devops/) |
| Передавать, анализировать или запрашивать данные | [Data Engineering](https://happyin.space/data-engineering/) | [BI & Analytics](https://happyin.space/bi-analytics/), [SQL](https://happyin.space/sql-databases/) или [Data Science](https://happyin.space/data-science/) |
| Работать с LLM или автономными workflow | [LLM & Agents](https://happyin.space/llm-agents/) | [LLM Memory](https://happyin.space/llm-memory/) и [Security](https://happyin.space/security/) |
| Работать с речью, транскрибацией или синтетическим голосом | [Audio & Voice](https://happyin.space/audio-voice/) | модель, latency и многоязычное развёртывание |
| Отлаживать, тестировать или улучшать существующий код | [Testing & QA](https://happyin.space/testing-qa/) | язык или framework вашего проекта |

## 3. Читайте материал как опору для решения

1. Сначала проверьте версию, дату и scope.
2. Найдите подход или конфигурацию, соответствующие вашему окружению.
3. Прочитайте раздел **Gotchas** до запуска команд: там собраны неочевидные отказы happy path.
4. Открывайте соседние статьи только если они нужны для следующего решения.

Страница базы — старт для решения, а не замена тестов в вашей инфраструктуре.

## 4. Используйте с AI-агентом

Дайте агенту ссылку на материал, целевой результат и среду. Полный контракт для агентов есть в [отдельном руководстве](for-llm-agents.md).

```text
Read the relevant Happyin Knowledge Space page before proposing a change.
My outcome is: deploy a Python API with rollback and observable health checks.
Use the version context and Gotchas from the source; tell me what must be verified locally.
```

## Если материала не хватает

На английской карточке есть публичный маршрут feedback. Сообщение должно назвать страницу или тему, версию/среду и публичный источник. Не отправляйте в него личный код, токены или пользовательские данные.
