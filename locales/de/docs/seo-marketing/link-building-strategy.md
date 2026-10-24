---
title: "Linkaufbau-Strategie"
category: techniques
tags: [seo-marketing, link-building, backlinks, anchor-text, light-links, heavy-links, link-dynamics]
level: 3
source_sha256: 28859b84d31e2e272021cb1ffcd1c9211e998157b2d5e28038ed876e141a20e2
translation: machine
translated_at: '2026-10-24'
---
# Linkaufbau-Strategie {#link-building-strategy}

Linktypen, Anchor-Zusammensetzung, Strategien nach Seitenalter und Unterschiede zwischen Suchmaschinen. Links sind der #1-Rankingfaktor bei Google und der #3-Rankingfaktor bei Yandex.

## Linkterminologie {#link-terminology}

- **Acceptor** - Domain, die den Link erhält
- **Donor** - Domain, die den Link setzt
- **Donor-Dokument** - konkrete Seite, auf der der Link platziert ist
- **Anchor** - sichtbarer Text des Links
- **rel-Attribut** - Link-Attribut (nofollow, sponsored usw.)

## Warum Links wichtig sind {#why-links-matter}

1. **Statisches Gewicht** - PageRank und Ableitungen
2. **Dynamisches (Anchor-)Gewicht** - Anchor-Liste, monolithischer Index
3. **BrowseRank** - Daten zur Klickrate auf Links
4. **Robot-Delivery** - Indexierung
5. **Geo-Binding** - regionale Signale

## Linktypen nach Anchor {#link-types-by-anchor}

| Typ | Beispiele |
|------|---------|
| Anchor | "Fernseher kaufen", "Wohnung mieten" |
| Non-Anchor | URL, Markenname, "hier", "Quelle" |
| URL-Links | Text rechts davon zählt als Anchor |
| Sitewide | Footer-/Header-Links auf allen Donor-Seiten |
| Nofollow | Google berücksichtigt nach eigenem Ermessen |
| Weiterleitungslinks | `/out.php?where=site.ru` (von Google gezählt) |
| Bildlinks | Das `alt`-Attribut fließt in die Anchor-Liste ein |

## Linkkategorien {#link-categories}

### Light Links {#light-links}
Leicht zu beschaffen; eine Seite kann schnell viele erhalten; überwiegend nofollow; Zweck = Verwässerung + natürliche Dynamik.

**Typen**:
1. **Crowd-Marketing** - Forenbeiträge, Kommentare, Q&A
2. **Submits** - Selbsteintragung in Verzeichnisse, Kataloge, Profile
3. **Pressemitteilungen** - Verteilung von News/PR an Medienportale

### Heavy Links {#heavy-links}
Schwer und teuer zu beschaffen; eine Seite verkraftet nicht viele auf einmal; überwiegend dofollow; Zweck = direkter Rankingschub.

**Typen**: Outreach, PBN, Glue/Redirect, dynamische Sitewide-Links, Linktausch, Multi-Tier-Links.

**Wichtig**: Liegt eine Anfrage unterhalb der TOP-50, bringen Heavy Links sie nicht in die TOP. Zuerst: On-Page + interne Verlinkung + Light Links. DANACH Heavy Links.

## Best Practices für Crowd-Marketing {#crowd-marketing-best-practices}
- Nur verifizierte Auftragnehmer
- Briefing so detailliert wie möglich ausfüllen: Plattformtypen, Themen
- Vorabprüfung von Plattformen, Themen und Texten verlangen
- Mit Spam überflutete Foren ablehnen: DR null, tot/defekt, mit Erwachsenen- oder Pharma-Inhalten kontaminiert
- Eine "Überlebensgarantie" von 2 Wochen verlangen
- Linkpräsenz überwachen (LinkChecker.pro)

## Best Practices für Submits {#submits-best-practices}
- Einzigartige Firmenbeschreibungen (keine Seitentexte wiederverwenden)
- Keine Logos/Bilder (nur das Logo ist erlaubt)
- Niemals automatische Massen-Submits bestellen
- Keine Anchor-Links aus Submits
- Gleichmäßiges Wachstum: 10, 20, 30 pro Monat

## Pressemitteilungen {#press-releases}
- Keine Anchors
- Zuerst mit einer Satellitenseite testen
- Dienst: pressfeed.ru
- Schnelle Nofollow-Links von autoritativen Hosts; helfen, dass LF-Rankings schneller starten

## Zusammensetzung der Anchor-Liste {#anchor-list-composition}

### Empfohlenes Verhältnis {#recommended-ratio}
- **70%** - URL-Varianten, Firmenname, Marke, Bilder
- **10%** - exakte Keyword-Treffer
- **20%** - Verwässerungs-Anchors und Varianten

### Vorgehen {#process}
1. Anchor-Listen der Konkurrenten für Top-Seiten dokumentweise analysieren
2. Das Verhältnis von Anchor/Verwässerung/Non-Anchor abschätzen
3. Eigene Anchor-Liste auf Basis der Ergebnisse erstellen

