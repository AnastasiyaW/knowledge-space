---
title: "Optimisation des textes"
category: techniques
tags: [seo-marketing, text-optimization, meta-tags, title, h1, description, tf-idf, bm25, content-brief]
level: 4
source_sha256: a9e0a64d88e859f416e64cd4f3bcdbe99a72d90e406037e2c330cdcc4ef2297a
translation: machine
translated_at: '2026-10-24'
---
# Optimisation des textes {#text-optimization}

Zones de texte d'un document, règles des balises meta, calcul de la pertinence textuelle (TF-IDF, BM25), processus de l'analyseur de texte et création de briefs de contenu. Couvre les stratégies d'optimisation orientées trafic et les stratégies d'optimisation positionnelle.

## Calcul de la pertinence textuelle {#text-relevance-calculation}

### TF-IDF {#tf-idf}
- **TF (Term Frequency)** - ratio des occurrences d'un mot par rapport au nombre total de mots du document
- **IDF (Inverse Document Frequency)** - inverse de la fréquence d'apparition d'un mot dans l'ensemble des documents
- TF-IDF élevé = mot fréquent dans UN document mais rare dans l'ensemble de la collection
- Les mots vides (prépositions, conjonctions) apparaissent partout -> TF-IDF très faible

### BM25 {#bm25}
Fonction de classement améliorée, activement utilisée par Yandex :
- Meilleur calcul de la pertinence pour les requêtes multi-mots que TF-IDF
- Ne tient PAS compte de la position des mots les uns par rapport aux autres
- Activement utilisée dans les algorithmes de classement de Yandex

### Filtrage par quorum et ordre des mots {#quorum-filtering-and-word-order}
- Les documents doivent contenir une couverture suffisante de passages (quorum) pour entrer dans le classement principal
- Les occurrences de paires de mots (AB) et l'ensemble complet (ABC) sont comptabilisés séparément
- Les mots les plus rares de la requête ont un poids plus élevé
- L'ordre des mots dans le document doit correspondre à la structure de la requête

## Deux stratégies d'optimisation {#two-optimization-strategies}

### Optimisation orientée trafic {#traffic-optimization}
**Pour** : e-commerce, agrégateurs, portails

- Couverture maximale d'un large noyau sémantique
- Nombreuses requêtes MF/LF, et non des positions sur des requêtes HF spécifiques
- Moteur de croissance : création et optimisation de nouvelles pages d'atterrissage
- Caractère de production de masse du SEO

**Itération** : sémantique de première approximation -> structure des sections principales -> création de toutes les pages possibles -> optimisation des templates -> sémantique détaillée par catégorie -> optimisation manuelle par catégorie -> répéter.

### Optimisation positionnelle {#positional-optimization}
**Pour** : sites de services, B2B, construction, transport, juridique

- Progression maximale des positions sur un petit ensemble de mots-clés
- Les requêtes HF sont particulièrement critiques
- Moteur de croissance : amélioration itérative d'un ensemble fixe de pages
- Caractère précis et ciblé du SEO

**Itération** : sémantique complète -> structure complète -> création de toutes les pages -> optimisation manuelle, itération 1 -> déployer, attendre, surveiller -> corrections, itération 2 -> répéter.

## Zones de texte d'un document {#document-text-zones}

| Zone | Balise | Impact sur le classement | Remarques |
|------|--------|--------------------------|-----------|
| Titre | `<title>` | Le plus élevé | Zone SEO la plus importante |
| H1 | `<h1>` | Très élevé | Un seul par page, requête principale |
| H2-H6 | `<h2>`, `<h3>` | Élevé | Titres structurants |
| Description | `<meta description>` | CTR uniquement (pas le classement) | Optimisation du taux de clic |
| Texte d'ancre | `<a>` | Élevé pour le donneur et l'accepteur | Liens internes + externes |
| Fragments de texte | Petit texte du corps | Moyen | Tableaux, caractéristiques, navigation |
| Texte SEO | Texte principal du corps | Moyen | Texte principal rédigé |
| Meta keywords | `<meta keywords>` | Aucun | Ignorée ; supprimer si spammy |
| Blocs noindex | `<!--noindex-->` | Suppression | Yandex uniquement |

## Règles de la balise title {#title-tag-rules}

