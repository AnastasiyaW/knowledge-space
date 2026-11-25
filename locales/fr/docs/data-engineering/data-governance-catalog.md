---
title: "Gouvernance des données et catalogue"
category: concepts
tags: [data-engineering, data-governance, data-catalog, dama, metadata]
level: 2
source_sha256: 6cbfd32be0a4febc5219c05726ac95fbde49ae845169915c06de222771ac266b
translation: machine
translated_at: '2026-10-24'
---
# Gouvernance des données et catalogue {#data-governance-and-catalog}

La gouvernance des données est le cadre de rôles, de politiques, de standards et de métriques qui garantit une gestion efficace des données. Un catalogue de données est un inventaire organisé des actifs de données permettant aux utilisateurs de les trouver, de les comprendre et de leur faire confiance.

## Gestion des données vs gouvernance {#data-management-vs-governance}

- **Gestion des données :** processus opérationnels (comment gérer les rôles, suivre la conformité, maintenir les standards)
- **Gouvernance des données :** cadre répondant à la question « qui décide quoi » concernant les données

## Domaines du DAMA DMBOK {#dama-dmbok-disciplines}

| Domaine | Description |
|-----------|-------------|
| Gouvernance des données | Rôles, politiques, standards, métriques |
| Architecture des données | Structure logique/physique des actifs de données |
| Modélisation des données | Diagrammes ER, DDL, modèles dbt |
| Stockage des données | Sauvegardes, sécurité, déploiement |
| Sécurité des données | Protection des PII/PHI, chiffrement, RGPD |
| Intégration des données | Processus ETL/ELT |
| Données de référence et données maîtres | Définitions standardisées, dédoublonnage |
| Entrepôt de données et BI | Traitement analytique, reporting |
| Gestion des métadonnées | Collecte et catégorisation des métadonnées |
| Qualité des données | Surveillance, définition de l'intégrité |

## Catalogue de données {#data-catalog}

Inventaire consultable comprenant :
- Nom et description du jeu de données
- Emplacement (base de données, schéma, table)
- Propriétaire / intendant (steward)
- Fréquence de mise à jour, schéma, descriptions des colonnes
- Tags, classifications, statistiques d'utilisation

### Outils {#tools}

| Outil | Type |
|------|------|
| **Apache Atlas** | Gestion de métadonnées open source |
| **DataHub** (LinkedIn) | Plateforme de métadonnées open source |
| **Amundsen** (Lyft) | Découverte de données open source |
| **Alation, Collibra** | Catalogues commerciaux |

## Rôles de gouvernance {#governance-roles}
- **Propriétaire des données (Data Owner) :** responsabilité métier pour un domaine de données
- **Intendant des données (Data Steward) :** gestion quotidienne de la qualité et des métadonnées
- **Gardien des données (Data Custodian) :** mise en œuvre technique des politiques

## RGPD et conformité {#gdpr-and-compliance}

Exigences clés :
- Droit d'accès, de rectification et d'effacement
- Minimisation des données, limitation des finalités
- Protection des données dès la conception et par défaut
- Notification de violation dans les 72 heures

### Mise en œuvre {#implementation}
- Classification et étiquetage des données (marqueurs PII, PHI)
- Chiffrement au repos et en transit
- Contrôle d'accès et journalisation d'audit
- Anonymisation / pseudonymisation
- Politiques de conservation et suppression automatisée

## Référentiels {#frameworks}
- **TOGAF** - cadre d'architecture d'entreprise
- **Zachman** - matrice d'architecture
- **DAMA DMBOK2** - corpus de connaissances en gestion des données

## Pièges à éviter {#gotchas}
- Un Data Lake sans gouvernance devient un « data swamp » (marécage de données)
- Le hachage n'est PAS un chiffrement : le hachage est irréversible, le chiffrement est réversible
- La classification doit être automatisée : l'étiquetage manuel ne passe pas à l'échelle
- Une gouvernance sans application est de la documentation, pas de la gouvernance

## Voir aussi {#see-also}
- [[data-quality]] - dimensions de qualité et surveillance
- [[data-lineage-metadata]] - lignage et provenance
- [[data-lake-lakehouse]] - gouvernance dans le contexte d'un lake
