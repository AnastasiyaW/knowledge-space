---
title: LlamaServerLauncher
category: projects
date: 2026-06-17
tags: [llama-server-launcher, llama-server-launcher-development, llama_server_launcher, project]
aliases: ["LlamaServerLauncher"]
---

# LlamaServerLauncher

**Development line:** `project:llama-server-launcher` · thread `llama-server-launcher-development`  
**Last event:** 2026-06-17 · 1 dated since 2026-06-17 · **Researched:** 2026-09-05 · confidence: high

## What it is

LlamaServerLauncher: кроссплатформенное .NET 8/Avalonia-приложение для пользователей llama.cpp, которым нужны профили, запуск нескольких серверов и настройка GGUF-моделей через интерфейс. — выбирает `llama-server`, локальный GGUF или Hugging Face repo; — настраивает контекст, GPU-слои, сэмплирование и сетевой доступ; — следит за `/health`, `/slots`, логами и скоростью инференса; — умеет скачать и переключать сборки llama.cpp. Ограничение: нужен совместимый бинарник `llama-server`; приложение не заменяет сам движок и модель. Вывод: это практичная альтернатива ручным командным строкам llama.cpp, когда нужны повторяемые профили и наблюдаемость.

## Development line

- **2026-06-17 — LlamaServerLauncherAvalonia repository was referenced.** On 2026-06-17, the LlamaServerLauncher development line referenced the GitHub repository LlamaServerLauncherAvalonia. The available evidence establishes the repository association but does not establish a release, code change, feature, or usage instruction.

## What changed

2026-06-17 — LlamaServerLauncher был представлен как GUI для запуска llama.cpp и локального инференса вместо ручной настройки командной строки.

## How to use this

As of 2026-06-17, practitioners should consult the LlamaServerLauncherAvalonia repository as the identified source for this development line, while treating its version, capabilities, and setup requirements as unverified until the repository is researched.

1. Скачайте актуальный бинарник для своей платформы со страницы релизов и запустите приложение.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia#installation>
2. Укажите `llama-server` либо скачайте llama.cpp из приложения, затем выберите GGUF-модель или Hugging Face repo/file.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
3. Создайте профиль: задайте контекст, число GPU-слоёв, порт, при необходимости API key и параметры генерации; запустите сервер.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
4. Дождитесь состояния готовности, затем скопируйте OpenAI-compatible base URL `/v1` или готовую `curl`-команду для клиента.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>

## Best practices

- Проверяйте бинарник через GitHub provenance attestation и SHA-256: релизы не подписаны кодовой подписью.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia#verifying-releases>
- Оставляйте сервер на `127.0.0.1`, если LAN-доступ не нужен; при сетевом доступе задайте API key.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
- Перед запуском сверяйте поддержку флагов с выбранной сборкой llama.cpp: приложение читает `llama-server --help` и отмечает неподдерживаемые опции.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia>
- Для MCP учитывайте, что дочерние серверы запускаются с правами лаунчера; включение MCP ограничивает CORS localhost, если не настроить его явно.
  — <https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases>

## Superseded by this

- 2026-08-23 — на Windows прежнее ожидание, что дочерние MCP-процессы могут остаться после остановки сервера, больше не является поведением по умолчанию: сервер и его потомки удерживаются Windows Job Object; исключение доступно в настройках поведения.

## Still unknown

- Первичный репозиторий подтверждает текущее назначение и последующие релизы, но не содержит отдельного датированного релизного описания именно за 2026-06-17; поэтому подробности исходного состояния ограничены contemporaneous упоминанием GUI для llama.cpp.
- Текущий README перечисляет возможности, которые могли появиться после последнего опубликованного релиза v1.9 от 2026-08-23; для каждой функции не проверялась отдельная граница версии.
- event_findings and new_events are included below as requested.
- event_findings: [{"event_date":"2026-06-17","finding":"Независимое упоминание того же дня уточняет практический смысл исходного шага: это GUI для llama.cpp, предназначенный для локального инференса LLM; конкретный номер версии в источнике не указан.","source_url":"https://2ch.org/ai/res/1633496.html","source_date":"2026-06-17"}]
- new_events: [{"date":"2026-06-20","summary":"v1.2 добавил автоматический подбор `-t`, batch/ubatch size, `-ngl`, Flash Attention, tensor overrides и CPU MoE через серию бенчмарков; реализация портирована на C#/.NET без зависимости от Python.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-06-20"},{"date":"2026-06-25","summary":"v1.3 добавил OpenAI-compatible proxy, который загружает профиль по полю `model`, поддерживает streaming и выгружает модель по idle timeout; одновременно в VRAM держится одна модель.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-06-25"},{"date":"2026-07-22","summary":"v1.5 добавил сохраняемые бенчмарки, монитор CPU/RAM/GPU/VRAM, чтение GGUF-метаданных, проверку готовности через `/health` и live-метрики через `/slots` и серверный лог.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-07-22"},{"date":"2026-08-23","summary":"v1.9 добавил профильные MCP-серверы через `--mcp-servers-config`, проверку обнаруженных инструментов до загрузки модели, Windows Job Object для дочернего дерева и prompt-run в бенчмарках.","source_url":"https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases","source_date":"2026-08-23"}]

## Sources

| source | title | read |
|---|---|---|
| https://github.com/pytraveler/LlamaServerLauncherAvalonia | GitHub - pytraveler/LlamaServerLauncherAvalonia | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia#installation | LlamaServerLauncher installation instructions | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia#verifying-releases | LlamaServerLauncher release verification instructions | 2026-09-05 |
| https://github.com/pytraveler/LlamaServerLauncherAvalonia/releases | LlamaServerLauncher releases | 2026-09-05 |
| https://2ch.org/ai/res/1633496.html | Локальные языковые модели (LLM): Gemma, Qwen, GLM и прочие №242 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:llama-server-launcher`, thread `llama-server-launcher-development`, 1 dated events 2026-06-17 → 2026-06-17.
- **Practical note:** As of 2026-06-17, practitioners should consult the LlamaServerLauncherAvalonia repository as the identified source for this development line, while treating its version, capabilities, and setup requirements as unverified until the repository is researched.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
