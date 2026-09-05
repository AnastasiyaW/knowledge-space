---
title: ComfyUI — ComfyUI Development
category: projects
tags: [comfy-cloud-pricing, comfyui, comfyui-development, comfyui_core_updates, comfyui_desktop, ecosystem_grants, product_updates, project]
aliases: ["Comfy Cloud", "ComfyUI"]
---

# ComfyUI — ComfyUI Development

**Development line:** `project:comfyui` · thread `comfyui-development`  
**Events:** 19 dated, 2023-11-24 → 2026-03-26 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ComfyUI — открытый узловой интерфейс и движок генерации для художников, разработчиков и команд, которым нужен редактируемый граф вместо фиксированного интерфейса с одним полем запроса. Возможности: — собирает рабочие процессы для изображений, видео, 3D и аудио; — запускается локально через Desktop, portable- или manual-установку либо как управляемый Comfy Cloud; — расширяется шаблонами, subgraph-блоками и версионируемыми custom nodes; — подключает закрытые модели через платные Partner Nodes; — превращает граф в упрощённое приложение через App Mode и допускает управление агентами через Comfy MCP. Мера: последний проверенный стабильный релиз — v0.34.0 от 2026-08-26; Cloud использует RTX 6000 Pro с 96 ГБ VRAM, а текущий Standard-план указывает 4200 кредитов и предел одного запуска 30 минут. Вердикт: локальный ComfyUI подходит для контроля, офлайн-работы и произвольных расширений; Cloud снимает настройку GPU и добавляет командный контур, но вводит лимиты времени, кредитов и доступных расширений.

## Development line

