---
title: "Optimisation des performances de Tableau"
category: tools
tags: [bi-analytics, tableau, performance, optimization, extract, query-tuning]
level: 4
source_sha256: 4870faac50263d5520f25e022713df08b37c91f4efc7ed23bbf753634a024c12
translation: machine
translated_at: '2026-10-24'
---
# Optimisation des performances de Tableau {#tableau-performance-optimization}

L'optimisation des performances dans Tableau porte sur quatre couches : la charge serveur, la source de données, les calculs et le niveau de la vue. L'objectif est un chargement initial < 10 secondes et un changement de filtre < 6 secondes. Utilisez le Performance Recorder intégré pour identifier les goulots d'étranglement.

## Points clés {#key-facts}

- Performances cibles : chargement principal < 10 s, changement de filtre < 6 s
- Performance Recorder : Aide -> Paramètres et performances -> Démarrer l'enregistrement des performances
- Serveur : ajoutez `?:record_performance=yes` à l'URL
- Formule de qualité d'un rapport : `(Contenu informatif x Crédibilité x Engagement) / Temps de chargement`
- La charge de pointe n'est pas linéaire : un seul rapport lourd peut consommer 75 % du CPU du serveur
- Solution : optimiser les rapports individuellement, et pas seulement faire évoluer le serveur

## Modèles {#patterns}

### Événements enregistrés par le Performance Recorder {#performance-recording-events}

| Événement | Description |
|-----------|-------------|
| Compiling query | Génération du SQL selon les filtres et les calculs |
| Executing query | Envoi de la requête à la base de données ou à l'Extract |
| Computing layouts | Calcul des champs calculés au niveau des lignes |
| Blending | Opérations de mélange de données (blending) |
| Geocoding | Placement des points sur la carte |
| Table Calculations | Calcul des calculs de tableau |
| Rendering | Rendu visuel |

### Optimisations de la charge serveur {#server-load-optimizations}

- Fixer la taille des tableaux de bord fréquemment utilisés (permet la mise en cache)
- Supprimer les rapports, Extracts et actualisations planifiées inutilisés
- Réduire la taille des Extracts : masquer les champs inutilisés, puis recréer l'Extract
- Retirer les classeurs obsolètes des actualisations planifiées
- Aucun classeur ni source de données en double
- Regrouper les autorisations d'accès individuelles (réduit la charge de vérification des permissions)

### Optimisations de la source de données {#data-source-optimizations}

- **Extract plutôt que Live** dans presque tous les cas (les données matérialisées sont plus rapides)
- Éviter le Custom SQL dans les connexions LIVE
- Éviter GROUP BY et ORDER BY dans le Custom SQL
- Utiliser INNER JOIN avec l'indicateur d'intégrité référentielle activé
- Réduire le nombre de lignes : agréger si la granularité la plus fine n'est pas visualisée
- Données non additives : stocker des données préagrégées par échelle ou par tranche plutôt que des lignes brutes
- Pour les données de granularités différentes : utiliser les Relations plutôt que le Data Blending (ou pré-joindre dans l'entrepôt de données)

### Optimisations des calculs {#calculation-optimizations}

- Privilégier la hiérarchie des types (du plus rapide au plus lent) : `Boolean > Numeric > Date > String`
- Utiliser `STARTSWITH` plutôt que `CONTAINS` pour la recherche de chaînes
- Éviter les LOD dans les calculs imbriqués complexes (chacun ajoute des JOIN)
- Matérialiser les champs calculés dans l'Extract avant la publication
- Déplacer les calculs complexes vers la source de données (SQL/ETL) lorsque c'est possible

### Optimisations au niveau de la vue {#view-level-optimizations}

- Limiter le nombre de feuilles par classeur (au-delà de 6, envisager de réduire)
- Privilégier des feuilles uniques plutôt que des feuilles similaires (les doublons génèrent des requêtes redondantes)
- Chaque feuille de calcul génère une requête vers la source
- Minimiser le nombre de marques sur une même vue (des milliers de points ralentissent le rendu)

### Extract publié et Extract intégré {#published-vs-embedded-extract}

- **Extract publié** : partagé entre plusieurs classeurs, mais perd son cache lorsqu'il est utilisé avec des filtres pertinents
- **Extract intégré** : intégré au classeur, meilleure conservation du cache pour ce classeur spécifique

### Performances du Data Blending {#data-blending-performance}

Le Data Blending est intrinsèquement lent : évitez-le. Il génère plusieurs requêtes. Privilégiez :
1. Les Relations (Tableau 2020+)
2. Les JOIN préparés en amont dans l'entrepôt de données
3. Le Blending uniquement lorsque des sources réellement indépendantes nécessitent une flexibilité par feuille de calcul

## Pièges courants {#gotchas}

- La taille du tableau de bord influence la mise en cache : les tableaux de bord à taille automatique ne peuvent pas être mis en cache aussi efficacement que ceux à taille fixe
- Masquer les champs inutilisés puis recréer l'Extract est un gain rapide, souvent négligé
- La sortie du Performance Recorder indique le temps par événement : concentrez-vous d'abord sur la barre la plus longue
- L'optimisation de l'Extract (filtrer les lignes et les colonnes au moment de la création de l'Extract) réduit la taille du fichier, mais c'est une étape manuelle facile à oublier
- En mode Live, le Custom SQL contourne entièrement l'optimiseur de requêtes de Tableau

## Voir aussi {#see-also}

- [[tableau-fundamentals]] - Live ou Extract, ordre des filtres
- [[tableau-lod-expressions]] - Implications des LOD sur les performances
- [[tableau-calculations]] - Performances selon le type de calcul
- [[bi-development-process]] - Propriétés de qualité des rapports
