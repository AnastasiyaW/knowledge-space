---
title: "img2threejs"
category: projects
date: 2026-07-24
tags: [img2threejs, project]
aliases: ["img2threejs"]
level: 2
source_sha256: 39f90ba725a789d2467cea8a24888238187a443d4d9a2bee93b1ebc667a8d092
translation: machine
translated_at: '2026-10-24'
---
# img2threejs {#img2threejs}

**Entwicklungslinie:** `project:img2threejs` · Thread `img2threejs`  
**Letztes Ereignis:** 2026-07-24 · 1 datiertes seit 2026-07-24 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

img2threejs ist ein Apache-2.0-Skill für Claude Code, Codex und OpenCode: Aus einem einzigen Bild erzeugt er eine TypeScript-Factory für `THREE.Group`, nicht eine GLB-Datei oder ein extrahiertes Mesh. — zerlegt das Objekt in Komponenten, Materialien, Sockets und Collider; — erzeugt das Modell in Durchgängen und vergleicht das Rendering mit der Referenz; — kann bei Charakteren ein Rig aufbauen und die Animation prüfen. Einschränkung: Ein einzelnes Bild zeigt keine verdeckten Seiten; für exakte Ähnlichkeit kennzeichnet das Projekt unsichere Bereiche ausdrücklich und fordert zusätzliche Ansichten an. Fazit: geeignet, wenn lesbarer und animierbarer Three.js-Code benötigt wird; ersetzt weder Photogrammetrie noch manuelle Modellierung für nicht sichtbare Geometrie.

## Entwicklungslinie {#development-line}

- **2026-07-24 — Das GitHub-Repository von img2threejs wurde öffentlich verlinkt.** Am 2026-07-24 enthielt die Entwicklungslinie von img2threejs einen direkten Link auf das GitHub-Repository. Dies dokumentiert einen öffentlichen Meilenstein als Quellenreferenz für das Projekt; die gesicherten Belege belegen weder Funktionsumfang, Release-Status noch eine konkrete Codeänderung.

## Was sich geändert hat {#what-changed}

2026-07-15 — v1.0 veröffentlichte die objektorientierte Pipeline mit gestuftem Sculpting, Side-by-side-Review und Runtime-Hierarchie; v1.1 ergänzte das verpflichtende Inventar kleiner Details und das Strict-Quality-Gate. 2026-07-21 — v1.2 führte humanoide Charaktere und hybride Objekte in eine eigene Route mit Proportionen und Diagnostik über. 2026-07-22 — v1.3 ergänzte den deterministischen Review-Harness Divine Eye, geometrische Prüfungen und referenzbasierte Materialien. 2026-07-24 — Das Projekt wurde als Python-Werkzeug vorgestellt, das aus einer einzigen Referenz eine prozedurale, animationsfähige Rekonstruktion in Three.js erzeugt. 2026-07-25 — v1.4.0 ergänzte eine spezialisierte CS2-Waffen-Pipeline mit Provenance, Geometriefamilien und Review-Gates. 2026-07-26 — v1.4.1 verschärfte die CS2-Prüfungen: Komponenten-Coverage, Glock-18-Vertrag und Nachweise echter Geometrie statt überzeugender Textur. 2026-07-30 — v1.4.3 legte 1.4.x als akzeptierte Release-Linie fest; eine Veröffentlichung ist nur noch aus einem genehmigten annotierten Tag möglich. 2026-08-12 — v1.5.0 ersetzte die Beta-Linie: ergänzt um validierbares Rig, Skinning, Hair-Pipeline, Links-/Rechts-Prüfung und Review-Gates pro Feature. 2026-08-22 — v1.5.1 ergänzte die GLB-Referenzroute: Die GLB-Datei dient als Messinstrument, das Ergebnis ist weiterhin TypeScript-Code. 2026-08-25 — v1.5.2 ergänzte messbare Animation-/Rigging-Gates; fehlende Daten bedeuten jetzt `unevaluated`, nicht PASS.

## Anwendung {#how-to-use-this}

Stand 2026-07-24 können Praktiker das verlinkte GitHub-Repository als öffentliche Quellenreferenz des Projekts nutzen; vor dem Einsatz sollten sie Funktionsumfang und Versionsstatus jedoch direkt prüfen.

1. Klonen Sie das Repository in das Skills-Verzeichnis; der Kern benötigt Python 3.10+ und die Standardbibliothek.
  — <https://github.com/img2threejs/img2threejs>
2. Übergeben Sie dem Agenten ein Bild und rufen Sie `/img2threejs` auf; die Pipeline klassifiziert das Subjekt selbst und erstellt assessment/spec.
  — <https://github.com/img2threejs/img2threejs>
3. Führen Sie die Strict-Quality-Validierung aus und erzeugen Sie die TypeScript-Factory erst nach bestandenem Gate.
  — <https://github.com/img2threejs/img2threejs>
4. Erstellen Sie für längere Arbeiten und Charaktere einen State-Index und setzen Sie anschließend den nächsten zulässigen Durchgang über `forge/next.py` fort.
  — <https://github.com/img2threejs/img2threejs>
