---
title: NVIDIA — AI and Accelerated Computing Platform
category: organizations
tags: [ai-and-accelerated-computing-platform, drivers, nvidia, nvidia-ace, nvidia_3d_photo_reconstruction, nvidia_drivers, nvidia_ediffi, nvidia_neuralangelo_launch, nvidia_open_source_drivers, nvidia_rtx_40_super, nvidia_streaming_sortformer, organization, unirelight]
aliases: ["NVIDIA", "Nvidia"]
---

# NVIDIA — AI and Accelerated Computing Platform

**Development line:** `organization:nvidia` · thread `ai-and-accelerated-computing-platform`  
**Events:** 12 dated, 2022-03-28 → 2025-08-22 · **Researched:** 2026-09-04 · confidence: medium

## What it is

NVIDIA — компания и сквозной вычислительный стек для локальной графики, ИИ и дата-центров; AMD — ближайший конкурент по GPU, но CUDA, TensorRT, NGC, ACE и NeMo образуют отдельную программную платформу. Возможности: - GeForce и RTX выполняют графику, генеративные задачи и нейронный рендеринг. - CUDA, TensorRT и NGC дают среды выполнения, оптимизацию моделей и контейнеры. - ACE, Riva, NeMo и Audio2Face обслуживают речь, персонажей и диалоговые приложения. - Instant-NGP, Neuralangelo, UniRelight и eDiff-I показывают исследовательские методы для 3D, света и генерации изображений. Мера/предел: на 2026-09-04 отдельная страница CUDA предлагает Toolkit 13.3 Update 1, тогда как контейнер PyTorch 26.08 включает CUDA 13.4.1; совместимость, лицензия и зрелость определяются для каждого компонента отдельно. Вердикт: NVIDIA следует использовать как набор независимо версионируемых ветвей, а не как один продукт с общей инструкцией обновления.

## Development line

- **2022-03-28 — NVIDIA Demonstrated 3D Reconstruction From Photographs.** On 2022-03-28, the NVIDIA branch documented a video demonstration of 3D reconstruction from photographs. The item marked a distinct image-to-3D research step in the company's development line.
- **2022-11-03 — NVIDIA Presented eDiffi for Generative Image Synthesis.** On 2022-11-03, the NVIDIA branch documented eDiffi as a distinct generative-image research project. The event extended the company's visible AI research line into image synthesis.
- **2023-03-02 — NVIDIA Released a Game Ready Driver for Atomic Heart and The Finals.** On 2023-03-02, NVIDIA published a GeForce Game Ready Driver for Atomic Heart and the closed beta of The Finals, with DLSS 3 named in the release. This advanced NVIDIA's delivery of RTX features through production driver updates.
- **2023-05-04 — NVIDIA Highlighted Graphics Research Advancing Generative AI.** On 2023-05-04, NVIDIA highlighted graphics-research advances directed at generative AI. The publication marked generative AI as a significant direction in the company's graphics research.
- **2023-05-24 — NVIDIA and Microsoft Expanded AI Support for Windows RTX Systems.** On 2023-05-24, NVIDIA and Microsoft announced work to expand AI development and deployment on Windows systems equipped with RTX hardware. The step connected NVIDIA's local AI platform more directly to the Windows developer ecosystem.
- **2023-06-01 — NVIDIA Introduced Neuralangelo for AI-Based 3D Reconstruction.** On 2023-06-01, NVIDIA introduced Neuralangelo, an AI research system for 3D reconstruction. The release established Neuralangelo as a named milestone in NVIDIA's work on recovering 3D scenes from visual inputs.
- **2023-10-19 — NVIDIA Published TensorRT Support for Stable Diffusion WebUI.** On 2023-10-19, NVIDIA published release materials spanning a Game Ready Driver, the Stable-Diffusion-WebUI-TensorRT extension, and its support documentation. This moved TensorRT-based Stable Diffusion acceleration into a concrete GeForce user workflow.
- **2024-01-09 — Coverage Documented NVIDIA's GeForce RTX 4070 SUPER Launch.** On 2024-01-09, linked coverage described NVIDIA's GeForce RTX 4070 SUPER at a listed US price of $599 and with an upgraded AD104 GPU. The product announcement refreshed the RTX 40-series consumer hardware line.
- **2024-03-19 — NVIDIA Showcased ACE AI Characters at GDC and GTC 2024.** On 2024-03-19, NVIDIA showcased ACE demonstrations for AI-driven characters in games and applications at GDC and GTC 2024. The demonstrations marked a visible step toward integrating NVIDIA's generative AI technology into interactive characters.
- **2024-07-18 — NVIDIA Transitioned Toward Fully Open-Source GPU Kernel Modules.** On 2024-07-18, NVIDIA announced that its GPU driver strategy was moving fully toward open-source kernel modules. The transition made the open kernel-module path a central part of NVIDIA's supported Linux driver development.
- **2025-07-07 — NVIDIA Research Presented UniRelight.** On 2025-07-07, NVIDIA's Toronto AI Lab presented UniRelight as a visual relighting research system. The project represented a distinct research release in controllable scene appearance and lighting.
- **2025-08-22 — NVIDIA Released Streaming Sortformer for Real-Time Speaker Diarization.** On 2025-08-22, NVIDIA published Streaming Sortformer for identifying speakers in real time in meetings, calls, and voice applications. NVIDIA also published the diar_streaming_sortformer_4spk-v2 model, adding a deployable streaming diarization capability to its speech AI line.

