---
title: "Analyse SEO et reporting"
category: techniques
tags: [seo-marketing, analytics, kpis, reporting, position-tracking, traffic-analysis, monitoring]
level: 3
source_sha256: 92318ddc560a413f7ab81f85c9bc7e01149623922f9afb8a1dd8baf56e108f2a
translation: machine
translated_at: '2026-10-24'
---
# Analyse SEO et reporting {#seo-analytics-and-reporting}

Système de pilotage de projet : indicateurs KPI, structure du reporting mensuel, surveillance par meta-scanner, construction d'hypothèses en cas de baisse de trafic et gestion des tâches.

## Mise en place du projet {#project-setup}

### Avec un historique existant {#with-existing-history}
1. Obtenir l'accès à : Yandex Metrika, Yandex Webmaster, Google Analytics, Google Search Console
2. Extraire les requêtes générant du trafic depuis Webmaster et Metrika
3. Ajouter ces requêtes au suivi de positions (Rush Analytics ou équivalent)

### Nouveau projet {#new-project}
1. Ajouter le site à : Metrika, Webmaster, GA, GSC
2. Collecter ou générer manuellement la liste initiale de requêtes
3. Ajouter ces requêtes au suivi de positions

## Routine de surveillance quotidienne {#daily-monitoring-routine}

Chaque matin (5 à 10 minutes) :
1. Ouvrir Yandex Metrika
2. Ouvrir Yandex Webmaster
3. Ouvrir Google Search Console
4. Vérifier que tout est en ordre

## Indicateurs KPI principaux {#core-kpi-metrics}

### 1. Trafic + segments {#1-traffic-segments}
- Trafic organique total
- Par moteur de recherche (Yandex, Google)
- Par type (marque vs hors marque)
- Par région (niveau ville)
- Taux de conversion par segment

### 2. Indexation + segments {#2-indexation-segments}
**Processus** : explorer le site -> segmenter par type de page -> vérifier l'indexation dans Rush Analytics -> identifier les anomalies.

Suivre par type de page : catégories, tags, marques, pagination, fiches produit.

**Remarque** : l'index de Google est généralement environ 30 % plus grand que celui de Yandex.

### 3. Liens + segments {#3-links-segments}
Suivre : nombre total de domaines et de pages donneurs, indicateurs des pages prioritaires, indicateurs des concurrents, dynamique des évolutions.

### 4. Visibilité {#4-visibility}
**Définition** : pourcentage estimé du trafic réalisable, compte tenu des fréquences du noyau sémantique et des positions actuelles.

**Mise en place** : segmenter les requêtes en projets, regrouper les segments, charger dans l'outil de suivi, suivre la dynamique des concurrents.

**Calendrier** : tous les concurrents tous les 3 à 6 mois ; audit approfondi des concurrents en croissance tous les 6 mois.

### 5. Positions + segments {#5-positions-segments}
Pourcentage de requêtes dans le TOP-3, TOP-5, TOP-10 par moteur de recherche. Moins utile que la visibilité, mais permet de repérer des tendances.

## Meta-scanner (surveillance des modifications de pages) {#meta-scanner-page-change-monitoring}

**Objectif** : détecter les modifications de pages avant qu'elles n'affectent le trafic.

**Fonctionnement** :
1. Charger les données actuelles comme référence de base
2. Le service effectue des contrôles à intervalles réguliers
3. Écart détecté -> notification push
4. Correction avant tout impact sur le trafic

**Éléments surveillés** : Title, Description, H1, URL, Meta robots, Canonical, robots.txt, contenu textuel.

**Intérêt** : un développeur déploie un robots.txt défectueux -> notification push le lendemain -> correction immédiate -> le trafic n'a jamais chuté.

## Structure du reporting mensuel {#monthly-report-structure}

Établir un rapport maître par mois :

1. **Dynamique des positions** : top-10, nombre dans le top-3, tendance de la visibilité
2. **Trafic organique** : sessions par rapport au mois précédent et en glissement annuel
3. **Conversions d'objectifs** : prospects, achats issus du référencement naturel
4. **Santé technique** : nouvelles erreurs d'exploration, évolutions de l'indexation
5. **Travaux réalisés** : liste de toutes les modifications mises en œuvre
6. **Plan du mois suivant**

Garder les rapports concis : un résumé de 1 à 2 pages avec graphiques est plus efficace qu'un document de 10 pages.

## Construction d'hypothèses en cas de baisse de trafic {#hypothesis-building-for-traffic-drops}

