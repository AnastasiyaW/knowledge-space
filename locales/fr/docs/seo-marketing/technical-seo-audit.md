---
title: "Audit SEO technique"
category: techniques
tags: [seo-marketing, technical-audit, hosting, duplicates, response-codes, crawl-budget, screaming-frog]
level: 3
source_sha256: 3ec7731532a6bb80cb4591f49fc3ba15b9686087604c33348e85c2a371f690a7
translation: machine
translated_at: '2026-10-24'
---
# Audit SEO technique {#technical-seo-audit}

Cadre complet d'audit technique couvrant la priorisation, les pages dupliquées, les codes de réponse serveur, les exigences d'hébergement, la validation du contenu et les exigences de développement du CMS.

## Cadre de priorisation de l'audit {#audit-prioritization-framework}

### Niveaux de priorité {#priority-levels}
1. **Erreurs bloquant l'indexation des pages** : problèmes d'hébergement, rendu JS, miroirs/canonicals, pages dupliquées
2. **Erreurs bloquant l'indexation correcte du contenu** : JS non rendu, problèmes de balisage
3. **Erreurs bloquant le classement des pages** : balises en double, liens cassés, contenu dupliqué, imbrication profonde, contenu sur-optimisé
4. **Autres** : corrections de moindre priorité

### Règles de priorisation {#priority-rules}
- Se concentrer sur les tâches affectant le plus grand nombre de pages
- Corriger les redirections de pagination incorrectes (priorité haute) plutôt que plus de 5 liens cassés vers des 404 (priorité basse)
- Déployer le nouveau modèle de title (priorité haute) plutôt que mettre à jour le sitemap HTML (priorité basse)
- Évaluer le budget client nécessaire à la mise en œuvre ; réaliser d'abord les tâches produisant des résultats

### Priorité selon la taille du site {#priority-by-site-size}
- **Petits sites (<50 pages)** : priorité basse, les erreurs ont un impact minime
- **Sites moyens** : priorité moyenne
- **Grands sites (50k+ pages)** : critique, une seule erreur structurelle peut exclure des milliers de pages de l'index

## Mise en place et surveillance {#setup-and-monitoring}

### Surveillance proactive {#proactive-monitoring}
1. Top 1000 des requêtes de Metrika → suivi de position
2. Mêmes requêtes → Favoris de Yandex Webmaster
3. Top 100 des pages de trafic → « Pages importantes » dans Webmaster
4. Configurer les notifications Webmaster
5. Connecter un meta-scanner (Rush Analytics) pour la détection quotidienne des modifications de pages
6. Ne pas encombrer robots.txt ; utiliser `clean-param` pour les paramètres GET

### Meta-scanner {#meta-scanner}
Suit l'état de référence des pages avant que les modifications n'affectent le trafic :
- Surveille : Title, Description, H1, URL, Meta robots, Canonical, robots.txt, contenu textuel
- Notification push en cas d'écart
- Évite la perte de trafic due à des modifications non détectées effectuées par les développeurs

### Exigences d'hébergement {#hosting-requirements}
- **HTTP/2** : vérifier sur `http2.pro/` ; contacter l'hébergeur pour l'activer
- **SSL/TLS** : vérifier sur `ssllabs.com/ssltest/` ; recommander TLS 1.2 ; configurer la politique DNS CAA
- **Tests de charge** : `loadimpact.com`
- **Stabilité** : connecter les alertes Metrika

## Pages dupliquées {#duplicate-pages}

### Types et solutions {#types-and-solutions}

| Type de doublon | Solution |
|----------------|----------|
| www vs non-www | Choisir le miroir principal, redirection 301 |
| http vs https | Redirection 301 vers https |
| Slash final | Vérifier la version qui se classe, redirection 301 |
| Variantes de la page d'accueil (`/index.html`) | Redirection 301 vers la page d'accueil |
| Sensibilité à la casse (`/Page` vs `/page`) | Redirection 301 vers la minuscule |
| Paramètres de tri des produits (`?sort=price`) | Exclure dans robots.txt ou implémenter via JS |
| Doublons de pagination | Modèles de meta distincts pour la page 2 et suivantes |
| Produit dans plusieurs catégories | Balises canonical ou redirection |
| Sous-domaines techniques (old., dev.) | Exclure de l'indexation ou protéger par authentification HTTP |
| Pages d'impression (`/print/`) | Exclure dans robots.txt |
| Paramètres UTM | Exclure dans robots.txt avec Disallow |

### Trouver les doublons {#finding-duplicates}
- Yandex Webmaster (section Pages dupliquées)
- Screaming Frog SEO Spider
- Opérateurs de recherche : `site:domain.ru`

## Codes de réponse serveur {#server-response-codes}

### Comportement requis {#required-behavior}
- **200 OK** : toutes les pages valides
- **301** : redirection permanente (toujours utiliser pour le SEO, jamais 302)
- **404** : les pages cassées doivent renvoyer un véritable 404 (et non un 200)
- **503** : pendant la maintenance (et non 403 ou 502)
- **500** : inacceptable, corriger immédiatement

### Qualité des liens {#link-quality}
- Aucun lien vers des pages 3xx/4xx lors d'un crawl complet du site
- Aucun lien cassé dans le crawl Screaming Frog

## Redirections de base (obligatoires sur chaque projet) {#basic-merges-required-on-every-project}

