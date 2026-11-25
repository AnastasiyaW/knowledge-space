---
title: "Structure du site et architecture des URL"
category: techniques
tags: [seo-marketing, site-structure, urls, nesting-level, click-depth, url-construction]
level: 3
source_sha256: 9644a0cb88d26f6c549b689b701f01331f08eb3865d2e1b8e3a747834237b0e2
translation: machine
translated_at: '2026-10-24'
---
# Structure du site et architecture des URL {#site-structure-and-url-architecture}

Principes de hiérarchie du site, règles de construction des URL, niveaux d'imbrication et modèles de structure selon le type de site. Une erreur de structure peut empêcher le classement, indépendamment des autres optimisations.

## Principes de construction de la structure {#principles-of-structure-building}

Quatre étapes séquentielles :
1. **Collecter la sémantique** : tous les segments de demande
2. **Construire la structure visuelle** : carte mentale avant la mise en œuvre
3. **Analyser les concurrents** : étudier la structure des leaders (éviter une structure identique, risque de filtre d'affiliation)
4. **Préparer les adresses URL** : créer l'arborescence des URL

## Niveau d'imbrication {#nesting-level}

**Définition** : nombre de clics depuis la page d'accueil pour atteindre la page (et NON le nombre de slashes dans l'URL).

### Règles {#rules}
- Toutes les pages principales mises en avant : pas plus de 3 clics depuis la page d'accueil
- Pages ciblant des requêtes HF : idéalement pas plus de 2 clics
- Faire passer une page de 5 clics à 1 clic peut la faire passer du top 20 au top 10

### Imbrication de l'URL et profondeur de clic {#url-nesting-vs-click-depth}
L'imbrication de l'URL (nombre de slashes) n'est PAS égale à la profondeur de clic :
- `site.ru/catalog/category/subcategory` : 3 slashes, mais peut être atteinte en 2 clics via le méga-menu
- L'imbrication de l'URL n'affecte pas directement le classement
- La profondeur de l'URL est utile pour la segmentation analytique (filtrer par dossier d'URL dans Metrica/GA)

## Structure dictée par la sémantique {#structure-under-semantics}

**Principe central** : la sémantique est une coupe transversale prête de la demande des utilisateurs. Créer des pages pour couvrir cette demande.

- Cluster avec une fréquence > 0 et une intention distincte : créer une page séparée
- Attention : de nombreuses pages sans contenu ou à contenu mince déclenchent des notifications de « qualité de page insuffisante »
- Page d'accueil = page la plus forte ; lui attribuer le cluster « parent » le plus important
- La page d'accueil doit proposer des liens vers toutes les sections du site

### Séparation informationnel / commercial {#informationcommercial-separation}
- **Requêtes commerciales** : pages de catégorie, de produit ou de service
- **Requêtes informationnelles** : blog, articles, FAQ
- **Super fiches** : pages produit ou service avec un contenu approfondi répondant aux deux types d'intention

## Règles de construction des URL {#url-construction-rules}

### URL optimisées pour le SEO (lisibles par l'humain) {#seo-optimized-urls-human-readable}
1. Des URL lisibles par l'humain sont obligatoires pour le SEO
2. Utiliser une translittération correcte (et non une traduction anglaise pour les sites en russe)
3. Doivent contenir les mots de la requête cible
4. Éviter les mots commerciaux dans l'URL (acheter, prix, commander)
5. Éviter la répétition de mots-clés dans le chemin de l'URL :
   - MAUVAIS : `/baby-strollers/baby-strollers-for-newborns/`
   - BON : `/baby-strollers/for-newborns/`
6. Éviter les URL trop longues ou comportant 6 slashes ou plus

### Exemples de qualité d'URL {#url-quality-examples}
```yaml
BAD:  splav.ru/catalog.aspx?cat=20081113151601100150
OK:   secretpoint.ru/catalog/shoes/military/
GOOD: voentorga.ru/catalog/bertsy/
```

### Exigences techniques pour les URL {#technical-url-requirements}
- Caractères latins uniquement
- Lettres et chiffres uniquement, sans caractères spéciaux
- Mots séparés uniquement par des tirets (pas de tirets bas)
- Minuscules uniquement ; les majuscules entraînent une redirection 301 vers la minuscule
- URL relatives dans le code
- Miroir principal : `https://site.ru/` (avec slash final)
- Pas de segments de chemin dupliqués
- Pas plus de 2 redirections ; pas de chaînes ni de boucles infinies
- Tous les environnements de développement et de préproduction fermés par authentification HTTP

## Modèles de structure selon le type de site {#structure-templates-by-site-type}

