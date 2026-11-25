---
title: "Analyse de cohortes et rétention"
category: concepts
tags: [bi-analytics, cohort-analysis, retention, ltv, product-analytics]
level: 3
source_sha256: b807ad7c5753e884efaa57a8809c43610cdc524f4072446b903620429922d98c
translation: machine
translated_at: '2026-10-24'
---
# Analyse de cohortes et rétention {#cohort-retention-analysis}

L'analyse de cohortes regroupe les utilisateurs selon une caractéristique commune à un moment donné et suit leur comportement sur les périodes suivantes. C'est la méthode principale pour mesurer la rétention, la LTV et l'impact des évolutions produit sur différents groupes d'utilisateurs.

## Points clés {#key-facts}

- **Cohorte** = groupe d'utilisateurs ayant effectué une action dans une fenêtre temporelle définie
- **Cohorte d'acquisition** : regroupement par semaine/mois d'installation ou d'inscription
- **Cohorte comportementale** : utilisateurs ayant accompli une action spécifique
- L'analyse de cohortes compare les métriques cibles entre cohortes dans le temps, en tenant compte de la saisonnalité
- Schéma typique : regrouper par date du premier événement, suivre la métrique (rétention, revenu) à J1, J7, J14, J30
- L'analyse de cohortes par source d'acquisition révèle quels canaux produisent les utilisateurs à LTV la plus élevée

## Patterns {#patterns}

### Types de mesure de la rétention {#retention-measurement-types}

**Rétention à N jours** : pourcentage des utilisateurs de la cohorte d'installation qui reviennent exactement au jour N.

**Rétention par tranche** : pourcentage des utilisateurs qui reviennent dans une plage de jours (par exemple, jours 7 à 14).

**Rétention « return-on »** : pourcentage des utilisateurs ayant utilisé l'application au moins une fois depuis l'installation, encore actifs au jour N.

### Requête SQL de rétention par cohorte {#sql-cohort-retention-query}

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', first_order_date) as cohort_month
    FROM users
),
activities AS (
    SELECT
        c.user_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month,
        DATEDIFF('month', c.cohort_month,
            DATE_TRUNC('month', o.order_date)) as period
    FROM cohorts c
    JOIN orders o ON c.user_id = o.user_id
)
SELECT
    cohort_month,
    period,
    COUNT(DISTINCT user_id) as users
FROM activities
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Analyse de cohortes dans Tableau {#cohort-analysis-in-tableau}

Utilisez `DATEDIFF` pour calculer le nombre de jours depuis le premier événement, `DATETRUNC` pour normaliser les groupes de cohortes par semaine/mois, puis faites pivoter les données avec des calculs de table pour obtenir la grille de cohortes.

```sql
-- First event date per user (LOD)
{FIXED [User ID] : MIN([Event Date])}

-- Cohort month
DATETRUNC('month', {FIXED [User ID] : MIN([Event Date])})

-- Period number
DATEDIFF('month',
    {FIXED [User ID] : MIN([Event Date])},
    [Event Date])
```

### Analyse de cohortes dans AppsFlyer {#cohort-analysis-in-appsflyer}

- Regrouper les installations par date
- Suivre la rétention à N jours et le revenu par cohorte
- Comparer les performances entre cohortes et sources
- La rétention à J1/J7/J30 indique la qualité de l'engagement
- Le ROAS à J30 (revenu / dépenses publicitaires) indique le retour financier

### Modèles de segmentation des utilisateurs {#user-segmentation-patterns}

Créez des segments à partir de l'historique des événements et de leurs propriétés :
- « Utilisateurs ayant terminé l'onboarding mais n'ayant pas effectué d'achat dans les 7 jours »
- « Utilisateurs ayant utilisé la fonctionnalité X au cours des 30 derniers jours »
- Exportez les segments pour les notifications push ou le ciblage publicitaire

### Analyse comportementale (Amplitude Pathfinder) {#behavioral-analysis-amplitude-pathfinder}

- Affiche les parcours de navigation réels des utilisateurs dans le produit
- Que font les utilisateurs APRÈS l'événement X ?
- Que faisaient les utilisateurs AVANT l'événement Y (abandon) ?
- Repérer des schémas d'usage inattendus

## Pièges à éviter {#gotchas}

- Dans AppMetrica, le mois en cours incomplet est exclu du calcul du pourcentage de rétention : filtrez par plage de dates et additionnez les installations des seuls mois complets
- Évitez d'optimiser uniquement pour le volume d'installations : un volume d'installations bon marché est souvent corrélé à une faible LTV
- La taille des cohortes varie naturellement ; les petites cohortes produisent des courbes de rétention bruitées qu'il ne faut pas surinterpréter
- Lorsque vous comparez des cohortes dans le temps, tenez compte de la saisonnalité (les cohortes des fêtes se comportent différemment des cohortes habituelles)
- Dans certains systèmes, les métriques de rétention ne sont valides qu'à l'échelle du jour : vérifiez la granularité des données avant tout calcul

## Voir aussi {#see-also}

- [[product-metrics-framework]] - définitions DAU/MAU, stickiness et churn
- [[unit-economics]] - calculs de LTV et de délai de récupération (payback period)
- [[funnel-analysis]] - optimisation du tunnel en amont de la rétention
- [[mobile-attribution-fraud]] - qualité des cohortes selon la source d'acquisition
- [[sql-for-analytics]] - fonctions de fenêtrage pour les requêtes de cohortes
