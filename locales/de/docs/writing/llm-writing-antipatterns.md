---
title: "LLM-Schreib-Anti-Patterns"
description: "Erkennbare KI-Textmuster: übermäßig verwendetes Vokabular, strukturelle Anti-Patterns, Burstiness- und Perplexitätsmetriken, russischspezifische Marker und Checkliste zur Humanisierung."
level: 3
source_sha256: 8df2f456fc144c888015e06193c31cf6c5b7b1d0f26749e0b8f50c82fb605cc4
translation: machine
translated_at: '2026-10-24'
---
# LLM-Schreib-Anti-Patterns {#llm-writing-anti-patterns}

Wie sich KI-generierte Textmuster erkennen und vermeiden lassen. Behandelt werden englische Vokabularmarker, strukturelle Signaturen, die Burstiness-Metrik, russischspezifische Muster und eine praktische Checkliste zur Überarbeitung.

## Aussagekräftiges englisches Vokabular {#high-signal-english-vocabulary}

Aus der Analyse von mehr als 15 Mio. PubMed-Abstracts (Liang et al., arXiv 2406.07016):

### Stufe 1: Sofortige Warnsignale {#tier-1-immediate-red-flags}

| Wort | Überschussverhältnis | Anmerkung |
|------|-------------|------|
| delves | 25,2-fach | Klassischer KI-Marker, verschwand nach breiter öffentlicher Thematisierung |
| showcasing | 9,2-fach | |
| underscores | 9,1-fach | |
| across, additionally, comprehensive | hoch | Gehören zu den 10 wirksamsten Erkennungsmarkern |
| crucial, enhancing, insights | hoch | |
| notably, particularly, within | hoch | |

**66 % des überschüssigen KI-Vokabulars sind Verben und Adjektive**, keine inhaltlichen Substantive. Deshalb ist KI-Text als *Stil* erkennbar, nicht als *Inhalt*.

### Stufe 2: Häufig markierte Begriffe {#tier-2-common-flagged-terms}

**Verben:** delve, dive into, embark, navigate, uncover, unveil, unlock, unleash, leverage, harness, foster, bolster, spearhead, champion, resonate, captivate, illuminate, elevate, underscore, shed light on

**Adjektive:** vibrant, meticulous, intricate, multifaceted, nuanced, holistic, comprehensive, compelling, profound, pivotal, paramount, cutting-edge, transformative, seamless, innovative

**Substantive/Metaphern:** tapestry, landscape, realm, labyrinth, beacon, crucible, interplay, synergy, zeitgeist, game changer, deep dive

**Übergänge:** Moreover, Furthermore, Additionally, Notably, In conclusion, In summary, That being said, Subsequently

**Füllphrasen:** „A testament to...“, „It's important to note...“, „Let's dive in“, „In the realm of...“

## Strukturelle Anti-Patterns {#structural-anti-patterns}

### Die „KI-Form“ {#the-ai-shape}

- Jeder Absatz etwa gleich lang
- Jeder Abschnitt hat 3 bis 5 Aufzählungspunkte
- Vorhersehbares Überschriftenmuster: „Understanding X“, „The Role of Y“, „Why Z Matters“
- Jeder Absatz beginnt mit einem Übergangswort
- „In conclusion...“ als unvermeidlicher Schluss

### Burstiness (am besten messbare Metrik) {#burstiness-most-detectable-metric}

Burstiness = Variation in Satzlänge und Satzbau.

**Menschliches Schreiben:** mischt natürlicherweise kurze, prägnante Sätze mit langen, komplexen. Ein Absatz kann einen Satz mit 5 Wörtern enthalten, gefolgt von einem mit 40 Wörtern.

**KI-Schreiben:** Sätze häufen sich um eine mittlere Länge (15 bis 25 Wörter). Der Rhythmus bleibt monoton, jeder Satz läuft im gleichen Tempo.

Burstiness lässt sich berechnen: Man misst die Standardabweichung der Satzlängen. KI-Text hat eine niedrige Standardabweichung, menschlicher Text eine hohe.

### Perplexität {#perplexity}

Niedrige Perplexität bedeutet, dass jedes Wort die „statistisch sicherste Wahl“ ist.

Menschliches Schreiben weist Spitzen hoher Perplexität auf (kreative Entscheidungen, unerwartete Metaphern, ungewöhnliche Wortkombinationen), die mit Abschnitten niedriger Perplexität wechseln. KI-Text ist durchgehend von niedriger Perplexität: technisch korrekt, aber langweilig.

### Die Kernsignatur {#the-core-signature}

„Glänzende Oberfläche, nichts darunter“ (Northeastern/Khoury-Forschung):
- Liest sich flüssig, sagt aber nichts Konkretes
- Weitschweifig, dabei informationsarm
- Allgemeine Rahmenmodelle statt konkreter Beispiele
- Ließe sich auf jedes ähnliche Thema anwenden

## Anti-Patterns im Ton {#tone-anti-patterns}

- **Übertriebene Begeisterung:** „Fascinating!“, „Remarkable!“. Jedes Thema wird gleich aufregend dargestellt.
- **Starkes Relativieren:** „It's worth noting that...“, „One could argue that...“. Es wird nie eine eindeutige Position bezogen.
- **Übertriebene Ausgewogenheit:** „On the one hand... on the other hand...“, auch wenn eine Seite klar richtig ist.
- **Fehlende Marker:** keine persönlichen Meinungen, keine natürlich ausgedrückte Unsicherheit, kein Humor, keine Selbstkorrektur

## Russischspezifische Marker {#russian-specific-markers}

### Wortmarker {#word-markers}

