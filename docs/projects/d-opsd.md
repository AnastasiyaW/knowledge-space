---
title: d-OPSD — Research paper and code release
category: projects
date: 2026-06-21
tags: [d-opsd, project, research-paper-and-code-release]
aliases: ["d-OPSD"]
---

# d-OPSD — Research paper and code release

**Development line:** `project:d-opsd` · thread `research-paper-and-code-release`  
**Last event:** 2026-06-21 · 1 dated since 2026-06-21 · **Researched:** 2026-09-05 · confidence: medium

## What it is

d-OPSD — исследовательский фреймворк post-training для diffusion language models. — строит self-teacher из собственного ответа как suffix conditioning; — переносит supervision с токенов на шаги денойзинга; — сравнивался с RLVR и SFT на четырёх reasoning-бенчмарках. Авторы сообщают около 10% числа оптимизационных шагов RLVR; публичный код есть, но готовой модели или независимой репликации результатов источник не показывает.

## Development line

- **2026-06-21 — d-OPSD research paper and code repository linked.** Self-generated answer используется как суффиксный контекст teacher, а loss считается по шагам денойзинга.

## What changed

2026-06-21 — d-OPSD был представлен как OPSD для dLLM: self-generated answer используется как суффиксный контекст teacher, а loss считается по шагам денойзинга.

## How to use this

From 2026-06-21, practitioners should treat d-OPSD as a project with a linked research paper and public code repository, and consult both before evaluating or attempting to use it.

1. Создать Conda-окружение из `env.yml` и активировать `dOPSD`.
  — <https://github.com/xingzhejun/d-opsd-code>
2. Заменить или пропатчить `trl/trainer/grpo_trainer.py` и `utils.py` версиями из репозитория; это требуется для допустимого числа generations и выравнивания teacher prompt/output.
  — <https://github.com/xingzhejun/d-opsd-code>
3. Запустить скрипт нужного набора: GSM, math, Countdown или Sudoku из `d-opsd/run`.
  — <https://github.com/xingzhejun/d-opsd-code>
4. Указать свой checkpoint в evaluation-скрипте, сохранить generations и посчитать accuracy через `eval/parse_and_get_acc.py`.
  — <https://github.com/xingzhejun/d-opsd-code>

## Best practices

- Зафиксировать версию TRL и применить обе авторские замены trainer-файлов, а не только `grpo_trainer.py`.
  — <https://github.com/xingzhejun/d-opsd-code>
- Для A100 и H100 установить `BATCH_DIVIDE=8`, чтобы избежать OOM; значение `4` в скриптах предназначено для B200.
  — <https://github.com/xingzhejun/d-opsd-code>
- Перед сравнением с результатами статьи сверить Python 3.10, CUDA 12.9 и конфигурацию из `used-env.txt`; авторы указывают A100/H100/B200.
  — <https://github.com/xingzhejun/d-opsd-code>

## Superseded by this

- 2026-08-17 — ранняя инструкция окружения, где заменяется только `grpo_trainer.py`, устарела: README требует также заменить `utils.py` из-за исправлений TRL и формата warning.

## Still unknown

- d-OPSD легко спутать с одноимённым D-OPSD для step-distilled image diffusion models (arXiv:2605.05204); этот материал относится к dLLM-работе Luo et al., arXiv:2606.18195.
- Авторы заявляют преимущество на четырёх бенчмарках и около 10% числа шагов RLVR, но в проверенных источниках нет независимой репликации, релиза чекпойнтов или production-интеграции.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/papers/2606.18195 | Learning from the Self-future: On-policy Self-distillation for dLLMs | 2026-09-05 |
| https://arxiv.org/abs/2606.18195 | Learning from the Self-future: On-policy Self-distillation for dLLMs | 2026-09-05 |
| https://github.com/xingzhejun/d-opsd-code | xingzhejun/d-opsd-code | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:d-opsd`, thread `research-paper-and-code-release`, 1 dated events 2026-06-21 → 2026-06-21.
- **Practical note:** From 2026-06-21, practitioners should treat d-OPSD as a project with a linked research paper and public code repository, and consult both before evaluating or attempting to use it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