### E-commerce {#e-commerce}
```text
/ (Homepage)
+-- /contacts/
+-- /about/
+-- /delivery/
+-- /blog/
|   +-- /blog/article-1/
+-- /catalog/
    +-- /catalog/category/           <- "Digital technology"
    |   +-- /catalog/category/sub/   <- "Laptops"
    |   +-- /catalog/category/brand/ <- "Laptops Asus"
    |   +-- /catalog/category/tag/   <- "Gaming laptops"
    +-- /catalog/product-card/       <- Product card
```

**Sous-pages de fiche produit** (astuce SEO) : créer des sous-pages optimisées individuellement :
- `/product/reviews/` : avis
- `/product/specifications/` : caractéristiques techniques
- `/product/photos/` : photos
- `/product/accessories/` : accessoires, avec des sous-titres H2 par type

### Site de services {#service-site}
```text
/ (Homepage)
+-- /contacts/
+-- /about/
+-- /blog/          (with anchor links to services)
+-- /services/
    +-- /services/service-1/
    +-- /services/category-1/
        +-- /services/category-1/service-3/
```

### Blog / informationnel {#bloginformational}
```text
/ (Homepage)
+-- /about/
+-- /section-1/
|   +-- /section-1/article-1/
+-- /section-2/
|   +-- /section-2/article-3/
+-- /tags/
```

## Instruments de structure pour la navigation par clics {#click-through-structure-instruments}

### Page d'accueil {#homepage}
- Page la plus puissante (poids le plus élevé)
- Ajouter des liens vers les pages prioritaires pour réduire la profondeur de clic
- Blocs « Nouveautés » pour une indexation rapide des nouvelles pages
- Mettre en avant les sous-catégories importantes pour renforcer leur poids

### Plan du site HTML {#html-sitemap}
- Page accessible aux utilisateurs, avec des liens d'ancrage vers toutes les sections
- Réduit la profondeur de clic : page principale → plan du site (1 clic) → n'importe quelle section (2 clics)
- Pour les grands sites : découper en plusieurs plans par section
- Généralement placé en pied de page sous l'intitulé « Plan du site »
- Jusqu'à 1 000 liens internes par page : sans problème ; maximum 5 000

### Plan du site XML {#xml-sitemap}
- Fichier technique à l'adresse `yourdomain.ru/sitemap.xml`
- Contient toutes les URL ainsi que les balises `lastmod`
- À soumettre à Webmaster et à Search Console
- Toujours inclure l'URL du plan du site dans robots.txt

### Menu de navigation transversal {#cross-navigational-menu}
- Navigation en en-tête, en pied de page ou en barre latérale, sur toutes les pages
- **Doit utiliser des balises HTML `<a href>`** et non JavaScript
- Une navigation uniquement en JavaScript est invisible pour les robots de recherche

## Erreurs courantes de structure {#common-structure-errors}

1. **Erreurs de fil d'Ariane** : page courante cliquable (auto-référencement), titre dans le fil d'Ariane (trop long), fil d'Ariane en JavaScript (invisible pour les robots)
2. **Liens cycliques** : une page qui pointe vers elle-même ; gaspille le budget d'exploration
3. **Cannibalisation des requêtes** : une page hub entre en concurrence avec ses pages enfants pour les mêmes requêtes. Correction : renommer le hub ou le retirer de l'indexation
4. **Pages prioritaires inaccessibles depuis la page d'accueil**
5. **Absence de « nœuds pendants »** : pages ne menant nulle part
6. **Navigation uniquement en JavaScript** : les robots ne peuvent pas la suivre

## Livrables du travail de structure {#deliverables-from-structure-work}
1. Carte mentale complète du site
2. Document de structure de profondeur de clic
3. Tableau des adresses URL (hiérarchie des URL)
4. Schéma de menu et exigences de maillage interne par type de page

## Pièges à éviter {#gotchas}
- **La profondeur de clic compte bien plus que la profondeur de l'URL** : une page située à `site.com/a/b/c/d/` mais à 2 clics de l'accueil surpasse une page `site.com/x/` enfouie à 5 clics
- **Une structure concurrente identique risque le filtre d'affiliation** : analyser les concurrents, mais se différencier
- **Le plan du site HTML est un instrument SEO, pas seulement d'ergonomie** : il contrôle directement la profondeur d'exploration
- **La navigation JavaScript est invisible** : tous les liens critiques doivent être des balises HTML `<a>` directes
- **Les sous-pages de fiche produit sont sous-exploitées** : des pages séparées pour les avis, les caractéristiques et les accessoires captent du trafic longue traîne supplémentaire

## Voir aussi {#see-also}
- [[internal-linking]] - Méthodes de maillage, SILO, pagination
- [[keyword-research-semantic-core]] - Comment les clusters se traduisent en structure
- [[technical-seo-audit]] - Validation technique de la structure
- [[seo-strategy-by-site-type]] - Différences de structure selon le type de site
