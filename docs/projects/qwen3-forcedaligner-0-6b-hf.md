---
title: Qwen3-ForcedAligner-0.6B-hf — Qwen3 ASR
category: projects
date: 2026-06-26
tags: [project, qwen3-asr, qwen3-forcedaligner-0-6b-hf]
aliases: ["Qwen3-ForcedAligner-0.6B-hf"]
---

# Qwen3-ForcedAligner-0.6B-hf — Qwen3 ASR

**Development line:** `project:qwen3-forcedaligner-0-6b-hf` · thread `qwen3-asr`  
**Last event:** 2026-06-26 · 1 dated since 2026-06-26 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Qwen3-ForcedAligner-0.6B-hf — токен-классификационная NAR-модель для выравнивания аудиозаписи с транскриптом; подходит вместо WhisperX, когда нужны таймкоды и уже есть текст.

Возможности:

- принимает аудио, транскрипт и язык;
- возвращает временные метки слов или символов;
- работает с транскриптом Qwen3-ASR либо другого ASR;
- поддерживает китайский, английский, кантонский, французский, немецкий, итальянский, японский, корейский, португальский, русский и испанский.

Лимит: до пяти минут речи на один запрос; это модель выравнивания, а не самостоятельный распознаватель речи.

Вердикт: практична для субтитров и сегментации уже распознанной короткой речи, если язык входит в 11 поддерживаемых.

## Development line

- **2026-06-26 — Qwen3-ForcedAligner-0.6B-hf was linked on Hugging Face.** On 2026-06-26, the Qwen3-ForcedAligner-0.6B-hf Hugging Face model page was linked in the Qwen3 ASR thread. This is a material development-line event because it identifies a specific forced-alignment model artifact. The original post and model-card contents were not provided, so no capabilities, release claims, or usage details are asserted.

## What changed

2026-06-26 — опубликован Transformers-совместимый checkpoint Qwen/Qwen3-ForcedAligner-0.6B-hf для принудительного выравнивания речи и текста.

## How to use this

From 2026-06-26, practitioners can treat Qwen3-ForcedAligner-0.6B-hf as an identified forced-alignment model candidate in the Qwen3 ASR line, then verify the model card before adopting it.

1. Установите актуальную сборку Transformers из исходников, как указано в карточке checkpoint, пока не подтверждена минимальная стабильная версия с этой архитектурой.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>
2. Загрузите AutoProcessor и AutoModelForTokenClassification из Qwen/Qwen3-ForcedAligner-0.6B-hf; для GPU используйте bfloat16 и device_map="auto".
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>
3. Получите транскрипт и язык через Qwen3-ASR либо другой ASR, затем передайте аудио, текст и язык в prepare_forced_aligner_inputs.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>
4. Запустите модель без вычисления градиентов и декодируйте logits через decode_forced_alignment, чтобы получить таймкоды.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>

## Best practices

- Подавайте запись речи не длиннее пяти минут и явно задавайте один из 11 поддерживаемых языков.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>
- Сначала проверяйте соответствие транскрипта записи: модель выравнивает предоставленный текст, а не исправляет ошибки ASR.
  — <https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/qwen3_asr.md>
- Для пакетной GPU-обработки измерьте torch.compile на собственных данных; в карточке приведён ориентир около 2,5× на A100 при batch size 4, а не универсальная гарантия.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Официальная минимальная стабильная версия Transformers для checkpoint с суффиксом -hf не указана: карточка рекомендует установку из исходников, хотя актуальная документация Transformers уже описывает эту архитектуру.
- Независимых датированных публикаций именно для checkpoint -hf, помимо обновления официальной коллекции 2026-06-26, не найдено.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf | Qwen/Qwen3-ForcedAligner-0.6B-hf — model card | 2026-09-05 |
| https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/qwen3_asr.md | Transformers documentation: Qwen3-ASR and forced alignment | 2026-09-05 |
| https://arxiv.org/abs/2601.21337 | Qwen3-ASR Technical Report | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B | Qwen/Qwen3-ForcedAligner-0.6B — Qwen ASR package documentation and benchmarks | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-forcedaligner-0-6b-hf`, thread `qwen3-asr`, 1 dated events 2026-06-26 → 2026-06-26.
- **Practical note:** From 2026-06-26, practitioners can treat Qwen3-ForcedAligner-0.6B-hf as an identified forced-alignment model candidate in the Qwen3 ASR line, then verify the model card before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
