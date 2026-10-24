---
title: "Mécanique des moteurs de recherche"
category: concepts
tags: [seo-marketing, search-engines, crawling, indexing, ranking, relevance]
level: 3
source_sha256: e3dca74ae901ea1f5c189ebd6fa0d195507d4e28fe93924947c122eb670dcbeb
translation: machine
translated_at: '2026-10-24'
---
# Mécanique des moteurs de recherche {#search-engine-mechanics}

Comment les moteurs de recherche découvrent, traitent et classent les documents web. Couvre l'exploration (crawling), le pipeline d'indexation, le traitement linguistique et les grands groupes de facteurs de classement qui déterminent les positions dans les SERP.

## Terminologie clé {#key-terminology}

- **Document** - une page web (pas un site) ; l'unité fondamentale de la recherche
- **Collection** - ensemble total des documents indexés (environ 13,5 milliards chez Yandex)
- **Terme** - un mot unique
- **Requête** - texte saisi dans le champ de recherche
- **Intention** - ce que l'utilisateur veut réellement (pas seulement ce qu'il a tapé)
- **Pertinence** - degré de correspondance entre un document et l'intention de l'utilisateur exprimée par la requête

## Architecture d'exploration {#crawling-architecture}

**Crawler (bot/robot/spider de recherche)** - programme qui trouve et parcourt les sites en suivant les liens, et stocke le contenu dans la base du moteur de recherche.

### Mécanismes de contrôle du crawler {#crawler-control-mechanisms}
1. `robots.txt` - règles d'autorisation et d'interdiction d'accès pour les bots
2. `sitemap.xml` - plan des pages à explorer
3. Yandex Webmaster / Google Search Console - gestion directe
4. Balises meta robots, canonical, x-robot-tag, noindex/nofollow
5. Flux RSS
6. Fichier YML (format de catalogue produits de Yandex)
7. IndexNow / Google Indexing API - notifications push instantanées

## Traitement linguistique {#linguistic-processing}

### Lemmatisation {#lemmatization}
Toutes les formes d'un mot sont ramenées à leur forme de base (lemme). Cela permet de faire correspondre les requêtes aux documents quelle que soit la flexion.

### Index inversé {#inverted-index}
Pour chaque terme, parmi l'ensemble des documents, il stocke les documents qui contiennent ce terme.

```yaml
Direct:   Document 1 → [word_a, word_b, word_c]
Inverted: word_a → [Document 1, Document 3]
          word_b → [Document 1, Document 2]
```

**Recherche booléenne** : `Cat AND Hare AND NOT Fox` - trouve tous les documents correspondant à l'expression.

### Réécriture de requête {#query-rewriting}
- **Query rewrite** - modification des poids de chaque mot de la requête pour améliorer les résultats
- **Query reformulation** - ajout automatique de synonymes à la requête
- Exemple : « what is seo » réécrite pour inclure « means », « abbreviation », « stands for »

## Groupes de facteurs de classement {#ranking-factor-groups}

Plus de 2000 facteurs existent. Ils sont regroupés en catégories :

### Facteurs textuels (internes) {#text-factors-internal}
- Fréquence des termes dans les zones du document (TF-IDF, BM25)
- Unicité du texte
- LSI (latent semantic indexing - termes apparentés)
- Longueur du texte, qualité grammaticale
- Présence directe des mots-clés et des permutations de mots

### Facteurs de liens (externes) {#link-factors-external}
- Composition de la liste des ancres
- Taux de croissance des liens et nombre total de backlinks
- Autorité et nombre de domaines référents
- Similarité thématique entre le donneur et le receveur
- Indicateur de « vendabilité » commerciale du donneur

### Facteurs commerciaux (internes) {#commercial-factors-internal}
- Taille de l'assortiment de produits ou services
- Options de paiement et de livraison
- Garantie et politique de retour, visibilité des prix
- Catalogue structuré, plusieurs moyens de contact
- Éléments de conversion (CTA, formulaires, demande de rappel)

### Facteurs d'hôte (internes) {#host-factors-internal}
- Âge du domaine, nombre de pages indexées
- Historique des changements de propriétaire du domaine
- Zone du domaine (.ru, .com, etc.)

### Facteurs techniques (internes) {#technical-factors-internal}
- Codes de réponse du serveur, validité du code
- Vitesse de chargement des pages, HTTPS
- Contenu dupliqué et redirections

### Facteurs comportementaux {#behavioral-factors}
- **Internes (sur le site)** : temps passé sur le site, profondeur de navigation, taux de rebond
- **Externes (dans la SERP)** : dernier clic, clic unique, retours par saisie directe, CTR du snippet

## Priorité de classement par moteur de recherche {#ranking-priority-by-search-engine}

| Groupe de facteurs | Priorité Yandex | Priorité Google |
|-------------|----------------|----------------|
| Comportementaux | n° 1 (la plus élevée) | n° 3 |
| Textuels | n° 2 | n° 2 |
| Liens | n° 3 | n° 1 (la plus élevée) |
| Commerciaux | n° 4 | n° 4 |
| Techniques | fondamentaux | fondamentaux |

## Filtre Sandbox {#sandbox-filter}

Filtre temporaire appliqué aux nouveaux sites pour empêcher la manipulation :
- Durée : 2 à 12 mois selon le site
- Concerne presque tous les sites nouvellement créés
- Objectif : écarter les sites créés par des méthodes black-hat

## Pièges courants {#gotchas}
- **Les priorités Yandex et Google sont inversées** : les liens dominent chez Google, les facteurs comportementaux dominent chez Yandex. La stratégie doit en tenir compte
- **2000+ facteurs** ne signifie pas que tous ont le même poids : une poignée de facteurs par type de requête explique plus de 80 % de la variance du classement
- **Pertinence != nombre de mots-clés** : les moteurs modernes utilisent une compréhension sémantique, pas seulement la correspondance de termes
- **Le Sandbox s'applique à tous** : même les nouveaux sites légitimes subissent 2 à 12 mois de classement freiné

## Voir aussi {#see-also}
- [[ranking-algorithms-history]] - Chronologie des algorithmes et évolution des réseaux de neurones
- [[text-optimization]] - Zones du document et scoring de pertinence
- [[behavioral-factors-ctr]] - Étude approfondie des facteurs comportementaux
- [[commercial-ranking-factors]] - Facteurs commerciaux et E-E-A-T