### KI-gestützte Erstellung der Anchor-Liste {#ai-assisted-anchor-list-construction}
**Iteration 1**: CSV-Exporte aus Ahrefs (Links und Anchors der Konkurrenz) und den semantischen Kern einreichen. Anchor-Muster analysieren.

**Iteration 2**: Prozentuale Aufteilung nach Typ berechnen: vollständige URL, URL ohne Protokoll, URL mit www, Marken-Anchors, Bildlinks, exakte Keyword-Treffer, verwässerte Treffer, generische Phrasen. Irrelevantes ausschließen.

**Iteration 3**: 30 Anchors für die Zielseite gemäß den ermittelten Verhältnissen erstellen.

## Strategie nach Seitenalter {#strategy-by-site-age}

### Neue Seite (erste 3 Monate) {#new-site-first-3-months}
- Minimale Anchor-Links
- Nur Light Links (Non-Anchor und Marke): Verzeichnisse, Foren, Q&A, Pressemitteilungen, Hersteller-/Partnerlinks
- Glue/301 von Drops: maximal 2-3, alle 2 Monate
- Nach 100 hochwertigen Donoren -> Anchor-Links hinzufügen
- Qualität > Quantität
- Einen jungen Konkurrenten finden, der schnell gewachsen ist -> nachbauen

### Gealterte Seite mit Linkhistorie {#aged-site-with-link-history}
1. Konkurrenten ähnlichen Seitentyps finden
2. Die am schnellsten wachsenden im Detail untersuchen
3. Plan nach Typen, Dynamik und Anchors zusammenstellen
4. Die Strategien der Konkurrenz verbessern
5. Heavy Links einsetzen
6. Kontinuierlich überwachen und anpassen

## Link-Zeitplan für neue Seiten {#link-timeline-for-new-sites}
- Erste 2-3 Monate: kein Linkaufbau (Fokus auf Technik, Inhalt, Struktur)
- Monat 3-6: 2-3 Light Links pro Woche
- Keine "gezackte Dynamik" - gleichmäßiges Wachstum (6->6->6->8->8->8->10)
- Nach einem Jahr mit ca. 100 Donoren: Tempo gemäß Konkurrenzanalyse erhöhen
- Yandex: Ergebnisse nach 2-3 Monaten; Google: etwa 1 Jahr; 1,5-2 Jahre, bis sich beide angleichen

## Unterschiede zwischen Suchmaschinen {#search-engine-differences}

### Yandex {#yandex}
- Links auf Dokumente (interne Gewichtung begrenzt)
- Nicht-kommerzielle Hosts erforderlich (sonst Minusinsk-Penalty)
- Yandex verfügt über einen Link-Klassifikator: ca. 94% Precision, ca. 99% Coverage
- Links werden als Good (wirksam) oder Bad (Gewicht=0) eingestuft
- Kritische Masse an Bad Links -> Minusinsk

### Google {#google}
- Kann auf die Startseite oder Hub-Seiten verlinken
- Dynamik des Linkwachstums ist wichtig
- Anchor-Liste ist entscheidend
- Vielfältige Linktypen erforderlich

## Framework für die Linkstrategie {#link-strategy-framework}
1. Konkurrenten sammeln
2. Diejenigen identifizieren, die aktiv Links aufbauen
3. Ausgangsbasis erfassen: Donor-Domains/-Seiten, Projektalter, Wachstumsdynamik, Anchor-Verhältnis, Linktypen
4. Durchschnittliche Kennzahlen der Konkurrenz als Ziel setzen
5. Auf den aktuellen Stand des eigenen Projekts abbilden
6. Gleichmäßiges, systematisches Wachstum über 1-2 Jahre planen
7. Konsequent umsetzen

## Testen der Linkwirksamkeit {#testing-link-effectiveness}
- Testseite oder schwachen Konkurrenten verwenden (TOP-50 für Schlüsselanfragen, Seite ohne Links)
- Exakten LF-Anchor platzieren und die Wirkung bewerten
- Nicht viele Links auf einmal auf der Live-Seite platzieren

## Stolperfallen {#gotchas}
- **Heavy Links bringen Anfragen unterhalb der TOP-50 nicht nach oben** - zuerst On-Page optimieren
- **Yandex erkennt, wer Links kauft und verkauft** - 95% der Links von bekannten Börsen werden als SEO-Links markiert
- **Auch über Börsen gekaufte Non-Anchor-Links können als SEO-Links zählen** - "hier", "dort" von Börsen werden erkannt
- **Gezackte Dynamik deutet auf Manipulation hin** - gleichmäßiges, stetiges Wachstum ist entscheidend
- **"Hier/dort" nicht als Anchor verwenden** - legt das Linkprofil für die Analyse durch Konkurrenten offen
- **Keine Anchor-Links aus Submits verwenden** - Submits dienen nur der Verwässerung

## Siehe auch {#see-also}
- [[link-quality-assessment]] - Donor-Qualität, Drop-Domains, PBN
- [[filters-and-penalties]] - Details zu Minusinsk- und Penguin-Filtern
- [[seo-strategy-by-site-type]] - Linkstrategie nach Seitentyp
- [[internal-linking]] - Interne Verlinkung ergänzt externe Links
