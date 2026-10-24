---
title: "Recherche de mots-clés et noyau sémantique"
category: techniques
tags: [seo-marketing, keywords, semantic-core, wordstat, clustering, search-demand]
level: 3
source_sha256: 53a8ba01bec6098c07dbaade3ac13f0c9fa596c447464df1da8fe599d4f23ccf
translation: machine
translated_at: '2026-10-24'
---
# Recherche de mots-clés et noyau sémantique {#keyword-research-and-semantic-core}

Processus complet de collecte, nettoyage, regroupement et attribution des groupes de mots-clés aux pages. Couvre les opérateurs de Yandex Wordstat, les méthodes de collecte, le clustering basé sur la SERP et les outils.

## Terminologie de base {#core-terminology}

- **Noyau sémantique** - ensemble complet des groupes de mots-clés couvrant toute la demande de recherche des utilisateurs pour un site
- **Marqueur** - requête d'ancrage décrivant le plus précisément le contenu d'une page ; base de l'expansion
- **Cluster** - groupe de requêtes servies par une seule page
- **Fréquence** - nombre de fois qu'une requête a été recherchée par mois (données Wordstat)
- **Nuage de requêtes** - ensemble complet des requêtes étendues collectées autour des marqueurs

## Sources de collecte des requêtes {#sources-for-query-collection}

### Sources fiables {#reliable-sources}
1. **Yandex Wordstat** - données directes sur la demande de recherche (les plus précises pour le segment RU)
2. **Parsing des suggestions de recherche** - outils collectant les suggestions de saisie automatique
3. **Programmes de parsing** - Key Collector, Rush Analytics (automatisent la collecte Wordstat/suggestions)

### Moins fiables (complémentaires) {#less-reliable-supplementary}
1. **Bases de mots-clés** - listes de requêtes préétablies ; origine et exhaustivité incertaines ; peuvent contenir des données inutilisables
2. **Parsing de sites concurrents** - reflète les choix structurels du concurrent, pas la demande complète

### Données de support {#supporting-data}
- Yandex Metrika - requêtes ayant déjà généré du trafic
- Yandex Webmaster - statistiques d'apparition dans les résultats de recherche
- Google Keyword Planner - équivalent Google de Wordstat

## Analyse approfondie de Yandex Wordstat {#yandex-wordstat-deep-dive}

### Colonne de gauche et colonne de droite {#left-vs-right-column}
- **Colonne de gauche** - dictionnaire de fréquences de N-grammes : somme de toutes les requêtes contenant la expression, sous toute forme, dans n'importe quel ordre et quelle que soit la longueur
- **Colonne de droite** - « Requêtes similaires » - peu fiable ; affiche les requêtes que les mêmes utilisateurs ont recherchées, et non des synonymes

### Opérateurs Wordstat {#wordstat-operators}

| Opérateur | Effet | Exemple |
|---------|--------|---------|
| Aucun | Toutes les requêtes contenant le N-gramme | `phone samsung` -> 1 250 000 |
| `"expression"` | Fixe le nombre de mots (nombre exact uniquement) | `"phone samsung"` -> 12 000 |
| `!mot` | Fixe la forme exacte du mot (sans flexions) | `!mobile !phones` -> 61 000 |
| `[expression]` | Fixe l'ordre des mots | `[mobile phones]` -> 938 000 contre `[phones mobile]` -> 60 |
| `+mot` | Force l'inclusion de mots vides | `fridge +how` |
| `-mot` | Exclut les requêtes contenant le mot | `fridge -reviews` |
| `(a\|b)` | Opérateur OU pour les variantes | `smartphone (samsung\|galaxy)` |

### Combinaison d'opérateurs {#combining-operators}
**Pour la collecte de requêtes :**
```text
fridge (samsung|lg) (buy|price|order) -reviews
```

**Pour une fréquence précise :**
```text
"[!fridge !samsung]"
```
Guillemets + crochets + point d'exclamation = fréquence la plus précise (les trois contraintes).

### Astuce des 7 mots {#7-word-trick}
Écrire le même mot 7 fois entre guillemets pour trouver toutes les requêtes de cette longueur exacte :
```text
"keyword keyword keyword keyword keyword keyword keyword"
```
Ne fonctionne pas pour les requêtes de plus de 7 mots.

