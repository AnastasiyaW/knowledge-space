---
title: CARLA-Air
category: projects
date: 2026-04-03
tags: [carla-air, carla-air-release, carla_air_release, project]
aliases: ["CARLA-Air"]
---

# CARLA-Air

**Development line:** `project:carla-air` · thread `carla-air-release`  
**Last event:** 2026-04-03 · 1 dated since 2026-04-03 · **Researched:** 2026-09-05 · confidence: medium

## What it is

CARLA-Air — открытая среда air-ground симulation для исследователей embodied AI, навигации, восприятия и RL. Она даёт единый мир, синхронные сенсоры и два Python API: CARLA для автомобилей и AirSim для мультикоптеров. Текущий публичный релиз — v0.1.7; основной предел — карта Town10HD требует около 8 GB VRAM, а координатная калибровка зависит от карты. Вердикт: практичнее связки CARLA с отдельным AirSim-процессом, когда нужен общий мир для дрона и автомобиля.

## Development line

- **2026-04-03 — CARLA-Air GitHub repository linked.** On 2026-04-03, the CARLA-Air development line included a link to the project's GitHub repository, louis zeng CN/CarlaAir. This provides a dated public-source reference for the project. The available evidence does not establish a release, version, change set, or repository contents.

## What changed

2026-03-19 — вышел публичный v0.1.6: единый процесс CARLA 0.9.16 и AirSim, автотрафик, collision toggle и ground clamping. 2026-03-24 — v0.1.7 исправил VSync и стабильность трафика, добавил one-click setup, запись полёта и документацию координат; совместимость со скриптами и конфигурациями v0.1.6 заявлена сохранённой. 2026-04-03 — зафиксирована ссылка на проект; первичный источник не содержит отдельного changelog-события этой датой, поэтому считать её новым релизом нельзя. 2026-04-10 — опубликована ветка исходников для Windows. 2026-04-16 — стал доступен готовый бинарный пакет v0.1.7 для Windows 11 x86_64. 2026-04-17 — опубликован сайт проекта. 2026-04-20 — добавлены минимальные примеры ROS 2 Humble для сенсоров автомобиля и дрона, с RViz 2.

## How to use this

As of 2026-04-03, practitioners can use the linked GitHub repository as a candidate source for CARLA-Air, while verifying its contents and relevance before relying on it.

1. Скачайте и распакуйте готовый Linux- или Windows-пакет; для первого запуска на Linux используйте поддерживаемый Ubuntu 20.04/22.04.
  — <https://github.com/louiszengCN/CarlaAir>
2. В каталоге v0.1.7 запустите `bash env_setup/setup_env.sh`, затем `bash env_setup/test_env.sh` и активируйте conda-окружение `carlaAir`.
  — <https://github.com/louiszengCN/CarlaAir/releases>
3. Запустите `./CarlaAir.sh Town10HD`; дождитесь готовности CARLA на localhost:2000 и AirSim на localhost:41451.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>
4. Проверьте оба API отдельными клиентами `carla.Client` и `airsim.MultirotorClient`, затем начните с `examples/quick_start_showcase.py`.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>

## Best practices

- Для интерактивного управления оставляйте асинхронный режим; для датасета, воспроизведения и записи используйте fixed-step synchronous mode и синхронизируйте Traffic Manager.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md>
- Всегда возвращайте мир в асинхронный режим в `finally`, иначе сервер будет ждать `world.tick()` после завершения скрипта.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md>
- При смене карты повторно калибруйте CARLA-AirSim offsets; формула из релиза откалибрована для Town10HD.
  — <https://github.com/louiszengCN/CarlaAir/releases>
- При нехватке VRAM или низком FPS начните с меньшей карты и снизьте качество либо число actors.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>

## Superseded by this

- 2026-03-24: v0.1.7 заменяет v0.1.6 как текущий релиз; обновляться следует в новый каталог, повторно запустив setup, а не поверх старой установки.
- 2026-04-16: для Windows прежнее отсутствие готового пакета устарело — доступен Windows 11 x86_64 binary v0.1.7.
- 2026-04-20: для базовой ROS 2 визуализации больше не требуется собирать carla-ros-bridge из исходников; проектные примеры используют прямые Python API и rclpy. Полный bridge всё ещё нужен для его дополнительных actions, services и Ackermann control.

## Still unknown

- Текст сообщения от 2026-04-03 недоступен; ссылка на репозиторий сама по себе не доказывает, что в этот день был релиз или конкретное изменение.
- Первичные материалы, найденные при проверке, не дают отдельного датированного факта, который можно без натяжки добавить именно к событию 2026-04-03.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/louiszengCN/CarlaAir | CARLA-Air: Fly Drones Inside a CARLA World | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/releases | CARLA-Air releases | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md | CARLA-Air Quick-Start Guide | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md | CARLA-Air FAQ | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:carla-air`, thread `carla-air-release`, 1 dated events 2026-04-03 → 2026-04-03.
- **Practical note:** As of 2026-04-03, practitioners can use the linked GitHub repository as a candidate source for CARLA-Air, while verifying its contents and relevance before relying on it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