### Approche par analyse segmentée {#segmented-analysis-approach}

**Exemple de chute brutale** :
1. Le trafic chute
2. Segmenter par type de page
3. Les pages de marque chutent spécifiquement
4. Investiguer les pages de marque
5. Le modèle de title a cassé sur les pages de marque
6. Corriger avec l'équipe de développement

**Exemple de déclin progressif** :
1. Le trafic diminue progressivement
2. Vérifier les indicateurs principaux
3. L'indexation diminue
4. Segmenter l'indexation
5. Les pages de tags perdent leur indexation
6. Le développeur les a fermées par erreur via la meta robots
7. Corriger

### Diagnostic d'une baisse de positions {#position-drop-diagnosis}
1. **Ne pas paniquer** (première règle)
2. Identifier la nature :
   - **Baisse généralisée** (toutes les pages) -> problème technique (robots.txt, sitemap, serveur)
   - **Baisse segmentée** (un type précis) -> problème de texte ou technique pour ce gabarit
   - **Baisse ponctuelle** (une seule page) -> problème de texte ou de liens pour cette page

## Gestion des tâches {#task-management}

**Premiers mois** (nombreux briefs et tâches) :
- Identifier 3 à 5 tâches prioritaires
- Vérifier le statut en continu
- Planifier chaque mois, comparer le prévu et le réalisé en fin de mois
- Suivre les tâches bloquées

## Calendrier des audits récurrents {#repeat-audit-schedule}

| Taille du projet | Audit technique | Visibilité des concurrents |
|--------------|-----------------|----------------------|
| Petit | Pas de répétition | Tous les 3 à 6 mois |
| Moyen | Tous les 3 à 6 mois | Tous les 3 à 6 mois |
| Grand | Mensuel | Tous les 3 à 6 mois |

## Outils d'analyse {#analytics-tools}

| Indicateur | Outil principal | Alternative |
|--------|-------------|-------------|
| Trafic | Yandex Metrika + GA4 | - |
| Positions | Rush Analytics | Serpstat, SE Ranking |
| Indexation | Yandex Webmaster + GSC | - |
| Prospects/ventes | CRM (AmoCRM, TildaCRM) | Google Sheets |
| Multi-canal | Roistat, Utmstat | - |

### Configuration du suivi de positions Rush Analytics {#rush-analytics-position-tracking-setup}
1. Créer le projet : nom + URL de domaine complète
2. Ajouter le moteur cible + la région (ex. Yandex/Russie/Moscou)
3. Ajouter Google avec la même région
4. Ajouter desktop et mobile (SERP distincts)
5. Définir un suivi quotidien (recommandé)
6. Importer la liste de mots-clés (minimum 20 à 50 requêtes)
7. Lancer la première vérification ; configurer les vérifications récurrentes

## Synthèse : système de pilotage {#summary-control-system}

**Mise en place au démarrage** : connecter tous les outils, configurer le meta-scanner, ajouter les requêtes au suivi, segmenter les requêtes.

**Mensuel** : trafic + indexation + liens + visibilité + positions (tout segmenté).

**Opérationnel** : 3 à 5 tâches prioritaires, suivre les tâches bloquées, vérification quotidienne du matin.

**Périodique** : audit technique selon le calendrier, visibilité des concurrents tous les 3 à 6 mois.

## Pièges à éviter {#gotchas}
- **Ne pas paniquer en cas de baisse de trafic** - segmenter d'abord, diagnostiquer ensuite, agir en dernier
- **L'index de Google est environ 30 % plus grand que celui de Yandex** - c'est normal, ce n'est pas une erreur
- **Les positions sont moins utiles que la visibilité** - les positions fluctuent au quotidien, la visibilité montre les tendances
- **Le meta-scanner est rentabilisé dès la première détection** - erreurs de développeur détectées en 1 jour au lieu de 2 à 3 semaines
- **La distinction trafic de marque / hors marque est essentielle** - la croissance du trafic de marque peut masquer le déclin du trafic hors marque
- **Les rapports mensuels doivent être concis** - les clients lisent des résumés de 2 pages, pas des documents de 10 pages

## Voir aussi {#see-also}
- [[seo-tools-workflow]] - Configuration et mise en place des outils
- [[technical-seo-audit]] - Méthodologie d'audit
- [[seo-strategy-by-site-type]] - La stratégie guide le choix des KPI
- [[behavioral-factors-ctr]] - Indicateurs comportementaux dans l'analyse