- **2023-11-24 — ComfyUI Publishes Stable Video Diffusion Workflows.** On 2023-11-24, ComfyUI published first-party Stable Video Diffusion example workflows for image-to-video generation. The examples documented model placement and controls for frame count, motion, frame rate, and reviewer-free guidance.
- **2024-06-12 — ComfyUI Core Adds SD3 Support.** On 2024-06-12, ComfyUI added SD3 support to its core engine in commit 8c4a9be. The change established native engine support for building SD3 workflows.
- **2024-09-16 — ComfyUI Adds SD3 and Flux Inpainting ControlNet Support.** On 2024-09-16, ComfyUI added support for AliMama ControlNet models for SD3 and Flux inpainting in commit f48e390. The change expanded structurally conditioned inpainting workflows for those model families.
- **2024-10-21 — ComfyUI V1 Introduces a New Interface and Desktop Beta.** On 2024-10-21, ComfyUI introduced its V1 interface and opened closed-beta Desktop packaging. The release added a bundled Manager, tabs, settings, model and workflow browsers, and model-download assistance while placing the original interface on a maintenance path.
- **2024-12-06 — ComfyUI Responds to the Ultralytics Package Compromise.** On 2024-12-06, ComfyUI documented its response to malicious Ultralytics 8.3.41 and 8.3.42 packages encountered through some custom-node dependency chains. The project distinguished the compromised dependency from ComfyUI core and added Manager warnings and version pinning.
- **2025-07-28 — ComfyUI Adds Day-Zero Wan 2.2 Support.** On 2025-07-28, ComfyUI added native day-zero support for Wan 2.2. The release provided official mixture-of-experts text-to-video and image-to-video workflows and packaged model files.
- **2025-08-13 — ComfyUI Expands Wan 2.2 Fun InP and Control Workflows.** On 2025-08-13, ComfyUI added Wan 2.2 Fun InP, Control, and LightX2V support. The workflows enabled first-and-last-frame generation, structural controls, and faster four-step generation with LoRA acceleration.
- **2025-08-26 — ComfyUI Adds Native Qwen-Image DiffSynth ControlNet Support.** On 2025-08-26, ComfyUI added native Qwen-Image DiffSynth ControlNet support. The update expanded controllable image generation and documented optional cache-based workflow acceleration.
- **2025-08-27 — ComfyUI Adds Hosted Gemini and Local Qwen-Image Control Paths.** On 2025-08-27, ComfyUI added two distinct execution paths: Google Gemini 2.5 Flash Image through credit-billed Partner Nodes and local InstantX Qwen-Image Unified ControlNet workflows. The local workflows supported canny, depth, pose, and soft-edge controls.
- **2025-08-28 — Second Comfy Challenge Expands the Community Workflow Program.** On 2025-08-28, ComfyUI expanded its community showcase and workflow-learning program through the second Comfy Challenge. This was an ecosystem and education milestone rather than a core runtime release.
- **2025-09-24 — ComfyUI Adds Wan 2.2 Animate and Qwen Image Editing Workflows.** On 2025-09-24, ComfyUI added native workflows for Wan 2.2 Animate and Qwen-Image-Edit-2509. They supported performer-driven character animation and replacement as well as multi-image editing.
- **2025-10-07 — ComfyUI 0.3.63 Makes Subgraphs Publishable.** On 2025-10-07, ComfyUI 0.3.63 made subgraphs publishable as reusable blueprint nodes. The release also redesigned selection tooling for graph editing.
- **2025-10-09 — ComfyUI Adds Sora 2 Partner Nodes.** On 2025-10-09, ComfyUI made Sora 2 and Sora 2 Pro available through paid Partner Nodes. The integration supported text-to-video and image-to-video generation with sound.
- **2025-10-22 — ComfyUI 0.3.66 Improves Subgraph and Template Tooling.** On 2025-10-22, ComfyUI 0.3.66 added a parameter panel for subgraphs. The release also redesigned workflow-template discovery and filtering.
- **2025-11-26 — Comfy Cloud Expands Infrastructure and Feature Allowances.** On 2025-11-26, Comfy Cloud announced a move to RTX 6000 Pro infrastructure and support for using personal LoRAs. It also described longer Pro runs and unified credits across Cloud GPU execution and Partner Nodes.
- **2025-12-30 — ComfyUI Begins Moving Its Canonical Repository to Comfy-Org.** On 2025-12-30, ComfyUI began moving its canonical GitHub repository from comfyanonymous/ComfyUI to Comfy-Org/ComfyUI. GitHub redirects were retained, and users were advised to update their Git remotes.
- **2026-01-27 — ComfyUI Adds Day-Zero Z-Image Support.** On 2026-01-27, ComfyUI added day-zero support for the non-distilled Z-Image model. The release included an official workflow and model-specific sampling guidance.
- **2026-02-05 — ComfyUI Ecosystem Announces an Open-Model Grant Initiative.** On 2026-02-05, the ComfyUI ecosystem announced an open-model grant initiative described as a $1 million program alongside the Anima launch. The initiative was presented as funding for open model development.
- **2026-03-26 — ComfyUI Introduces Stable Dynamic VRAM Management.** On 2026-03-26, ComfyUI documented Dynamic VRAM as a stable mechanism for reducing memory pressure and out-of-memory failures on supported Nvidia systems. Its guidance emphasized measuring total workflow time instead of isolated iteration speed.

## What changed

