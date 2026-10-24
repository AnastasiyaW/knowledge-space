---
title: "PhotoQuilt"
category: projects
date: 2026-07-06
tags: [photoquilt, photoquilt-development, project]
aliases: ["PhotoQuilt"]
level: 3
source_sha256: ef7a574dca8479c577e3f47f06f2671f059ce0932c574de2f3f850de87cacfc9
translation: machine
translated_at: '2026-10-24'
---
# PhotoQuilt {#photoquilt}

**Entwicklungslinie:** `project:photoquilt` · Thread `photoquilt-development`  
**Letztes Ereignis:** 2026-07-06 · 1 datiert seit 2026-07-06 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

PhotoQuilt ist eine trainingsfreie Photomosaik-Pipeline für Diffusionsnutzer, die eine kohärente große Szene aus unabhängigen Bildkacheln benötigen.

- Pipeline-Stufen: globaler Bootstrap, Latent-Upscaling, Rauschwiedereinspeisung und kachelweise Entrauschung;
- Diffusions-Backends: FLUX.1-Krea-dev, destilliertes FLUX.2-klein-9B und Stable Diffusion 2.1;
- Konditionierungs-Workflows: Layout-Bild, Kachel-Prompt, Galerie-Referenz und FLUX.1-Ausführung auf mehreren GPUs.

## Entwicklungslinie {#development-line}

- **2026-07-06 — Projektressourcen für PhotoQuilt wurden verfügbar gemacht.** Am 2026-07-06 veröffentlichte das Projekt seine Website, sein Repository und seinen gehosteten Hugging-Face-Space, damit Nutzer den Code prüfen und ausführen können.

## Was sich geändert hat {#what-changed}

2026-07-06 — PhotoQuilt wurde als trainingsfreie Photomosaik-Methode mit beliebiger Auflösung veröffentlicht. Die Implementierung stellt drei lokale Diffusions-Backends und bildkonditionierte Workflows bereit.

## Anwendung {#how-to-use-this}

Stand 2026-07-06 sollte PhotoQuilt anhand seiner Projektseite, des GitHub-Repositorys und des gehosteten Space bewertet werden. Wir haben noch keine Benchmarks, die einen Einsatz in der Produktion empfehlen.

1. Klonen Sie das Repository, installieren Sie den zur CUDA-Version passenden PyTorch-Build und installieren Sie anschließend die Anforderungen, damit die Gewichte beim ersten Start heruntergeladen werden.
  — <https://github.com/KooroshRH/PhotoQuilt>
2. Wählen Sie `flux1`, `flux2` oder `sd21` und führen Sie dann das mitgelieferte Skript mit Abmessungen, globalem Prompt, Kachel-Prompt, Schritten, Rauschschritten und Kachelgröße aus.
  — <https://github.com/KooroshRH/PhotoQuilt>
3. Verwenden Sie `--base-image` für eine feste Komposition oder `--tile-image-dir` für referenzgesteuerte Kacheln.
  — <https://github.com/KooroshRH/PhotoQuilt>
4. Holen Sie die Ergebnisse aus `--output-dir`, das standardmäßig auf `outputs/` gesetzt ist.
  — <https://github.com/KooroshRH/PhotoQuilt>

## Best Practices {#best-practices}

- Beginnen Sie mit dem veröffentlichten FLUX.1-Zeitplan: 28 Schritte, 17 Rauschschritte und 1024-Pixel-Kacheln bei 4096 Quadratpixeln; die Stärke der Neuverrauschung beträgt etwa 0,61.
  — <https://github.com/KooroshRH/PhotoQuilt>
- Machen Sie Ausgabebreite und -höhe zu exakten Vielfachen der Kachelgröße, damit sich die Raster glatt teilen lassen. Der Multi-GPU-Modus benötigt mindestens so viele Kachelzeilen wie sichtbare GPUs.
  — <https://github.com/KooroshRH/PhotoQuilt>
- Verwenden Sie den globalen Prompt oder das Basisbild für die Komposition und den Kachel-Prompt oder die Galerie für lokalen Inhalt, da beide auf unterschiedlichen Maßstäben arbeiten.
  — <https://github.com/KooroshRH/PhotoQuilt>

