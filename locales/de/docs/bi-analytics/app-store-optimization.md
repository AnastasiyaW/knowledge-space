---
title: "App Store Optimization (ASO)"
category: concepts
tags: [bi-analytics, aso, app-store, google-play, apple, keywords, ratings, mobile]
level: 4
source_sha256: a3ca02a818f1736e208f9c0ea81b5c946de629569cb6a9b4b1177160c7702e32
translation: machine
translated_at: '2026-10-24'
---
# App Store Optimization (ASO) {#app-store-optimization-aso}

ASO ist die organische Suchmaschinenoptimierung für App Stores. Ziel ist es, für relevante Keywords ohne bezahlte Anzeigen in den Top-Ergebnissen zu erscheinen. Sie umfasst Keyword-Optimierung, Conversion-Rate-Optimierung, Bewertungsmanagement und Wettbewerbsanalyse in Google Play und im Apple App Store.

## Kernfakten {#key-facts}

- ASO = organische Suchmaschinenoptimierung für App Stores
- Richtwert Conversion-Rate (Impressionen -> Installationen): 25-35 % für gut optimierte Apps
- Der App-Titel hat in beiden Stores das höchste Keyword-Gewicht
- Eine Auswahl als Featured-App durch Apple/Google vervielfacht die Installationen um das 10- bis 100-Fache
- A/B-Tests verfügbar: Google Play Store Listing Experiments, Apple Product Page Optimization
- Apps mit einer Bewertung unter 4,0 haben eine deutlich niedrigere Conversion

## Muster {#patterns}

### Ranking-Faktoren {#ranking-factors}

**Keyword-Faktoren:**
- **App-Titel** (höchstes Gewicht): primäres Keyword aufnehmen
- **Untertitel** (iOS) / **Kurzbeschreibung** (Android): sekundäre Keywords
- **Keyword-Feld** (nur iOS, 100 Zeichen, durch Kommas getrennt, für Nutzer nicht sichtbar)
- **Beschreibung** (Android): Die ersten 167 Zeichen sind ohne "Mehr" sichtbar

**Leistungsfaktoren:**
- Installationsvolumen (mehr Installationen = besseres Ranking)
- Conversion-Rate (Impressionen -> Installationen)
- Bewertungen und Rezensionen (Durchschnitt + Anzahl)
- Deinstallationsrate (negatives Signal)
- Engagement (Sitzungen pro Nutzer, Retention)

### Keyword-Recherche-Prozess {#keyword-research-process}

1. Ausgangs-Keywords sammeln (Produktfunktionen, Anwendungsfälle, Synonyme)
2. Die Top-Keywords der Wettbewerber mit ASO-Tools analysieren
3. Suchvolumen und Schwierigkeit für jedes Keyword prüfen
4. Priorisieren: hohes Volumen + geringe Schwierigkeit = beste Chance
5. Long-Tail-Keywords: leichter zu ranken, aber geringeres Volumen

**ASO-Tools:** AppFollow, AppTweak, Sensor Tower, MobileAction, AppMagic.

### Conversion-Rate-Optimierung {#conversion-rate-optimization}

Elemente, die die Installations-Conversion beeinflussen (nach Wirkung sortiert):
1. **Icon**: erster visueller Eindruck, muss in kleiner Größe erkennbar sein
2. **Screenshots**: die ersten 2-3 sind ohne Scrollen sichtbar (wichtigstes visuelles Element)
3. **Vorschauvideo**: wird unter iOS automatisch abgespielt, Kernnutzen in den ersten 3 Sekunden zeigen
4. **App-Name + Untertitel**: vermitteln das Nutzenversprechen sofort
5. **Bewertungen**: Apps unter 4,0 haben eine deutlich niedrigere Conversion
6. **Rezensionen**: aktuelle positive Rezensionen zählen mehr als alte

A/B-Tests:
- **Google Play**: Store Listing Experiments (3 Varianten testen, automatische Auswahl des Gewinners)
- **App Store**: Product Page Optimization (Screenshots/Icon testen)

### Google Play vs. Apple App Store {#google-play-vs-apple-app-store}

