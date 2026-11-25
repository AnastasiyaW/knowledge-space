---
title: "Finanzdatenwissenschaft"
category: applications
tags: [data-science, finance, portfolio, derivatives, risk]
level: 3
source_sha256: 3ab902a1b29be785fb97b5707c0bf23cc4340966e7737c4476e545218217ca71
translation: machine
translated_at: '2026-10-24'
---
# Finanzdatenwissenschaft {#financial-data-science}

Anwendung von Methoden der Datenwissenschaft auf Finanzmärkte. Behandelt Portfoliotheorie, Risikokennzahlen, Grundlagen von Derivaten und quantitative Analysemuster.

## Portfoliotheorie {#portfolio-theory}

### Wichtige Kennzahlen {#key-metrics}
- **Erwartete Rendite**: gewichteter Durchschnitt der Renditen der Anlagen
- **Portfolio-Volatilität**: sqrt(w^T * Cov * w), wobei w = Gewichtsvektor
- **Sharpe-Ratio**: (Rendite - risikofreier Zins) / Volatilität
- **Beta**: Sensitivität gegenüber Marktbewegungen

### Effizienzkurve {#efficient-frontier}
Menge der Portfolios, die für ein gegebenes Risikoniveau die Rendite maximieren. Wird mittels Monte-Carlo-Simulation oder quadratischer Programmierung ermittelt.

```python
# Monte Carlo portfolio optimization
port_return = weights @ daily_returns.mean() * 252
port_vol = np.sqrt(weights @ cov_matrix @ weights) * np.sqrt(252)
sharpe = port_return / port_vol
```

## Finanzderivate {#financial-derivatives}

### Optionen {#options}
- **Call**: Recht, zum Basispreis zu kaufen. Auszahlung = max(0, Kassakurs - Basispreis)
- **Put**: Recht, zum Basispreis zu verkaufen. Auszahlung = max(0, Basispreis - Kassakurs)
- **Prämie**: Preis, der für die Option gezahlt wird

### Termingeschäfte/Futures {#forwardsfutures}
Festschreibung eines Preises für eine zukünftige Lieferung. Mark-to-Market: tägliches G&V auf Basis von Kassakurs gegenüber Vertragspreis.

## Risikokennzahlen {#risk-metrics}

### Value at Risk (VaR) {#value-at-risk-var}
Maximal erwarteter Verlust bei einem Konfidenzniveau über einen Zeitraum.

```python
# Historical VaR (95%)
var_95 = np.percentile(returns, 5)

# Parametric VaR
var_95 = returns.mean() - 1.645 * returns.std()
```

### Volatilität {#volatility}
Standardabweichung der Renditen. DAS grundlegende Risikomaß in der Finanzwirtschaft.

```python
daily_vol = returns.std()
annualized_vol = daily_vol * np.sqrt(252)
```

**68-95-99,7-Regel**, angewendet auf Renditen: 95 % der täglichen Renditen liegen innerhalb von +/- 2*sigma.

## Finanzielle Konstanten {#financial-constants}
- Handelstage pro Jahr: 252
- Handelstage pro Monat: ~20
- Handelstage pro Quartal: ~60
- Annualisierungsfaktor: sqrt(252) für Volatilität

## Asset-Backed Securities (ABS) {#asset-backed-securities-abs}

**Verbriefung**: Umwandlung illiquider Vermögenswerte (Hypotheken, Kredite) in handelbare Anleihen.
- **SPV** (Special Purpose Vehicle): rechtlich eigenständige Gesellschaft, die den Forderungspool hält
- **Tranchierung**: Umverteilung der Cashflows auf Anleihen mit unterschiedlichen Risiko-/Renditeprofilen
- **Senior-Tranche**: wird zuerst bedient, geringstes Risiko (AAA-Rating)
- **Equity-Tranche**: Restbetrag nach Bedienung aller übrigen Tranchen, höchstes Risiko/höchste Rendite

## Wichtige Finanzkennzahlen {#key-financial-ratios}

| Kategorie | Kennzahlen |
|-----------|------------|
| Rentabilität | EBIT, EBITDA, Nettomarge |
| Liquidität | Current Ratio, Quick Ratio |
| Solvenz | Verschuldungsgrad, Zinsdeckungsgrad |
| Bewertung | KGV, EV/EBITDA, KBV |
| Cashflow | FCF, operativer Cashflow |

**Free Cash Flow (FCF)**: wichtigste Kennzahl für die Fähigkeit zur Cashgenerierung. Berücksichtigt Veränderungen des Working Capital und CapEx.

## Stolperfallen {#gotchas}
- Finanzrenditen sind NICHT normalverteilt – schwere Ränder (Kurtosis > 0)
- Vergangene Wertentwicklung lässt keine Prognose künftiger Renditen zu
- Die Korrelation zwischen Anlagen ändert sich in Krisen (Korrelation geht gegen 1)
- VaR unterschätzt das Risiko in den Rändern – für Extremszenarien CVaR (Expected Shortfall) verwenden
- Für Mehrperiodenanalysen immer logarithmische Renditen verwenden, für Einzelperioden einfache Renditen

## Siehe auch {#see-also}
- [[monte-carlo-simulation]] - Simulationstechniken für die Finanzwirtschaft
- [[probability-distributions]] - Verteilungstheorie
- [[time-series-analysis]] - Finanzzeitreihen
- [[descriptive-statistics]] - Analyse von Renditeverteilungen