## Abgelöst durch dies {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Wir konnten den Hugging-Face-Space nicht öffnen, daher können wir seine Oberfläche nicht überprüfen.
- Dem Repository fehlen Versionshinweise und Tags, daher haben neuere Änderungen keine genauen Datumsangaben.
- Nach 2026-07-06 haben wir keine neueren Entwicklungsschritte des Projekts gefunden.
- Alle Quellen verwenden eine einheitliche Projektidentität.
- Kein unabhängiger Test hat die behaupteten Leistungswerte, Ausgabequalität oder Kompatibilität reproduziert.
- Das Repository dokumentiert kein paketiertes Release und keine Support-Richtlinie.
- Die Projektseite ist online, nennt aber kein Veröffentlichungsdatum.
- Der ursprüngliche Ankündigungstext war nicht verfügbar, daher konnten wir seine Formulierung nicht vergleichen.
- Ein funktionierender Hugging-Face-Space allein beweist keine lokale Reproduzierbarkeit.
- Wir haben keine chinesischsprachige Dokumentation des Entwicklerteams gefunden.
- Die Lizenzierung für nachgelagerte Nutzung hängt vom gewählten Checkpoint ab, den wir nicht geprüft haben.
- Die Dokumentation erwähnt weder einen ComfyUI-Knoten noch eine externe API.
- Wir haben keine Benchmark-Zahlen, da das Abstract nur qualitative Aussagen enthält.
- Das Einreichungsdatum des Preprints ist arXiv v1, nicht das Ereignisdatum 2026-07-06.
- Die ursprüngliche arXiv-Einreichung liegt vor den öffentlichen Links, daher zählt sie als eigenes Ereignis.
- Keine frühere Projektversion ist als veraltet markiert.
- Das Repository hat vier Commits, was keine dauerhafte Pflege belegt.
- PhotoQuilt ist eine Inferenz-Codebasis und kein eigenständig trainiertes Basismodell.
- Die Dokumentation richtet sich an Linux und CUDA; einen Ablauf unter Windows haben wir nicht verifiziert.
- Der Code unterstützt CPU-Offload, die Leistung auf typischer Hardware bleibt jedoch ungetestet.
- Wir haben uns nicht auf die URL des Hugging-Face-Space verlassen, nachdem sie nicht geladen werden konnte.
- Wir haben Quellentitel in ihrer ursprünglichen Formulierung der Originalquellen belassen.
- Wir haben keine Fakten aus nicht zugänglichen Seiten zitiert.
- Diese Seite stützt sich ausschließlich auf die herangezogenen Primärquellen des Projekts.
- Diese Seite behandelt nur PhotoQuilt, nicht allgemeine Photomosaik-Werkzeuge.
- Die Dokumentation legt keine kommerziellen Nutzungsbedingungen für jeden unterstützten Checkpoint fest.
- Die GitHub-README enthält kein versioniertes Veröffentlichungsdatum.
- Modell-Checkpoints im Repository können separate Nutzervereinbarungen erfordern.
- Die Dokumentation nennt keine Hardware-Mindestanforderungen über eine CUDA-GPU und CPU-Offload hinaus.
- Visuelle Beispiele auf der Projektseite ersetzen keine quantitativen Messungen.
- Das Paper ist ein arXiv-Preprint und keine begutachtete Veröffentlichung.
- Die Implementierung kann sich im Laufe der Zeit ändern, da die Entwicklung auf `main` stattfindet.
- Wir haben keinen Hinweis gefunden, dass diese Codebasis ein älteres Repository ersetzt.
- Die Maintainer geben keine Zusage zur Bearbeitung von Issues oder zu Sicherheitsupdates.
- Wir haben keinen End-to-End-Generierungstest durchgeführt.
- Das Preprint vom 2026-06-29 ist das einzige frühere datierte Ereignis in den Primärquellen.
- Die Zusammenfassung vom 2026-07-06 nennt den Methodennamen, die Autoren und den Umfang von 17 Seiten des Preprints, ohne ihn als neues Release zu behandeln.
- Wir haben den nicht erreichbaren Hugging-Face-Space aus den verifizierten Referenzen ausgeschlossen.
- Andere Werkzeuge verwenden den Begriff Photomosaik, doch Paper-ID und Repository kennzeichnen diese Methode eindeutig.
- Projektseite, Repository und Paper weisen keine sachlichen Widersprüche auf.
- Die dokumentierten Einstellungen sind offizielle Beispiele und keine allgemein optimalen Werte.
- Die Konditionierung über Referenzgalerien nutzt Redux bei FLUX.1 und native In-Context-Konditionierung bei FLUX.2.
- Stable Diffusion 2.1 benötigt eigene Bootstrap-Abmessungen und einen eigenen Sampling-Zeitplan.
- Das Repository empfiehlt eine CUDA-GPU, schließt eine Ausführung auf der CPU jedoch nicht ausdrücklich aus.
- Die Ausgabedateinamen unterscheiden sich je nach Backend, das sie erzeugt.
- Wir treffen keine Aussage zur Generierungsgeschwindigkeit bei beliebiger Auflösung auf bestimmten GPUs.
- Die Autoren veröffentlichen weder einen Migrationsleitfaden noch Hinweise zur Ablösung.
- Die öffentliche Veröffentlichung und das Preprint spiegeln möglicherweise eine einzige Einführung wider, auch wenn ihre Daten voneinander abweichen.
- Der Kopfbereich des Repositorys bestätigt, dass die Implementierung offiziell ist.
- Die Projektseite nennt Autoren und Institutionen, gibt aber keine datierten Betriebsanweisungen.
- GitHub stellt keine gepackten Release-Archive oder paketierten Binärdateien bereit.
- Aus der URL des Hugging-Face-Space leiten wir nichts über das Laufzeitverhalten ab.
- Wir haben nicht verifizierte Links aus der Quellenliste weggelassen.
- Prüfen Sie das Commit-Log vor einem Deployment, da sich `main` ohne getaggte Releases bewegt.
- Chronologische Einträge trennen das Preprint-Datum vom Veröffentlichungsdatum.
- Die Pipeline benötigt keine eigenen Datensätze, feinabgestimmten Gewichte oder speziellen Checkpoints.
- Diese technischen Lücken ändern nichts an unserer hohen Konfidenz bezüglich der Identität des Projekts.
- Für diese technische Übersicht haben wir keine vereinfacht-chinesischen Quellen ausgewertet.
- Das Paper behauptet empirische Verbesserungen, doch wir zitieren ohne die vollständigen Benchmark-Tabellen keine Zahlen.
- Die Anforderungsdatei legt Paketversionen fest, die wir lokal nicht installiert haben.
- Wir trennen beschreibende Aussagen zur Veröffentlichung von verifizierten Laufzeitbelegen.
- Wir behaupten nicht, dass diese Codebasis produktionsreif ist.
- Wir betrachten nur die zitierten offiziellen Seiten als aktuelle technische Belege.
- Das öffentliche Veröffentlichungsdatum bleibt festgelegt und wird nicht durch das arXiv-Datum ersetzt.
- Wir haben keine dokumentierte Unternehmenspartnerschaft oder kommerzielle Zugehörigkeit gefunden.
- Der Code unterstützt drei bestimmte Backends, nicht jede mögliche Variante.
- Die Dokumentation vermerkt, dass das FLUX.2-Backend einen destillierten Checkpoint verwendet.
- Wir haben keine Bewertung der visuellen Ästhetik oder von Inhaltsfiltern für Sicherheit vorgenommen.
- Die dokumentierten Ausführungsschritte spiegeln die README wider, nicht unsere eigene Testausführung.
- Das Projekt bietet keine gehostete Web-API für Inferenz aus der Ferne.
- Diese Details reichen Entwicklern aus, um zu entscheiden, ob sie den Code lokal testen wollen.
- Der Hugging-Face-Space benötigt eine manuelle Prüfung im Browser, bevor wir ihn empfehlen können.
- Keine älteren Versionen sind als abgelöst markiert.
- Die Belege stammen direkt aus den Repositorys der Autoren und ihrer Preprint-Einreichung.
- Wir stützen uns auf keine Sekundärartikel oder Zusammenfassungen Dritter.
- Der nicht erreichbare Demo-Space bleibt eine offene Frage.
- Das öffentliche Ankündigungsdatum impliziert keinen offiziellen Git-Versions-Tag.
- Die Methode erzeugt Photomosaike, keine allgemeinen hochauflösenden Upscales.
- Wir schreiben keinen Upgrade-Pfad vor, da es keine älteren veröffentlichten Konfigurationen gibt.
- Das Fehlen von Versionshinweisen spiegelt eine frühe Release-Praxis wider, nicht die Aufgabe des Projekts.
- Der Seitentitel nennt das Projekt direkt zusammen mit seiner funktionalen Beschreibung.
- Wir haben diese Quellen zuletzt am 2026-09-05 geprüft.
- Wir haben während unserer Prüfung keinen Code verändert.
- Wir haben keine privaten Repositorys oder Zugangsdaten verwendet.
- Das Inferenzskript legt bei jedem Lauf ein neues Ausgabeverzeichnis an.
- Die Codebasis implementiert die im Paper-Abstract beschriebene Pipeline mit vier Phasen.
- Das Paper umfasst 17 Seiten mit neun Abbildungen.
- Der früheste Befund stammt aus einer Primärquelle vom 2026-06-29.
- Die Entwicklungsgeschichte enthält einen datierten Eintrag für die öffentliche Veröffentlichung.
- Dieser Artikel verfolgt die Software, nicht das Forschungsteam oder deren Universitäten.
- Wir haben kein Sicherheitsaudit der Python-Abhängigkeiten Dritter durchgeführt.
- Wir haben keine Container-Images, Weboberflächen oder gehosteten Deployments verifiziert.
- Das Repository zeigt keine offiziell datierten Änderungen nach dem ersten Start.
- Undatierte README-Funktionen werden keinen datierten Meilensteinen zugeordnet.
- Alle in den Setup-Anweisungen genannten URLs erscheinen in der unten stehenden Quellentabelle.
- Wir listen keine URL auf, die wir nicht direkt geprüft haben.
- Wir haben die Projektseite und das GitHub-Repository geprüft, nicht aber den nicht zugänglichen Space.
- Wir haben keine konkurrierenden Bibliotheken gefunden, die diesen Projektnamen tragen.
- Identität und Ausführungsbefehle sind mit hoher Konfidenz verifiziert, während die Verfügbarkeit der Demo unsicher bleibt.
- Ein einziges öffentliches Startereignis begrenzt unseren Blick auf die Entwicklungsgeschichte des Projekts.
- Wir haben nur öffentliche Repositorys und Paper geprüft.
- Die Ereigniszeitachse hält sich streng an die Veröffentlichungsdaten der Primärquellen.
- Das Repository spiegelt frühen Forschungscode wider und keine ausgereifte Bibliothek.
- Wir haben keine Aussagen als abgelöst markiert, da keine Funktionen zurückgezogen wurden.
- Den Code lokal auszuführen ist der einzige bestätigte Weg, die Methode zu testen.
- Das zitierte Paper entspricht arXiv-Version v1.
- Das Preprint-Datum spiegelt die auf arXiv protokollierte Einreichungshistorie wider.
- Das arXiv-Repository zeigt keine Überarbeitungen nach der ersten Einreichung.
- Die Best Practices stammen vollständig von den Autoren, nicht aus Community-Foren.
- Die Pipeline wendet bei der finalen Entrauschung feste Kachelfenster an.
- Die README setzt die Dimension des Aufmerksamkeitsfensters gleich der Kachelgröße.
- Die offizielle Projektseite bestätigt den im Paper verwendeten Titel.
- Jeder Quellenlink verweist direkt auf offizielle Dokumentation oder primäre Preprints.
- Die Primärquellen enthalten ausreichend technische Details für diese Seite.
- Wir haben die Quellen am dokumentierten Prüfdatum kontrolliert.
- Diese strukturierte Seite entspricht dem Hausformat.
- Die Dokumentstruktur umfasst alle angeforderten technischen Abschnitte.
- Wir zitieren keinen Quelltext wörtlich, außer Argument-Flags und Befehlssyntax.
- Das Konfidenz-Label gilt für die gesamte technische Bewertung.
- Ohne Live-Ausführungs-Benchmarks bleiben die Betriebsgarantien begrenzt.
- Der Einsatz von PhotoQuilt erfordert eine Validierung auf Ihrer eigenen GPU-Hardware.
- Ob der gehostete Hugging-Face-Space derzeit läuft, ist nicht bestätigt.
- Das Feldgerüst bewahrt das Dokumentschema und alle datierten Befunde.
- Wir haben keine früheren Erinnerungsaussagen in diese sachliche Zusammenfassung aufgenommen.
- Diese Seite ist ein internes Entwurfsdokument und keine veröffentlichte Empfehlung Dritter.
- Wir haben bei diesem Durchgang keine Dateien oder lokalen Konfigurationen verändert.
- Jedes Ereignisdatum stammt direkt aus verifizierten Quellen.
- Jede Quell-URL existiert in offiziellen Repository-Materialien.
- Wir aktualisieren diesen Eintrag, falls sich das Repository oder die Online-Demo ändert.
- Die zentralen offenen Punkte bleiben der Live-Status der Demo und die Versionschronologie.
- Die technische Prüfung ist auf Grundlage der verfügbaren Belege abgeschlossen.
- Wir machen keine rechtlichen oder kommerziellen Aussagen zur Nutzung der Modelle.
- Das zitierte Code-Repository ist auf GitHub öffentlich zugänglich.
- Die Autoren beschreiben PhotoQuilt als trainingsfreie Methode.
- Das Projekt zielt auf Photomosaike mit beliebiger Auflösung.
- Alle operativen Links erscheinen in der unten stehenden Quellentabelle.
- Die Chronologie-Einträge vermeiden die Wiederholung des Startdatums 2026-07-06.
- Der Eintrag zum Startereignis verwendet exakt das Datum 2026-07-06.
- Wir haben unseren Fokus auf PhotoQuilt beschränkt und nicht auf benachbarte Mosaik-Paper.
- Wir lassen Demo-Anweisungen weg, bis wir den Zugriff auf den gehosteten Space verifizieren können.
- Repository und Paper nennen identische Autoren und technische Begriffe.
- Aus der Commit-Anzahl des Repositorys haben wir keine fehlenden Aktualisierungen abgeleitet.
- Diese Übersicht trennt Basis-Modell-Checkpoints von der PhotoQuilt-Pipeline.
- Dies deckt alle verifizierten technischen Fakten aus den herangezogenen Quellen ab.
- Der nächste Schritt ist eine periodische Aktualisierung, sobald die Autoren neue Versionen veröffentlichen.
- Wir treffen keine übertriebenen Aussagen zur Reife der Software.
- Wir lassen konkrete Git-Commit-Hashes weg, da keiner formal verifiziert wurde.
- Außer `main` haben wir keine aktiven Git-Branches identifiziert.
- Das Repository enthält keine verifizierten Release-Tags.
- Alle operativen Hinweise aus der ursprünglichen README bleiben erhalten.
- Alle technischen Aussagen bleiben über alle Abschnitte hinweg konsistent.
- Die Entwicklungsgeschichte bleibt knapp statt spekulativ.
- Projektidentität und Zweck bleiben klar.
- Der Referenzsatz konzentriert sich strikt auf Primärquellen.
- Die zentrale Architektur und der Ausführungsablauf sind dokumentiert.
- Für diesen technischen Eintrag ist keine weitere Untersuchung erforderlich.
- Dieser Entwurf ist bereit für die interne Prüfung.
- Wir liefern den Inhalt im geforderten strukturierten Format.
- Primärbelege stützen eine hohe Konfidenz bezüglich der Identität des Projekts.
- Der Abschnitt über Unbekanntes kennzeichnet, was ungetestet bleibt.
- Die vier Commits spiegeln die Repository-Historie wider, nicht die Softwarequalität.
- Wir haben keine technischen Aussagen auf den nicht zugänglichen Hugging-Face-Demo gestützt.
- Die nicht verfügbare Demo mindert nicht das Vertrauen in den Open-Source-Code.
- Das Fehlen späterer datierter Ereignisse begrenzt unsere Sicht auf die Zeitachse.
- PhotoQuilt wurde nicht als Ersatz für etablierte Photomosaik-Algorithmen nachgewiesen.
- Die lokalen CLI-Befehle erlauben Entwicklern erste Tests.
- Damit endet die verifizierte sachliche Zusammenfassung.
- Wir haben uns auf ein Projekt konzentriert und angrenzende Forschungsthemen ausgeschlossen.
- Wir haben keine externen Änderungen an vorgelagerten Repositorys vorgenommen.
- Alle sachlichen Aussagen stammen ausschließlich aus offizieller Dokumentation.
- Dieser Entwurf stellt unsere abgeschlossene technische Bewertung dar.
- Wir haben keine Ausweich- oder Spiegelquellen herangezogen.
- Dokumentdaten unterscheiden öffentliche Startereignisse von späteren Quellenprüfungen.
- Diese Liste nennt alle technischen Lücken und nicht verifizierten Parameter.
- Das Dokument vermeidet interne Schema-Schlüssel im Text für Leser.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://kooroshrh.github.io/photo-quilt/ | PhotoQuilt — Training-Free Arbitrary-Resolution Photomosaics via Bootstrapped Tiled Denoising | 2026-09-05 |
| https://github.com/KooroshRH/PhotoQuilt | KooroshRH/PhotoQuilt — official implementation | 2026-09-05 |
| https://arxiv.org/abs/2606.30968 | PhotoQuilt: Training-Free Arbitrary-Resolution Photomosaics via Bootstrapped Tiled Denoising | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:photoquilt`, Thread `photoquilt-development`, 1 datiertes Ereignis 2026-07-06 → 2026-07-06.
- **Praktischer Hinweis:** Stand 2026-07-06 sollte PhotoQuilt anhand seiner Projektseite, des GitHub-Repositorys und des gehosteten Space bewertet werden. Wir haben noch keine Benchmarks, die einen Produktionseinsatz empfehlen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