ComfyUI — с 2023 по 2026 год прошёл путь от локального графа с примерами видео до семейства из core-движка, Desktop, Cloud, App Mode, Partner Nodes и MCP. 2023-11-24 — опубликованы практические video-workflow для Stable Video Diffusion: загрузка графа из WebP, выбор числа кадров, FPS и силы движения. 2024-06-12 — core получил поддержку Stable Diffusion 3. 2024-09-16 — добавлены AliMama SD3 и FLUX inpainting ControlNet. 2024-10-21 — V1 принёс новый frontend, Desktop в закрытой бете, встроенный Manager/Registry, вкладки, браузеры моделей и workflow; старый интерфейс перевели в режим поддержки. 2024-12-06 — после вредоносных Ultralytics 8.3.41–8.3.42 Manager начал предупреждать о зависимости и фиксировать безопасную 8.3.40; инцидент показал, что custom nodes расширяют границу доверия до сторонних пакетов. 2025-07-28 — появилась нативная поддержка Wan 2.2, включая TI2V-5B и MoE-варианты I2V/T2V-A14B. 2025-08-13 — добавлены Wan 2.2 Fun InP, Fun Control и четырёхшаговая LightX2V LoRA; ещё одно объявление этой даты осталось непроверенным из-за недоступной первичной страницы. 2025-08-26 — Qwen Image получил DiffSynth ControlNet, Union LoRA, EasyCache и оптимизации для Blackwell. 2025-08-27 — Nano Banana появился как кредитный Partner Node, а Qwen-Image InstantX — как единый ControlNet для Canny, Soft Edge, Depth и Pose. 2025-08-28 — Challenge #2 Falling расширил конкурсную часть сообщества, но не изменил возможности продукта. 2025-09-24 — нативно добавлены Wan 2.2 Animate и Qwen-Image-Edit-2509. 2025-10-07 — v0.3.63 позволил сохранять и публиковать subgraph-блоки в библиотеку. 2025-10-09 — Sora 2 и Sora 2 Pro появились как Partner Nodes для text-to-video и image-to-video со звуком. 2025-10-22 — v0.3.66 добавил редактирование параметров subgraph без входа внутрь и фильтры библиотеки шаблонов. 2025-10-24 — изменение не атрибутировано: доступной первичной ссылки нет. 2025-11-04, найдено 2026-09-04 — Comfy Cloud вышел из waitlist в публичную бету. 2025-11-26 — Cloud перешёл с A100 на RTX 6000 Pro Blackwell с 96 ГБ VRAM, объединил оплату GPU и Partner Nodes в Comfy Credits и добавил импорт LoRA. 2025-12-26 — изменение не установлено: связанная первичная страница недоступна. 2025-12-30 — перенос репозитория из comfyanonymous в Comfy-Org назначили на 2026-01-06; старые ссылки сохранили через перенаправление. 2026-01-27 — добавлена нативная недистиллированная Z-Image с рекомендуемыми 30–50 шагами и CFG 3–5. 2026-02-05 — условия AI Grant не удалось подтвердить по читаемой первичной странице. 2026-02-21 — изменение не атрибутировано: доступной первичной ссылки нет. 2026-03-02, найдено 2026-09-04 — Cloud объявил бесплатный уровень с 400 кредитами в месяц; текущая pricing-страница уже показывает другую модель. 2026-03-04, найдено 2026-09-04 — Comfy Cloud вышел из беты. 2026-03-10, найдено 2026-09-04 — App Mode, App Builder и ComfyHub позволили скрывать граф за формой ввода и делиться приложением по ссылке. 2026-03-26 — Dynamic VRAM стал стабильным режимом для NVIDIA на Windows и Linux: веса выгружаются экономнее, снижаются расход RAM и риск OOM. 2026-05-12 — изменение цены не установлено: связанная первичная страница недоступна. 2026-07-23, найдено 2026-09-04 — Comfy for Teams добавил общий workspace, пул кредитов, единый счёт и администрирование участников. 2026-08-18, найдено 2026-09-04 — открыт Comfy MCP для Local и Cloud: агенты могут читать окружение, собирать и запускать workflow, устанавливать модели и nodes. 2026-08-26, найдено 2026-09-04 — v0.34.0 добавил новые форматы сохранения видео и HDR, расширил модельную поддержку и включил Dynamic VRAM по умолчанию для ROCm 7.14+. 2026-09-04, найдено сегодня — актуальная pricing-страница предлагает пять бесплатных запусков без карты; Standard начинается с $20 в месяц, включает 4200 кредитов и ограничивает запуск 30 минутами. Мера: последняя подтверждённая стабильная точка — v0.34.0; шесть дат остаются без проверяемого содержания. Вердикт: главная линия развития — унификация локального графа и облачного сервиса при одновременном росте двух операционных рисков: исполняемого кода custom nodes и расходуемых Cloud-кредитов.

## How to use this

As of 2026-09-03, practitioners should build new workflows against Comfy-Org/ComfyUI and official templates, explicitly choose between local or Desktop execution, Comfy Cloud, and paid Partner Nodes, and treat custom-node dependencies as supply-chain inputs requiring review and version pinning. They should consult live Cloud pricing and current model or hardware requirements instead of relying on historical release announcements.

1. 1. Выберите среду: Local для собственного GPU, офлайн-работы и полной свободы расширений; Cloud — для управляемого GPU и готового набора моделей.
  — <https://docs.comfy.org/get_started/cloud>
