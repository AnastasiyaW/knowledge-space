---
title: "Publikationsplattformen für technische Inhalte"
category: tools
tags: [writing, publishing, platforms, seo, marketing]
level: 3
source_sha256: ab28e7ef5ab25dfcfd99fad3b13acb8f2fc415c06671396b0142c460d897cf50
translation: machine
translated_at: '2026-10-24'
---
# Publikationsplattformen für technische Inhalte {#publishing-platforms-for-technical-content}

Wo man technische Artikel veröffentlicht, mit Zielgruppenprofilen, Formatierungsanforderungen und einer Strategie für Cross-Posting. Die Wahl der Plattform hängt von der Zielgruppe (Entwickler, Data Scientists oder allgemeines Tech-Publikum), der Sprache (EN/RU) und dem Ziel ab (SEO-Hoheit, Reichweite oder Community).

## Plattformvergleich {#platform-comparison}

| Plattform | Zielgruppe | Sprache | Geeignet für | SEO-Hoheit |
|-----------|------------|---------|--------------|------------|
| Persönlicher Blog (Hashnode/Hugo) | Deine eigene Leserschaft | Beliebig | Kanonische Heimat, volle Kontrolle | Vollständig |
| Habr | RU-Entwickler, überwiegend Senior-Level | RU | Tiefgehende Technik, Untersuchungen, OSS | Teilweise |
| Dev.to | EN-Entwickler, Junior bis Mid-Level | EN | Tutorials, Cross-Posts | Teilweise (canonical) |
| Medium / Towards Data Science | EN, Data Science, ML | EN | KI/ML-Inhalte, breite Reichweite | Keine (Paywall) |
| HackerNoon | EN-Entwickler | EN | Redaktionelle Reichweite, Long-Form | Teilweise |
| Hacker News (Show HN) | EN, Senior/Startup | EN | OSS-Launches, größte Wirkung über einen einzelnen Kanal | N/A (Link) |
| Reddit | Je nach Subreddit | EN | Nischenzielgruppen, praktisches Feedback | N/A (Link) |

## Habr (Russisch) {#habr-russian}

**Zielgruppe**: erfahrene russischsprachige Entwickler. Überwiegend Senior-Level. Geringe Toleranz gegenüber oberflächlichen Inhalten.