## Types de fréquence {#frequency-types}

| Type | Opérateur | Quand l'utiliser |
|------|----------|-------------|
| Générale | `requête` | Noyau abrégé, marqueurs HF |
| Expression | `"requête"` | Noyau étendu, validation de la fréquence |
| Exacte | `"[!exact !requête]"` | Comptage le plus précis, confirmation de la demande |

## Processus de collecte standard {#standard-collection-process}

### Étape 1 : Collecter les marqueurs {#step-1-collect-markers}
**Manuelle** - pour les niches « sales » ou les sémantiques réduites (moins de 30 pages Wordstat). Outils : extensions WordStatter, WordStat Assistant.

**Automatisée** - pour les grands catalogues et les niches propres. Outils : Rush Analytics, Key Collector.

**Étendre les marqueurs avant la collecte** : ajouter des variantes cyrilliques/latines, des préfixes commerciaux, des indicateurs de prix ; chacun génère des ensembles de suggestions différents.

### Étape 2 : Parser la colonne de gauche de Wordstat {#step-2-parse-wordstat-left-column}
Pour chaque marqueur étendu, collecter toutes les requêtes de la colonne de gauche.

### Étape 3 : Parser les suggestions de recherche {#step-3-parse-search-suggestions}
Les suggestions peuvent multiplier la liste des requêtes par 5 à 7. Chacun des 100 marqueurs peut générer 600 à 700 requêtes uniques.

### Étape 4 : Parser la structure des concurrents (facultatif) {#step-4-parse-competitor-structure-optional}
Explorer les pages de catégories concurrentes avec Screaming Frog, extraire les valeurs H1 = choix sémantiques structurés du concurrent.

**Exemple** : pour une boutique de téléphones, explorer uniquement les pages `/tag/` d'un concurrent (sans la pagination) pour extraire toutes les pages de filtres et d'attributs sous forme de valeurs H1.

### Étape 5 : Combiner et nettoyer {#step-5-combine-and-clean}
Supprimer les mots vides : mots vides non commerciaux (« avis », « forum », « fait maison »), noms de marques concurrentes, mots vides géographiques si non nécessaires.

### Étape 6 : Vérifier la fréquence {#step-6-check-frequency}
Récupérer la fréquence de toutes les requêtes collectées. Supprimer les requêtes à fréquence nulle avant de créer les pages.

### Étape 7 : Clustériser {#step-7-cluster}
**Clustering basé sur la SERP** (standard) :
- Le service collecte les 10 premiers résultats pour chaque requête
- Si 2 requêtes partagent au moins 8 pages du TOP-10 -> même groupe (même intention)
- Principe : mêmes documents dans la SERP = intention utilisateur identique

**Révision manuelle toujours nécessaire** : fusionner les clusters mal séparés, scinder ceux mal fusionnés, corriger les noms de clusters.

### Étape 8 : Multiplication croisée (grands catalogues) {#step-8-cross-multiplication-large-catalogs}
Produits × Marques × Attributs = liste de requêtes générée. Récupérer la fréquence, supprimer les résultats à fréquence nulle.

## Attribution des clusters aux pages {#cluster-to-page-assignment}

| Type de page | Règle d'attribution |
|-----------|----------------|
| Page d'accueil | Cluster « parent » le plus fréquent |
| Pages de catégories | Clusters au niveau de la catégorie |
| Pages de sous-catégories | Clusters de sous-catégories |
| Pages produits/services | Clusters de produits spécifiques |
| Blog/informationnel | Clusters de requêtes informationnelles |

Certaines requêtes ne peuvent être positionnées QUE sur la page d'accueil : vérifier la SERP. Si tous les premiers résultats sont des pages d'accueil, attribuer la requête à la page d'accueil.

## Flux de travail assistés par l'IA {#ai-assisted-workflows}

### Génération de marqueurs avec l'IA {#marker-generation-with-ai}
**Itération 1** : fournir le type de site, le sujet, les mots-clés de base et les caractéristiques connues -> obtenir TOUS les types de caractéristiques.

