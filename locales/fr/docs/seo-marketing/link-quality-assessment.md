---
title: "Évaluation de la qualité des liens"
category: techniques
tags: [seo-marketing, link-quality, outreach, pbn, drop-domains, donor-evaluation, link-audit]
level: 3
source_sha256: 17219edacf8607fdba75916525fa65bd09eab3528e46d523bd0f1ec7e0b40981
translation: machine
translated_at: '2026-10-24'
---
# Évaluation de la qualité des liens {#link-quality-assessment}

Critères d'évaluation des donneurs de liens, méthodologie d'outreach, utilisation des PBN (Private Blog Network), stratégies avec les drop domains et procédures d'audit des liens.

## Outreach {#outreach}

Contact direct avec des sites pour acheter ou négocier le placement d'un article contenant un lien.

**Avantages** : pousse activement les requêtes vers le TOP ; améliore l'ensemble du site grâce à des liens faisant autorité ; bonne indexation.

**Inconvénients** : coûteux ; chronophage ; difficile à contrôler ; environ 20 % de risque d'arnaque.

### Critères de sélection des donneurs {#donor-selection-criteria}
- Dynamique de croissance des liens actifs dans Ahrefs
- Thématique proche de la vôtre ou adjacente, + média
- DR >= 20, trafic >= 1000, index >= 100 pages
- Pas de niches spam (adulte, pharma) dans l'index
- Pas d'articles étiquetés « contenu sponsorisé » / « publicité »
- Possède des requêtes de votre niche dans le TOP
- Design soigné (pas de style années 90)
- Liens entrants de qualité depuis le contenu
- Pas de mots spam dans le code source
- Contenu de qualité, nouveaux articles réguliers
- Non créé uniquement pour vendre des liens

## Liens sitewide dynamiques {#dynamic-sitewide-links}

Un même donneur place différents liens vers votre site depuis différentes pages, avec des ancres variées.

### Règles de mise en place {#setup-rules}
- 10 à 20 liens vers une de vos pages (depuis différentes pages du donneur)
- Ancres différentes par cluster de requêtes
- 1 lien par ancre/requête
- ~30 % de dilution pour Google (URL, marque, toponyme)
- Pas de liens en double sur une même page du donneur
- Ne pas placer de liens depuis TOUTES les pages du donneur
- Maximum 3 à 4 sites « voisins » par page du donneur
- Le donneur doit faire autorité : portails, sites d'actualité, sites régionaux

## PBN (Private Blog Network) {#pbn-private-blog-network}

Réseau géré de sites destiné à renforcer le domaine principal.

### Quand l'utiliser {#when-to-use}
- Niches black/gray
- Niches très concurrentielles
- Boosts ponctuels pour les requêtes HF/ultra-HF dans les niches white
- Généralement non rentable sur le marché russe pour la plupart des niches

### Exigences de qualité {#quality-requirements}
- PBN : DR 5, TF 8, CF/TF > 1,8 ; archive web préférée
- Money site : DR 15, TF 15, CF/TF > 2
- Glue : similaire au PBN, légèrement inférieur si très spécialisé

### Règles {#rules}
- Volume du PBN <= 10 à 30 % du profil de liens total (boost ponctuel uniquement)
- Les liens doivent s'intégrer naturellement au site
- Pas de PBN sur les jeunes sites sans dilution, surtout pendant les 6 premiers mois
- Ne pas acheter de réseaux bon marché auprès de webmasters non vérifiés

## Stratégies avec les drop domains {#drop-domain-strategies}

### Qu'est-ce qu'un drop domain {#what-drop-domains-are}
Un domaine existant mais abandonné, conservant une valeur résiduelle : ancienneté, confiance, backlinks, index des requêtes.

### Redirection 301 / Glue {#301-redirect-glue}
Redirection depuis le drop domain vers votre site. Transfère les liens, l'ancienneté et la confiance.

**Objectif** : booster l'ensemble de l'hôte avec une masse de liens ; rattacher l'ancienneté du domaine ; booster la page promue ; augmenter la confiance de Google.

**Critères de sélection** :
- Domaine solide avec des liens provenant de sources difficiles à obtenir (.gov, sites de niche, sites concurrents)
- Très proche de votre thématique (ou adjacent et très autoritaire)
- Idéalement un domaine d'enchère (ancienneté préservée)
- Domaine présent dans l'index et positionné

### Protocole de test avant application {#testing-protocol-before-applying}
1. Acheter le domaine
2. Trouver un concurrent dans le TOP 20-30 pour vos requêtes
3. Suivre les positions du concurrent
4. Appliquer la redirection vers le concurrent (de la même manière que pour votre propre site)
5. Surveiller pendant 2 à 4 semaines
6. Si croissance -> rediriger vers votre site
7. Si aucune réaction -> ne pas utiliser
8. Si le concurrent chute -> supprimer la redirection, abandonner le domaine

### Mise en place de la redirection {#redirect-setup}
- Installer un .htaccess antibot sur le drop domain (bloquer les crawlers au départ)
- 301 : page d'accueil -> page d'accueil ; autres pages -> page d'accueil OU selon une table de redirection
- Rediriger manuellement les pages qui ont les liens les plus forts
- Option : rediriger un drop thématiquement proche vers la catégorie pertinente

