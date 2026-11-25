---
title: "Cursor — Développement produit"
category: projects
date: 2026-06-29
tags: [cursor, product-development, project]
aliases: ["Cursor"]
level: 3
source_sha256: 4fad5d2f7e14bb8085d66c3c9c4e58bab7a7220023caae1259e1520de59c30f3
translation: machine
translated_at: '2026-10-24'
---
# Cursor — Développement produit {#cursor-product-development}

**Ligne de développement :** `project:cursor` · fil `product-development`  
**Dernier événement :** 2026-06-29 · 1 événement daté depuis le 2026-06-29 · **Recherche effectuée le :** 2026-09-04 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

Cursor est un éditeur de code et un agent destinés aux développeurs qui doivent comprendre un dépôt, déléguer des modifications et fusionner les changements.

- Indexation du code source pour cartographier le dépôt, planifier des fonctionnalités, écrire du code, corriger des bogues et relire les diffs.
- Environnement d'exécution multiplateforme couvrant l'application de bureau, des VM cloud isolées, le web et iOS, avec transfert de session entre les exécutions locales et cloud.
- Injection de contexte via Rules, `AGENTS.md`, skills et MCP, pour des consignes propres au dépôt.

## Ligne de développement {#development-line}

- **2026-06-29 — Cursor a annoncé une application mobile iOS.** Cursor a annoncé son application mobile iOS le 2026-06-29, dans un billet de blog et une fiche sur l'App Store. Cette sortie étend l'éditeur aux appareils iOS. Les liens de l'annonce confirment la date de sortie, mais ne précisent ni les fonctionnalités, ni la disponibilité régionale, ni le statut final de la version.

## Ce qui a changé {#what-changed}

Cursor est passé d'un point d'entrée web unique à un espace de travail agentique multi-appareils.