2. 2. Для Local выберите поддерживаемую установку: Desktop на Windows или macOS ARM, portable на Windows либо manual install для остальных поддерживаемых систем и GPU.
  — <https://docs.comfy.org/installation/system_requirements>
3. 3. Откройте встроенный официальный шаблон нужной задачи; ComfyUI проверит отсутствующие модели и зависимости.
  — <https://docs.comfy.org/interface/features/template>
4. 4. Укажите checkpoint и входные данные, измените prompt и параметры, затем запустите очередь через Run или Ctrl+Enter и сохраните результат.
  — <https://docs.comfy.org/get_started/first_generation>
5. 5. Если граф требует сторонние nodes, установите их через Manager только из доверенного источника, перезапустите ComfyUI и проверьте журнал загрузки.
  — <https://docs.comfy.org/installation/install_custom_node>
6. 6. Для закрытых API-моделей добавьте Partner Node, войдите в аккаунт и заранее пополните общий баланс Comfy Credits.
  — <https://docs.comfy.org/tutorials/partner-nodes/overview>
7. 7. Для передачи workflow человеку без опыта работы с графами задайте входы и выходы в App Builder, сохраните workflow и откройте App Mode.
  — <https://docs.comfy.org/interface/app-mode>
8. 8. Обновляйтесь по stable-каналу для обычной работы; переходите на nightly только когда конкретная новая модель или Partner Node ещё не вошли в stable.
  — <https://docs.comfy.org/installation/update_comfyui>

## Best practices

- Фиксируйте рабочую версию ComfyUI и используйте stable-обновления; nightly оправдан только измеримой необходимостью новой функции.
  — <https://docs.comfy.org/installation/update_comfyui>
- Начинайте с официального native-шаблона и сохраняйте workflow JSON или PNG с метаданными: это уменьшает ошибки путей, моделей и структуры графа.
  — <https://docs.comfy.org/interface/features/template>
- Считайте custom node исполняемым сторонним кодом: проверяйте автора, назначение и зависимости, избегайте малоизвестных ZIP-сборок.
  — <https://docs.comfy.org/installation/install_custom_node>
- Закрепляйте semantic version registry-node: версия записывается в workflow, а опубликованный релиз Registry остаётся неизменным.
  — <https://docs.comfy.org/registry/overview>
- Перед массовым Update All в legacy Manager сохраняйте snapshot и после восстановления обязательно перезапускайте и проверяйте граф.
  — <https://docs.comfy.org/manager/legacy-ui>
- В Desktop не изменяйте встроенный каталог resource/ComfyUI: обновление может его пересоздать; модели и пользовательские данные держите во внешних каталогах.
  — <https://docs.comfy.org/installation/desktop/windows>
- Перед длинной Cloud-очередью проверяйте лимит запуска и баланс: включённые ежемесячные кредиты сбрасываются, а Partner Nodes расходуют тот же пул.
  — <https://comfy.org/pricing>
- Не принимайте высокое заполнение VRAM при Dynamic VRAM за утечку само по себе; сравнивайте OOM, расход системной RAM и время загрузки до отключения режима.
  — <https://blog.comfy.org/p/dynamic-vram-in-comfyui-saving-local>
- Для получателя, которому нужны только параметры и результат, публикуйте App Mode, а не полный редактируемый граф.
  — <https://docs.comfy.org/interface/app-mode>

## Superseded by this

- 2024-10-21 — закрытая бета Desktop и waitlist Cloud устарели: Cloud перешёл в публичную бету 2025-11-04 и вышел из беты 2026-03-04.
- 2024-10-21 — заявление о готовом Desktop для Windows, macOS и Linux больше не соответствует текущей матрице: готовые Desktop-сборки документированы для Windows и macOS ARM, а Linux требует manual/self-hosted установки.
- 2025-11-04 — A100 как базовая Cloud-машина заменён 2025-11-26 на RTX 6000 Pro Blackwell с 96 ГБ VRAM.
- До 2026-01-06 — git remote github.com/comfyanonymous/ComfyUI устарел; канонический репозиторий находится в github.com/Comfy-Org/ComfyUI, хотя перенаправление старых ссылок сохраняется.
- 2026-03-02 — обещание 400 бесплатных кредитов каждый месяц расходится с актуальной на 2026-09-04 pricing-страницей, где указаны пять бесплатных запусков без карты; для покупки и планирования следует использовать текущую pricing-страницу.
- 2026-03-25 — описание Dynamic VRAM как NVIDIA-only неполно после v0.34.0: режим включён по умолчанию и для ROCm 7.14+.
- 2025-10-21 — v0.3.66 больше не является актуальной стабильной точкой; на 2026-09-04 последний проверенный релиз — v0.34.0.

