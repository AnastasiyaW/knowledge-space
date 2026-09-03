---
title: Amazon — Amazon generative AI platform and models
category: organizations
tags: [amazon, amazon-generative-ai-platform-and-models, amazon-nova, amazon_bedrock_codewhisperer, organization]
aliases: ["Amazon"]
---

# Amazon — Amazon generative AI platform and models

**Development line:** `organization:amazon` · thread `amazon-generative-ai-platform-and-models`  
**Events:** 2 dated, 2023-04-13 → 2024-12-04 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Amazon — в этой линии AWS два разных рабочих пути: Amazon Bedrock — управляемая платформа для GenAI-приложений и агентов; Amazon Nova — собственное семейство моделей в Bedrock; Amazon Q Developer — помощник для кода, в который вошёл CodeWhisperer. Возможности: - открыть модели AWS и сторонних поставщиков через Model Catalog и API Bedrock; - прототипировать Nova 2 Lite и Sonic в playground или вызывать Nova 2 через Converse и InvokeModel; - использовать Q Developer в IDE для предложений кода и чата, пока поддержка плагинов действует. Ограничение: запрос Nova может выполняться до 60 минут, а поддержка IDE-плагинов Q Developer заканчивается 2027-04-30. Вывод: для нового GenAI-сервиса выбирайте Bedrock и нужную модель Nova или стороннего поставщика; CodeWhisperer/Q Developer не следует считать долгосрочным основанием новой IDE-интеграции.

## Development line

- **2023-04-13 — Amazon introduces Bedrock and expands its generative AI offering.** On 2023-04-13, Amazon introduced Amazon Bedrock as part of its entry into the generative AI platform market. The linked materials also place Amazon CodeWhisperer within this developer-facing AI expansion, making the post a material step in Amazon's generative AI development.
- **2024-12-04 — Amazon announces Amazon Nova models for Bedrock.** On 2024-12-04, Amazon announced the Amazon Nova family of AI models for use through Amazon Bedrock. This was a material development because it extended Amazon's generative AI line from a platform for model access toward named first-party model offerings.

## What changed

2023-04-13 — Amazon Bedrock вышел в ограниченном preview как API к базовым моделям AWS и сторонних поставщиков. В тот же день CodeWhisperer стал общедоступным помощником для кода в IDE с individual и professional уровнями. Это с начала были разные продукты: платформа инференса и кодовый помощник. 2023-09-28 (найдено сегодня) — Bedrock стал общедоступным: AWS добавила управляемый выбор моделей, provisioned throughput и интеграции с CloudWatch и CloudTrail; состояние preview закончилось. 2024-04-30 (найдено сегодня) — Amazon CodeWhisperer вошёл в Amazon Q Developer; самостоятельное наименование CodeWhisperer перестало быть текущим для IDE-продукта. 2024-12-04 — Amazon представила Nova в Bedrock: исходные Micro (только текст), Lite и Pro (мультимодальные), а также Canvas для изображений и Reel для видео; Premier был заявлен как следующая модель. 2026-08-17 (найдено сегодня) — AWS задокументировала, что поддержка IDE-плагинов Amazon Q Developer закончится 2027-04-30, и указывает Kiro как путь к сходным возможностям. 2026-09-03 (найдено сегодня) — текущие каталог Bedrock и документация Nova показывают более новую линию Nova 2, включая Lite и Sonic; для большинства сценариев AWS рекомендует Converse API. Не считайте набор моделей из анонса 2024 года полным текущим списком.

## How to use this

Since 2023-04-13, practitioners evaluating Amazon's AI stack should treat Bedrock as a core platform option; since 2024-12-04, they should also assess Amazon Nova alongside third-party Bedrock models for relevant workloads.

1. Для нового GenAI-приложения откройте Model Catalog Amazon Bedrock, выберите модель и проверьте разрешения AWS Marketplace: при корректных разрешениях модели доступны по умолчанию; затем запускайте playground или вызывайте InvokeModel либо Converse.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html>
2. Для быстрого прототипа Amazon Nova 2 используйте Chat или Text playground с Nova 2 Lite либо Sonic; для приложения перейдите к Bedrock InvokeModel или Converse API.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/getting-started-nova-2.html>
3. В коде создайте клиент bedrock-runtime и вызывайте Converse с modelId и массивом сообщений; добавьте system-инструкцию, параметры инференса и потоковый ответ только когда это нужно интерфейсу.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-converse-api.html>
4. Для регулируемого сценария привяжите конкретный guardrail и его числовую версию к IAM-политике через условие bedrock:GuardrailIdentifier, чтобы запрос без нужной защиты был отклонён.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html>
5. Если команда временно продолжает Amazon Q Developer, установите расширение для IDE и войдите через AWS Builder ID или IAM Identity Center; одновременно заведите отдельный план миграции до 2027-04-30.
  — <https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html>

## Best practices

