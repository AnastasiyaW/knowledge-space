---
title: "Qualité des données"
category: concepts
tags: [data-engineering, data-quality, validation, testing, observability]
level: 2
source_sha256: b6afc4fa06600a31e61c8b56e85fb8a5a75641337c13a26f14995e0a0d40d8cf
translation: machine
translated_at: '2026-10-24'
---
# Qualité des données {#data-quality}

La qualité des données englobe la surveillance, la définition et le maintien de l'intégrité des données. Elle est essentielle dans les grandes organisations pour éviter des décisions métier incorrectes fondées sur de mauvaises données.

## Dimensions de la qualité {#quality-dimensions}

| Dimension | Question |
|-----------|----------|
| **Complétude** | Toutes les valeurs requises sont-elles présentes ? |
| **Exactitude** | Les valeurs représentent-elles correctement les entités du monde réel ? |
| **Cohérence** | Les mêmes faits sont-ils représentés de la même manière dans tous les systèmes ? |
| **Fraîcheur** | Les données sont-elles disponibles au moment voulu ? Sont-elles suffisamment récentes ? |
| **Unicité** | Existe-t-il des enregistrements dupliqués ? |
| **Validité** | Les données respectent-elles les formats, types et plages définis ? |

## Pratiques de qualité des données {#data-quality-practices}
- Définir les règles de qualité et les seuils par jeu de données et par colonne
- Contrôles automatisés dans les pipelines (avant ET après chargement)
- Tableaux de bord de qualité et alertes en cas de non-respect des SLA
- Analyse des causes racines des problèmes de qualité
- Profilage des données pour détecter les anomalies

## Outils {#tools}

| Outil | Type |
|-------|------|
| **Great Expectations** | Validation Python open source |
| **dbt tests** | Assertions intégrées et personnalisées sur les modèles |
| **Apache Griffin** | Open source pour le big data |
| **Monte Carlo, Bigeye, Soda** | Plateformes d'observabilité commerciales |

## Observabilité des données {#data-observability}

Va au-delà de la surveillance des pipelines pour détecter :
- Les changements de schéma
- Les dérives de distribution
- Les variations du taux de valeurs nulles
- Les anomalies de volume
- Les violations de fraîcheur

## Surveillance des pipelines {#pipeline-monitoring}

| Catégorie | Métriques |
|-----------|-----------|
| **Santé des pipelines** | Taux de succès/échec des DAG, durée des tâches, nombre de tentatives |
| **Fraîcheur des données** | Temps écoulé depuis la dernière mise à jour, conformité aux SLA |
| **Volume des données** | Nombre de lignes par chargement, écart par rapport à l'attendu |
| **Infrastructure** | CPU/mémoire/disque des workers, retard du scheduler |
| **Qualité des données** | Nombre de validations échouées, tendances du taux de valeurs nulles |

## Bonnes pratiques d'alerting {#alerting-best-practices}
- Alerter sur les **dépassements de SLA**, et pas seulement sur les échecs
- Utiliser la **détection d'anomalies** pour les nombres de lignes (chute ou pic soudain)
- Définir des niveaux d'escalade (warning -> critical -> pager)
- Inclure des **liens vers les runbooks** dans les messages d'alerte
- Éviter la fatigue liée aux alertes : ajuster les seuils et regrouper les alertes liées

## Pièges courants {#gotchas}
- Un Data Lake sans gouvernance devient un « marécage de données »
- La sécurité au niveau des lignes doit être testée avec de véritables comptes utilisateurs
- Le modèle en mode pull de Prometheus exige que toutes les cibles soient accessibles depuis le réseau
- Le fichier `_SUCCESS` garantit la fin du job, pas l'exactitude des données

## Voir aussi {#see-also}
- [[data-governance-catalog]] - cadre de gouvernance
- [[data-lineage-metadata]] - remonter à l'origine des problèmes de données
- [[etl-elt-pipelines]] - où s'exécutent les contrôles de qualité
- [[apache-airflow]] - orchestration des contrôles de qualité
