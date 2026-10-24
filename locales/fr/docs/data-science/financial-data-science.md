---
title: "Science des données financières"
category: applications
tags: [data-science, finance, portfolio, derivatives, risk]
level: 3
source_sha256: 3ab902a1b29be785fb97b5707c0bf23cc4340966e7737c4476e545218217ca71
translation: machine
translated_at: '2026-10-24'
---
# Science des données financières {#financial-data-science}

Application des méthodes de la science des données aux marchés financiers. Couvre la théorie du portefeuille, les mesures de risque, les bases des produits dérivés et les schémas d'analyse quantitative.

## Théorie du portefeuille {#portfolio-theory}

### Indicateurs clés {#key-metrics}
- **Rendement espéré** : moyenne pondérée des rendements des actifs
- **Volatilité du portefeuille** : sqrt(w^T * Cov * w) où w = vecteur des poids
- **Ratio de Sharpe** : (rendement - taux sans risque) / volatilité
- **Bêta** : sensibilité aux mouvements du marché

### Frontière efficiente {#efficient-frontier}
Ensemble des portefeuilles maximisant le rendement pour un niveau de risque donné. Déterminée par simulation de Monte Carlo ou par programmation quadratique.

```python
# Monte Carlo portfolio optimization
port_return = weights @ daily_returns.mean() * 252
port_vol = np.sqrt(weights @ cov_matrix @ weights) * np.sqrt(252)
sharpe = port_return / port_vol
```

## Produits dérivés financiers {#financial-derivatives}

### Options {#options}
- **Call** : droit d'acheter au prix d'exercice. Gain = max(0, spot - strike)
- **Put** : droit de vendre au prix d'exercice. Gain = max(0, strike - spot)
- **Prime** : prix payé pour l'option

### Contrats à terme (forwards/futures) {#forwardsfutures}
Fixer un prix pour une livraison future. Marking-to-market : P&L quotidien basé sur la différence entre le spot et le prix du contrat.

## Mesures de risque {#risk-metrics}

### Value at Risk (VaR) {#value-at-risk-var}
Perte maximale espérée à un niveau de confiance donné sur une période donnée.

```python
# Historical VaR (95%)
var_95 = np.percentile(returns, 5)

# Parametric VaR
var_95 = returns.mean() - 1.645 * returns.std()
```

### Volatilité {#volatility}
Écart-type des rendements. LA mesure de risque fondamentale en finance.

```python
daily_vol = returns.std()
annualized_vol = daily_vol * np.sqrt(252)
```

**Règle 68-95-99,7** appliquée aux rendements : 95 % des rendements quotidiens se situent dans l'intervalle +/- 2*sigma.

## Constantes financières {#financial-constants}
- Jours de bourse par an : 252
- Jours de bourse par mois : ~20
- Jours de bourse par trimestre : ~60
- Facteur d'annualisation : sqrt(252) pour la volatilité

## Titres adossés à des actifs (ABS) {#asset-backed-securities-abs}

**Titrisation** : transformer des actifs peu liquides (hypothèques, prêts) en obligations négociables.
- **SPV** (Special Purpose Vehicle) : entité juridiquement distincte détenant le pool d'actifs
- **Tranchage** : redistribuer les flux de trésorerie en obligations présentant des profils risque/rendement différents
- **Tranche senior** : premier remboursée, risque le plus faible (notation AAA)
- **Tranche equity** : résiduel après remboursement de toutes les autres tranches, risque et rendement les plus élevés

## Ratios financiers clés {#key-financial-ratios}

| Catégorie | Indicateurs |
|----------|---------|
| Rentabilité | EBIT, EBITDA, marge nette |
| Liquidité | Ratio courant, ratio de liquidité réduite |
| Solvabilité | Dette/capitaux propres, couverture des intérêts |
| Valorisation | P/E, EV/EBITDA, P/B |
| Flux de trésorerie | FCF, flux de trésorerie d'exploitation |

**Free Cash Flow (FCF)** : indicateur le plus important de la capacité à générer de la trésorerie. Tient compte des variations du besoin en fonds de roulement et des CapEx.

## Pièges à éviter {#gotchas}
- Les rendements financiers ne suivent PAS une loi normale : queues épaisses (kurtosis > 0)
- Les performances passées ne préjugent pas des rendements futurs
- La corrélation entre actifs évolue en période de crise (la corrélation tend vers 1)
- La VaR sous-estime le risque de queue : utiliser la CVaR (expected shortfall) pour les scénarios extrêmes
- Toujours utiliser les rendements logarithmiques pour les analyses multi-périodes, les rendements simples pour une seule période

## Voir aussi {#see-also}
- [[monte-carlo-simulation]] - techniques de simulation en finance
- [[probability-distributions]] - théorie des distributions
- [[time-series-analysis]] - séries temporelles financières
- [[descriptive-statistics]] - analyse des distributions de rendements
