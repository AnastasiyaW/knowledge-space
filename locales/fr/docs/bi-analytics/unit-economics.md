---
title: "Économie unitaire"
category: concepts
tags: [bi-analytics, unit-economics, ltv, cpa, arpu, business-metrics]
level: 3
source_sha256: 7a1b2fa1a2306b3f97e0069316b5970a7ca0a8a43d7cb7b6286de403aaf4df85
translation: machine
translated_at: '2026-10-24'
---
# Économie unitaire {#unit-economics}

L'économie unitaire est une méthode de modélisation économique permettant de déterminer la rentabilité d'une activité en évaluant la rentabilité par unité de produit ou par client. Elle s'applique lors du lancement de startups, de la planification d'une croissance, de la présentation à des investisseurs, ou lorsque l'acquisition d'utilisateurs et la publicité constituent les principaux postes de coûts.

## Points clés {#key-facts}

- Formule de base : `Profit = Revenu - Coûts variables - Coûts fixes`
- L'activité est viable lorsque la marge brute > coûts fixes
- **La marge brute est reine** - la métrique principale de l'économie unitaire
- Un coût par lead plus élevé ne signifie pas une économie moins bonne : la qualité des leads (taux de conversion en transaction) compte davantage que leur quantité
- La marge sur coûts variables (revenu moins coûts variables par unité) doit être positive avant toute mise à l'échelle

## Formules principales {#core-formulas}

```yaml
Profit (Margin) = Gross Profit - Fixed Costs
Gross Profit = Revenue - Variable Costs

Main Unit Economics Formula:
User Acquisition x (ARPU - CPA) = Gross Profit

Where:
ARPU = C1 x APC x AvP x Margin

Expanded:
User Acquisition x (C1 x APC x AvP x Margin - CPA) = Gross Profit

Payback Period = CPA / (Monthly ARPU x Margin)
```

## Modèles {#patterns}

### Métriques clés {#key-metrics}

| Métrique | Définition |
|--------|-----------|
| **CPA/CAC** | Coût par acquisition / Coût d'acquisition client |
| **ARPU** | Revenu moyen par utilisateur |
| **GMV** | Gross Merchandise Value - volume total avant dépenses |
| **LTV** | Lifetime Value - revenu total généré par un client sur sa durée de vie |
| **ROMI** | Retour sur investissement marketing |
| **C1** | Conversion vers le premier achat (% d'utilisateurs) |
| **APC** | Average Payment Count (nombre moyen d'achats répétés) |
| **AvP** | Prix moyen par transaction (Average Price) |
| **COGS** | Cost of Goods Sold - coût direct par transaction |
| **ROAS** | Return On Ad Spend = Revenu / Dépenses publicitaires |
| **ROI** | Retour sur investissement = (Revenu - Coût) / Coût |

### Métriques de coût marketing {#marketing-cost-metrics}

| Métrique | Formule |
|--------|---------|
| **CPI** | Coût par installation = Dépenses publicitaires / Installations |
| **CPC** | Coût par clic = Dépenses publicitaires / Clics |
| **CPM** | Coût pour mille = Coût pour 1 000 impressions |
| **CTR** | Taux de clics = Clics / Impressions |
| **CVR** | Taux de conversion = Actions / Clics |

### Leviers de croissance (théorie des contraintes de Goldratt) {#growth-levers-goldratt-theory-of-constraints}

1. Identifier le paramètre dont la variation apporte la plus forte contribution à la marge brute
2. Subordonner le produit à ce paramètre (se concentrer sur lui)
3. L'étendre/le mettre à l'échelle

Décisions possibles selon les métriques :
- Attirer davantage d'utilisateurs (augmenter l'acquisition d'utilisateurs)
- Réduire le coût d'acquisition (réduire le CPA)
- Augmenter la conversion en achat (augmenter la C1)
- Augmenter le panier moyen (augmenter l'AvP)
- Augmenter le nombre d'achats répétés (augmenter l'APC)
- Augmenter le GMV

### Segmentation RFM (exemple DAX) {#rfm-segmentation-dax-example}

RFM = Recency, Frequency, Monetary - modèle de segmentation client :

```dax
Recency = DATEDIFF(MAX(Orders[OrderDate]), TODAY(), DAY)
Frequency = COUNT(Orders[OrderID])
Monetary = SUM(Orders[Revenue])
```

Classer les clients de 1 à 5 sur chaque dimension, puis combiner les résultats en un score RFM pour le ciblage.

## Pièges à éviter {#gotchas}

- Un canal d'acquisition bon marché attirant des utilisateurs de faible qualité est pire qu'un canal coûteux attirant des utilisateurs à forte LTV : analysez toujours le comportement des cohortes par source d'acquisition
- Un ARPU moyen calculé sur l'ensemble des utilisateurs peut masquer des distributions bimodales (gros dépensiers contre utilisateurs gratuits)
- La période de retour sur investissement (payback) est critique pour les modèles par abonnement : si le payback dépasse la durée de vie moyenne d'un utilisateur, le modèle ne fonctionne pas
- Une économie unitaire calculée au lancement peut ne pas tenir à grande échelle, en raison de la saturation du marché et de la hausse des coûts d'acquisition

## Voir aussi {#see-also}

- [[product-metrics-framework]] - DAU/MAU et métriques d'engagement
- [[cohort-retention-analysis]] - analyse de la LTV par cohortes
- [[mobile-attribution-fraud]] - attribution et mesure du ROAS
- [[web-marketing-analytics]] - analyse des sources de trafic et du ROI