- 2023-08-21 — `cursor.so` servait d'adresse publique d'origine. Le site redirige désormais et ne conserve plus les anciennes descriptions de fonctionnalités, de sorte qu'aucune base de référence vérifiable n'existe pour cette date.
- 2026-04-02 (trouvé aujourd'hui) — Cursor 3 a ajouté une interface d'agent unifiée pour plusieurs espaces de travail, avec des agents locaux et cloud en parallèle, des transferts de session, des workflows de diff et de PR, un navigateur intégré et des plugins.
- 2026-06-29 — Cursor a publié une application iOS native en bêta publique, permettant de lancer des agents cloud, de piloter à distance des agents locaux, de suivre les notifications, d'inspecter les artefacts et de fusionner des PR.
- 2026-09-04 (trouvé aujourd'hui) — La documentation actuelle relie iOS au backend d'agents partagé avec le bureau et le web. Elle recense les points d'entrée de l'agent cloud sur le bureau, le web, iOS, Slack, les commentaires du gestionnaire de sources, Linear et l'API.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-06-29, testez l'application iOS de Cursor en parallèle des workflows actuels si un accès mobile est nécessaire. Les sources datées ne permettent pas de justifier une migration complète ni des recommandations de fonctionnalités plus larges.

1. Installez l'application de bureau, authentifiez-vous et ouvrez le répertoire du projet.
  — <https://cursor.com/docs/get-started/quickstart>
2. Demandez à Agent d'expliquer la structure du dépôt, les points d'entrée et les modules principaux avant de proposer des modifications.
  — <https://cursor.com/docs/get-started/quickstart>
3. Commencez par une modification réduite et à faible risque, et passez en Plan Mode pour les recherches, les tâches multi-fichiers ou les validations sensibles.
  — <https://cursor.com/docs/get-started/quickstart>
4. Ajoutez les consignes du dépôt sous `.cursor/rules/*.mdc`, ou placez un fichier `AGENTS.md` à la racine pour les consignes globales du projet.
  — <https://cursor.com/docs/rules>
5. Relisez les diffs générés, puis exécutez les suites de tests existantes, les vérifications de types, les linters ou les builds avant d'accepter tout changement.
  — <https://cursor.com/docs/get-started/quickstart>
6. Connectez le gestionnaire de sources pour les tâches en arrière-plan, configurez l'environnement d'exécution de l'agent cloud dans une VM isolée, puis inspectez les artefacts, diffs et pull requests produits.
  — <https://cursor.com/docs/cloud-agent>
7. Connectez-vous sur iPhone ou iPad, sélectionnez le dépôt et la branche cible, donnez ses instructions à l'agent, puis relisez ou fusionnez les pull requests en dehors du bureau.
  — <https://cursor.com/docs/cloud-agent/mobile>

## Bonnes pratiques {#best-practices}

- Gardez les Rules du projet ciblées et sous 500 lignes pour qu'elles restent exploitables. Découpez les ensembles de règles trop volumineux, référencez les fichiers canoniques au lieu de recopier leur contenu, et versionnez-les dans Git.
  — <https://cursor.com/docs/rules>
- Fournissez le contexte du dépôt avant de déléguer un travail. Testez une modification réduite avant de tenter des changements étendus, et utilisez Plan Mode lorsque l'implémentation exige une recherche ou une validation préalable.
  — <https://cursor.com/docs/get-started/quickstart>
- Configurez les environnements de l'agent cloud avant d'exécuter des tâches. Injectez les secrets via le tableau de bord, utilisez OIDC plutôt que des clés cloud de longue durée, placez sur liste d'autorisation les routes réseau sortantes nécessaires, et exécutez les tests sans dépendances externes.
  — <https://cursor.com/docs/cloud-agent/best-practices>
- Considérez toute production de l'agent comme un brouillon. Inspectez le diff et exécutez les vérifications du dépôt avant de décider de fusionner.
  — <https://cursor.com/docs/get-started/quickstart>
- Lancez Quick Agent Review pour des contrôles de cohérence rapides. Appliquez Deep review pour la logique complexe, les modifications sensibles en matière de sécurité ou les refactorisations importantes.
  — <https://cursor.com/docs/agent/agent-review>

## Remplacé par ceci {#superseded-by-this}

- 2023-08-21 — `cursor.com` remplace l'ancien domaine `cursor.so`. L'ancienne URL redirige vers le nouveau site, et les étapes de configuration actuelles figurent dans la documentation officielle.
- 2026-04-02 — Les hypothèses d'un éditeur unique sur bureau sont obsolètes. Cursor 3 coordonne des agents locaux et cloud sur plusieurs espaces de travail, tout en conservant une inspection au niveau de l'IDE.
- 2026-06-29 — Considérer les applications mobiles comme de simples flux de notifications en lecture seule est dépassé. Le client iOS natif lance et pilote les agents, inspecte leurs productions et fusionne les pull requests.

## Toujours inconnu {#still-unknown}

- La source de 2023 redirige vers le site principal sans conserver les notes de lancement d'origine, les numéros de version ni les détails des fonctionnalités.
- Le billet de juin 2026 décrit iOS comme une bêta publique. La documentation actuelle détaille ses fonctionnalités, mais ne précise pas si l'application est passée en disponibilité générale.
- La documentation actuelle ne précise pas les modèles actifs, les niveaux d'abonnement, les limites tarifaires ni la disponibilité régionale sur l'App Store.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://www.cursor.so/ | Agent de code IA pour créer des logiciels ambitieux | Cursor | 2026-09-04 |
| https://cursor.com/blog/cursor-3 | Découvrez le nouveau Cursor | Cursor | 2026-09-04 |
| https://cursor.com/blog/ios-mobile-app | Développer de n'importe où avec Cursor pour iOS | Cursor | 2026-09-04 |
| https://apps.apple.com/app/cursor/id6767085653 | Cursor App | App Store | 2026-09-04 |
| https://cursor.com/docs/get-started/quickstart | Démarrage rapide | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/rules | Rules | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent | Agents cloud | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent/best-practices | Bonnes pratiques pour l'agent cloud | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/agent/agent-review | Agent Review | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent/mobile | Cursor pour iOS | Cursor Docs | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:cursor`, fil `product-development`, 1 événement daté du 2026-06-29 au 2026-06-29.
- **Note pratique :** à partir du 2026-06-29, les équipes ayant besoin d'un support mobile devraient évaluer le client iOS de Cursor en parallèle des outils actuels. Les liens examinés ne justifient pas une migration plus large vers la plateforme ni un déploiement élargi des fonctionnalités.
- **Confiance :** moyenne. Les mentions datées de remplacement restent la référence pour les workflows obsolètes.