## What changed

NVIDIA — развитие прошло от отдельных графических исследований к нескольким производственным стекам, которые обновляются независимо. Изменения: - NVIDIA Instant NeRF — 2022-03-28: реконструкция сцены из нескольких фотографий стала занимать секунды обучения и миллисекунды рендеринга; это исследовательский 3D-процесс, а не замена обычному фотограмметрическому конвейеру. - NVIDIA eDiff-I — 2022-11-03: один денойзер был заменен ансамблем экспертов для разных уровней шума, добавлены T5/CLIP-условия, стилевой образец и локальное управление словами; результат остался исследовательской архитектурой. - NVIDIA Game Ready — 2023-03-02: драйвер добавил DLSS 3 для Atomic Heart, профиль THE FINALS и RTX Video Super Resolution для браузерного видео на RTX 30/40; конкретная сборка теперь историческая. - NVIDIA Graphics Research — 2023-05-04: около двадцати работ связали генерацию изображений, inverse rendering, 3D-реконструкцию, нейронную физику и рендеринг; это была карта исследований, не единый продукт. - NVIDIA AI on Windows RTX — 2023-05-24: Windows-ветка получила связку WSL GPU, Olive, ONNX Runtime и DirectML для локального ИИ; привязанный к драйверу 532.03 рецепт больше не является текущим минимумом. - NVIDIA ACE for Games — 2023-05-29: речь, диалог и лицевая анимация были собраны в конвейер Riva, NeMo и Audio2Face для игровых персонажей. - NVIDIA Neuralangelo — 2023-06-01: видео с известными позами камер стало преобразовываться в детализированную нейронную поверхность и mesh; качество зависит от COLMAP-поз, резкости и памяти GPU. - NVIDIA Game Ready и TensorRT WebUI — 2023-10-19: драйвер 545.84 расширил DLSS и RTX Video Super Resolution, а расширение Automatic1111 добавило TensorRT-движки для Stable Diffusion; профиль движка стал зависеть от разрешения и batch size. - NVIDIA GeForce RTX 40 SUPER — 2024-01-09: появились RTX 4070 SUPER, 4070 Ti SUPER и 4080 SUPER, включая 4070 SUPER по стартовой цене 599 долларов; семейство остается рабочим, но уже не является текущим поколением. - NVIDIA ACE — 2024-03-19: демонстрации GDC/GTC показали локальные и облачные персонажи с Riva и Audio2Face; партнерские демо не означали доступность всех компонентов как одного SDK. - NVIDIA Limited-Interval Guidance — 2024-04-12: исследование показало, что reviewer-free guidance полезнее в средней части диффузионной траектории; на ImageNet 512 авторы улучшили FID с 1,81 до 1,40, но результат требует проверки на конкретной модели. - NVIDIA Open GPU Kernel Modules — 2024-07-18: начиная с R560 открытые модули стали рекомендуемым и стандартным вариантом для Turing, Ampere, Ada и Hopper, обязательным для новых платформ и несовместимым с Maxwell, Pascal и Volta. - NVIDIA GeForce 576.02 — 2025-04-21: появились неподтвержденные сообщения о зависшем мониторинге температуры и некорректном поведении вентиляторов после сна; это был диагностический сигнал, а не доказательство повреждения GPU. - NVIDIA GeForce Hotfix 576.15 — 2025-04-22: NVIDIA исправила остановку мониторинга температуры после выхода из сна и несколько сбоев RTX 50, игр и SteamVR; временная сборка позднее уступила место WHQL-драйверу. - NVIDIA UniRelight — 2025-07-07: единая модель совместила декомпозицию материала и перенос освещения для изображений и видео, включая тени, отражения и временную согласованность; опубликованный код имеет некоммерческую лицензию. - NVIDIA Streaming Sortformer v2 — 2025-08-22: потоковая диаризация стала выдавать покадровые метки до четырех говорящих с настраиваемой задержкой; английский язык остается основной областью качества. - GreenBoost — 2026-08-07: сторонний Linux-модуль предложил иерархию VRAM, RAM и NVMe для CUDA-нагрузок; его собственная документация отрицает связь с NVIDIA, а RTX IO описывает ввод-вывод и декомпрессию, не расширение VRAM. - NVIDIA Current Platform — 2026-09-04, найдено сегодня: текущие точки входа включают GeForce RTX 50 с DLSS 4.5, NVIDIA App, актуальный ACE для локального и облачного выполнения, TensorRT for RTX и Streaming Sortformer v2.1. - NVIDIA Legacy Support — 2026-09-04, найдено сегодня: Maxwell, Pascal и Volta получают только критические обновления безопасности до октября 2028 года, тогда как новые функции Game Ready ориентированы на Turing и новее. Мера/предел: линия охватывает потребительские драйверы, платформенный ИИ, игровые компоненты и исследовательские прототипы с разными циклами поддержки. Вердикт: практический переход состоит не в обновлении всей NVIDIA сразу, а в выборе конкретной ветви и проверке ее матрицы совместимости.