### Règles générales {#general-rules}
- Zone SEO la plus importante
- Inclusion exacte des requêtes les plus importantes
- Requête la plus importante en début de titre
- Une seule phrase, NON coupée par un point
- Yandex : jusqu'à 20 mots ; Google : jusqu'à 12 mots
- Utiliser les synsets (groupes de synonymes)
- Ajouter le toponyme régional principal
- Seule zone où l'accord grammatical n'est pas critique

### Title orienté trafic {#traffic-title}
Couvrir le maximum de requêtes :
```text
Buy fridge in Moscow, prices for fridges, online store Brand
```

**Formule de modèle :**
```text
Buy %Category.Nom.Sg% in %City.Prep% online, prices for %Category.Nom.Pl%.
Sale of %Category.Gen.Pl%.
```

Règles : synonymes, translittérations, permutations ; sacrifier la forme exacte du mot-clé au profit de la largeur ; ordre des mots > forme des mots ; 2 occurrences du mot principal sous des formes différentes.

### Title positionnel {#positional-title}
Position maximale sur des requêtes spécifiques :
```sql
PVC windows from manufacturer - Moscow
```

Règles : occurrences exactes des mots-clés saisies « telles quelles » ; presque aucune requête de longue traîne ; modèle repris des concurrents forts ; plus court que le title orienté trafic ; 1 occurrence du mot principal.

### Title d'article {#article-title}
Clics et intention informationnelle :
```text
Simple recipe for cottage cheese pancakes with step-by-step photos
```

Règles : inclusion des mots-clés + accroche (clickbait) ; formulation accrocheuse ; examiner les solutions des concurrents.

## Balise H1 {#h1-tag}
- Doit être UNIQUE par page, placée au-dessus du contenu
- Uniquement la requête principale (de préférence sous forme exacte)
- Courte, grammaticalement correcte
- Ne pas la polluer avec d'autres balises (`<p>` à l'intérieur d'un H1 = mauvais)

## Meta description {#meta-description}
- NON visible dans le navigateur (code uniquement)
- NE participe PAS au classement textuel
- Objectif : augmenter le CTR du snippet dans les SERP
- Longueur : 120-170 caractères (Yandex), jusqu'à 300 caractères (Google)
- Les deux occurrences clés doivent tenir dans 170 caractères
- 2-3 phrases ; 1 mot-clé par phrase
- Caractères spéciaux : unicode-table.com

## Balise noindex (Yandex uniquement) {#noindex-tag-yandex-only}
```html
<!--noindex-->content to hide<!--/noindex-->
```
Interdit l'indexation de n'importe quelle section de la page. NE fonctionne PAS dans Google.

## Analyseur de texte (TA) {#text-analyzer-ta}

**Objectif** : outil de référence à utiliser avant de rédiger TOUT texte SEO.

**Ce qu'il fait** :
- Analyse les textes des concurrents dans le TOP
- Détermine le nombre sûr d'occurrences de mots-clés selon le type
- Indique si un texte est nécessaire
- Crée un brief de contenu presque automatiquement
- Vérifie toutes les zones du document pour détecter le spam de mots-clés

**Outil** : analyseur de texte Rush Analytics

### Exigences du TA {#ta-requirements}
- Clustering : mode HARD avec un seuil de 3
- Exclure de l'analyse les sites d'un type différent
- Utiliser des synonymes ; NE PAS analyser une requête unique
- Jusqu'à 6 requêtes au maximum (au-delà, les résultats se diluent)
- NE PAS inclure de requêtes LF : elles faussent les résultats
- Utiliser la SERP de la région cible

## Texte SEO sur les sites commerciaux {#seo-text-on-commercial-sites}

- Suivre strictement les exigences de l'analyseur de texte
- Respecter le nombre exact d'occurrences de mots-clés et le volume de texte
- Parfois, un texte n'est tout simplement pas nécessaire
- Densité de mots-clés homogène dans tout le texte
- Ne pas abuser des mots commerciaux (acheter, prix, commander)
- Inclure des mots LSI thématiques, sans remplissage
- **SANS ANALYSE PAR L'ANALYSEUR DE TEXTE - NE PAS RÉDIGER DU TOUT**

### Tension entre Yandex et Google sur le texte {#yandex-vs-google-text-tension}
Google récompense les textes optimisés et volumineux ; Yandex peut pénaliser TOUT texte sur les pages commerciales.

**Si les concurrents du TOP Yandex n'ont pas de texte -> vous ne pouvez pas utiliser de texte optimisé sans risque.**

