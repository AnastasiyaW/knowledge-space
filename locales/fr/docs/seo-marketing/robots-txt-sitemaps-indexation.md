---
title: "robots.txt, sitemaps et indexation"
category: techniques
tags: [seo-marketing, robots-txt, sitemap-xml, indexation, crawl-budget, indexnow, google-indexing-api]
level: 3
source_sha256: 42aad566216b7e3a57d6a86ff1a736224dc04e7014b0cdce77f6a4111e62a6c2
translation: machine
translated_at: '2026-10-24'
---
# robots.txt, Sitemaps et indexation {#robotstxt-sitemaps-and-indexation}

Présentation détaillée de la configuration de robots.txt, des exigences relatives au sitemap.xml, de l'analyse de l'indexation, de l'optimisation du budget de crawl et des méthodes d'indexation forcée.

## robots.txt {#robotstxt}

### Exigences {#requirements}
- Trois blocs distincts : Yandex, Google, autres moteurs de recherche
- Ne pas bloquer les dossiers contenant des fichiers CSS et JS (les moteurs de recherche doivent pouvoir les rendre)
- Vérifier visuellement la conformité
- Toujours inclure l'URL du sitemap

### Quoi interdire {#what-to-disallow}
```yaml
Disallow: /admin/                    # Admin panel
Disallow: /search/                   # Internal search results
Disallow: /?sort=                    # Sorting parameters
Disallow: /?results_on_page=         # Items per page
Disallow: /print/                    # Print pages
Disallow: /rss/                      # RSS feeds
Disallow: /?utm_                     # UTM parameters
```

### robots.txt vs autres directives {#robotstxt-vs-other-directives}
- **robots.txt** - contrôle le crawl (et NON l'indexation) ; permet d'économiser le budget de crawl ; ne supprime pas les pages déjà indexées
- **Balise meta robots** - contrôle l'indexation ; utiliser `noindex` pour l'empêcher
- **X-Robots-Tag** - en-tête HTTP pour les documents non HTML (PDF, etc.)

### Utiliser `clean-param` pour les paramètres GET {#use-clean-param-for-get-parameters}
Plutôt que de bloquer chaque variante de paramètre dans robots.txt, Yandex prend en charge la directive `clean-param` pour regrouper les variantes d'URL.

## sitemap.xml {#sitemapxml}

### Exigences {#requirements_1}
- Accessible à l'adresse `https://site.ru/sitemap.xml`
- Ne contient que des pages en 200 OK
- 50 000 URL maximum par fichier sitemap
- 10 Mo maximum par fichier sitemap
- Plusieurs sitemaps -> créer un sitemap index
- Aucune URL bloquée dans robots.txt
- Toutes les URL utilisent l'hôte principal (sans www), https://, avec slash final
- Chaque URL n'apparaît qu'une seule fois
- Généré dynamiquement (doit être à jour à chaque requête)
- Doit comporter des balises `lastmod` avec des dates exactes
- Soumettre à Yandex Webmaster et à Google Search Console

## Analyse de l'indexation {#indexation-analysis}

### Processus {#process}
1. Crawler le site avec Screaming Frog
2. Télécharger les pages exclues et indexées depuis Yandex Webmaster (50 000 maximum)
3. Comparer les deux listes : ce qui est présent sur le site et ce qui n'est pas dans l'index
4. Analyser la raison de chaque page non indexée

### Contrôle du niveau d'imbrication {#nesting-level-check}
1. Crawler avec Screaming Frog
2. Trier par niveau d'imbrication
3. Tout ce qui se situe à plus de 5 niveaux de profondeur -> analyser
4. Si des pages générant du trafic sont enfouies en profondeur -> créer un sitemap ou restructurer

### Contrôles d'accessibilité à l'indexation {#indexation-accessibility-checks}
- Vérifier la présence de `noindex` et `nofollow` dans les balises meta
- Vérifier les balises canonical (pointant ailleurs)
- X-Robots-Tag dans les en-têtes HTTP
- Pages bloquées dans robots.txt

### Index supplémentaire de Google {#google-supplemental-index}
Index secondaire de faible qualité. La présence d'un grand nombre de pages dans cet index nuit au classement global.

**Causes principales** :
1. Duplication de contenu - la plus fréquente
2. Maillage interne incorrect entraînant un faible poids de page
3. Textes trop courts ou spammy ; contenu généré automatiquement et illisible

## Optimisation du budget de crawl {#crawl-budget-optimization}

### En-têtes Last-Modified / If-Modified-Since {#last-modified-if-modified-since-headers}
- **Erreur courante** : définir la date de modification sur l'heure actuelle à chaque requête
- **Correct** : ne mettre à jour la date que lorsque le contenu change réellement
- **Avantages** : chargement de page plus rapide, charge serveur réduite, date de modification visible dans les SERP, indexation plus rapide

### Analyse des logs serveur {#server-log-analysis}
Utiliser Screaming Frog Log File Analyser pour :
- Trouver les redirections rencontrées par les robots des moteurs de recherche
- Identifier les URL les plus et les moins crawlées
- Repérer les URL non crawlées et les pages orphelines
- Identifier les robots à bloquer
- Corréler la fréquence de crawl avec l'importance des pages

## Forcer l'indexation {#forcing-indexation}

### Google Indexing API {#google-indexing-api}
- Ajouter de grands volumes de pages sans intervention des développeurs
- Permet d'indexer des pages de sites sans accès à Search Console
- Les comptes de service, créés une seule fois, sont réutilisables pour n'importe quel site
- Idéal pour les ajouts de pages à grande échelle

### Yandex IndexNow {#yandex-indexnow}
- Signaler les pages nouvelles, modifiées ou supprimées
- Utiliser les plugins IndexNow pour les CMS courants
- Dans la plupart des cas, un maillage interne correct résout l'ensemble des problèmes d'indexation Yandex

### Autres méthodes {#other-methods}
- Soumettre l'URL via l'Inspection d'URL de Google Search Console
- Soumettre dans Yandex Webmaster
- S'assurer que les pages sont liées depuis des pages déjà indexées (le maillage interne résout la plupart des problèmes)

## Pièges à éviter {#gotchas}
- **robots.txt bloque le crawl, pas l'indexation** - une page bloquée dans robots.txt peut tout de même apparaître dans les résultats de recherche si d'autres pages la lient
- **Les sitemaps statiques deviennent obsolètes** - toujours les générer dynamiquement ; un sitemap périmé est pire que l'absence de sitemap
- **lastmod doit être exact** - attribuer la date du jour à toutes les pages réduit l'efficacité du crawl
- **Les anciens prestataires laissent souvent de mauvaises règles robots.txt** - toujours les vérifier manuellement au démarrage d'un projet
- **L'index supplémentaire de Google est un signal d'alerte** - un grand nombre de pages à cet endroit signale des problèmes de qualité à l'échelle du site
- **IndexNow ne garantit pas l'indexation** - il accélère seulement la découverte ; la qualité détermine toujours si une page est indexée

## Voir aussi {#see-also}
- [[technical-seo-audit]] - Cadre d'audit complet, incluant robots.txt
- [[core-web-vitals-performance]] - Performance et son impact sur le budget de crawl
- [[site-structure-urls]] - Structure et son impact sur la profondeur de crawl
- [[seo-analytics-reporting]] - Suivi des métriques d'indexation
