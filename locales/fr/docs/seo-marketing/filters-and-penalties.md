---
title: "Filtres et pénalités des moteurs de recherche"
category: reference
tags: [seo-marketing, filters, penalties, baden-baden, minusinsk, penguin, panda, ymyl]
level: 3
source_sha256: 741a4ceba15a28ba7bc5e63fc5b33593f608c2bac8933fd847114bf1115e97c8
translation: machine
translated_at: '2026-10-24'
---
# Filtres et pénalités des moteurs de recherche {#search-engine-filters-and-penalties}

Référence complète des filtres de Yandex et de Google, de leurs déclencheurs, de leurs symptômes, de leurs méthodes de diagnostic et des procédures de rétablissement.

## Diagnostic d'une baisse de trafic {#traffic-drop-diagnostics}

Lorsque les analyses montrent une baisse de trafic :
1. Vérifier si la page est indexée : `url:site.ru/the-dropped-document/`
2. Vérifier la validité de la copie enregistrée dans le moteur de recherche
3. Vérifier le niveau d'imbrication
4. Analyser la nature de la baisse :
   - **Baisse de l'hôte** -> vérifier les sanctions
   - **Baisse de la page** -> vérifier : modification de la page pertinente, sanctions du document, problèmes de texte, problèmes de liens

## Ce que les moteurs de recherche sanctionnent {#what-search-engines-penalize-for}
1. Problèmes de qualité du texte (spam, contenu pauvre)
2. Tromperie des utilisateurs sur le site
3. Manipulation des facteurs comportementaux
4. Affiliation : plusieurs sites commerciaux d'un même propriétaire
5. Manipulation des liens
6. Tromperie du moteur de recherche
7. Contenu pornographique, publicité intrusive
8. Piratage, vol de contenu

## Où vérifier le statut des filtres {#where-to-check-filter-status}
- **Yandex Webmaster** -> section « Violations »
- **Google Search Console** -> « Actions manuelles »

### Types de portée des filtres {#filter-scope-types}
- Requête-document, document, domaine, suppression de page/section, suppression de domaine
- Par type : automatique ou manuel

## Filtres Yandex {#yandex-filters}

### Baden-Baden {#baden-baden}
**Date** : mars 2017 | **Type** : automatique | **Portée** : requête-document et domaine

**Déclencheurs** : spam de densité de mots-clés, volume de texte excessif, texte caché, faible qualité du texte.

**Symptômes** :
- Au niveau de la requête : chute brutale d'un groupe de requêtes (et non de toutes) de 5 à 40 positions ; le document reste positionné pour d'autres requêtes
- Au niveau de l'hôte : chute brutale de TOUTES les requêtes de plus de 20 positions ; seules les requêtes de marque subsistent ; notification dans Webmaster

**Diagnostic** : `arsenkin.ru/tools/filter/` ; une chute massive de plus de 10 positions = probablement Baden-Baden.

**Suppression** :
- Au niveau de la requête : ajouter d'abord la balise `<noindex>`, puis réécrire ; réduire le nombre d'occurrences des mots-clés et le volume de texte ; si rien ne fonctionne -> supprimer le texte
- Au niveau de l'hôte : **SEULE LA SUPPRESSION DU TEXTE** fonctionne, rien d'autre n'est efficace

### Minusinsk {#minusinsk}
**Date** : mai 2015 | **Type** : automatique | **Portée** : domaine

**Déclencheurs** : manipulation de liens pour promouvoir le site.

**Ce qui est considéré comme un lien SEO** : presque tous les liens d'ancre vers le site commercial ; 95 % des liens provenant de places d'échange connues ; même les liens sans ancre provenant de places d'échange.

**Suppression** :
1. Supprimer TOUS les liens SEO en une seule fois
2. Attendre la réindexation des pages donatrices
3. Le filtre est levé en 1 à 8 mois
4. Le trafic se rétablit entièrement si le site est de haute qualité
5. Le support Yandex peut montrer des exemples de liens détectés

### Manipulation des facteurs comportementaux {#behavioral-factor-manipulation}
**Date** : juillet 2011 | **Portée** : domaine | **Type** : manuel ou automatique

**Symptômes** :
- Automatique : -30 à -40 positions sur l'ensemble du site, à l'exception de la marque (sans notification)
- Manuel : notification dans Webmaster -> Diagnostic -> Sécurité et violations

**Caractéristiques** :
- Sanctions les plus sévères chez Yandex
- Levée de l'interdiction 6 à 8 mois APRÈS l'aveu de la manipulation
- **Sortie rapide** : redirection 301 vers un autre domaine
- **Ne jamais donner l'accès à Webmaster/Metrika à des tiers**

### Clickjacking {#clickjacking}
**Date** : décembre 2015 | **Portée** : domaine | **Type** : automatique

**Déclencheur** : éléments invisibles collectant les données des utilisateurs sans consentement.

**Suppression** : cesser d'utiliser des services d'exploitation ; cliquer sur « J'ai tout corrigé » dans Webmaster ; levée dans un délai de 30 jours.

### Filtre de réputation {#reputation-filter}
**Date** : octobre 2021 | **Portée** : domaine | **Type** : automatique

**Déclencheur** : avis négatifs, appels téléphoniques frauduleux via la téléphonie SIP. Chute de 15 à 30 positions.

### Filtre d'affiliation {#affiliate-filter}
**Type** : manuel

**Déclencheur** : 2 sites commerciaux ou plus appartenant à une même entreprise pour des produits ou services identiques.