Solutions de contournement pour n'afficher le texte qu'à Google :
- Afficher le texte via JavaScript `document.write`
- Ajouter le texte via Google Tag Manager
- Via GTM : définir le canonical d'une page sans texte vers la copie avec texte

## Types de contenu par page {#content-types-by-page}

### Fiches de catégorie produits {#product-listings}
- N'écrire un texte que si l'analyseur de texte le recommande
- TA recommande <100 mots -> texte NON nécessaire
- TA recommande ~100-150 mots -> génération uniquement
- TA recommande >150 mots -> possibilité de rédiger un texte complet
- Suivre séparément les occurrences dans la zone d'ancre `<a>`

### Règles de génération des listings (ère Baden-Baden) {#listing-generation-rules-baden-baden-era}
- 1 occurrence de la requête principale
- 1-2 occurrences de mots isolés (espacées les unes des autres)
- NE PAS écrire de mots commerciaux à proximité de la requête
- 2-3 phrases, jusqu'à 100 mots au total
- Texte cohérent et utile

### Fiches produit {#product-cards}
- L'unicité du texte n'est PAS critique
- Unicité de la page assurée par : texte généré, avis clients, section accessoires
- Mêmes règles de génération que pour les pages de catégorie

### Pages de services {#service-pages}
- Uniquement un texte pertinent rédigé par un rédacteur
- NE PAS générer ; obligatoire : utiliser l'analyseur de texte
- Rédiger uniquement sur la base d'un audit de contenu

### Articles informationnels {#informational-articles}
- Table des matières, structure H1/H2/H3 claire
- Inclure des termes LSI (50 au maximum)
- Couvrir TOUS les points utiles de tous les concurrents + compléments
- Taille : plus longs que n'importe quel concurrent pris isolément
- Plus d'images, de vidéos ; alterner texte, images, listes et citations

## Structure du brief rédacteur {#copywriter-brief-structure}

Un brief complet doit contenir :
1. La structure des titres (H2-H3 avec les mots-clés cibles)
2. Les instructions pour chaque section
3. Les mots-clés LSI pour chaque paragraphe
4. Le nombre de mots/paragraphes par section
5. Des liens vers les meilleurs exemples concurrents
6. La sortie de l'analyseur de texte avec les occurrences requises mises en évidence

**Décompte en tokens** : 1 mot = 1,3 token ; 1 000 mots = 1 300 tokens.

## Liste de contrôle de l'optimisation selon le type de site {#optimization-checklist-by-site-type}

| Zone | Site orienté trafic | Site positionnel | Informationnel |
|------|---------------------|------------------|----------------|
| Title | Template, large couverture | Correspondance exacte, court | Clickbait + requête |
| H1 | Template ou manuel, exact | Exact, court | Formulation naturelle |
| Description | Template | Manuelle, axée CTR | Manuelle, axée CTR |
| Texte SEO | Selon le TA ; généré si court | Selon le TA ; rédacteur | Article complet |
| Structure des titres | Template h2/h3 | Sémantique manuelle | h2/h3/h4 riches |
| Mots LSI | Généré automatiquement | Selon le TA | Riches, 50 LSI |
| Audit de contenu | Requis | Requis | Requis |

## Pièges à éviter {#gotchas}
- **La balise meta keywords ne sert à rien** - la supprimer si elle est spammy, sinon l'ignorer
- **Baden-Baden pénalise la densité de mots-clés** - toujours vérifier avec l'analyseur de texte avant de rédiger
- **Les mots-clés en gras ou dans des balises strong signalent une manipulation** - ne pas utiliser `<b>`, `<strong>`, `<em>` sur les mots-clés
- **La description n'affecte pas le classement** - seulement le CTR ; ne pas bourrer de mots-clés dans un but de classement
- **Le conflit textuel entre Yandex et Google est réel** - la solution GTM/JS est une pratique standard, pas un hack
- **Les mots commerciaux de longue traîne nuisent** - « acheter », « prix », « commander » à proximité des mots-clés déclenchent la détection de spam

## Voir aussi {#see-also}
- [[keyword-research-semantic-core]] - Collecte du noyau sémantique et clustering
- [[behavioral-factors-ctr]] - Optimisation du CTR via les snippets
- [[niche-content-audit]] - Méthodologie d'audit de contenu
- [[filters-and-penalties]] - Détails des filtres Baden-Baden
