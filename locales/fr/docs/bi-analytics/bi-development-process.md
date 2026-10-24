---
title: "Processus de développement BI"
category: concepts
tags: [bi-analytics, requirements, dashboard-map, metrics-registry, workflow, stakeholders]
level: 3
source_sha256: eeba7ae76cb4f3f385e38954d0867a3af78c7db44217264de44d583ddc30580f
translation: machine
translated_at: '2026-10-24'
---
# Processus de développement BI {#bi-development-process}

Le processus de développement BI couvre le cycle de vie complet, depuis le recueil des besoins à travers les entretiens avec les parties prenantes, la planification des tableaux de bord avec des maquettes, l'exploration des données, la construction, les itérations et la publication. Suivre un processus structuré évite l'anti-pattern le plus courant : construire la mauvaise chose.

## Faits clés {#key-facts}

- Anti-pattern courant : « Construis juste quelque chose, on verra les détails plus tard » -> boucles de reprise et tableaux de bord inutilisés
- Investir 2 jours dans les besoins permet d'économiser 2 semaines de reprise
- Dashboard Map = maquette + correspondance questions-réponses, réalisée avant d'ouvrir Tableau
- Registre des métriques = source unique de vérité pour toutes les définitions de métriques
- Matrice de compétences de l'analyste BI : 4 niveaux (théorique -> capable d'enseigner aux autres)
- Visualisation = conception de l'information + design graphique + UX + storytelling + maîtrise de l'outil

## Modèles {#patterns}

### Workflow de développement BI {#bi-development-workflow}

1. **Recueil des besoins** - interroger les parties prenantes, documenter les questions et les KPI
2. **Dashboard Map** - maquetter la structure avant de toucher à Tableau
3. **Exploration des données** - comprendre la structure réelle des données, leur granularité, leurs particularités
4. **Préparation des données** - modéliser les jointures, créer les champs calculés (d'abord sur papier)
5. **Construire un MVP** - version minimale, à tester avec les parties prenantes
6. **Itérer** - affiner selon les retours
7. **Publier et documenter** - publier sur le serveur, documenter les sources de données et les métriques

### Entretien de recueil des besoins {#requirements-gathering-interview}

**Questions métier :**
- Quelles décisions ce tableau de bord aide-t-il à prendre ?
- À quelle fréquence est-il utilisé ? (quotidien, hebdomadaire, mensuel)
- Quelles actions découlent de la lecture des données ? (investiguer, escalader, ne rien faire)

**Utilisateurs :**
- Qui sont les utilisateurs ? (chefs de produit, analystes, dirigeants)
- Quel est leur niveau de compétence sur Tableau/BI ?
- Qui fait partie du groupe de test ?

**Questions sur les données :**
- Quelles données sont disponibles ? (tables DWH, fichiers CSV, exports CRM)
- Les données sont-elles propres ou brutes ? Qui les a préparées ?
- Y a-t-il des métriques non additives ? (nécessitent un champ d'échelle séparé, impossible de simplement faire un SUM)
- Y a-t-il des particularités dans les données ? (par ex., une ligne « All Regions » dans le champ région doit être filtrée)

**Calendrier :**
- Date limite ? MVP ou version complète ?

### Dashboard Map (structure) {#dashboard-map-structure}

Planifier avant de construire. Pour chaque élément, définir :
- **Question** que pose l'utilisateur (« Quelle région est en sous-performance ? »)
- **Type de graphique** qui y répond le mieux
- **Champs de données** nécessaires
- **Filtres** applicables

Modèle de structure du tableau de bord :
```text
Level 1: KPI summary (total state, one number per metric)
Level 2: Trend over time (improving or declining?)
Level 3: Breakdown by dimension (which segment drives the trend?)
Level 4: Detail/drill-down (individual records, anomalies)
```

### Registre des métriques {#metrics-registry}

Une source unique de vérité pour toutes les définitions de métriques métier :

| Champ | Exemple |
|-------|---------|
| **Nom** | active_sellers |
| **Définition métier** | Vendeurs ayant au moins une annonce sur la période |
| **SQL/formule** | `COUNT(DISTINCT seller_id) WHERE adverts > 0` |
| **Responsable** | Équipe Listings |
| **Source de données** | Table DWH `listings.sellers` |
| **Granularité** | Quotidienne, avec champ d'échelle pour hebdomadaire/mensuel |
| **Remarques particulières** | La ligne « All Regions » doit être exclue pour les totaux |

Sans registre, différents tableaux de bord affichent des chiffres différents pour la même métrique, car chaque analyste l'a définie à sa manière.

### Exemple de dictionnaire des champs de données {#data-field-dictionary-example}

Pour un tableau de bord sur les annonces :
- `execution_date` - Date
- `region` - Région géographique ; remarque : il existe une ligne « All Regions », à filtrer lorsqu'on affiche des totaux
- `scale` - Granularité des données (jour/semaine/mois) ; non additive, doit être filtrée par échelle et non sommée
- `listers` - Vendeurs actifs (ceux ayant au moins une annonce)
- `retention_7_days` - % encore actifs 7 jours après la première annonce (valide uniquement à l'échelle du jour)
- `retention_28_days` - % encore actifs 28 jours après (valide uniquement à l'échelle du jour)

### Communication avec les parties prenantes {#stakeholder-communication}

**Anti-pattern** : construire en isolation, puis surprendre les parties prenantes avec un travail présenté comme « fini ».

**Approche préférable :**
- Montrer la maquette avant de construire
- Montrer une version brouillon à 50 % d'avancement
- Points d'avancement hebdomadaires sur les projets importants

**Gérer les demandes « construis juste quelque chose » :**
« Si je construis sans comprendre les besoins, il y a de fortes chances que nous devions tout refaire. 2 jours de recueil des besoins = 2 semaines de reprise économisées. »

**Gérer la pression d'un calendrier urgent :**
Convenir d'un périmètre de MVP : le tableau de bord minimal viable qui apporte de la valeur dans le temps disponible.

### Évaluation des compétences de l'analyste BI {#bi-analyst-competency-assessment}

5 composantes de la visualisation : conception de l'information, design graphique, UX, storytelling, maîtrise de l'outil.

Échelle de compétence à 4 niveaux :
1. Connaissance théorique uniquement
2. Capable de faire avec la documentation ou une recherche
3. Connaît les nuances, possède ses propres exemples
4. Capable d'enseigner aux autres

S'auto-évaluer par rapport au niveau visé pour identifier les écarts.

## Pièges {#gotchas}

- Les métriques non additives (par ex., métriques stockées avec un champ « scale » jour/semaine/mois) ne peuvent pas être sommées : il faut filtrer par échelle
- Les métriques de rétention peuvent n'être valides qu'à l'échelle du jour : vérifier la granularité avant de calculer
- Les lignes « All Regions » ou autres lignes agrégées dans les données source doivent être filtrées lors de l'affichage des totaux, sans quoi il y a double comptage
- La charge de pointe sur les serveurs BI est non linéaire et imprévisible : un seul rapport lourd peut consommer 75 % du CPU du serveur
- Les périodes courantes incomplètes doivent être exclues ou clairement signalées pour éviter des comparaisons trompeuses

## Voir aussi {#see-also}

- [[dashboard-design-patterns]] - conception visuelle une fois les besoins définis
- [[product-analytics-fundamentals]] - pyramide des métriques et sélection des KPI
- [[tableau-fundamentals]] - construction dans Tableau
- [[powerbi-fundamentals]] - construction dans Power BI
- [[bi-tools-comparison]] - choisir le bon outil BI