## How to use this

As of 2025-08-22, practitioners evaluating NVIDIA should treat it as a versioned end-to-end stack spanning hardware, drivers and kernel modules, acceleration extensions, and deployable AI models. Each workflow should be pinned to the dated first-party documentation for its components rather than treating a hardware announcement, community warning, or rumor as compatibility proof.

1. На Windows установите NVIDIA App, выберите Game Ready Driver для новых игр или Studio Driver для рабочих приложений, затем проверьте номер фактически загруженного драйвера.
  — <https://nvidia.custhelp.com/app/answers/detail/a_id/5521/~/nvidia-app-faq>
2. На Linux сначала определите поколение каждого GPU: для Turing и новее выбирайте открытый модуль, для Maxwell, Pascal, Volta или смешанного парка — проприетарный модуль.
  — <https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html>
3. Установите CUDA Toolkit поддерживаемым пакетным менеджером дистрибутива, предварительно сверив GPU, ОС и компилятор; не смешивайте пакетную и runfile-установку.
  — <https://docs.nvidia.com/cuda/cuda-installation-guide-linux/>
4. Сопоставьте версию драйвера с CUDA Toolkit или CUDA внутри контейнера и только после этого выполните проверочный sample приложения.
  — <https://docs.nvidia.com/deploy/cuda-compatibility/index.html>
