---
title: "LUNA"
category: projects

tags: [luna, luna-development, project]
aliases: ["LUNA"]
level: 2
source_sha256: 568556b67211e6b8db1f11a7711b4cfce0d6e19c3be95d0a21ccca2e68a6ff5e
translation: machine
translated_at: '2026-10-24'
---
# LUNA {#luna}

**Entwicklungslinie:** `project:luna` · Thread `luna-development`  
**Letztes Ereignis:** - · 0 datierte Einträge seitdem · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

LUNA ist ein Forschungsmodell zur Erzeugung animierbarer 3D-Avatare menschlicher Figuren aus N=4 nicht posierten Bildern und einem Steuersignal.

- 3D-Gaussian-Repräsentation: ersetzt Linear Blend Skinning (LBS) durch direkte Transformation.
- 2D-Steuerung: animiert den Avatar mithilfe von RGB-Video, Keypoints oder einer Skizze.

Die öffentliche Projektseite zeigt visuelle Ergebnisse, stellt aber keinen Code, keine Gewichte und kein reproduzierbares Setup bereit. Sie eignet sich als Material für die Forschungsbewertung, nicht als fertiges Werkzeug.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht aufgearbeitet; das bekannte Wissen findet sich in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

2026-07-01 — LUNA: Learning Universal 3D Human Animation Beyond Skinning stellte ein LBS-freies Modell für die Animation von 3D Gaussians vor, das mehrere 2D-Steuertypen verwendet.

## Verwendung {#how-to-use-this}

Stand 2026-07-01 ist die verlinkte LUNA-Seite als ungeprüfter Hinweis zu behandeln, nicht als verifizierte Projektentwicklungshistorie, bis das verlinkte Material und der Originalbeitrag recherchiert sind.

1. Die erforderliche Eingabe prüfen: N=4 nicht posierte Bilder einer Person und ein 2D-Steuersignal aus RGB, Keypoints oder Skizze.
  — <https://penghtyx.github.io/LUNA/>
2. Projektseite und Paper nutzen, um Methode und Ergebnisse zu bewerten; vor der Planung einer Integration nach offiziellem Code, Gewichten und Lizenz suchen.
  — <https://arxiv.org/abs/2606.31981>

## Best Practices {#best-practices}

- Demo-Ergebnisse nicht ohne lokale Tests für Zielpersonen, Kleidung, Kamerawinkel und Steuersignale in die Produktion übernehmen.
  — <https://penghtyx.github.io/LUNA/>
- Die N=4-Grenze einhalten: Die veröffentlichte Pipeline rekonstruiert kanonische 3D Gaussians speziell aus 4 Multiview-Bildern.
  — <https://penghtyx.github.io/LUNA/>

## Hiermit abgelöst {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die öffentliche Seite verlinkt kein offizielles Repository, keine Modellgewichte, keine Lizenz, keine Hardwareanforderungen und keine Ausführungsanleitung; die aktuellen Quellen können nicht bestätigen, ob diese Materialien veröffentlicht sind.
- Inhaltliche Änderungen in arXiv v2 vom 2026-09-01 bleiben unverifiziert: Die Metadaten bestätigen das Update, liefern aber kein Änderungsprotokoll.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://penghtyx.github.io/LUNA/ | LUNA: Learning Universal 3D Human Animation Beyond Skinning | 2026-09-05 |
| https://arxiv.org/abs/2606.31981 | LUNA: Learning Universal 3D Human Animation Beyond Skinning | 2026-09-05 |
| https://rawalkhirodkar.github.io/ | Rawal Khirodkar — Publications | 2026-09-05 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:luna`, Thread `luna-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-07-01 ist die verlinkte LUNA-Seite als ungeprüfter Hinweis zu behandeln, nicht als verifizierte Projektentwicklungshistorie, bis das verlinkte Material und der Originalbeitrag recherchiert sind.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
