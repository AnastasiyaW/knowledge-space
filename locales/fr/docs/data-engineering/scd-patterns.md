---
title: "Dimensions à évolution lente (SCD)"
category: concepts
tags: [data-engineering, scd, dimensions, data-modeling, history-tracking]
level: 3
source_sha256: 95dface110853d902f79a6e646703e13815d3b1e1477529eb91656b42eff4a15
translation: machine
translated_at: '2026-10-24'
---
# Dimensions à évolution lente (SCD) {#slowly-changing-dimensions-scd}

Les patterns SCD gèrent les modifications des attributs de dimension au fil du temps. SCD2 est le plus courant dans les entrepôts de données, car il conserve l'historique complet en ajoutant de nouvelles lignes avec des dates de validité.

## Types de SCD {#scd-types}

| Type | Comportement | Historique | Cas d'usage |
|------|--------------|------------|-------------|
| **SCD0** | Ne change jamais | Aucun | Données de référence statiques |
| **SCD1** | Écrasement de l'ancienne valeur | Perdu | Corrections, attributs non historisés |
| **SCD2** | Ajout d'une nouvelle ligne avec dates | Complet | La plupart des changements de dimension |
| **SCD3** | Ajout d'une colonne pour la valeur précédente | Limité (1 antérieure) | Rarement utilisé |
| **SCD6** | Hybride (1 + 2 + 3) | Complet + indicateur courant | Accès rapide à la valeur courante |

## Pattern SCD2 {#scd2-pattern}

```sql
-- SCD2 table structure
customer_id | name    | city      | valid_from | valid_to   | is_current
1           | Alice   | New York  | 2023-01-01 | 2023-06-15 | false
1           | Alice   | Boston    | 2023-06-15 | 9999-12-31 | true
```

### Logique de fusion SCD2 {#scd2-merge-logic}

```sql
-- Step 1: Close existing records
UPDATE dim_customer
SET valid_to = CURRENT_DATE, is_current = false
WHERE customer_bk = 'C001' AND is_current = true
  AND (name != 'New Name' OR city != 'New City');

-- Step 2: Insert new version
INSERT INTO dim_customer (customer_bk, name, city, valid_from, valid_to, is_current)
SELECT 'C001', 'New Name', 'New City', CURRENT_DATE, '9999-12-31', true
WHERE EXISTS (
    SELECT 1 FROM staging WHERE customer_bk = 'C001'
      AND (name != 'New Name' OR city != 'New City')
);
```

### Requête à un instant donné {#point-in-time-query}

```sql
-- What was the customer's city on 2023-03-15?
SELECT * FROM dim_customer
WHERE customer_bk = 'C001'
  AND '2023-03-15' BETWEEN valid_from AND valid_to;
```

## Points de vigilance {#gotchas}
- Les jointures SCD2 entre satellites ayant des fréquences de changement différentes produisent une explosion cartésienne sur les plages de dates qui se chevauchent
- La convention `valid_to = '9999-12-31'` marque les enregistrements courants : filtrer systématiquement sur `is_current = true` pour obtenir l'état le plus récent
- Les clés de hachage dans les SCD2 de Data Vault doivent être calculées de manière cohérente dans tous les processus ETL
- Les tables SCD2 croissent en continu : prévoir le stockage et les performances des requêtes

## Voir aussi {#see-also}
- [[data-vault]] - SCD2 dans les tables satellites
- [[dimensional-modeling]] - patterns de conception des dimensions
- [[data-modeling]] - contexte de normalisation
