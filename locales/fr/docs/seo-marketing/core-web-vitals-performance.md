---
title: "Core Web Vitals et performance"
category: techniques
tags: [seo-marketing, core-web-vitals, lcp, cls, fid, mobile-first, spa, ssr, page-speed]
level: 4
source_sha256: e66f27d5b69833dae9697ceb2f1fb67c25a718c9c1c3549f48e159a6393b9733
translation: machine
translated_at: '2026-10-24'
---
# Core Web Vitals et performance {#core-web-vitals-and-performance}

Signaux d'expérience de page, notamment les métriques Core Web Vitals, l'indexation mobile-first, les solutions de rendu SPA/AJAX et le workflow d'analyse de performance.

## Métriques Core Web Vitals {#core-web-vitals-metrics}

| Métrique | Ce qu'elle mesure | Seuil critique |
|----------|-------------------|----------------|
| LCP (Largest Contentful Paint) | Temps de rendu de l'élément visible le plus grand | >= 4000ms |
| TBT (Total Blocking Time) | Temps de blocage par le JS | >= 300ms |
| CLS (Cumulative Layout Shift) | Stabilité visuelle (blocs publicitaires qui décalent le contenu) | >= 0.25 |
| FID (First Input Delay) | Interactivité après la première interaction | Déprécié au profit de l'INP |
| INP (Interaction to Next Paint) | Temps de réponse après n'importe quelle interaction | Remplace le FID |

**Position de Google** : la qualité du contenu prime sur l'expérience de page. L'expérience de page ne peut pas remplacer un contenu pertinent et utile.

## Signaux d'expérience de page {#page-experience-signals}
- Core Web Vitals (LCP, FID/INP, CLS)
- Optimisation mobile
- HTTPS
- Absence d'interstitiels intrusifs

## Workflow d'analyse {#analysis-workflow}

### 1. Configurer Screaming Frog avec l'API PageSpeed {#1-setup-screaming-frog-with-pagespeed-api}
- Configuration -> API Access -> PageSpeed Insights
- Créer un compte de service, obtenir une clé API, activer l'API PageSpeed Insights
- Connecter dans Screaming Frog ; choisir Mobile ou Desktop

### Catégories de données disponibles {#available-data-categories}
- **Overview** : taille de la page, taille du HTML, taille du CSS
- **CrUX Metrics** : données réelles d'utilisateurs issues de Chrome (moyenne sur 28 jours)
- **Lighthouse Metrics** : données de laboratoire (scores LCP, TBT, CLS)
- **Opportunities** : suggestions d'amélioration par page
- **Diagnostics** : nombre d'éléments du DOM, détails de performance

### 2. Filtrer les pages qui dépassent les seuils {#2-filter-pages-exceeding-thresholds}
- LCP >= 4000ms
- TBT >= 300ms
- CLS >= 0.25

### 3. Examiner les problèmes spécifiques {#3-investigate-specific-issues}
Cliquer sur la page -> PageSpeed Details -> Opportunities -> par exemple « Eliminate Rendering-Blocking Resources » -> affiche les URL des ressources bloquantes.

### 4. Comparaison concurrentielle {#4-competitive-comparison}
- Screaming Frog -> Mode -> List
- Comparer : page d'accueil, page de catégorie, fiche produit de votre site et des principaux concurrents
- Export -> analyse comparative
- **Objectif : atteindre la moyenne de la niche, pas des scores parfaits**

## Indexation mobile-first {#mobile-first-indexation}

- Google indexe la version mobile pour le classement
- Auditer la parité entre le contenu mobile et desktop
- Tous les types de pages doivent réussir les tests d'optimisation mobile
- Balisage adaptatif requis pour PC, tablettes et smartphones
- Le contenu réservé au desktop et invisible sur mobile risque de ne pas être indexé

## Sites SPA/AJAX {#spaajax-sites}

### Problème {#problem}
- SPA (Single Page Application) : le rendu se fait côté client via JS
- Bien indexées par Google (avec des problèmes) ; mal indexées par Yandex
- Technologies : Angular, React, Vue, Elm

### Solution : rendu côté serveur (SSR/prérendu) {#solution-server-side-rendering-ssrprerendering}
Le bot reçoit du HTML statique ; les utilisateurs reçoivent la version JS. Yandex a confirmé que servir un HTML différent aux bots n'est PAS une violation tant que cela ne vise pas à tromper les utilisateurs.

### Ce qui doit figurer dans le HTML rendu {#what-must-be-in-rendered-html}
- Balises meta standard
- Contenu graphique avec toutes les balises meta
- Liens internes et externes avec tous leurs attributs
- Contenu textuel avec mise en forme
- Menus et éléments de navigation
- Micro-balisage (OpenGraph, Schema.org)

### Vérifier la vue du bot {#checking-bots-view}
1. Activer User-Agent Switcher avec YandexBot/Googlebot
2. Désactiver le JS (extension Web Developer)
3. Ouvrir les pages, vérifier le contenu dans la source via CTRL+U
4. Vérifier dans Yandex Webmaster
5. Vérifier dans Google Search Console
6. Vérifier dans la copie enregistrée (cache)

### Services de prérendu {#prerender-services}
- prerender.io
- getseojs.com
- phantomjs.org
- SEO.js
- HtmlUnit

## Optimisation des images {#image-optimization}

### Exigences de nommage {#naming-requirements}
- Formats standard : .jpg, .png
- Toutes les images dans le dossier `/images/`
- Nom de fichier : H1 translittéré (minuscules, séparés par des tirets)
- Attribut `alt` : même modèle que le nom de fichier (dans la langue d'origine)
- Attribut `title` : identique à alt
- Pré-optimiser toutes les images pour la vitesse (cause la plus fréquente de scores faibles)

## Outils de performance {#performance-tools}

| Outil | Usage |
|-------|-------|
| PageSpeed Insights | Métriques Core Web Vitals par page |
| Google Lighthouse | Données de laboratoire + recommandations d'amélioration |
| Screaming Frog + API PageSpeed | Analyse CWV par lots pour l'ensemble du site |
| GTmetrix | Outil alternatif de test de vitesse |

## Principe clé {#key-principle}

**Ne pas chercher des scores PageSpeed parfaits** : cela fait perdre du temps et du budget. L'objectif est d'atteindre la moyenne de la niche. Si les concurrents obtiennent 40 à 50, vous n'avez pas besoin de 95.

## Pièges à éviter {#gotchas}
- **Les CWV sont un critère départageant, pas un signal de classement principal** : la qualité et la pertinence du contenu l'emportent toujours sur la vitesse
- **Les données CrUX nécessitent du trafic** : les pages nouvelles ou peu visitées n'ont pas de métriques réelles d'utilisateurs, seulement des données de laboratoire
- **Les images sont la première cause de lenteur** : optimiser les images avant de toucher au CSS/JS
- **Mobile-first signifie que le mobile EST l'index principal** : les fonctionnalités ou contenus présents uniquement sur desktop peuvent être totalement ignorés
- **Les sites SPA sont mal indexés par Yandex** : le SSR/prérendu est obligatoire, pas facultatif
- **Le contenu masqué sous des spoilers/accordéons a un poids complet** : Google a confirmé qu'il n'y a aucune réduction pour les contenus extensibles compatibles mobile

## Voir aussi {#see-also}
- [[technical-seo-audit]] - Cadre d'audit complet
- [[robots-txt-sitemaps-indexation]] - Indexation et budget de crawl
- [[seo-tools-workflow]] - Stack d'outils pour l'analyse de performance
- [[search-engine-mechanics]] - Place des facteurs techniques dans le classement