**Comment éviter le problème avec plusieurs sites** :
- Hébergeurs et bureaux d'enregistrement différents
- Enregistrement au nom de personnes différentes
- Gamme et prix différents
- Conventions de nommage des produits différentes
- Webmaster/Metrika sur des comptes différents (ordinateur ou machine virtuelle distincts)
- Coordonnées différentes
- Publicité depuis des comptes différents

### Autres filtres Yandex {#other-yandex-filters}
- **Notifications d'abonnement intrusives** (janvier 2019)
- **Publicité agressive** (avril 2019) - principalement la monétisation Adsense ; blocs publicitaires déguisés en navigation

## Filtres Google {#google-filters}

### Google Panda {#google-panda}
**Date** : février 2011 | **Portée** : document et domaine | **Type** : automatique

**Déclencheurs** : contenu de faible qualité, contenu volé ou dupliqué, duplication interne.

**Rétablissement** : repérer les pages sans trafic via GSC/GA ; réécrire (supprimer le copier-coller, le spam) ; ajouter du contenu de qualité, des images, des vidéos ; ajouter des contenus générés par les utilisateurs modérés.

### Google Fred {#google-fred}
**Date** : mars 2017 | **Portée** : domaine | **Type** : automatique

**Déclencheurs** : faible qualité du contenu, liens de faible qualité, publicité excessive, absence de valeur ajoutée.

**Rétablissement** : réduire les blocs publicitaires ; améliorer le profil de liens ; ajouter des services à valeur ajoutée (calculateurs, tests).

### YMYL (Your Money or Your Life) {#ymyl-your-money-or-your-life}
**Date** : août 2018 | **Portée** : domaine | **Type** : automatique

**Niches YMYL** : finance, médical, juridique, sécurité des enfants, sécurité routière.

**Rétablissement via E-A-T** : certificats, preuves et justificatifs, liens faisant autorité, qualité du contenu, grammaire, gamme de produits, informations sur l'achat et la livraison.

### Google Penguin {#google-penguin}
**Date** : avril 2012 | **Portée** : requête-document | **Type** : automatique

**Déclencheurs** :
- Nombre élevé d'ancres commerciales
- Répartition anormale des ancres (aucune ancre de marque)
- Liens uniquement vers la page d'accueil ou vers un petit nombre de pages
- Part élevée de liens achetés ou de faible qualité

**Rétablissement** :
- Supprimer les mauvais liens, modifier le profil de liens
- Répartir les liens sur l'ensemble de l'hôte
- Augmenter la part des liens sans ancre à plus de 20 %
- Diluer le spam d'ancres avec des liens sans ancre
- Désavouer les mauvais liens dans Google Disavow Links

### Spam de micro-balisage {#micromarkup-spam}
**Date** : 2016 | **Portée** : document | **Type** : automatique

**Déclencheur** : abus de micro-balisage pour manipuler les extraits. Vérifier tous les types et supprimer les balisages inappropriés.

### DMCA (piratage) {#dmca-piracy}
**Date** : 2012 | **Portée** : document

**Déclencheur** : copie de contenu provenant d'autres sites. Supprimer le contenu non unique, demander la levée du filtre.

### Domaine à correspondance exacte (EMD) {#exact-match-domain-emd}
**Date** : 2012 | **Portée** : domaine | **Type** : automatique

**Déclencheur** : expression commerciale mot-clé dans le nom de domaine. Correction : changer de domaine avec une redirection 301. Prévention : ne pas utiliser plus d'un mot-clé dans le nom de domaine.

## Tableau de référence des filtres {#filter-reference-table}

| Filtre | Moteur | Portée | Type | Déclencheur principal |
|--------|--------|--------|------|-----------------------|
| Baden-Baden | Yandex | Requête-doc/domaine | Auto | Spam de texte |
| Minusinsk | Yandex | Domaine | Auto | Manipulation de liens |
| Clickjacking | Yandex | Domaine | Auto | Collecte de données invisible |
| Comportemental | Yandex | Domaine | Manuel/Auto | Clics de robots/payants |
| Réputation | Yandex | Domaine | Auto | Avis négatifs/arnaque |
| Affiliation | Yandex | Domaine | Manuel | Plusieurs sites, même niche |
| Panda | Google | Doc/domaine | Auto | Faible qualité/doublons |
| Fred | Google | Domaine | Auto | Faible qualité + publicité excessive |
| YMYL | Google | Domaine | Auto | Déficit d'E-A-T |
| Penguin | Google | Requête-doc | Auto | Spam de liens |
| Micro-balisage | Google | Document | Auto | Manipulation du balisage |
| DMCA | Google | Document | - | Violation du droit d'auteur |
| EMD | Google | Domaine | Auto | Domaine-mot-clé |

## Points d'attention {#gotchas}
- **Baden-Baden au niveau de l'hôte : supprimer UNIQUEMENT le texte** - réécrire ne fonctionne pas, seule la suppression complète est efficace
- **Minusinsk calcule par hôte, et non par page** - un seul mauvais lien par domaine compte autant que 100
- **La manipulation comportementale est la sanction la plus sévère** - interdiction de 6 à 8 mois sans autre solution que le changement de domaine
- **Le filtre d'affiliation exige une séparation extrême** - même des analyses sur le même compte peuvent déclencher la détection
- **Penguin agit au niveau requête-document** - certaines pages peuvent se rétablir alors que d'autres restent pénalisées
- **EMD compte toujours** - évitez de placer plus d'un mot-clé commercial dans le nom de domaine

## Voir aussi {#see-also}
- [[link-building-strategy]] - Stratégies de liens qui évitent les pénalités
- [[text-optimization]] - Optimisation du texte dans des limites sûres
- [[behavioral-factors-ctr]] - Bonnes pratiques pour les facteurs comportementaux
- [[commercial-ranking-factors]] - E-A-T pour le rétablissement YMYL