**Überstrapazierte Kopulaverben:**
- „является“ (ist): Menschen verwenden das im informellen und halbformellen Schreiben selten.
- „выступает“ / „служит“ (dient als, fungiert als)
- „играет важную роль“ (spielt eine wichtige Rolle)

**Beliebte Konstruktionen:**
- „не просто..., а...“ (nicht nur ..., sondern ...): die typische Formulierung von ChatGPT im Russischen
- „мощный“ (leistungsstark, mächtig): überstrapaziertes Adjektiv
- Überall Deverbalsubstantive: привлечение, обеспечение, тестирование

**Englische Lehnkonstruktionen:** Wortstellung, die für das Russische unnatürlich ist und aus der englischen Syntax übernommen wurde. Das Russische erlaubt eine deutlich freiere SVO-Stellung, zu starre Wortstellung wirkt verdächtig.

### Strukturelle Merkmale {#structural-signs}

- Jeder Absatz beginnt mit einem Deverbalsubstantiv und einem Doppelpunkt.
- Überall Subjekt-Prädikat-Reihenfolge (das Russische hat eine freiere Wortstellung).
- Absätze lassen sich umordnen, ohne dass etwas verloren geht: keine logische Kette.
- Perfekte Zeichensetzung, keinerlei grammatische Unregelmäßigkeiten

### Indikatorphrasen {#indicator-phrases}

- „Я надеюсь, это помогло Вам“ (Ich hoffe, das hat Ihnen geholfen)
- „Конечно“ / „Безусловно“ in der Eröffnungsposition (Natürlich / Zweifellos)
- „Вы абсолютно правы“ (Sie haben völlig recht)
- „По состоянию на [дата]“ (Stand: [Datum])

## Wie menschliches Schreiben tatsächlich aussieht {#what-human-writing-actually-looks-like}

- **Ungleichmäßige Absatzlängen** (manche aus einem Satz, manche aus zehn)
- **Klare Meinungen**, ohne Relativierung formuliert
- **Konkrete Beispiele** mit Namen, Daten, Zahlen, nicht „consider a scenario where...“
- **Selbstkorrektur** („Eigentlich stimmt das so nicht ganz...“)
- **Registerwechsel** (formell zu informell und zurück)
- **Abschweifungen**, die die These nicht perfekt stützen
- **Fehler und Korrekturen**, die den Denkprozess zeigen

## Checkliste zur Überarbeitung {#editing-checklist}

Vor der Veröffentlichung:
- [ ] Keine Wörter der Stufe 1 (delve, crucial, comprehensive usw.)
- [ ] Satzlängen variieren deutlich (kürzesten mit längstem Satz vergleichen)
- [ ] Mindestens eine persönliche Meinung pro 500 Wörter
- [ ] Keine symmetrische Absatzstruktur
- [ ] Konkrete Beispiele mit Namen, Zahlen, Daten
- [ ] Mindestens ein Eingeständnis von Unsicherheit oder Grenzen
- [ ] Nicht mehr als 2 Übergangswörter pro Seite (Moreover, Furthermore)
- [ ] Mindestens eine Stelle, an der du widersprichst oder Stellung beziehst
- [ ] Keine generischen Schlussfolgerungen („In conclusion, X is important for Y“)

**Speziell für technische Artikel:**
1. Beginne mit dem Problem, das du tatsächlich hattest, nicht mit einer Themenübersicht.
2. Zeige Sackgassen: „Ich habe X versucht, aber es ist fehlgeschlagen, weil...“
3. Zeige konkrete Fehlermeldungen, Stack Traces und Versionsnummern.
4. Nutze deine eigenen Messwerte: „hat 47 Minuten auf meinem M1 MacBook gedauert“
5. Widersprich etwas: beziehe Stellung.
6. Nenne Zeitpunkte: „Um 2 Uhr nachts wurde mir klar...“

## Der grundlegende Unterschied {#fundamental-difference}

**Spezifität vs. Allgemeinheit.**

Menschlicher Text ist spezifisch: Er bezieht sich auf konkrete Dinge, bezieht Position, macht Fehler und zeigt Persönlichkeit.  
KI-Text ist allgemein: Er deckt alle Bereiche ab, relativiert alles, verwendet die gängigsten Formulierungen und erzeugt Text, der auf jedes ähnliche Thema passen könnte.

Die Achse Spezifisch/Allgemein ist die verlässlichste einzelne Dimension zur Erkennung.

## Stolpersteine {#gotchas}

- **KI-Muster ändern sich nach öffentlicher Bekanntheit.** „Delve“ ging stark zurück, nachdem es breit kritisiert worden war. LLMs und Menschen entwickeln sich gemeinsam weiter, die konkrete Wortliste wird sich daher ändern. Die strukturellen Muster und die Burstiness sind stabiler.
- **Blogbeiträge mit „500 KI-Wörtern, die du vermeiden solltest“ folgen oft denselben Mustern.** Die meisten dieser Listen sind selbst KI-generierte Inhalte über KI-generierte Inhalte. Die akademischen Quellen (Liang et al., Northeastern) sind verlässlicher.
- **Die KI-Erkennung im Russischen unterscheidet sich von der im Englischen.** Das Signal des Kopulaverbs („является“) ist im Russischen deutlich stärker als „is“ im Englischen, weil das Russische selten eine Kopula braucht. Die englisch geprägte Wortstellung ist ein eigenständiges russisches KI-Signal ohne direktes englisches Gegenstück.

## Siehe auch {#see-also}

- [[natural-writing-style]]
- [[overused-words-phrases]]
- [[ai-text-detection]]
- [[structural-antipatterns]]
