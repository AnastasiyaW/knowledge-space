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

CARLA-Air is an open air-ground simulation environment for embodied AI, navigation, perception, and RL researchers.

- Unified world, combines air and ground actors in one simulation.
- Synchronous sensors, capture feeds across both platforms at the same time.
- Two Python APIs, CARLA for cars and AirSim for multicopters.

Current public release is v0.1.7. Town10HD requires about 8 GB VRAM, and coordinate calibration depends on the map. It beats running CARLA and AirSim as separate processes when drone and car need a shared world.

## Development line

- **2026-04-03 — CARLA-Air GitHub repository linked.** On 2026-04-03, the CARLA-Air development line linked the project's GitHub repository, louis zeng CN/CarlaAir. This provides a dated public-source reference for the project. Available evidence does not show a release, version, change set, or repository contents.

## What changed

- 2026-03-19 — Public release v0.1.6: single process CARLA 0.9.16 and AirSim, autotraffic, collision toggle, and ground clamping.
- 2026-03-24 — Release v0.1.7 fixed VSync and traffic stability, adding one-click setup, flight recording, and coordinate documentation; compatibility with v0.1.6 scripts and configurations is preserved.
- 2026-04-03 — Project link recorded; primary source has no changelog entry for this date, so we cannot treat it as a new release.
- 2026-04-10 — Published a Windows source code branch.
- 2026-04-16 — Prebuilt binary package v0.1.7 became available for Windows 11 x86_64.
- 2026-04-17 — Published project website.
- 2026-04-20 — Added minimal ROS 2 Humble examples for car and drone sensors, with RViz 2.

## How to use this

As of 2026-04-03, use the linked GitHub repository as a candidate source for CARLA-Air, verifying its contents and relevance before relying on it.

1. Download and unpack the prebuilt Linux or Windows package; for a first run on Linux, use supported Ubuntu 20.04/22.04.
  — <https://github.com/louiszengCN/CarlaAir>
2. In the v0.1.7 directory, run `bash env_setup/setup_env.sh`, then `bash env_setup/test_env.sh`, and activate the `carlaAir` conda environment.
  — <https://github.com/louiszengCN/CarlaAir/releases>
3. Run `./CarlaAir.sh Town10HD`; wait until CARLA is ready on localhost:2000 and AirSim on localhost:41451.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>
4. Test both APIs with separate `carla.Client` and `airsim.MultirotorClient` clients, then start with `examples/quick_start_showcase.py`.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>

## Best practices

- Keep asynchronous mode for interactive control; for datasets, replay, and recording, use fixed-step synchronous mode and sync Traffic Manager.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md>
- Always restore the world to asynchronous mode in `finally`, so the server does not hang waiting for `world.tick()` after script completion.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md>
- Recalibrate CARLA-AirSim offsets when switching maps; the release formula is calibrated for Town10HD.
  — <https://github.com/louiszengCN/CarlaAir/releases>
- Start with a smaller map and lower quality or actor counts if VRAM runs low or frame rates drop.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>

## Superseded by this

- 2026-03-24: v0.1.7 replaces v0.1.6 as the current release; update into a clean directory by rerunning setup rather than over an old install.
- 2026-04-16: Windows no longer lacks a prebuilt package; a Windows 11 x86_64 binary is available for v0.1.7.
- 2026-04-20: Basic ROS 2 visualization no longer requires building carla-ros-bridge from source; project examples use direct Python APIs and rclpy. The full bridge remains necessary only for its extra actions, services, and Ackermann control.

## Still unknown

- Message text for 2026-04-03 is unavailable; the repository link alone does not prove a release or a specific change on that date.
- Primary sources checked provide no dated fact that ties directly to the 2026-04-03 event.

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