Toutes les redirections en 301 vers l'URL canonique :
1. `http://` → `https://` (SSL obligatoire)
2. `www.domain.ru` → `domain.ru` (en choisir une, rediriger l'autre en 301)
3. `domain.ru/page/` → `domain.ru/page` (normalisation du slash final)
4. `domain.ru/Page` → `domain.ru/page` (normalisation des majuscules)

Vérifier chaque cas avec l'extension de navigateur Redirect Path.

## Contrôles d'audit du contenu {#content-audit-checks}

### Texte masqué {#hidden-text}
1. Désactiver les styles et les scripts
2. Contrôler 5 à 10 pages de chaque type
3. Le texte pertinent masqué PEUT être utilisé, mais JAMAIS via `display:none`
4. Mobile-First : le contenu situé sous des spoilers ou des éléments repliables ne subit PAS de réduction de poids (confirmé par Google)

### Qualité du contenu {#content-quality}
- Contrôler 5 à 10 pages par type pour l'unicité (content-watch.ru pour les lots)
- Spam et génération automatique : rechercher les textes incohérents, le bourrage de mots-clés, le spam de balises sémantiques
- Le texte généré doit être statique

### Audit du balisage et de la mise en page {#markuplayout-audit}
- Désactiver JS et CSS, vérifier que le contenu, les prix et les photos sont visibles
- Styles dans des fichiers .css (pas de style en ligne) ; JS dans des fichiers externes
- Maximum 20 fichiers CSS/JS externes par page
- Jeu de caractères par défaut : UTF-8

## Défense contre le parsing automatisé {#anti-parsing-defense}

### Méthodes inefficaces {#ineffective-methods}
- Restrictions par User-Agent (facilement contournées)
- Restrictions par pays/fournisseur (perte de trafic réel)
- CAPTCHA (contournés, irritants pour les utilisateurs)

### Méthodes efficaces {#effective-methods}
1. **Empreinte numérique (fingerprinting)** : évaluation du client sur plusieurs paramètres
2. **Classification du trafic** : bons bots, mauvais bots, navigateurs, trafic suspect
3. **Limitation de débit (rate limiting)** : par minute, par session, par durée
4. **Classification ML/statistique** : identification de schémas
5. **Biométrie comportementale** : mouvements de souris, orientation de l'appareil

### Blocage du scraping par faux bots {#blocking-fake-bot-scraping}
**Validation par DNS inverse** :
1. Le bot se déclare GoogleBot/YandexBot → extraire l'IP
2. DNS inverse → obtenir le nom d'hôte
3. Vérifier : Google = `googlebot.com`/`google.com` ; Yandex = `yandex.ru`/`.net`/`.com`
4. DNS direct : nom d'hôte → IP
5. Les IP ne correspondent pas → faux bot → bloquer

## Exigences CMS et développement {#cmsdevelopment-requirements}

- Title, Description, H1, texte SEO : modifiables indépendamment par page ET via des modèles
- Alt et Title des images : individuellement et via des modèles à compléter
- Utilisateurs et robots voient un contenu identique ; aucun texte masqué dans le code source
- Lorsque JS est désactivé : les liens vers toutes les pages sont accessibles depuis la page d'accueil
- favicon.ico à la racine du site
- Ressources statiques : compression gzip ; en-têtes de cache >= 3 jours ; invalidation du cache via un horodatage
- Tous les environnements de développement et de préproduction fermés aux robots via une authentification HTTP

## Outils {#tools}

| Outil | Usage |
|------|-----|
| Screaming Frog SEO Spider | Crawl complet du site : 404, chaînes de redirection, titles en double, H1 manquants, problèmes de canonical |
| Screaming Frog Log File Analyser | Analyse des logs serveur : URL crawlées/non crawlées, pages orphelines, identification des bots |
| Redirect Path (extension) | Vérifier les chaînes de redirection pour toute URL |
| SEO in 1 Click (extension) | Afficher les balises meta, H1-H6, canonical de la page courante |
| Web Developer (extension) | Désactiver JS/CSS pour voir la page comme les robots |
| User-Agent Switcher | Simuler un bot pour vérifier le rendu |
| Link Redirect Trace | Suivre les chaînes de redirection |

**Note sur l'infrastructure** : pour crawler de grands sites (des centaines de milliers de pages), acheter un serveur dédié, installer Screaming Frog et lancer le crawl pendant plusieurs jours.

## Calendrier des audits récurrents {#repeat-audit-schedule}

| Taille du projet | Audit technique | Audit de visibilité des concurrents |
|--------------|-----------------|---------------------------|
| Petit | Pas de répétition nécessaire | Tous les 3 à 6 mois |
| Moyen | Tous les 3 à 6 mois | Tous les 3 à 6 mois |
| Grand | Mensuel | Tous les 3 à 6 mois |

## Pièges courants {#gotchas}
- **robots.txt contrôle l'exploration, non l'indexation** : les pages bloquées dans robots.txt peuvent quand même apparaître dans l'index si elles sont liées depuis ailleurs
- **Les redirections 302 ne transmettent PAS les signaux de classement** : toujours utiliser le 301 pour les déplacements permanents
- **Les anciens prestataires laissent souvent de mauvaises règles dans robots.txt** : toujours les vérifier manuellement avant toute autre tâche
- **CloudFlare peut provoquer de faux 403** dans des outils d'audit comme bertal.ru
- **« Qualité de page insuffisante » dans Webmaster** signifie généralement un contenu pauvre sur des pages générées automatiquement, et non une erreur technique
- **Les modifications des développeurs peuvent silencieusement casser le SEO** : le meta-scanner détecte les problèmes avant la chute du trafic

## Voir aussi {#see-also}
- [[robots-txt-sitemaps-indexation]] - robots.txt, sitemap.xml et analyse approfondie de l'indexation
- [[core-web-vitals-performance]] - Vitesse de chargement et Core Web Vitals
- [[site-structure-urls]] - Règles d'URL et validation de la structure
- [[seo-analytics-reporting]] - Workflow de surveillance et de diagnostic