### Où les trouver {#where-to-find}
- mydrop.io, expired.ru, reg.ru, nic.ru, dropmonitor.ru
- Analyse des archives web via rush-analytics.ru
- Analyse des backlinks depuis des sites faisant autorité
- Analyse des SERP (top 100 pour les mots-clés -> extraire les domaines -> vérifier le WHOIS)

### Évaluation d'un drop domain {#drop-domain-evaluation}
1. Vérifier manuellement que les 10 à 15 meilleurs liens sont toujours actifs
2. Liens pointant directement (sans chaînes)
3. Dofollow >= 60 %
4. Vérifier la présence de caractères chinois (indicateur de réutilisation)
5. Vérifier les explosions de liens
6. Pharma, gambling, essais, commerce de détail -> passer
7. Beaucoup d'ancres exactes -> passer
8. Archive web existante -> bon signe ; vérifier l'historique des changements de thématique
9. Nombre de drops : plus de 2 réinitialisations -> mauvais signe
10. Vérifier l'IKS et l'index des requêtes via Keys.So

## Audit des liens {#link-audit}

### Points à vérifier {#what-to-check}
1. Quantité (liens, hôtes)
2. Ancres spam et ancres SEO (par hôte)
3. Dynamique de croissance des liens (en particulier les liens SEO)
4. Donneurs saturés de spam qui se vendent activement sur les plateformes d'échange
5. Sites cassés, liens Xrumer, liens cachés
6. **Attention particulière aux nouveaux liens**

### Détection automatique des liens spam {#auto-detection-of-link-spam}
1. Exporter depuis Ahrefs + GSC : 1 lien par domaine
2. Vérifier dans Screaming Frog (avec émulation de navigateur) :
   - Recherche personnalisée : regex pour les liens vers votre domaine
   - Recherche personnalisée : mots spam (`viagra|payday|porn`)
3. Rejeter via Google Disavow Links

Alternative : section PBN de Rush-Analytics -> « Spam in links »

## Checklist d'évaluation des donneurs {#donor-quality-checklist}

### Liens articles (Yandex + Google) {#article-links-yandex-google}
- IKS >= 50 (vérifier : be1.ru/yandex-iks/)
- Trafic Google via Ahrefs >= 5 000
- Prix <= 1 000 à 1 500 RUB
- TF >= 5 (Majestic.com)
- Thématique : sujet, adjacent, journaux, médias, portails
- Indexation > 1 000 pages (opérateur `site:`)
- Contrôle spam : `site:site.com "mots spam"` - examiner les résultats
- Trier les restants par trafic ou IKS ; vérifier manuellement :
  - Site actif, articles récents publiés régulièrement
  - Tous les articles ne sont pas commerciaux
  - Ahrefs : les liens sortants ne dépassent pas les pages indexées
  - Ahrefs UR des articles payants != 0

### Liens forums {#forum-links}
- Trafic Google via Ahrefs >= 100
- Indexation > 1 000 pages
- Contrôle spam (identique aux liens articles)
- Forum actif avec des sujets récents réguliers
- Les sujets payants ne doivent pas dominer
- Trouver des forums : `inurl:forum OR inurl:showthread [mot-clé]`

## Plateformes d'échange de liens {#link-exchange-platforms}

Places de marché pour acheter des liens permanents (achat unique) ou en location.

**Règles** :
- Sélection manuelle des donneurs obligatoire
- Planifier les ancres et la dynamique en fonction des concurrents
- Inutile d'acheter des liens à plus de 1 500 à 2 000 RUB
- Ne pas suivre les recommandations de la plateforme
- Ne pas utiliser le « link boosting » (la plateforme envoie des bots -> risque de pénalité)

**Plateformes (RU)** : Miralinks, GGL, pr.Sape

## Outils d'analyse des liens {#link-analysis-tools}

| Outil | Usage |
|------|---------|
| Ahrefs | Base complète de backlinks, analyse des ancres, dynamique, métriques |
| MegaIndex | Gratuit (RU) : ratio liens SEO vs organiques (>40-50 % de SEO = alerte) |
| LinkPad | Analyse des backlinks sur le marché russe |
| Majestic | Métriques Trust Flow / Citation Flow |

## Pièges courants {#gotchas}
- **Toujours tester les drop domains sur un concurrent d'abord** - appliquer une redirection non testée sur votre site peut faire chuter vos positions
- **Taux d'arnaque de 20 % en outreach** - vérifier la qualité du donneur indépendamment avant de payer
- **Un PBN ne doit jamais dépasser 30 % du profil de liens** - à utiliser uniquement comme boost ponctuel
- **Caractères chinois dans l'archive web = domaine réutilisé** - généralement de faible qualité
- **Plus de 2 drops/réinitialisations de domaine = toxique** - écarter ces domaines
- **Les recommandations des plateformes d'échange ne sont pas fiables** - toujours sélectionner les donneurs manuellement

## Voir aussi {#see-also}
- [[link-building-strategy]] - Stratégie de liens globale et composition des ancres
- [[filters-and-penalties]] - Pénalités Minusinsk et Penguin liées aux mauvais liens
- [[seo-analytics-reporting]] - Suivi des liens dans les rapports mensuels
- [[seo-tools-workflow]] - Ahrefs et outils d'analyse des liens