5. Для воспроизводимой среды выберите в NGC явный тег или digest контейнера, изучите его release notes и сохраните выбранную версию вместе с конфигурацией проекта.
  — <https://docs.nvidia.com/ngc/latest/ngc-catalog-user-guide.html>
6. Для RTX-инференса экспортируйте модель в ONNX, соберите переносимый AOT-движок TensorRT for RTX, затем выполните JIT-специализацию и сохраните runtime cache на целевой машине.
  — <https://docs.nvidia.com/deeplearning/tensorrt-rtx/latest/getting-started/quick-start-guide.html>
7. Для Stable Diffusion WebUI установите TensorRT-расширение, создайте движок под нужные разрешения и batch size и выберите его в поле SD Unet.
  — <https://github.com/NVIDIA/Stable-Diffusion-WebUI-TensorRT>
8. Для быстрого NeRF подготовьте перекрывающиеся фотографии или видео, получите позы через COLMAP и загрузите набор в instant-ngp.
  — <https://github.com/NVlabs/instant-ngp>
9. Для детализированного mesh подготовьте откалиброванный набор с надежными позами, запустите Neuralangelo через Docker или Conda и отдельно выполните извлечение поверхности.
  — <https://github.com/NVlabs/neuralangelo>
10. Для интерактивного персонажа выберите только необходимые части ACE — распознавание речи, языковую модель или Audio2Face — и отдельно решите, где они выполняются: локально или в облаке.
  — <https://developer.nvidia.com/ace>
11. Для переноса света установите зависимости UniRelight, загрузите опубликованные веса и подайте исходное видео вместе с целевой HDRI, учитывая некоммерческую лицензию.
  — <https://github.com/nv-tlabs/UniRelight>
12. Для потоковой диаризации загрузите Streaming Sortformer v2.1 через NeMo, приведите аудио к 16 кГц и выберите профиль задержки до интерпретации четырех выходных каналов говорящих.
  — <https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2.1>

## Best practices

- Фиксируйте точные версии драйвера, контейнера и модели, а для контейнера сохраняйте тег или digest; обозначение latest не является воспроизводимой конфигурацией.
  — <https://docs.nvidia.com/ngc/latest/ngc-catalog-user-guide.html>
- Не смешивайте пакетный менеджер и runfile для одного CUDA-стека: конфликтующие методы установки затрудняют обновление и удаление.
  — <https://docs.nvidia.com/cuda/cuda-installation-guide-linux/>
- Выбирайте открытый или проприетарный Linux-модуль по поколению самого старого GPU в узле; смешанный парк требует совместимого для всех устройств варианта.
  — <https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html>
- Рассматривайте hotfix как временную сборку: после появления WHQL-драйвера с теми же исправлениями переходите на него, если контрольная нагрузка проходит.
  — <https://www.nvidia.com/en-us/geforce/news/geforce-rtx-april-30-2025-game-ready-driver/>
- Для NeRF снимайте резкие кадры с хорошим перекрытием и покрытием объекта; ориентир instant-ngp — примерно 50–150 кадров, а отсутствие сходимости обычно указывает на данные или позы.
  — <https://github.com/NVlabs/instant-ngp/blob/master/docs/nerf_dataset_tips.md?plain=1>
- Перед Neuralangelo планируйте память: стандартная конфигурация рассчитана минимум на 24 ГБ VRAM, а профили 8–16 ГБ снижают качество или размер задачи.
  — <https://github.com/NVlabs/neuralangelo>
- Для TensorRT WebUI заранее включайте в профиль все используемые разрешения и batch size; стороны должны быть кратны 64, а SDXL обычно требует не менее 12 ГБ VRAM.
  — <https://github.com/NVIDIA/Stable-Diffusion-WebUI-TensorRT>
- Limited-interval guidance применяйте как проверяемую гипотезу: подбирайте интервал заново для конкретной модели и сравнивайте качество с полным CFG.
  — <https://arxiv.org/abs/2404.07724>
