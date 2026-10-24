---
title: "Modélisation dimensionnelle (Kimball)"
category: concepts
tags: [data-engineering, dimensional-modeling, star-schema, snowflake-schema, kimball]
level: 3
source_sha256: 58505c92a668c7c0131abfc51e5170b5de9860cce5fd682e8e630e2fe9277f65
translation: machine
translated_at: '2026-10-24'
---
# Modélisation dimensionnelle (Kimball) {#dimensional-modeling-kimball}

La modélisation dimensionnelle organise les données en tables de faits (mesures/événements) entourées de tables de dimensions (contexte descriptif). C'est l'approche standard pour les data marts et les couches analytiques optimisées pour la BI.

## Schéma en étoile {#star-schema}

```text
         dim_date
            |
dim_product--fact_sales--dim_customer
            |
         dim_store
```

- **Table de faits :** clés étrangères vers les dimensions + mesures (montant, quantité, durée)
- **Tables de dimensions :** attributs descriptifs (nom, catégorie, adresse) - dénormalisées pour la performance des requêtes

## Schéma en flocon {#snowflake-schema}

Les dimensions sont normalisées (découpées en sous-tables). Cela réduit le stockage mais nécessite davantage de JOIN. Moins courant en pratique en raison de la complexité des requêtes.

## Concepts clés {#key-concepts}

| Concept | Description |
|---------|-------------|
| **Clés de substitution** | Clés primaires entières générées par le système dans les dimensions (et non les clés métier) |
| **Dimension dégénérée** | Valeur de dimension stockée directement dans la table de faits (par exemple, le numéro de facture) |
| **Junk dimension** | Regroupe les indicateurs et drapeaux à faible cardinalité dans une seule dimension |
| **Dimension conforme** | Partagée entre plusieurs tables de faits/marts pour garantir la cohérence |

## Processus de conception {#design-process}

1. Choisir le processus métier à modéliser
2. Déclarer le grain (que représente une ligne ?)
3. Identifier les dimensions (qui, quoi, quand, où)
4. Identifier les faits (mesures - additives, semi-additives, non additives)

## Patterns {#patterns}

### DDL du schéma en étoile {#star-schema-ddl}

```sql
CREATE TABLE dim_customer (
    customer_sk SERIAL PRIMARY KEY,  -- surrogate key
    customer_bk VARCHAR(50),          -- business key
    name VARCHAR(200),
    segment VARCHAR(50),
    valid_from DATE,
    valid_to DATE DEFAULT '9999-12-31'
);

CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_sk INT REFERENCES dim_date(date_sk),
    customer_sk INT REFERENCES dim_customer(customer_sk),
    product_sk INT REFERENCES dim_product(product_sk),
    quantity INT,
    amount NUMERIC(12,2)
);
```

## Points d'attention {#gotchas}
- La dénormalisation du schéma en étoile échange du stockage contre la performance des requêtes - acceptable pour l'OLAP
- Chaque mart peut définir les métriques différemment en l'absence de dimensions conformes
- Les clés de substitution découplent le DWH des changements de clés du système source
- Toujours définir le grain en premier - un grain flou conduit à des agrégations incorrectes

## Voir aussi {#see-also}
- [[data-modeling]] - théorie de la normalisation
- [[data-vault]] - alternative pour la couche DWH cœur
- [[scd-patterns]] - gestion des changements de dimensions
- [[dwh-architecture]] - approches Kimball vs Inmon
