---
title: "Unitree"
category: organizations

tags: [organization, unitree, unitree-development]
aliases: ["Unitree"]
level: 2
source_sha256: 272495f16804600e2afe61cedda5e51d4bde926bac4f2ebf11df2a9c4765a82e
translation: machine
translated_at: '2026-10-24'
---
# Unitree {#unitree}

**Entwicklungslinie:** `organization:unitree` · Strang `unitree-development`  
**Letztes Ereignis:** - · 0 datierte seit - · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Unitree entwickelt Hardware und Software für praktische Arbeit mit dem humanoiden Roboter G1, Vierbeinern und Robotarmen.

- Physische Roboter: humanoide und vierbeinige Plattformen für Feldtests.
- SDK2 und DDS: programmatische Kommunikation und Robotersteuerung.
- ROS und MuJoCo: Simulationsumgebungen für Regler.
- Teleoperation und Policy-Kits: Werkzeuge für Datenerfassung und Policy-Training.

Der G1 EDU bietet 23–43 Freiheitsgrade, etwa 2 Stunden Laufzeit und Möglichkeiten zur Weiterentwicklung; der Basis-G1 hat 23 Freiheitsgrade.
Dies ist eine Plattform für technische Integration und Tests auf realer Hardware, kein fertiger universeller autonomer Arbeiter.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

- 2026-04-12 — Ein veröffentlichtes Unitree-Video ließ sich nicht zuverlässig einem bestimmten Modell, einer Version oder einem Release zuordnen. Die verfügbare Ansicht lieferte keine Metadaten, daher können wir diesen Sachverhalt nicht erweitern.
- 2026-06-01 — Unitree kündigte den H2 Plus als Referenz-Humanoiden für die akademische Forschung mit NVIDIA Isaac GR00T an. Dies ist ein separates, späteres Ereignis und keine Klärung des Aprilvideos.
- 2026-09-05 — Die aktuelle G1-Seite nennt einen Einstiegspreis ab 13.500 USD. Der historische Nachrichtenbeitrag von 2024 nannte einen Preis ab 16.000 USD.

## Wie man das anwendet {#how-to-use-this}

Stand 2026-04-12 keine Änderung der Praxis auf Basis dieser Linie vornehmen, bis das verlinkte Video recherchiert und die Ereignisfakten verifiziert sind.

1. Wählen Sie das konkrete Modell und Paket. Die G1-Entwicklung erfordert die EDU-Variante, da der Basis-G1 keine Weiterentwicklung unterstützt.
  — <https://www.unitree.com/g1/>
2. Verbinden Sie den Roboter gemäß den offiziellen Anleitungen mit dem Netzwerk. Installieren Sie die Python-SDK2-Schnittstelle und die Cyclone-DDS-Abhängigkeiten und beginnen Sie dann mit Status- und Steuerbeispielen.
  — <https://github.com/unitreerobotics/unitree_sdk2_python>
3. Testen Sie den Regler im Unitree-MuJoCo-Simulator, bevor Sie auf die Hardware deployen. Verwenden Sie für den G1 die unitree_hg-Nachrichten, nicht unitree_go.
  — <https://github.com/unitreerobotics/unitree_mujoco>
4. Nutzen Sie den veröffentlichten Unitree-Imitation-Learning-Stack, um Policies zu trainieren und zu deployen. Er umfasst Datenerfassung, Algorithmenentwicklung, Training und Verifikation auf dem G1.
  — <https://www.unitree.com/mobile/opensource/>

## Bewährte Praktiken {#best-practices}

- Beginnen Sie mit den offiziellen SDK2-Beispielen und prüfen Sie den Namen der Netzwerkschnittstelle, bevor Sie Befehle an den Roboter senden.
  — <https://github.com/unitreerobotics/unitree_sdk2_python>
- Führen Sie Regelschleifen zuerst in MuJoCo aus. Wählen Sie für den G1 explizit die unitree_hg-Nachrichten.
  — <https://github.com/unitreerobotics/unitree_mujoco>
- Kombinieren Sie Low-Level- und High-Level-Steuermodi nicht ohne Prüfung des Zustands. Offene SDK-Meldungen bestätigen RPC-Fehler und Konflikte nach dem Ausführen von Low-Level-Beispielen.
  — <https://github.com/unitreerobotics/unitree_sdk2_python/issues/39>

## Abgelöst durch dies {#superseded-by-this}

- 2024-07-05 — Die historische Unitree-Angabe zum G1 ab 16.000 USD ist als Preisreferenz veraltet. Die aktuelle G1-Seite nennt Preise ab 13.500 USD.

## Weiterhin unbekannt {#still-unknown}

- Das Video vom 2026-04-12 lieferte von YouTube keinen überprüfbaren Titel, Autor, Veröffentlichungsdatum oder Beschreibung. Das konkrete Modell und die Bedeutung des Ereignisses bleiben unbekannt.
- Unitree pflegt mehrere Produktlinien. Ohne Metadaten können wir das Aprilvideo nicht dem G1, H2, H1, R1 oder einem Vierbeiner zuordnen.
- Der aktuelle Preis ab 13.500 USD gilt für die G1-Seite. Er bestätigt keinen Preis für eine bestimmte Konfiguration, Region, Versand oder Steuern.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.youtube.com/watch?v=zoMDadPQLKA | YouTube-Video zoMDadPQLKA | 2026-09-05 |
| https://www.unitree.com/g1/ | Unitree G1 | 2026-09-05 |
| https://www.unitree.com/news/ | Unitree News Center | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_sdk2_python | unitree_sdk2_python | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_mujoco | unitree_mujoco | 2026-09-05 |
| https://www.unitree.com/mobile/opensource/ | Official Open Source | 2026-09-05 |
| https://github.com/unitreerobotics/unitree_sdk2_python/issues/39 | Can't run g1 high_level example after running low_level examples | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `organization:unitree`, Strang `unitree-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-04-12 keine Änderung der Praxis auf Basis dieser Linie vornehmen, bis das verlinkte Video recherchiert und die Ereignisfakten verifiziert sind.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich für das, was veraltet ist.