## Still unknown

- Название ComfyUI объединяет разные поверхности: open-source core, Desktop, Comfy Cloud, Partner Nodes, App Mode/ComfyHub, MCP и грантовую программу. Это одна экосистема, но не один продукт с общей моделью установки, оплаты и доверия.
- Не удалось проверить содержание страниц https://x.com/ComfyUI/status/1955118670562394213, https://twitter.com/ComfyUI/status/2003928596440928427 и https://x.com/ComfyUI/status/2053913932738507171; им не приписаны продуктовые изменения.
- Для событий 2025-10-24 и 2026-02-21 не было доступной первичной ссылки, поэтому их содержание неизвестно.
- Страница https://comfy.org/ai-grant не дала читаемых актуальных условий; дата запуска, объём финансирования и статус приёма заявок не подтверждены.
- Первичные страницы расходятся по бесплатному Cloud-доступу: публикация и часть документации говорят о 400 кредитах ежемесячно, текущая pricing-страница — о пяти бесплатных запусках. Актуальным ориентиром принята pricing-страница, но поведение нового аккаунта не проверялось.
- Video Examples — изменяемая страница без видимой даты версии; наличие примеров подтверждено, но точный состав страницы на 2023-11-24 восстановить нельзя.
- Установка, Cloud-биллинг, Partner Nodes и MCP не запускались в реальном аккаунте; подтверждены документация и публичные релизы, а не вертикальный runtime-проход.

## Sources