5. Wenn eine GLB-Datei des Charakters vorliegt, nutzen Sie die separate GLB-Referenzroute; ohne sie bleiben Sie bei der bildbasierten Kern-Pipeline.
  — <https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1>

## Best Practices {#best-practices}

- Beginnen Sie mit einem abgegrenzten Hard-Surface-Objekt mit lesbarer Silhouette; verdeckte Flächen dürfen nicht als gemessen dargestellt werden.
  — <https://github.com/img2threejs/img2threejs>
- Listen Sie zuerst die identitätsbestimmenden Details auf und ordnen Sie jedes einer Komponente oder einem Material zu; umgehen Sie `--strict-quality` nicht.
  — <https://github.com/img2threejs/img2threejs>
- Prüfen Sie jeden Durchgang anhand eines Vergleichsblatts „Referenz neben Rendering“ und gehen Sie ohne PASS nicht weiter.
  — <https://github.com/img2threejs/img2threejs>
- Betrachten Sie bei Charakteren einen vorhandenen `AnimationClip` nicht als funktionierende Animation: Führen Sie die Rig-/Animation-Gates aus und werten Sie `unevaluated` als unvollständige Prüfung.
  — <https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md>

## Abgelöst durch {#superseded-by-this}

- 2026-07-30: Die automatische Veröffentlichung nach dem Merge eines PR ist veraltet; ein Release erfordert einen genehmigten annotierten Versions-Tag.
- 2026-08-12: `1.4.4-beta.1`, `1.4.4-beta.2` und `v1.5-beta` wurden durch das stabile v1.5.0 ersetzt; 1.4.4 wurde nicht als stabile Version veröffentlicht.
- 2026-08-25: Die Regel „Ein Clip ohne Travel/Rise darf wiederholt werden“ wurde durch die Messung der Rückkehr der Pose und der Beckenposition ersetzt; ein ungeprüfter Loop darf nicht mehr stillschweigend als `false` gelten.

## Noch unbekannt {#still-unknown}

- Das Repository, auf das die ursprüngliche Verlinkung zeigte, leitet derzeit von `hoainho/img2threejs` auf `img2threejs/img2threejs` weiter; Datum und Grund der Verlagerung sind nicht ermittelt.
- Das aktuelle Changelog enthält nach v1.5.2 einen Abschnitt Unreleased; dieser ist kein veröffentlichtes Release und sollte nicht als verfügbare stabile Version gelten.
- event_findings:[{"event_date":"2026-07-24","source_date":"2026-07-24","finding":"Am selben Datum präzisiert ein unabhängiger Katalog den praktischen Rahmen: Es handelt sich um ein Python-Werkzeug, das aus einer Referenz ein prozedurales, animationsfähiges Three.js-Modell erzeugt; es ist kein eigenständiger Mesh- oder Bild-zu-3D-Dienst.","source_url":"https://buttondown.com/surfaced/archive/surfaced-friday-july-24-2026/"}]
- new_events:[{"date":"2026-07-15","finding":"v1.0 und v1.1: objektbezogene gestufte Pipeline und verpflichtendes Inventar kleiner Details mit Strict-Quality-Gate.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-21","finding":"v1.2: eigene Route für humanoide Charaktere und hybride Subjekte.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-22","finding":"v1.3: Divine Eye sowie deterministische Prüfungen von Geometrie, Materialien und Eingabedaten.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-25","finding":"v1.4.0: CS2-Waffen-Pipeline mit Provenance und familienspezifischer Rekonstruktion.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-26","finding":"v1.4.1: Komponenten-Coverage-Gate und Glock-18-Vertrag.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-30","finding":"v1.4.3: akzeptierte Release-Linie 1.4.x und Veröffentlichung nur aus einem genehmigten annotierten Tag.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-08-12","finding":"v1.5.0: validierbares Rig, Skinning, Hair-Subsystem und Review-Gates für Charaktere.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-08-22","finding":"v1.5.1: GLB-Referenzroute mit Vermessung der Parameter und Code als Ergebnis.","source_url":"https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1"},{"date":"2026-08-25","finding":"v1.5.2: ausführbare Animation-/Rigging-Gates, bei denen ungeprüfte Eingaben nicht zu PASS werden können.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"}]

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/hoainho/img2threejs | img2threejs-Repository: Weiterleitung auf das kanonische Organisations-Repository | 2026-09-05 |
| https://github.com/img2threejs/img2threejs | img2threejs README | 2026-09-05 |
| https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md | img2threejs-Changelog | 2026-09-05 |
| https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1 | Release 1.5.1: GLB-Referenzroute hinzugefügt | 2026-09-05 |
| https://buttondown.com/surfaced/archive/surfaced-friday-july-24-2026/ | Surfaced — Friday, July 24, 2026 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Gegenstand:** `project:img2threejs`, Thread `img2threejs`, 1 datiertes Ereignis 2026-07-24 → 2026-07-24.
- **Praxishinweis:** Stand 2026-07-24 können Praktiker das verlinkte GitHub-Repository als öffentliche Quellenreferenz des Projekts nutzen; vor dem Einsatz sollten sie Funktionsumfang und Versionsstatus direkt prüfen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.
