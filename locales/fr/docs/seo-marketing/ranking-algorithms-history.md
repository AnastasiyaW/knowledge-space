---
title: "Historique des algorithmes de classement"
category: concepts
tags: [seo-marketing, algorithms, yandex, google, neural-networks, bert, yati]
level: 3
source_sha256: 88d9fc948e6601fe5439d13a68466b96fabe22efcb89164801ebb0f19ff833a0
translation: machine
translated_at: '2026-10-24'
---
# Historique des algorithmes de classement {#ranking-algorithms-history}

Chronologie des principales mises à jour des algorithmes de moteurs de recherche, pour Yandex et Google, depuis le classement heuristique jusqu'aux systèmes fondés sur les réseaux de neurones.

## Chronologie des algorithmes Yandex {#yandex-algorithm-timeline}

| Algorithme | Année | Importance |
|-----------|------|-------------|
| Filtre Nepot | 2005 | Annulait le poids du lien lorsque celui-ci était jugé commercial ou payant |
| Magadan | 2008 | Début de l'ère des algorithmes nommés ; dépendance géographique ; reconnaissance de l'unicité du texte |
| Filtre ACS | 2009 | Sanctions pour les contenus générés automatiquement de faible qualité |
| Snozhinks | 2009 | Introduction de Matrixnet (ML) ; pénalisation des textes à bourrage de mots-clés |
| Krasnodor | 2010 | Technologie « Spectrum » : classe les requêtes selon différentes intentions |
| Baden-Baden | 2017 | Pénalité pour les contenus sur-optimisés présentant une densité excessive de mots-clés |
| YATI | 2020 | Analyse de texte fondée sur les transformers ; amélioration majeure du NLP |
| Y1 | 2021 | Mise à jour majeure (+2000 améliorations) ; YaTI basé sur les transformers + YaLM |

## Évolution des réseaux de neurones chez Yandex {#yandex-neural-network-evolution}

### Avant 2016 : l'ère heuristique {#pre-2016-heuristic-era}
Algorithmes heuristiques, facteurs basés sur des tables, signaux limités au contenu.

### 2016-2018 : Palekh et Korolev {#2016-2018-palekh-and-korolev}
- Fondés sur le Deep Structured Semantic Model (DSSM)
- **Palekh** : compare la requête au titre du document
- **Korolev** : étend la comparaison à l'ensemble du contenu de la page ; intègre les avis des évaluateurs

### 2019 : réseaux de neurones entraînés sur l'évaluation d'experts {#2019-expert-assessment-neural-networks}
Cibles d'entraînement fondées sur les notations de qualité attribuées par des experts.

### 2020 et après : YATI (Yandex Attention to Intent) {#2020-yati-yandex-attention-to-intent}
- Architecture transformer
- Flux multiples : liste d'ancres, index d'URL fondé sur les clics
- Prise en compte de textes plus longs : les textes allant jusqu'à 10 phrases sont traités intégralement
- Espace vectoriel de mots pour la compréhension sémantique

### Yandex Proxima (métrique de qualité) {#yandex-proxima-quality-metric}
Combine des signaux commerciaux, de conversion et d'experts :
- Composantes de qualité commerciale
- Qualité propre à chaque domaine (médecine, droit, finance)
- Signaux de valeur pour l'utilisateur : expertise, autorité, fiabilité

## Chronologie des algorithmes Google {#google-algorithm-timeline}

| Algorithme | Année | Importance |
|-----------|------|-------------|
| Panda | 2011 | Pénalise les contenus minces, dupliqués ou de faible qualité ; a touché 12 % des résultats |
| Penguin | 2012 | Pénalise les liens spam, les fermes de liens et les schémas de liens achetés |
| Hummingbird | 2012 | Compréhension sémantique des requêtes ; le contexte prime sur les mots-clés isolés |
| RankBrain | 2015 | Composant de ML ; pertinence des pages selon le sens, sans correspondance exacte |
| Mobile-Friendly | 2015 | Les pages optimisées pour mobile sont prioritaires dans la recherche mobile |
| Mobile-First Index | 2018 | La version mobile sert de référence principale pour l'indexation |
| BERT | 2019 | Analyse bidirectionnelle du contexte ; prise en compte des prépositions et du sens de la phrase complète |
| Core Web Vitals | 2020 | LCP, FID/INP et CLS comme signaux de classement |

## Cadre E-E-A-T de Google {#google-e-e-a-t-framework}

Initialement E-A-T, puis étendu à E-E-A-T :
- **E (Experience)** : expérience directe et de première main du sujet
- **E (Expertise)** : connaissance de niveau expert du sujet
- **A (Authoritativeness)** : autorité de l'auteur et du site dans leur niche
- **T (Trustworthiness)** : fiabilité du site : contenu de qualité, coordonnées complètes, informations de paiement et de livraison

Les sites YMYL (santé, finance, droit, sécurité) sont soumis aux exigences E-E-A-T les plus strictes depuis 2018.

## BERT de Google (2019) {#google-bert-2019}

Bidirectional Encoder Representations from Transformers : traite le contexte de la requête, y compris les prépositions et la phrase complète, et non seulement les mots-clés isolés. Marque le passage de la correspondance de mots-clés à la compréhension sémantique.

## Faits clés {#key-facts}
- Yandex utilise plus de 2000 facteurs de classement
- Les mises à jour des algorithmes de Google ciblent de plus en plus la qualité du contenu et l'intention de l'utilisateur
- Les deux moteurs ont convergé vers des architectures fondées sur les transformers pour la compréhension sémantique
- Les niches YMYL sont soumises aux exigences de qualité les plus strictes sur les deux plateformes

## Pièges courants {#gotchas}
- **Les noms des algorithmes comptent pour le diagnostic** : lorsque le trafic chute, corréler la date avec les déploiements connus d'algorithmes est le moyen le plus rapide d'identifier la cause
- **YATI a tout changé pour Yandex** : les conseils d'optimisation de texte pour Yandex antérieurs à 2020 sont largement obsolètes
- **E-E-A-T n'est pas un facteur de classement direct** : c'est un cadre de qualité utilisé par des évaluateurs humains dont les notations servent à entraîner les algorithmes
- **Mobile-First signifie que le mobile EST l'index** : un contenu uniquement visible sur desktop et absent de la version mobile risque de ne pas être indexé du tout

## Voir aussi {#see-also}
- [[search-engine-mechanics]] - Groupes de facteurs de classement principaux
- [[filters-and-penalties]] - Algorithmes de pénalité spécifiques
- [[commercial-ranking-factors]] - Détail de E-A-T et des facteurs commerciaux
- [[text-optimization]] - Fonctionnement du calcul de pertinence textuelle