- Streaming Sortformer проверяйте на собственном языке, акустике, перебиваниях и числе участников; опубликованная модель ограничена четырьмя говорящими и преимущественно английской речью.
  — <https://developer.nvidia.com/blog/identify-speakers-in-meetings-calls-and-voice-apps-in-real-time-with-nvidia-streaming-sortformer/>
- Не включайте UniRelight в коммерческий продукт до отдельного разрешения: опубликованный код и веса распространяются по NVIDIA OneWay Noncommercial License.
  — <https://github.com/nv-tlabs/UniRelight>
- GreenBoost рассматривайте как независимый экспериментальный модуль ядра: проверяйте его на непроизводственной машине и не приписывайте результат поддержке NVIDIA или RTX IO.
  — <https://gitlab.com/IsolatedOctopi/greenboost>
- Для Maxwell, Pascal и Volta планируйте миграцию, если нужны новые функции и оптимизации: после октября 2025 года для них заявлены только критические исправления безопасности.
  — <https://nvidia.custhelp.com/app/answers/detail/a_id/5676/kw/gpu%20scaling>

## Superseded by this

- 2023-03-02 — драйвер для Atomic Heart, THE FINALS и первого RTX Video Super Resolution является исторической сборкой; текущий драйвер следует получать через NVIDIA App или официальный каталог.
- 2023-05-24 — рецепт Windows AI, привязанный к драйверу 532.03, Olive и раннему ONNX/DirectML-стеку, больше не задает актуальный минимум; применяются текущие требования выбранного runtime.
- 2023-10-19 — указание справки TensorRT WebUI о будущем появлении SDXL устарело: текущий репозиторий поддерживает SDXL, SDXL Turbo и LCM.
- 2024-01-09 — RTX 40 SUPER больше не является текущим поколением GeForce; текущая продуктовая линия — RTX 50, хотя это не означает прекращения поддержки RTX 40.
- 2024-07-18 — R560 был переходной точкой к открытым модулям; текущая документация сохраняет поколенческое правило, но использует более новые ветви драйверов.
- 2025-04-22 — Hotfix 576.15 был заменен WHQL-драйвером 576.28 от 2025-04-30 и последующими выпусками; сохранять hotfix как рабочий baseline не следует.
- 2025-08-22 — модель diar_streaming_sortformer_4spk-v2 заменена моделью v2.1; новые интеграции должны начинаться с карточки v2.1.
- 2025-10 — полная Game Ready-поддержка Maxwell, Pascal и Volta завершена; до октября 2028 года для них заявлены только критические обновления безопасности.

## Still unknown

- NVIDIA в этой линии означает как минимум четыре разных предмета: потребительские GPU и драйверы, CUDA/TensorRT/NGC, ACE и речевые модели, а также исследовательские прототипы. Единой установки, лицензии и политики совместимости для них нет.
- Некоторые даты событий на один–четыре дня позднее даты публикации первичного материала; хронология сохраняет даты самих событий, а не задним числом заменяет их датой статьи.
- Для eDiff-I не подтвержден публичный поддерживаемый API, официальный набор весов или текущий продуктовый маршрут; надежно установлен только статус исследования.
- Вывод по источникам: GreenBoost является независимым проектом с измерениями автора на ограниченной конфигурации, а не подтвержденной функцией NVIDIA. Первичного объявления NVIDIA о превращении SSD в дополнительную CUDA VRAM не найдено.
- Производственное качество UniRelight вне опубликованных примеров не подтверждено независимыми измерениями; лицензия опубликованного кода некоммерческая.
- Обозначение последней CUDA зависит от артефакта: отдельная страница Toolkit показывает 13.3 Update 1, а NGC PyTorch 26.08 включает CUDA 13.4.1. Выбирать версию следует по точной матрице компонента.
- Исторические показатели ускорения, FID и задержки получены авторами на конкретных моделях и GPU; они не гарантируют тот же результат на другой конфигурации.