- По умолчанию выбирайте Converse: он даёт единый интерфейс для разных моделей; Invoke API оставляйте для случаев, когда требуется нативная схема конкретной модели.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html>
- Настройте read timeout клиента под долгие запросы Nova: AWS предупреждает, что отдельный инференс может занимать до 60 минут, и показывает конфигурацию на 3600 секунд.
  — <https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html>
- Пишите простую однозначную инструкцию после контекста, отделяйте входные данные разделителями, явно задавайте формат результата и параметры инференса; изменения промпта проверяйте на отложенном наборе, а не только на примерах разработки.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html>
- Не полагайтесь на добровольное подключение защиты вызывающим кодом: IAM должен требовать конкретные идентификатор и версию guardrail для каждого inference-запроса.
  — <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html>
- Перед принятием подсказки CodeWhisperer/Q Developer проверяйте код, URL исходного репозитория и лицензию, если система отметила сходство с публичным кодом; это не заменяется автоматическим принятием рекомендации.
  — <https://aws.amazon.com/ru/codewhisperer/>

## Superseded by this

- 2023-04-13 — статус Amazon Bedrock как limited preview устарел: сервис стал общедоступным 2023-09-28.
- 2023-04-13 — самостоятельное наименование Amazon CodeWhisperer как текущего IDE-продукта устарело: с 2024-04-30 он входит в Amazon Q Developer.
- 2024-12-04 — считать исходные Nova Micro, Lite, Pro, Canvas и Reel полным актуальным выбором моделей устарело: текущий каталог включает линию Nova 2, в том числе Lite и Sonic.
- До 2026-08-17 — совет строить новую долгоживущую IDE-интеграцию на Amazon Q Developer без миграционного срока устарел: объявлен конец поддержки именно IDE-плагинов 2027-04-30.

## Still unknown

- Amazon Nova/Bedrock и CodeWhisperer/Amazon Q Developer — две разные продуктовые линии AWS, а не один продукт и не последовательные версии; эта запись объединяет их только на уровне компании.
- Уведомление о 2027-04-30 относится именно к IDE-плагинам Amazon Q Developer; из проверенных источников нельзя вывести статус Q Developer CLI, консоли и остальных компонентов после этой даты.
- Доступность Nova, цены, квоты, Marketplace-условия и нужные разрешения зависят от региона и аккаунта AWS; в этой проверке не было доступа к конкретному аккаунту или региону.
- Анонс 2024 года планировал Nova Premier на первый квартал 2025 года; его текущая региональная доступность и цена отдельно не проверялись.
- Для Bedrock 2023-04-13 здесь использован датированный вторичный источник; отдельный первичный AWS-анонс limited preview не был получен.

## Sources

| source | title | read |
|---|---|---|
| https://techcrunch.com/2023/04/13/with-bedrock-amazon-enters-the-generative-ai-race/ | With Bedrock, Amazon enters the generative AI race | 2026-09-03 |
| https://aws.amazon.com/ru/codewhisperer/ | Генератор кода на основе искусственного интеллекта – Amazon CodeWhisperer – AWS | 2026-09-03 |
| https://aws.amazon.com/about-aws/whats-new/2023/04/amazon-codewhisperer-generally-available/ | Amazon CodeWhisperer is now generally available | 2026-09-03 |
| https://aws.amazon.com/about-aws/whats-new/2023/09/amazon-bedrock-generally-available/ | Amazon Bedrock is now generally available | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/doc-history.html | Document history for Amazon Q Developer User Guide | 2026-09-03 |
| https://www.aboutamazon.com/news/aws/amazon-nova-artificial-intelligence-bedrock-aws | Amazon Nova: Meet our new foundation models in Amazon Bedrock | 2026-09-03 |
| https://aws.amazon.com/bedrock | Amazon Bedrock – Build genAI applications and agents at production scale – AWS | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html | Models at a glance - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html | Request access to models - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/getting-started-nova-2.html | Getting started with Amazon Nova 2 - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-converse-api.html | Using the Converse API - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/nova/latest/nova2-userguide/core-inference.html | Core inference - Amazon Nova | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html | Design a prompt - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html | Enforce the use of specific guardrails in model inference requests - Amazon Bedrock | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html | Installing the Amazon Q Developer extension or plugin in your IDE - Amazon Q Developer | 2026-09-03 |
| https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-developer-ide-end-of-support.html | Amazon Q Developer IDE plugins end of support - Amazon Q Developer | 2026-09-03 |

## Agent brief {#agent-brief}

- **Subject:** `organization:amazon`, thread `amazon-generative-ai-platform-and-models`, 2 dated events 2023-04-13 → 2024-12-04.
- **Practical note:** Since 2023-04-13, practitioners evaluating Amazon's AI stack should treat Bedrock as a core platform option; since 2024-12-04, they should also assess Amazon Nova alongside third-party Bedrock models for relevant workloads.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
