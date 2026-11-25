---
title: "Kausale Inferenz"
category: techniques
tags: [data-science, statistics, causality, quasi-experiments, observational]
level: 2
source_sha256: 87d6b3471645eb3bd5dc40fa6f00eb9cfc1755f1cf344287ceed2d6c5611821f
translation: machine
translated_at: '2026-10-24'
---
# Kausale Inferenz {#causal-inference}

Bestimmung von Ursache und Wirkung aus Daten. Korrelation impliziert keine Kausalität – mit den richtigen Methoden können wir jedoch auch ohne randomisierte Experimente kausalen Aussagen näherkommen.

## Methodenhierarchie (nach Stärke) {#methods-hierarchy-by-strength}

1. **Randomisierte A/B-Tests** – Goldstandard
2. **Quasi-Experimente** – natürliche Gruppenzuordnung
3. **Kontrafaktische Analyse** – keine Kontrollgruppe

## DAGs (Directed Acyclic Graphs) {#dags-directed-acyclic-graphs}

Visualisierung kausaler Zusammenhänge. Identifikation von Confoundern, Mediatoren und Colliders.

- **Confounder**: beeinflusst sowohl Behandlung als auch Ergebnis (muss kontrolliert werden)
- **Mediator**: liegt auf dem kausalen Pfad zwischen Behandlung und Ergebnis
- **Collider**: wird sowohl durch Behandlung als auch durch Ergebnis verursacht (darf nicht kontrolliert werden)

Beispiel: Schul-Notendurchschnitt -> Universitätszulassung, wobei Motivation, Einkommen und Schulqualität miteinander zusammenhängen.

## Difference-in-Differences (DiD) {#difference-in-differences-did}

Vergleich von Behandlungs- und Kontrollgruppe vor und nach der Intervention.

**Effekt = (Behandlung_nach - Behandlung_vor) - (Kontrolle_nach - Kontrolle_vor)**

**Voraussetzung**: Annahme paralleler Trends – die Gruppen hätten ohne Intervention denselben Trend aufgewiesen.

## Propensity Score Matching (PSM) {#propensity-score-matching-psm}

Wenn Gruppen nicht zufällig zugeordnet wurden:
1. Wahrscheinlichkeit für den Erhalt der Behandlung je Einheit schätzen (Propensity Score)
2. Behandlungseinheiten mit Kontrolleinheiten ähnlichen Propensity Scores zuordnen
3. Ergebnisse zwischen den gematchten Paaren vergleichen

**Validierung**: prüfen, ob sich die Verteilungen der Kovariaten nach dem Matching angleichen.

## Synthetic Control {#synthetic-control}

Wenn Nutzer gar nicht aufgeteilt werden können:
1. Feature in der Behandlungsregion ausrollen
2. Modell erstellen, das die Metrik der Behandlungsregion anhand der Kontrollregionen vorhersagt
3. Tatsächliche mit vorhergesagter Basislinie vergleichen
4. Differenz = geschätzter Effekt

**Einschränkung**: benötigt Kontrollregionen, anfällig für außergewöhnliche Ereignisse.

## Instrumentelle Variablen (IV) {#instrumental-variables-iv}

Wenn die Zuordnung zur Behandlung konfundiert ist:
- Eine Variable (Instrument) finden, die die Behandlung beeinflusst, aber nicht direkt das Ergebnis
- Das Instrument verwenden, um die kausale Variation der Behandlung zu isolieren
- Klassisches Beispiel: Entfernung zur Hochschule als Instrument für den Effekt von Bildung auf das Einkommen

## Regression Discontinuity (RDD) {#regression-discontinuity-rdd}

Wenn die Behandlung über einen Schwellenwert zugeordnet wird (Testergebnis, Alter, Einkommensniveau):
- Einheiten knapp über und knapp unter dem Schwellenwert vergleichen
- Nahe am Cutoff sind sie effektiv zufällig zugeordnet
- Behandlungseffekt an der Unstetigkeitsstelle schätzen

## Stolperfallen {#gotchas}
- **Omitted Variable Bias**: fehlende Confounder entkräften kausale Aussagen
- Die Annahme paralleler Trends bei DiD ist nicht testbar (nur im Vorperiodenzeitraum prüfbar)
- PSM kontrolliert nur für beobachtete Confounder – verborgene Confounder bleiben bestehen
- Synthetic Control ist bei wenigen Kontrolleinheiten fragil
- Vorhersagemodelle nicht mit kausalen Modellen verwechseln – ein Feature kann gut vorhersagen, ohne kausal zu sein
- „Natürliche Experimente“ sind nur so gut wie das Argument für Exogenität

## Siehe auch {#see-also}
- [[hypothesis-testing]] – A/B-Tests als randomisiertes Experiment
- [[descriptive-statistics]] – Daten vor der kausalen Analyse verstehen
- [[bi-dashboards]] – Präsentation kausaler Analyseergebnisse
