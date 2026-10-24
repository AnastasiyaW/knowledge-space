---
title: "Fondamentaux de Tableau"
category: tools
tags: [bi-analytics, tableau, data-connections, joins, extract, live]
level: 2
source_sha256: f0a9ff5b7f752567232ea76791e33cff33cdb90652b53ac8539073d9c853f83f
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de Tableau {#tableau-fundamentals}

Tableau est une plateforme BI d'entreprise (Desktop + Server/Cloud) dotée du moteur de visualisation le plus puissant du marché de la BI. Cette entrée couvre les connexions aux données, les types de jointures, l'ordre d'application des filtres et les concepts d'architecture fondamentaux.

## Points clés {#key-facts}

- Tableau se connecte via : Tableau Server (sources publiées), fichiers (Excel/CSV/JSON/PDF), serveur/base de données (plus de 200 connecteurs natifs), stockage cloud
- Deux modes de connexion : Live (requêtes en temps réel) et Extract (fichier instantané `.hyper`)
- Indicateur visuel : Live = une icône de baril, Extract = deux barils
- SQL personnalisé disponible, mais Tableau N'optimise PAS celui-ci avant de l'envoyer à la base de données
- ClickHouse n'est pas pris en charge nativement : un pilote ODBC ou JDBC est nécessaire
- Écosystème : Tableau Prep (ETL visuel), Tableau Catalog (gouvernance des données), module complémentaire Data Management

## Modèles {#patterns}

### Live vs Extract {#live-vs-extract}

**Mode Live** : chaque action sur une feuille envoie une requête à la base de données. Les données sont toujours à jour, et les performances dépendent de la vitesse de la base.

**Mode Extract** : instantané des données enregistré dans un fichier `.hyper` à forte compression. Stocké dans le dossier `Datasources`.

Paramètres d'extraction :
- Mode de table logique ou physique
- Filtres (par exemple par ville ou par zone géographique)
- Agrégation au niveau de l'extraction (optimise la vitesse et la taille)
- Limite de lignes
- **Actualisation incrémentielle** : n'actualise que les nouvelles données
- **Masquer tous les champs inutilisés** : supprime les champs inutilisés pour optimiser

**Règle** : Extract > Live dans presque tous les cas (les données matérialisées sont plus rapides).

### SQL personnalisé vs éditeur visuel {#custom-sql-vs-visual-editor}

Avantages du SQL personnalisé : création rapide de sources ad hoc ; possibilité d'intégrer des paramètres.

Inconvénients du SQL personnalisé :
- Pas de coloration syntaxique dans l'éditeur
- Transformation invisible pour les autres membres de l'équipe
- Tableau N'optimise PAS le SQL personnalisé avant de l'envoyer à la base de données
- Éviter GROUP BY et ORDER BY dans le SQL personnalisé

**Règle** : pour les opérations simples, utiliser l'éditeur visuel. Ne recourir au SQL personnalisé que lorsque la flexibilité est réellement nécessaire.

### Méthodes de combinaison de tables {#table-combining-methods}

**Jointure** : jointure relationnelle standard. Crée automatiquement une jointure sur les champs de même nom. Types : interne, gauche, droite, externe complète.
- Jointure logique : Tableau joint d'abord, puis crée l'Extract (données fusionnées, puis instantané)
- Jointure physique : un Extract par table, puis jointure à l'exécution de la requête

**Union** : empile des tables de schéma identique. Prend en charge l'union automatique selon un motif de nom de feuille ou de table.

**Relations** (Tableau 2020+) : analyse de données réparties sur des tables de granularités différentes. Les relations joignent et agrègent les données pendant l'analyse, au niveau de détail requis. Elles résolvent la duplication de données sans calculs LOD.

Pour un décalage de granularité temporelle (commandes par jour, plan par mois) :
```sql
DATE(DATETRUNC("month", [Order Date]))
```

**Blending** : mélange des données provenant de sources différentes par feuille de calcul. Source principale = premier champ glissé ; source secondaire = marquée d'une couleur différente.

Quand préférer le Blending aux Relations :
1. Besoin de flexibilité par feuille (Blending = par feuille, Relations = par source de données)
2. Deux sources indépendantes, sans calculs croisés, mais avec un seul filtre qui doit contrôler les deux

**Data Blending = problème de performance** : génère plusieurs requêtes ; à éviter lorsque c'est possible.

### Ordre d'application des filtres {#filter-order-of-operations}

Les filtres s'appliquent dans cet ordre (critique pour les calculs LOD) :

1. Filtres d'extraction
2. Filtres de source de données
3. Filtres de contexte
4. Filtres de dimension (inclut : ensembles, conditionnels, Top N, **FIXED LOD**)
5. Filtres de mesure (inclut : **INCLUDE/EXCLUDE LOD**, Data Blending)
6. Filtres de calcul de tableau (inclut : prévisions, calculs de tableau, clusters, totaux)

### Sécurité au niveau des lignes et des colonnes {#rowcolumn-security}

**Sécurité au niveau des lignes (RLS)** : afficher des lignes différentes selon les utilisateurs.
- Intégrée : onglet Server -> créer des filtres utilisateur, affecter les utilisateurs à des régions
- Évolutive : table d'accès (paires utilisateur + région), jointure physique avec la table de faits, filtre où `regional_manager = USERNAME()`

**Sécurité au niveau des colonnes** : afficher des dimensions différentes selon les groupes d'utilisateurs.

**Important** : la RLS nécessite une jointure physique (et non logique) pour éviter une explosion des données.

## Pièges {#gotchas}

- Les Relations sont préférables au Blending pour les données de granularités différentes (ou pré-jointure dans le DWH)
- FIXED LOD s'évalue au niveau des filtres de contexte (étape 4), INCLUDE/EXCLUDE au niveau des filtres de dimension (étape 5) : cette distinction influe sur le comportement des tableaux de bord
- Le SQL personnalisé dans les connexions LIVE pose particulièrement problème pour les performances
- Chaque feuille de calcul génère une requête vers la source : plus de feuilles = plus de requêtes
- Une Published Extract perd son cache lorsqu'elle est utilisée avec des filtres pertinents ; une Embedded Extract conserve mieux son cache

## Voir aussi {#see-also}

- [[tableau-calculations]] - champs calculés et calculs de tableau
- [[tableau-lod-expressions]] - détail de FIXED/INCLUDE/EXCLUDE
- [[tableau-performance-optimization]] - optimisation des performances
- [[bi-tools-comparison]] - Tableau vs Power BI vs alternatives