| source | title | read |
|---|---|---|
| https://comfyanonymous.github.io/ComfyUI_examples/video/ | Video Examples | ComfyUI_examples | 2026-09-04 |
| https://github.com/comfyanonymous/ComfyUI/commit/8c4a9befa7261b6fc78407ace90a57d21bfe631e | SD3 Support. · Comfy-Org/ComfyUI@8c4a9be | 2026-09-04 |
| https://github.com/comfyanonymous/ComfyUI/commit/f48e390032f8d27a450a35ef4aa4b775b078cbf9 | Support AliMama SD3 and Flux inpaint controlnets. · Comfy-Org/ComfyUI@f48e390 | 2026-09-04 |
| https://blog.comfy.org/p/comfyui-v1-release | ComfyUI V1 Release | 2026-09-04 |
| https://blog.comfy.org/p/comfyui-statement-on-the-ultralytics-crypto-miner-situation | ComfyUI Statement on the Ultralytics Crypto Miner Situation | 2026-09-04 |
| https://blog.comfy.org/p/wan22-day-0-support-in-comfyui | Wan2.2 Day 0 Support in ComfyUI | 2026-09-04 |
| https://blog.comfy.org/p/comfyui-wan22-fun-inp-support | ComfyUI Wan2.2 Fun Native Support and LightX2V 4-Step LoRA Integration | 2026-09-04 |
| https://blog.comfy.org/p/comfyui-now-supports-qwen-image-controlnet | ComfyUI Now Supports Qwen Image ControlNet | 2026-09-04 |
| https://blog.comfy.org/p/nano-banana-via-comfyui-api-nodes | Nano Banana via ComfyUI API Nodes | 2026-09-04 |
| https://blog.comfy.org/p/day-1-support-of-qwen-image-instantx | Day 1 Support of Qwen-Image InstantX ControlNet | 2026-09-04 |
| https://blog.comfy.org/p/the-comfy-challenge-2-falling | The Comfy Challenge #2: Falling | 2026-09-04 |
| https://blog.comfy.org/p/wan22-animate-and-qwen-image-edit-2509 | Wan2.2 Animate and Qwen-Image-Edit-2509 | 2026-09-04 |
| https://blog.comfy.org/p/comfyui-0363-subgraph-publishing | ComfyUI 0.3.63: Subgraph Publishing | 2026-09-04 |
| https://blog.comfy.org/p/sora-2-api-nodes-now-in-comfyui | Sora 2 Partner Nodes Now in ComfyUI | 2026-09-04 |
| https://blog.comfy.org/p/comfyui-0366-updates | ComfyUI 0.3.66 Updates | 2026-09-04 |
| https://blog.comfy.org/p/comfy-cloud-is-now-in-public-beta | Comfy Cloud Is Now in Public Beta | 2026-09-04 |
| https://blog.comfy.org/p/comfy-cloud-new-features-and-pricing | Comfy Cloud: New Features and Pricing | 2026-09-04 |
| https://blog.comfy.org/p/comfyui-repo-will-moved-to-comfy | ComfyUI Repo Will Be Moved to Comfy Organization | 2026-09-04 |
| https://blog.comfy.org/p/z-image-day-0-support-in-comfyui | Z-Image Day 0 Support in ComfyUI | 2026-09-04 |
| https://blog.comfy.org/p/free-tier-arrives-in-comfy-cloud | Free Tier Arrives in Comfy Cloud | 2026-09-04 |
| https://blog.comfy.org/p/comfy-cloud-is-out-of-beta-and-its | Comfy Cloud Is Out of Beta | 2026-09-04 |
| https://blog.comfy.org/p/from-workflow-to-app-introducing | From Workflow to App: Introducing App Mode, App Builder, and ComfyHub | 2026-09-04 |
| https://blog.comfy.org/p/dynamic-vram-in-comfyui-saving-local | Dynamic VRAM in ComfyUI: Saving Local System RAM | 2026-09-04 |
| https://blog.comfy.org/p/comfy-for-teams-is-here | Comfy for Teams Is Here | 2026-09-04 |
| https://blog.comfy.org/p/open-sourcing-comfy-mcp-on-local | Open-Sourcing Comfy MCP on Local and Cloud | 2026-09-04 |
| https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.34.0 | Release v0.34.0 · Comfy-Org/ComfyUI | 2026-09-04 |
| https://github.com/Comfy-Org/ComfyUI | Comfy-Org/ComfyUI · GitHub | 2026-09-04 |
| https://docs.comfy.org/ | ComfyUI Official Documentation | 2026-09-04 |
| https://docs.comfy.org/get_started/cloud | Comfy Cloud — Official ComfyUI Cloud Platform | 2026-09-04 |
| https://docs.comfy.org/installation/system_requirements | ComfyUI System Requirements | 2026-09-04 |
| https://docs.comfy.org/interface/features/template | Templates — ComfyUI Built-in Workflow Templates | 2026-09-04 |
| https://docs.comfy.org/get_started/first_generation | Getting Started with AI Image Generation | 2026-09-04 |
| https://docs.comfy.org/installation/install_custom_node | How to Install Custom Nodes in ComfyUI | 2026-09-04 |
| https://docs.comfy.org/tutorials/partner-nodes/overview | Partner Nodes Overview | 2026-09-04 |
| https://docs.comfy.org/interface/app-mode | ComfyUI App Mode Guide | 2026-09-04 |
| https://docs.comfy.org/installation/update_comfyui | How to Update ComfyUI | 2026-09-04 |
| https://docs.comfy.org/registry/overview | ComfyUI Registry Overview | 2026-09-04 |
| https://docs.comfy.org/manager/legacy-ui | Managing Custom Nodes with the Legacy UI | 2026-09-04 |
| https://docs.comfy.org/installation/desktop/windows | Windows Desktop — Local Self-Hosted | 2026-09-04 |
| https://comfy.org/pricing | Pricing — Comfy Cloud | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui`, thread `comfyui-development`, 19 dated events 2023-11-24 → 2026-03-26.
- **Practical note:** As of 2026-09-03, practitioners should build new workflows against Comfy-Org/ComfyUI and official templates, explicitly choose between local or Desktop execution, Comfy Cloud, and paid Partner Nodes, and treat custom-node dependencies as supply-chain inputs requiring review and version pinning. They should consult live Cloud pricing and current model or hardware requirements instead of relying on historical release announcements.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