**Itération 2** : pour chaque type de caractéristique, lister toutes les valeurs, y compris les synonymes, le jargon et les fautes d'orthographe. Présenter sous forme de tableau.

**Résultat** : combinaisons [caractéristique] × [valeur] -> chaque ligne devient un marqueur de parsing.

### Génération des balises méta {#meta-tag-generation}
**Règles pour le title** : requête la plus fréquente en début ; chaque mot une seule fois ; jusqu'à 80 caractères / 12 mots ; phrase naturelle, pas une liste de mots-clés ; pas de mots promotionnels.

**Règles pour la description** : 150 à 159 caractères, 18 mots maximum ; appel à l'action + USP ; synonymes des mots-clés ; 1 à 2 emojis neutres autorisés.

### Génération d'un brief de contenu par l'IA {#content-brief-generation-via-ai}
1. Lancer une analyse de texte via Rush Analytics sur les mots-clés cibles
2. Parser les pages concurrentes - extraire le texte avec la hiérarchie des titres et le nombre de tokens
3. Générer le plan via l'IA : titre, résumé, public cible, structure H2-H3
4. Répartir les mots-clés et les LSI dans les sections du plan avec des nombres d'occurrences précis

## Outils pour le travail sémantique {#tools-for-semantic-work}

### Complément Excel SEOXL {#seoxl-excel-add-in}
- **Couleur par cluster** - couleurs alternées pour délimiter les clusters
- **Tri au sein d'un cluster** - trie par fréquence à l'intérieur de chaque cluster
- **Tri des clusters par fréquence totale** - clusters les plus trafiqués en premier
- **Dictionnaire de lemmes** - racines de mots les plus fréquentes dans les requêtes ; permet d'identifier les catégories de mots vides
- **Revue des clusters** - feuille séparée avec la première ligne de chaque cluster ; fusion par glisser-déposer des clusters adjacents
- **Squeeze** - supprime les racines de mots spécifiées ; met en évidence les modificateurs distinctifs pour la déduplication

### Key Collector (bureau) {#key-collector-desktop}
- Parsing Wordstat en masse, collecte de fréquences, clustering interne
- Collecte de fréquences en 4 passes (base, expression, expression exacte, [exact exact])
- Clustering basé sur la SERP : strict (intersection) ou souple (union), configurable
- Planificateur de tâches pour les exécutions nocturnes sans surveillance
- Mode multi-groupes : appliquer les opérations à tous les groupes simultanément

### Rush Analytics (cloud) {#rush-analytics-cloud}
Parsing dans le cloud, vérification des fréquences, clustering basé sur la SERP.

### Scripts Google Sheets {#google-sheets-scripts}
Toutes les fonctions SEOXL peuvent être reproduites avec Google Apps Script généré par l'IA. Format de requête : décrire le périmètre (« travailler sur la plage sélectionnée ») -> décrire l'action par cellule -> préciser l'emplacement de sortie -> itérer avec des corrections.

## Pièges à éviter {#gotchas}
- **La colonne de droite de Wordstat est peu fiable** - à utiliser uniquement en complément ; elle affiche les « requêtes recherchées par les mêmes utilisateurs », et non des synonymes
- **Les requêtes à fréquence nulle ne doivent pas recevoir de pages** - elles créent du contenu pauvre qui nuit à la qualité globale du site
- **Le clustering basé sur la SERP exige une révision manuelle** - le clustering automatique échoue dans 10 à 20 % des cas
- **L'expansion des marqueurs est essentielle** - les marqueurs nus manquent 5 à 7 fois plus de requêtes que les variantes étendues
- **La multiplication croisée génère des données inutilisables** - toujours valider avec les données de fréquence avant de créer des pages
- **Ne pas inclure de requêtes LF dans l'analyseur de texte** - elles faussent les résultats ; utiliser jusqu'à 6 requêtes au maximum, valeur optimale

## Voir aussi {#see-also}
- [[text-optimization]] - Utiliser le noyau sémantique pour les briefs de contenu et l'analyseur de texte
- [[site-structure-urls]] - Comment les clusters se projettent sur la structure du site
- [[seo-tools-workflow]] - Détails de configuration et de mise en place des outils
- [[seo-strategy-by-site-type]] - Différences de stratégie sémantique selon le type de site
