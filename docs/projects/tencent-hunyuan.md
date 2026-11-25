---
title: Tencent Hunyuan — Hunyuan model releases
category: projects
date: 2025-07-04
tags: [hunyuan, hunyuan-model-releases, project, tencent-hunyuan, tencent_hunyuan]
aliases: ["Hunyuan-A13B", "Tencent Hunyuan"]
---

# Tencent Hunyuan — Hunyuan model releases

**Development line:** `project:tencent-hunyuan` · thread `hunyuan-model-releases`  
**Last event:** 2025-07-04 · 2 dated since 2024-07-02 · **Researched:** 2026-09-04 · confidence: high

## What it is

Tencent Hunyuan — не одна последовательная модель, а бренд нескольких несовместимых семейств: HunyuanDiT для генерации изображений и Hunyuan-A13B для текста, reasoning и tool calling. Hunyuan-A13B: 80B параметров, 13B активных, контекст 256K. Практический вывод: для нового LLM-проекта берут A13B и его официальный serving-путь; DiT выбирают только для поддержки существующего T2I-пайплайна.

## Development line

- **2024-07-02 — Tencent Hunyuan resources around HunyuanDiT v1.2 were recorded.** On 2024-07-02, the record linked the HunyuanDiT-v1.2 model page, the Hunyuan-Captioner Space, and Tencent-Hunyuan’s Hugging Face profile. From the links alone, this establishes a dated public-resource record around HunyuanDiT v1.2 and captioning tooling, but not whether those assets were released or updated that day.
- **2025-07-04 — Tencent Hunyuan A13B Instruct resources were recorded.** 80B общих и 13B активных параметров, режимы thinking/no-thinking, 256K-контекст и официальные пути Transformers, vLLM, SGLang и Docker.

## What changed

2024-07-02 — HunyuanDiT v1.2 был доступен как пакет весов и кода для двуязычной text-to-image генерации; это не LLM. 2024-07-08 — вышел HYDiT/HunyuanDiT v1.2; официальный репозиторий отделяет это обновление от материалов, опубликованных 2 июля. 2024-07-15 — для HunyuanDiT 1.1/1.2 добавлены стандартизированные ComfyUI workflows и совместимость с LoRA. 2025-06-27 — Tencent открыла Hunyuan-A13B-Pretrain, Instruct, Instruct-FP8 и Instruct-GPTQ-Int4; это отдельная MoE-LLM-линейка, а не следующая версия DiT. 2025-07-04 — актуальность шага подтверждается релизом A13B: 80B общих и 13B активных параметров, режимы thinking/no-thinking, 256K-контекст и официальные пути Transformers, vLLM, SGLang и Docker.

## How to use this

As of 2025-07-04, practitioners should treat Tencent Hunyuan’s dated public references as separate checkpoints: inspect the HunyuanDiT v1.2/captioning resources for the 2024 image-model line and the A13B Instruct model plus code repository for the 2025 language-model line, rather than assuming they are one interchangeable implementation.

1. Выберите `tencent/Hunyuan-A13B-Instruct` для чат-, reasoning- или tool-calling сервиса; загрузите его через Transformers с `trust_remote_code=True` и штатным chat template.
  — <https://huggingface.co/tencent/Hunyuan-A13B-Instruct>
2. Для OpenAI-совместимого локального API поднимите A13B через `vllm serve "tencent/Hunyuan-A13B-Instruct"`.
  — <https://huggingface.co/tencent/Hunyuan-A13B-Instruct>
3. Отключайте reasoning через `enable_thinking=False` либо префикс `/no_think`, когда важнее задержка, чем развёрнутое рассуждение.
  — <https://github.com/Tencent-Hunyuan/Hunyuan-A13B>
4. Для существующего image-пайплайна HunyuanDiT используйте Diffusers-пайплайн `Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers`; для более быстрого вывода доступна distilled-вариация.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>

## Best practices

- Не смешивайте веса, API и ожидания HunyuanDiT с A13B: это T2I diffusion transformer и MoE LLM соответственно.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>
- Для HunyuanDiT ControlNet берите distilled base weights: именно на них обучены опубликованные ControlNet-веса.
  — <https://github.com/Tencent-Hunyuan/HunyuanDiT>
- Для A13B при локальном serving используйте официальный контейнер или документированный backend и проверяйте поведение thinking-mode на своих задачах до включения в агентный маршрут.
  — <https://github.com/Tencent-Hunyuan/Hunyuan-A13B>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Две датированные точки относятся к разным модальностям: HunyuanDiT — генерация изображений, Hunyuan-A13B — языковая MoE-модель. Доказательств, что A13B заменяет DiT, нет.
- Для события 2024-07-02 не найден независимый первичный материал, который датирует сам релиз v1.2 именно 2 июля; официальный журнал указывает выпуск v1.2 на 2024-07-08.
- event_findings: 2025-07-04 — официальный репозиторий датирует открытие четырёх A13B-вариантов 2025-06-27; источник: https://github.com/Tencent-Hunyuan/Hunyuan-A13B. Новые отдельные события: 2024-07-08 — выпуск HYDiT v1.2; 2024-07-15 — ComfyUI workflows и LoRA-совместимость; источник: https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.2.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.2 | Tencent-Hunyuan/HunyuanDiT-v1.2 model card | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/HunyuanDiT | Tencent-Hunyuan/HunyuanDiT | 2026-09-05 |
| https://huggingface.co/tencent/Hunyuan-A13B-Instruct | tencent/Hunyuan-A13B-Instruct model card | 2026-09-05 |
| https://github.com/Tencent-Hunyuan/Hunyuan-A13B | Tencent-Hunyuan/Hunyuan-A13B | 2026-09-05 |
| https://developer.cloud.tencent.com/article/2536652?policyId=1003 | 腾讯混元首款开源混合推理MoE模型发布，性能优异，激活参数仅13B | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:tencent-hunyuan`, thread `hunyuan-model-releases`, 2 dated events 2024-07-02 → 2025-07-04.
- **Practical note:** As of 2025-07-04, practitioners should treat Tencent Hunyuan’s dated public references as separate checkpoints: inspect the HunyuanDiT v1.2/captioning resources for the 2024 image-model line and the A13B Instruct model plus code repository for the 2025 language-model line, rather than assuming they are one interchangeable implementation.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
