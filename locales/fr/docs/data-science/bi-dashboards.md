---
title: "Systèmes BI et tableaux de bord"
category: practices
tags: [data-science, bi, dashboards, analytics, tableau, superset]
level: 3
source_sha256: d5bbdd57e9558ca11ecf63eaae8fbd6eb4062382baf3a6dbaa7a9d3d4af482e6
translation: machine
translated_at: '2026-10-24'
---
# Systèmes BI et tableaux de bord {#bi-systems-and-dashboards}

La Business Intelligence transforme les données en décisions actionnables. Un système BI est un produit - et non un projet ponctuel. Couvre la conception des tableaux de bord, le choix des outils et le pipeline d'infrastructure analytique.

## Types de tableaux de bord {#dashboard-types}

| Type | Objectif | Schéma de conception |
|------|----------|----------------------|
| Alertes/Envois | Alerte précoce | Indicateurs simples bon/mauvais |
| Vue d'ensemble/Hub | État actuel en un coup d'œil | KPI + sparkline + listes de tête |
| Page d'entité | Analyse approfondie d'une entité | Sections correspondant au cycle de vie |
| Analytique | Test d'hypothèses complexes | Grand graphique principal + contexte de soutien |
| Libre-service | Exploration pilotée par l'utilisateur | Filtres à gauche, résultats à droite |

## Métriques clés et KPI {#key-metrics-and-kpis}

### Métriques produit {#product-metrics}
- **DAU/MAU** : utilisateurs actifs quotidiens/mensuels
- **Taux de rétention** : % revenant après N jours (D1, D7, D30)
- **Taux de churn** : 1 - rétention
- **ARPU** : revenu / utilisateurs actifs
- **LTV** : revenu total prévu d'un utilisateur
- **CAC** : dépenses marketing / nouveaux clients
- **LTV/CAC > 3** pour une activité saine

### Entonnoir de conversion {#conversion-funnel}
```sql
SELECT
    COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as views,
    COUNT(DISTINCT CASE WHEN event = 'add_to_cart' THEN user_id END) as carts,
    COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as purchases
FROM events WHERE date BETWEEN '2024-01-01' AND '2024-01-31';
```

### Analyse de cohortes {#cohort-analysis}
Regrouper les utilisateurs par date d'inscription, suivre la métrique dans le temps pour chaque cohorte.

```sql
WITH cohorts AS (
    SELECT user_id,
        DATE_TRUNC('month', first_visit) as cohort_month,
        DATE_TRUNC('month', visit_date) as activity_month
    FROM user_visits
)
SELECT cohort_month, activity_month,
    COUNT(DISTINCT user_id) as active_users
FROM cohorts GROUP BY 1, 2;
```

## SQL pour l'analytique {#sql-for-analytics}

```sql
-- Running total
SELECT date, revenue,
    SUM(revenue) OVER (ORDER BY date) as running_total
FROM daily_revenue;

-- Rolling 7-day average
SELECT date, revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    as rolling_7d_avg
FROM daily_revenue;

-- Month-over-month growth
SELECT month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as prev_month,
    (revenue - LAG(revenue) OVER (ORDER BY month))
    / LAG(revenue) OVER (ORDER BY month) * 100 as growth_pct
FROM monthly_revenue;
```

## Processus de conception des tableaux de bord {#dashboard-design-process}

### Cadre Canvas {#canvas-framework}
1. **Utilisateurs et contexte** : qui, quand, comment ils l'utilisent
2. **Compréhension de la tâche** : quelles décisions ils prennent
3. **Questions** : quelles questions spécifiques le tableau de bord permet de traiter
4. **Visualisation** : quels types de graphiques correspondent à quelles questions

### Principes de maquettage (wireframe) {#wireframe-principles}
- La taille des blocs reflète l'importance de l'information
- Attirer l'attention grâce à : la position (en haut à gauche), le contraste (taille, couleur), une forme inhabituelle
- Alertes : éléments répartis uniformément avec mise en évidence des écarts
- Outils analytiques : grand graphique d'analyse + petits graphiques de tendance

## Outils BI {#bi-tools}

| Outil | Type | Force |
|-------|------|-------|
| **Tableau** | Commercial | Standard de l'industrie, glisser-déposer |
| **Apache Superset** | Open source | Basé sur SQL, graphiques riches |
| **Metabase** | Open source | Paradigme simple de « question » |
| **Redash** | Open source | Orienté SQL, pour les équipes data |
| **DataLens** | Gratuit (Yandex) | Natif ClickHouse |
| **Looker Studio** | Gratuit (Google) | Intégration BigQuery/GA |

**Différence clé** avec matplotlib/seaborn : les outils BI servent à présenter aux parties prenantes non techniques. Le tracé en Python sert à l'analyse.

## Pipeline de données pour les tableaux de bord {#data-pipeline-for-dashboards}

Source (OLTP) -> ETL/ELT -> Entrepôt de données (OLAP) -> Couche sémantique -> Outil BI -> Utilisateurs

### Architecture de l'entrepôt {#dwh-architecture}
1. **Staging** (brut) : chargement depuis les sources dans leur qualité d'origine
2. **Core** : consolidation, normalisation, règles métier
3. **Présentation** (data marts) : schémas en étoile, agrégats prêts pour le métier

## Pièges à éviter {#gotchas}
- Un tableau de bord sans KPI définis n'a pas de raison d'être - partir des objectifs métier
- La création anarchique de rapports conduit à une prolifération ingérable - systématiser le contenu
- La BI n'est PAS un projet ponctuel - la traiter comme un produit avec des itérations
- Un petit nombre d'utilisateurs dans un segment rend les statistiques peu fiables - toujours afficher N

## Voir aussi {#see-also}
- [[data-visualization]] - Tracé en Python pour l'analyse
- [[hypothesis-testing]] - Tests A/B sur les métriques des tableaux de bord
- [[ds-workflow]] - tableaux de bord dans le cycle de vie du projet
- [[select-fundamentals]] - SQL pour les requêtes analytiques