## Sources

| source | title | read |
|---|---|---|
| https://www.nvidia.com/en-us/about-nvidia/ | About Us: Company Leadership, History, Jobs, News | NVIDIA | 2026-09-04 |
| https://blogs.nvidia.com/blog/instant-nerf-research-3d-ai/ | NVIDIA Research Turns 2D Photos Into 3D Scenes in the Blink of an AI | 2026-09-04 |
| https://github.com/NVlabs/instant-ngp | GitHub - NVlabs/instant-ngp: Instant neural graphics primitives: lightning fast NeRF and more | 2026-09-04 |
| https://github.com/NVlabs/instant-ngp/blob/master/docs/nerf_dataset_tips.md?plain=1 | instant-ngp/docs/nerf_dataset_tips.md at master · NVlabs/instant-ngp · GitHub | 2026-09-04 |
| https://arxiv.org/abs/2211.01324 | eDiff-I: Text-to-Image Diffusion Models with an Ensemble of Expert Denoisers | 2026-09-04 |
| https://www.nvidia.com/en-us/geforce/news/atomic-heart-dlss-3-the-finals-closed-beta-game-ready-driver/ | Game Ready Driver Released For Atomic Heart DLSS 3, THE FINALS Closed Beta & RTX Video Super Resolution | 2026-09-04 |
| https://blogs.nvidia.com/blog/graphics-research-advances-generative-ai-next-frontier/ | Latest NVIDIA Graphics Research Advances Generative AI’s Next Frontier | 2026-09-04 |
| https://blogs.nvidia.com/blog/microsoft-build-nvidia-ai-windows-rtx/ | NVIDIA and Microsoft Drive Innovation for Windows PCs in New Era of Generative AI | 2026-09-04 |
| https://developer.nvidia.com/blog/?p=65490 | Generative AI Sparks Life into Virtual Characters with NVIDIA ACE for Games | 2026-09-04 |
| https://blogs.nvidia.com/blog/2023/06/01/neuralangelo-ai-research-3d-reconstruction/ | Digital Renaissance: NVIDIA Neuralangelo Research Reconstructs 3D Scenes | 2026-09-04 |
| https://github.com/NVlabs/neuralangelo | GitHub - NVlabs/neuralangelo: Official implementation of Neuralangelo: High-Fidelity Neural Surface Reconstruction | 2026-09-04 |
| https://www.nvidia.com/en-us/geforce/news/game-ready-driver-dlss-3-naraka-vermintide-rtx-vsr/ | New Game Ready Driver Released: DLSS 3 For NARAKA: BLADEPOINT and Warhammer: Vermintide 2, Plus RTX Video Super Resolution Enhancements & Stable Diffusion Is Now Up To 2X Faster | 2026-09-04 |
| https://github.com/NVIDIA/Stable-Diffusion-WebUI-TensorRT | GitHub - NVIDIA/Stable-Diffusion-WebUI-TensorRT: TensorRT Extension for Stable Diffusion Web UI | 2026-09-04 |
| https://nvidia.custhelp.com/app/answers/detail/a_id/5487/~/tensorrt-extension-for-stable-diffusion-web-ui | TensorRT Extension for Stable Diffusion Web UI | 2026-09-04 |
| https://nvidianews.nvidia.com/news/geforce-rtx-40-super-series/ | GeForce RTX 40 SUPER Series: New Heroes Debut in the Gaming and Creating Universe With AI as Their Superpower | 2026-09-04 |
| https://www.nvidia.com/en-eu/geforce/news/nvidia-ace-gdc-gtc-2024-ai-character-game-and-app-demo-videos/ | NVIDIA Digital Human Technologies Bring AI Game Characters To Life | 2026-09-04 |
| https://arxiv.org/abs/2404.07724 | Applying Guidance in a Limited Interval Improves Sample and Distribution Quality in Diffusion Models | 2026-09-04 |
| https://developer.nvidia.com/blog/nvidia-transitions-fully-towards-open-source-gpu-kernel-modules/ | NVIDIA Transitions Fully Towards Open-Source GPU Kernel Modules | 2026-09-04 |
| https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html | Kernel Modules — NVIDIA Driver Installation Guide | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1k3n6fj/read_to_save_your_gpu/ | Read to Save Your GPU! : r/StableDiffusion | 2026-09-04 |
| https://nvidia.custhelp.com/app/answers/detail/a_id/5650 | GeForce Hotfix Display Driver version 576.15 | 2026-09-04 |
| https://www.nvidia.com/en-us/geforce/news/geforce-rtx-april-30-2025-game-ready-driver/ | New GeForce Game Ready Driver Released | 2026-09-04 |
| https://research.nvidia.com/labs/toronto-ai/UniRelight/ | UniRelight: Learning Joint Decomposition and Synthesis for Video Relighting | 2026-09-04 |
| https://github.com/nv-tlabs/UniRelight | GitHub - nv-tlabs/UniRelight: UniRelight | 2026-09-04 |
| https://developer.nvidia.com/blog/identify-speakers-in-meetings-calls-and-voice-apps-in-real-time-with-nvidia-streaming-sortformer/ | Identify Speakers in Meetings, Calls, and Voice Apps in Real Time with NVIDIA Streaming Sortformer | 2026-09-04 |
| https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2 | nvidia/diar_streaming_sortformer_4spk-v2 | 2026-09-04 |
| https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2.1 | nvidia/diar_streaming_sortformer_4spk-v2.1 | 2026-09-04 |
| https://gitlab.com/IsolatedOctopi/greenboost | Ferran Duarri / greenboost · GitLab | 2026-09-04 |
| https://developer.nvidia.com/rtx-io | RTX IO Open Source Technology | NVIDIA Developer | 2026-09-04 |
| https://nvidia.custhelp.com/app/answers/detail/a_id/5521/~/nvidia-app-faq | NVIDIA App FAQ | 2026-09-04 |
| https://www.nvidia.com/Download/index.aspx/ | Official Drivers | NVIDIA | 2026-09-04 |
| https://developer.nvidia.com/cuda-downloads | CUDA Toolkit 13.3 Update 1 Downloads | NVIDIA Developer | 2026-09-04 |
| https://docs.nvidia.com/cuda/cuda-installation-guide-linux/ | CUDA Installation Guide for Linux — Installation Guide for Linux 13.3 documentation | 2026-09-04 |
| https://docs.nvidia.com/deploy/cuda-compatibility/index.html | CUDA Compatibility — CUDA Compatibility | 2026-09-04 |
| https://docs.nvidia.com/ngc/latest/ngc-catalog-user-guide.html | NGC Catalog User Guide | 2026-09-04 |
| https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel-26-08.html | PyTorch Release 26.08 - NVIDIA Docs | 2026-09-04 |
| https://docs.nvidia.com/deeplearning/tensorrt-rtx/latest/getting-started/quick-start-guide.html | Quick Start Guide — NVIDIA TensorRT for RTX | 2026-09-04 |
| https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/ | GeForce RTX 50 Series Graphics Cards | 2026-09-04 |
| https://developer.nvidia.com/ace | NVIDIA ACE for Games | 2026-09-04 |
| https://nvidia.custhelp.com/app/answers/detail/a_id/5676/kw/gpu%20scaling | Support Plan for Maxwell, Pascal, and Volta-series GeForce GPUs | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:nvidia`, thread `ai-and-accelerated-computing-platform`, 12 dated events 2022-03-28 → 2025-08-22.
- **Practical note:** As of 2025-08-22, practitioners evaluating NVIDIA should treat it as a versioned end-to-end stack spanning hardware, drivers and kernel modules, acceleration extensions, and deployable AI models. Each workflow should be pinned to the dated first-party documentation for its components rather than treating a hardware announcement, community warning, or rumor as compatibility proof.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
