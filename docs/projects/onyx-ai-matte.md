---
title: ONYX Ai Matte
category: projects
date: 2026-03-10
tags: [onyx-ai-matte, project]
aliases: ["ONYX Ai Matte"]
---

# ONYX Ai Matte

**Development line:** `project:onyx-ai-matte` · thread `onyx-ai-matte`  
**Last event:** 2026-03-10 · 1 dated since 2026-03-10 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ONYX Ai Matte — локальный OFX-инструмент для ротоскопинга и извлечения альфы в Nuke, DaVinci Resolve, Fusion, Flame и Natron. Возможности: prompts box/point/text/mask, трекинг до 16 объектов, VitMatte/MeMatte-уточнение края, экспорт запечённых масок. Лимит: Windows требует NVIDIA RTX 20-series+ и 6 GB VRAM; macOS — Apple Silicon и macOS 15+; результат обычно закрывает 60–80% матта, финальную доводку делает композер. Вердикт: практичная альтернатива Magic Mask для локального OFX-пайплайна, но не замена контролю качества финальной маски.

## Development line

- **2026-03-10 — ONYX Ai Matte project resources were linked.** On 2026-03-10, the ONYX Ai Matte development line was associated with its project website and a Hugging Face resource link. The dated links establish an externally accessible project reference, but do not establish a specific release, model version, capability, or change without the original post or research.

## What changed

2026-03-10 — ссылка в событии вела на официальный сайт ONYX; независимого датированного подтверждения конкретного изменения именно в этот день не найдено. 2026-03-24 — опубликован ONYX Ai Matte v2.5: пять режимов работы, авто-трекинг, text/mask prompts и многoобъектная сегментация. 2026-07-17 — v3.1.0 добавила управление входным цветом для ACES/OCIO, прокси-активацию и исправления стабильности. 2026-08-03 — v3.2.0 добавила Apple Silicon/macOS и Flame. 2026-08-12 — v3.3.0 увеличила кэш отслеженных масок примерно до 12 000 6K кадров. 2026-08-31 — v3.4.0 добавила раздельные каналы для object mask и unknown zone в Refiner Direct.

## How to use this

From 2026-03-10, practitioners should treat ONYX Ai Matte as a separately linked project/resource line and verify current availability and usage against its official site and Hugging Face resource before adoption.

1. Закройте хост, установите актуальный пакет, затем перезапустите хост и добавьте OFX-эффект ONYX Ai Matte v3; пробный период на 7 дней стартует при первом добавлении ноды.
  — <https://onyxofx.com/docs/>
2. Подайте клип в Source, на стартовом кадре выделите объект box/point/text/mask prompt и запустите однопроходное воспроизведение для последовательного трекинга.
  — <https://onyxofx.com/docs/>
3. Проверьте маску, скорректируйте край VitMatte/MeMatte и при необходимости запеките PNG/EXR-последовательность в отдельную папку.
  — <https://onyxofx.com/docs/>

## Best practices

- Отключайте Loop при трекинге; для полного прохода от стартового кадра в обе стороны используйте Bounce/Ping-Pong.
  — <https://onyxofx.com/docs/>
- Для нестабильного или обрезанного на быстром движении трека увеличивайте Crop Padding либо отключайте Crop Mode.
  — <https://onyxofx.com/docs/>
- Не принимайте AI-матт без проверки: инструмент рассчитан примерно на 60–80% результата, оставляя финальную доводку композеру.
  — <https://onyxofx.com/docs/>

## Superseded by this

- 2026-08-31 — Refiner Direct Mode заменён назначением object mask и unknown zone по отдельным входным каналам в v3.4.0.
- 2026-08-12 — прежний малый кэш трекинга заменён сжатым кэшем v3.3.0.
- 2026-08-03 — состояние до macOS/Flame-поддержки устарело после v3.2.0.

## Still unknown

- Официальные release notes не содержат записи за 2026-03-10; поэтому нельзя надёжно приписать этому дню конкретную версию или функцию.
- Короткая ссылка https://hf.ru/linkd4c82 не открылась при проверке и не использована как доказательство.
- В заданной JSON-схеме нет полей event_findings и new_events; подтверждённые дополнительные даты включены в what_changed, а привязка к событию 2026-03-10 сохранена как неопределённость.

## Sources

| source | title | read |
|---|---|---|
| https://onyxofx.com/ | ONYX Ai Matte — AI Roto for Nuke & Resolve. No Subscription | 2026-09-05 |
| https://onyxofx.com/docs/ | ONYX Ai Matte Documentation | Install and Parameters | 2026-09-05 |
| https://onyxofx.com/release-notes/ | Release Notes — ONYX Ai Matte | 2026-09-05 |
| https://www.cgchannel.com/2026/03/onyx-ai-matte-automatically-generates-masks-from-video-footage/ | ONYX Ai Matte automatically generates masks from video | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:onyx-ai-matte`, thread `onyx-ai-matte`, 1 dated events 2026-03-10 → 2026-03-10.
- **Practical note:** From 2026-03-10, practitioners should treat ONYX Ai Matte as a separately linked project/resource line and verify current availability and usage against its official site and Hugging Face resource before adoption.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