**Was funktioniert:**
- Pet-Projekte mit technischer Tiefe („Ich habe X gebaut, so funktioniert es")
- Untersuchungen und Reverse Engineering
- Komplexe Themen einfach erklärt (aber mit Tiefe)
- Kontroverse Standpunkte, mit Belegen untermauert
- Echte Messwerte und Vorher-nachher-Vergleiche

**Was scheitert:**
- Produktankündigungen, die als Artikel getarnt sind (werden als Werbung behandelt)
- Oberflächliche Übersichten ohne persönliche Erfahrung
- KI-generierter Text (ausdrücklich regelwidrig, die Community erkennt ihn schnell)
- Inhalte für Einsteiger ohne neuen Blickwinkel

**Formatierung:** WYSIWYG + Habr Flavored Markdown. H1/H2/H3, Codeblöcke mit Syntaxhervorhebung (30+ Sprachen), Spoiler, Tabellen. Das KPVD-Bild (Titelbild) ist entscheidend für die CTR: Es muss hell und relevant sein und darf kein Logo sein.

**Karma-System:** Moderation durch die Community. Neue Konten sind eingeschränkt. Negatives Karma beschränkt das Kommentieren. Für Karma muss man vor dem Veröffentlichen in umkämpften Hubs echte Beiträge leisten.

**Kennzahlen für erste Artikel:**
- Durchschnittliche Bewertung: +12
- Durchschnittliche Aufrufe: 6.716
- Durchschnittliche Kommentare: 20
- Nur 18 % der Autoren schreiben einen zweiten Artikel

**Optimale Länge:** 1500–2000 Wörter (7–10 Minuten Lesezeit). Habr rechnet die Lesegeschwindigkeit mit 1500 Zeichen pro Minute.

**Karma-Schwellen für Privilegien:**

| Karma | Ermöglicht |
|-------|------------|
| 0+ | Veröffentlichen in nicht primären Hubs |
| 1+ | Abstimmen über Artikel und Kommentare |
| 2+ | Abstimmen über das Karma anderer |
| 5+ | Voller Abstimmungszugang |
| 30+ | Veröffentlichen im Hub „Я пиарюсь" |
| 50+ | Neue Nutzer einladen |
| -1 bis -5 | 1 Kommentar pro 5 Minuten |
| -6 bis -10 | 1 Kommentar pro Stunde |
| -31 oder weniger | Nur Lesezugriff |

**Stimmgewicht:** Regulärer Nutzer = +1; Autor/Senior/Star = +2; Legende = +3 pro Stimme bei Artikeln.

**Google Discover:** Dynamik in der ersten Stunde (1000+ Aufrufe) löst eine Platzierung in den Trends aus. Discover ist eine wichtige sekundäre Traffic-Quelle für gut laufende Artikel. 0,3–1,2 % der Artikelleser abonnieren den Telegram-Kanal des Autors.

## Hacker News {#hacker-news}

**Geeignet für:** OSS-Projektlaunches, technische Artikel mit Neuigkeitswert.

**Format:** „Show HN: [Name] - [einzeilige Beschreibung]" für Projektlaunches.

**Timing:** Dienstag bis Donnerstag, 8–10 Uhr ET.

**Regeln:**
- Auf jeden Kommentar antworten (Interaktion treibt das Ranking)
- Keine Hype-Sprache: Zurückhaltend und technisch gewinnt
- Der Artikel bzw. das Projekt muss aus sich heraus technisch überzeugen
- Erneute Einreichungen sind in Ordnung, wenn die erste keine Resonanz fand

**Risiko:** HN-Kommentatoren finden jeden Fehler. Vor dem Posten etwas Solides ausliefern.

## Dev.to {#devto}

**Zielgruppe:** EN-Entwickler, eher Junior bis Mid-Level. Freundliche Community.

**Geeignet für:** Cross-Posting (unterstützt die kanonische URL), Tutorials, Indexierung.

**Formatierung:** Markdown. Unterstützt Titelbilder, Serien und Tags. Liquid-Tags für Einbettungen.

**SEO:** Unterstützt `canonical_url` im Frontmatter. Diesen Eintrag beim Cross-Posting aus dem eigenen Blog verwenden, um Strafen wegen doppelter Inhalte zu vermeiden.

## Medium / Towards Data Science / Towards AI {#medium-towards-data-science-towards-ai}

**Zielgruppe:** Breites Tech-Publikum bei Medium, Data Science/ML bei TDS/TAI.

**Geeignet für:** KI/ML-Artikel für ein Data-Science-Publikum.

**Nachteile:**
- Die Paywall verringert die Reichweite für Nicht-Abonnenten
- Keine Unterstützung für eine kanonische URL: Google kann Medium vor dem eigenen Blog ranken
- Die Bearbeitungsoberfläche ist sauber, aber für technische Inhalte eingeschränkt
- Die Plattform kontrolliert die Verbreitung

**Strategie:** Zuerst im eigenen Blog veröffentlichen, dann bei TDS/TAI-Publikationen einreichen. Sie nehmen externe Einreichungen mit redaktioneller Prüfung an.

## Persönlicher Blog {#personal-blog}

**Optionen:**
- **Hashnode**: entwicklerorientiert, eigene Domain, Verwaltung der kanonischen URL, integrierter Newsletter
- **Hugo/Jekyll + GitHub Pages**: volle Kontrolle, kostenloses Hosting, erfordert Einrichtung
- **Astro/Next.js**: maximale Flexibilität, mehr Wartungsaufwand

**Warum sich der Aufwand lohnt:** Die eigene SEO-Hoheit behalten. Cross-Posts auf dev.to/Medium können das Original überholen. Ein persönlicher Blog mit eigener Domain baut kumulative Autorität auf.

## Strategie für Cross-Posting {#cross-posting-strategy}

```bash
1. Publish on personal blog (canonical URL)
2. Cross-post to dev.to (with canonical_url in frontmatter)
3. Submit to HackerNoon (with canonical link)
4. Submit to TDS/TAI if ML-focused (accept editorial changes)
5. Post link on HN / Reddit after publication
6. For RU audience: write separate Habr version (not a translation - adapt for the audience)
```

**Wichtigste Regel:** Die kanonische URL zeigt immer auf die eigene Domain. Jeder Cross-Post enthält den kanonischen Link. So wird eine SEO-Kannibalisierung verhindert.

## Reddit-Subreddits für technische Inhalte {#reddit-subreddits-for-technical-content}

| Subreddit | Zielgruppe | Hinweise |
|-----------|------------|----------|
| r/MachineLearning | ML-Forscher und Praktiker | Strenge Qualitätsstandards, Diskussion von Papern |
| r/LocalLLaMA | Lokale Inferenz, Quantisierung | Praxisorientiertes Publikum, Fokus auf Anwendung |
| r/programming | Allgemeine Programmierung | Hoher Traffic, starke Konkurrenz |
| r/ExperiencedDevs | Senior-Ingenieure | Karriere und technische Tiefe |
| r/devops | DevOps/SRE | Infrastruktur, Tooling |
| r/selfhosted | Self-Hosting | OSS-Tools, Home-Lab |

**Reddit-Etikette:** Nicht einfach nur Links posten. Eine Textzusammenfassung im Beitrag oder in den Kommentaren bereitstellen. Sich an der Diskussion beteiligen. Die Regeln einzelner Subreddits variieren.

## Artikelformat für maximale Interaktion {#article-format-for-maximum-engagement}

Über alle Plattformen hinweg folgen die am besten laufenden Artikel diesem Muster:
- **1200–2000 Wörter** (7–10 Minuten Lesezeit)
- **Hook -> Problem -> Lösung -> Ergebnisse -> CTA** als Struktur
- **Diagramme/Bilder alle 300–500 Wörter** (lockert den Text auf, erhöht die Verweildauer)
- **Codebeispiele** im ersten Drittel des Artikels
- **Konkreter, nicht reißerischer Titel**, der nennt, was der Leser lernen wird

## Stolperfallen {#gotchas}

- **Problem:** Denselben Artikel ohne kanonische URLs auf mehreren Plattformen veröffentlichen führt dazu, dass Google eine Version als kanonisch auswählt, oft nicht die eigene. **Lösung:** Immer zuerst auf der eigenen Domain veröffentlichen, 24–48 Stunden auf die Indexierung warten und dann mit einer `canonical_url` auf die eigene Domain cross-posten.
- **Problem:** Einen Artikel schreiben und für EN- und RU-Leser übersetzen erzeugt Inhalte, die in beiden Sprachen unnatürlich wirken. **Lösung:** Separate Versionen schreiben. RU- und EN-Tech-Publikum haben unterschiedliche kulturelle Erwartungen, Humorstile und Referenzpunkte. Habr-Leser erwarten mehr Tiefe und Persönlichkeit als dev.to-Leser.
- **Problem:** In HN/Reddit posten, ohne die ersten 2–3 Stunden auf Kommentare antworten zu können, verschenkt den Launch. **Lösung:** Dann posten, wenn man aktiv antworten kann. Die erste Stunde der Kommentare entscheidet, ob der Beitrag Fahrt aufnimmt.

## Siehe auch {#see-also}

- [[technical-article-structure]]
- [[seo-for-articles]]
- [[natural-writing-style]]
- [[editing-checklist]]
