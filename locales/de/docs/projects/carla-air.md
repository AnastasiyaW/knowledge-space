---
title: "CARLA-Air"
category: projects
date: 2026-04-03
tags: [carla-air, carla-air-release, carla_air_release, project]
aliases: ["CARLA-Air"]
level: 2
source_sha256: 2b54d89e3d6f89205047e89b7a6cc6d89988e49c682f938899430b295454882d
translation: machine
translated_at: '2026-10-24'
---
# CARLA-Air {#carla-air}

**Entwicklungslinie:** `project:carla-air` · Thread `carla-air-release`  
**Letztes Ereignis:** 2026-04-03 · 1 datiertes seit 2026-04-03 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

CARLA-Air ist eine offene Simulationsumgebung für Luft-Boden-Szenarien für Forschende in den Bereichen Embodied AI, Navigation, Wahrnehmung und RL.

- Einheitliche Welt, kombiniert Luft- und Bodenakteure in einer Simulation.
- Synchrone Sensoren, erfassen gleichzeitig Daten von beiden Plattformen.
- Zwei Python-APIs, CARLA für Autos und AirSim für Multikopter.

Die aktuelle öffentliche Version ist v0.1.7. Town10HD benötigt etwa 8 GB VRAM, und die Koordinatenkalibrierung hängt von der Karte ab. Gegenüber dem getrennten Betrieb von CARLA und AirSim als separate Prozesse ist dies vorteilhaft, wenn Drohne und Auto eine gemeinsame Welt benötigen.

## Entwicklungslinie {#development-line}

- **2026-04-03 — CARLA-Air-GitHub-Repository verlinkt.** Am 2026-04-03 verlinkte die Entwicklungslinie von CARLA-Air das GitHub-Repository des Projekts, louis zeng CN/CarlaAir. Dies liefert eine datierte öffentliche Quellenreferenz für das Projekt. Die verfügbaren Belege zeigen weder ein Release, eine Version, einen Änderungssatz noch den Inhalt des Repositorys.

## Was sich geändert hat {#what-changed}

- 2026-03-19 — Öffentliches Release v0.1.6: Einzelprozess mit CARLA 0.9.16 und AirSim, Autotraffic, Kollisionsschalter und Bodenklemmung.
- 2026-03-24 — Release v0.1.7 behob Probleme mit VSync und Verkehrsstabilität und ergänzte Ein-Klick-Einrichtung, Flugaufzeichnung und Koordinatendokumentation; die Kompatibilität mit Skripten und Konfigurationen von v0.1.6 bleibt erhalten.
- 2026-04-03 — Projektlink erfasst; die Primärquelle enthält für dieses Datum keinen Changelog-Eintrag, daher können wir es nicht als neues Release behandeln.
- 2026-04-10 — Ein Quellcode-Branch für Windows veröffentlicht.
- 2026-04-16 — Vorkompiliertes Binärpaket v0.1.7 für Windows 11 x86_64 verfügbar.
- 2026-04-17 — Projektwebsite veröffentlicht.
- 2026-04-20 — Minimale ROS-2-Humble-Beispiele für Sensoren von Auto und Drohne hinzugefügt, mit RViz 2.

## So wird es verwendet {#how-to-use-this}

Ab dem 2026-04-03 die verlinkte GitHub-Repository als Kandidatenquelle für CARLA-Air verwenden, wobei dessen Inhalt und Relevanz vor dem Vertrauen darauf zu prüfen sind.

1. Das vorkompilierte Linux- oder Windows-Paket herunterladen und entpacken; für einen ersten Lauf unter Linux die unterstützten Ubuntu 20.04/22.04 verwenden.
  — <https://github.com/louiszengCN/CarlaAir>
2. Im Verzeichnis v0.1.7 `bash env_setup/setup_env.sh` und anschließend `bash env_setup/test_env.sh` ausführen und die conda-Umgebung `carlaAir` aktivieren.
  — <https://github.com/louiszengCN/CarlaAir/releases>
3. `./CarlaAir.sh Town10HD` ausführen; warten, bis CARLA auf localhost:2000 und AirSim auf localhost:41451 bereit ist.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>
4. Beide APIs mit getrennten `carla.Client`- und `airsim.MultirotorClient`-Clients testen und anschließend `examples/quick_start_showcase.py` starten.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>

## Bewährte Vorgehensweisen {#best-practices}

- Für interaktive Steuerung den asynchronen Modus verwenden; für Datensätze, Wiedergabe und Aufzeichnung den synchronen Modus mit festem Zeitschritt und synchronisiertem Traffic Manager nutzen.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md>
- Die Welt immer im `finally`-Block wieder in den asynchronen Modus versetzen, damit der Server nach Skriptende nicht auf `world.tick()` wartend hängen bleibt.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md>
- Die CARLA-AirSim-Offsets beim Kartenwechsel neu kalibrieren; die Release-Formel ist für Town10HD kalibriert.
  — <https://github.com/louiszengCN/CarlaAir/releases>
- Bei knappem VRAM oder sinkenden Bildraten mit einer kleineren Karte sowie niedrigerer Qualität oder geringerer Akteuranzahl beginnen.
  — <https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md>

## Hiermit ersetzt {#superseded-by-this}

- 2026-03-24: v0.1.7 ersetzt v0.1.6 als aktuelles Release; beim Aktualisieren in ein sauberes Verzeichnis die Einrichtung erneut ausführen, statt über eine alte Installation zu schreiben.
- 2026-04-16: Für Windows gibt es nicht mehr kein vorkompiliertes Paket; für v0.1.7 ist eine Windows-11-x86_64-Binärdatei verfügbar.
- 2026-04-20: Die grundlegende ROS-2-Visualisierung erfordert nicht mehr den Build von carla-ros-bridge aus dem Quellcode; die Projektbeispiele nutzen direkt die Python-APIs und rclpy. Die vollständige Bridge ist nur noch für ihre zusätzlichen Aktionen, Dienste und die Ackermann-Steuerung erforderlich.

## Weiterhin unbekannt {#still-unknown}

- Der Nachrichtentext zum 2026-04-03 ist nicht verfügbar; der Repository-Link allein belegt weder ein Release noch eine bestimmte Änderung an diesem Datum.
- Die geprüften Primärquellen enthalten keine datierte Tatsache, die direkt mit dem Ereignis vom 2026-04-03 in Verbindung steht.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/louiszengCN/CarlaAir | CARLA-Air: Fly Drones Inside a CARLA World | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/releases | CARLA-Air releases | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/Quick-Start.md | CARLA-Air Quick-Start Guide | 2026-09-05 |
| https://github.com/louiszengCN/CarlaAir/blob/main/CarlaAir_Release/guide/FAQ.md | CARLA-Air FAQ | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:carla-air`, Thread `carla-air-release`, 1 datiertes Ereignis 2026-04-03 → 2026-04-03.
- **Praxishinweis:** Ab dem 2026-04-03 können Praktiker das verlinkte GitHub-Repository als Kandidatenquelle für CARLA-Air nutzen, sollten aber dessen Inhalt und Relevanz prüfen, bevor sie sich darauf verlassen.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