| Merkmal | Google Play | Apple App Store |
|---------|------------|----------------|
| Prüfprozess | Automatisch + manuell bei neuen Apps | Manuell bei jedem Update (1-3 Tage) |
| Installationsanzahl | Öffentlich angezeigt (ungefähr) | Nicht öffentlich |
| Bewertungen | Bleiben über Versionen erhalten | Können pro Hauptversion zurückgesetzt werden |
| A/B-Tests | Store Listing Experiments | Product Page Optimization |
| Entwickler-Analytics | Google Play Console | App Store Connect |
| Featured | Redaktionelle Ansprache qualitativ hochwertiger Apps | Einreichung über App Store Promotions |

### Strategie für Bewertungen und Rezensionen {#ratings-reviews-strategy}

**Wann nach einer Bewertung fragen:**
- Nach positiven Momenten (Level abgeschlossen, Aufgabe erfolgreich erledigt)
- Niemals beim Start oder nach einem negativen Erlebnis
- iOS: Bewertungen können nur bei einer neuen Hauptversion zurückgesetzt werden
- Android: Bewertungen bleiben über Updates hinweg erhalten

**Analyse der Rezensionen:**
- Kategorisieren: Fehler, fehlende Funktionen, UX-Probleme, Lob
- Stimmung über die Zeit verfolgen (besonders nach Updates)
- Erwähnte Funktionen der Produkt-Roadmap zuordnen
- Häufung negativer Rezensionen nach einem Update = Hinweis auf Rollback oder Hotfix
- Auf negative Rezensionen zügig reagieren (zeigt, dass die App gepflegt wird)

### Featured werden {#getting-featured}

Faktoren, die helfen:
- Integration in Plattformfunktionen (iOS: Widgets, Siri-Kurzbefehle, App Clips; Android: Google Assistant, Instant Apps)
- Technische Qualität (keine Abstürze, schnelles Laden, Richtlinienkonformität)
- Timing (Anfrage mindestens 6 Wochen vor dem gewünschten Featured-Termin einreichen)
- Plattformkonformes Design

### Wettbewerbsanalyse {#competitor-analysis}

Wettbewerber analysieren auf:
- Keywords, für die sie ranken und du nicht
- Bewertungstrends (sinkend = deine Chance)
- Update-Frequenz
- Darstellungsmuster der Screenshots
- Nutzerbeschwerden in Rezensionen = Produktlücken

### Analytics-Tools {#analytics-tools}

**Kostenlos (integriert):**
- App Store Connect (Apple): Impressionen, Seitenaufrufe, Installationen, Abstürze, Umsatz, Retention
- Google Play Console: Store-Listing-Statistiken, Bewertungen, Abstürze, ANRs, Umsatz

**Kostenpflichtige Drittanbieter:**
- Sensor Tower: Marktintelligenz, Wettbewerbsanalyse, Download-Schätzungen
- AppTweak: ASO-Optimierung, Keyword-Tracking
- AppFollow: Bewertungsmanagement, Stimmungsanalyse
- AppMagic: Umsatzschätzungen, Marktgrößen

## Fallstricke {#gotchas}

- ASO ist ein kontinuierlicher Prozess und keine einmalige Optimierung, da sich Wettbewerber ständig verändern
- Keyword-Stuffing in Titel/Beschreibung kann zur Ablehnung im Store-Review führen
- Verschiedene Regionen benötigen unter Umständen unterschiedliche Keyword-Strategien: ASO lokalisieren
- Der Kategorie-Rang treibt die organische Entdeckung, lässt sich aber schwerer direkt beeinflussen als das Suchranking
- Die Rankings der Top Charts (Kostenlos, Bezahlt, Umsatzstärkste) basieren jeweils auf unterschiedlichen Metriken

## Siehe auch {#see-also}

- [[funnel-analysis]] - Installations-Conversion-Funnel
- [[mobile-analytics-platforms]] - Analytics nach der Installation
- [[mobile-attribution-fraud]] - Attribution vom Store bis zur In-App-Aktion
- [[product-metrics-framework]] - Engagement-Metriken, die ASO beeinflussen
