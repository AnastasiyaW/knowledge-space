---
title: RealityScan — Mobile Photogrammetry Launch and Release
category: projects
date: 2022-12-05
tags: [mobile-photogrammetry-launch-and-release, project, realityscan, realityscan_beta_launch]
aliases: ["RealityScan"]
---

# RealityScan — Mobile Photogrammetry Launch and Release

**Development line:** `project:realityscan` · thread `mobile-photogrammetry-launch-and-release`  
**Last event:** 2022-12-05 · 2 dated since 2022-04-04 · **Researched:** 2026-09-04 · confidence: high

## What it is

RealityScan — инструмент для создателей 3D-ассетов: мобильное приложение снимает объект серией фото и обрабатывает модель в облаке, настольная версия работает с фото и лазерными сканами. Мобильная версия требует iOS 16+ либо Android 7+ с ARCore; настольная бесплатна до $1 млн годовой выручки. Вердикт: для быстрого захвата объектов подходит мобильная версия, для точной съёмки и больших наборов данных нужен RealityScan Desktop.

## Development line

- **2022-04-04 — RealityScan Beta Was Introduced.** Началась ограниченная бета мобильного RealityScan — 10 000 мест TestFlight, обработка фотографий в 3D-модель и экспорт через Sketchfab.
- **2022-12-05 — RealityScan Reached Public Availability.** Приложение вышло из беты как бесплатная iOS/iPadOS-версия; на момент релиза Android ещё не поддерживался.

## What changed

2022-04-04: началась ограниченная бета мобильного RealityScan — 10 000 мест TestFlight, обработка фотографий в 3D-модель и экспорт через Sketchfab. 2022-12-05: приложение вышло из беты как бесплатная iOS/iPadOS-версия; на момент релиза Android ещё не поддерживался. 2023-06-20: мобильная версия стала доступна на Android и получила пошаговый workflow; Epic сообщила о более чем 200 000 загрузок iOS-версии. 2024-06-24: RealityScan Mobile 1.5 добавил локальную загрузку моделей, необязательную публикацию в Sketchfab и экспорт OBJ на iOS либо GLB на Android. 2025-06-17: профессиональный RealityCapture был переименован в RealityScan; RealityScan 2.0 стал настольным продуктом, а телефонное приложение — RealityScan Mobile. 2026-06-24: RealityScan 2.2 добавил аппаратно ускоренную реконструкцию на поддерживаемых AMD Radeon и Ryzen AI Max в Windows.

## How to use this

From 2022-12-05, practitioners could treat RealityScan as a publicly available mobile photogrammetry option rather than only a newly announced beta.

1. Проверьте совместимость устройства: iOS 16+ либо Android 7+ с ARCore, затем установите приложение и войдите в Epic Games account.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/RealityScan-System-Requirements-and-Installation?lang=en-US>
2. Создайте проект в Augmented Reality Mode и обойдите объект несколькими дугами на разной высоте; лимит съёмки — 300 кадров.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
3. Просмотрите облако точек, ограничьте reconstruction region, запустите обработку и дождитесь статуса Processed.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
4. Откройте View/Edit Scan, кадрируйте результат и экспортируйте модель на устройство или отправьте её в Sketchfab.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
5. Для настольной обработки установите нужную версию через вкладку RealityScan в Epic Games Launcher.
  — <https://dev.epicgames.com/documentation/en-us/realityscan/getting-realityscan>

## Best practices

- Держите объект в кадре минимум наполовину и обеспечьте высокий перекрывающийся охват со всех доступных сторон: невидимые в нескольких кадрах области не попадут в модель.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Не переключайтесь в другое приложение во время загрузки и первичного анализа, чтобы не прервать съёмочный workflow.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Перед обработкой исключите фон и лишние точки reconstruction region: всё за границами области не реконструируется.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide>
- Для контролируемой съёмки используйте Camera Control Mode и сохраняйте постоянные настройки света и вспышки в пределах одной сессии.
  — <https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-mobile-1-6-release-notes?lang=en-US>

## Superseded by this

- 2022-04-04: ограниченная TestFlight-бета и обещание будущего iOS Early Access заменены публичным мобильным приложением.
- 2022-12-05: iOS-only статус устарел после Android-релиза 2023-06-20.
- 2022-12-05: обязательный экспорт через Sketchfab устарел после RealityScan Mobile 1.5 от 2024-06-24, который добавил локальную загрузку моделей.
- 2025-06-17: RealityCapture как актуальное имя настольного продукта заменён на RealityScan; старое имя осталось только для legacy-версий и лицензий.

## Still unknown

- В заданной схеме ответа отсутствуют поля event_findings и new_events, поэтому дополнительные данные по событиям включены в what_changed и supersedes.
- События 2022-04-04 и 2022-12-05 относятся к одной мобильной линии RealityScan; настольный RealityScan появился под этим именем только после переименования RealityCapture в 2025 году.

## Sources

| source | title | read |
|---|---|---|
| https://www.capturingreality.com/introducing-realityscan | Introducing RealityScan: Now in Limited Beta | 2026-09-05 |
| https://habr.com/ru/news/t/703566/ | Мобильный 3D-сканер RealityScan от Epic Games вышел из беты и доступен в App Store | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-is-now-free-to-download-on-ios/717656 | RealityScan is now free to download on iOS | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-is-now-available-for-android-devices/1204921 | RealityScan is now available for Android devices! | 2026-09-05 |
| https://forums.unrealengine.com/t/realityscan-1-5-0-release-notes/1914888 | RealityScan 1.5.0 Release Notes | 2026-09-05 |
| https://www.realityscan.com/news/realityscan-20-new-release-brings-powerful-new-features-to-a-rebranded-realitycapture | RealityScan 2.0: New release brings powerful new features to a rebranded RealityCapture | 2026-09-05 |
| https://www.realityscan.com/news/realityscan-2-2-is-here-with-full-amd-gpu-support-download-today | RealityScan 2.2 is here with full AMD GPU support—download today | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/RealityScan-System-Requirements-and-Installation?lang=en-US | RealityScan System Requirements and Setup | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-step-by-step-guide | RealityScan Step by Step Guide | 2026-09-05 |
| https://dev.epicgames.com/documentation/realityscan-mobile/realityscan-mobile-1-6-release-notes?lang=en-US | RealityScan Mobile 1.6 Release Notes | 2026-09-05 |
| https://dev.epicgames.com/documentation/en-us/realityscan/getting-realityscan | Getting RealityScan | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:realityscan`, thread `mobile-photogrammetry-launch-and-release`, 2 dated events 2022-04-04 → 2022-12-05.
- **Practical note:** From 2022-12-05, practitioners could treat RealityScan as a publicly available mobile photogrammetry option rather than only a newly announced beta.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
