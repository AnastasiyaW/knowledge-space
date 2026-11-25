---
title: "Grok Build"
category: projects
date: 2026-07-16
tags: [grok-build, project]
aliases: ["Grok Build"]
level: 3
source_sha256: 7d47e7eab16496bcd07f680490f0b0cb022963feb557b4f0736c5695ed7e18e0
translation: machine
translated_at: '2026-10-24'
---
# Grok Build {#grok-build}

**Ligne de développement :** `project:grok-build` · fil `grok-build`  
**Dernier événement :** 2026-07-16 · 1 événement daté depuis 2026-07-16 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Grok Build est un agent de codage IA en terminal destiné aux travaux logiciels.

- Édition de la base de code : lit et modifie les fichiers du projet.
- Exécution shell : lance des commandes shell.
- Recherche web : effectue des recherches sur le web pour obtenir des informations techniques.
- Gestion des tâches : prend en charge les tâches longues via une TUI plein écran, une CLI headless ou ACP.

La documentation indique que grok-4.6 est le modèle sous-jacent et autorise la configuration d'un modèle personnalisé.
Le binaire publié constitue le point d'entrée pratique ; le code source, sous licence Apache-2.0, est ouvert à l'inspection et aux compilations locales, mais xAI n'accepte aucune contribution externe.

## Ligne de développement {#development-line}

- **2026-07-16 — Référence au dépôt public de Grok Build.** Le 2026-07-16, le fil Grok Build a référencé le dépôt GitHub public de Grok Build de xAI. Cela crée une référence source publique datée pour le projet, même si nous n'avons pas examiné le contenu du dépôt ni le contexte exact du message.

## Évolutions {#what-changed}

- **2026-05-25** — Grok Build est entré en bêta anticipée en tant qu'agent de codage en terminal, avec revue de plan, hooks, skills, prise en charge de MCP, sous-agents, mode headless et ACP.
- **2026-06-11** — Grok Build a ajouté une marketplace de plugins intégrée, avec installations de plugins distants épinglées à un commit.
- **2026-07-15** — La CLI/TUI en Rust de Grok Build et le runtime de l'agent ont été publiés en open source, avec une inférence personnalisée en priorité locale documentée.
- **2026-07-16** — Grok Build v0.2.102 a ajouté des indicateurs minimal/fullscreen par session, `/jump`, une barre latérale de chronologie, la configuration distante des permissions et un comportement amélioré de connexion et de session.
- **2026-07-23** — Grok Build a ajouté des workflows générés et réutilisables pour l'orchestration multi-agents en arrière-plan.
- **2026-08-19** — Grok Build a étendu une interface distincte de création d'applications web et mobiles à tous les plans, avec publication, partage, export vers GitHub, secrets et connecteurs.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-16, considérez le dépôt GitHub xAI lié comme la première référence publique pour Grok Build. Vérifiez son contenu avant de vous appuyer sur des détails d'implémentation.

1. Installez le binaire publié pour votre plateforme, puis exécutez `grok --version`.
  — <https://github.com/xai-org/grok-build>
2. Accédez au dépôt cible et exécutez `grok`. Authentifiez-vous dans le navigateur ou fournissez une clé API dans un environnement sans navigateur.
  — <https://docs.x.ai/build/overview>
3. Commencez les tâches complexes en mode Plan. Relisez ou modifiez le plan, approuvez l'exécution et inspectez les diffs obtenus.
  — <https://x.ai/news/grok-build-cli>
4. Automatisez une requête bornée avec `grok -p`. Utilisez le JSON en flux lorsqu'un autre programme consomme le résultat.
  — <https://docs.x.ai/build/overview>
5. Configurez volontairement le modèle, les permissions du projet, les plugins et les sources MCP. Exécutez `grok inspect` pour vérifier que la configuration a bien été chargée.
  — <https://docs.x.ai/build/settings>

## Bonnes pratiques {#best-practices}

- Conservez Ask comme mode de permission initial et utilisez le mode Plan pour les modifications soumises à revue. Ne confondez pas Auto ou Always-approve avec un substitut à la revue du plan.
  — <https://docs.x.ai/build/features/permissions>
- Exécutez les dépôts non fiables avec un sandbox strict et des règles de permission restreintes. Ajoutez des refus explicites pour `.env`, les clés privées et les autres chemins d'identifiants, car les profils intégrés ne les protègent pas de façon permanente.
  — <https://docs.x.ai/build/features/sandbox>
- Utilisez `grok inspect` après toute modification de la configuration afin que les sources actives d'instructions, de skills, de plugins, de hooks, de MCP et de modèles restent visibles.
  — <https://docs.x.ai/build/settings>
- Traitez les plugins tiers comme du code exécutable et n'installez que des sources que vous avez examinées. L'épinglage dans la marketplace vérifie une révision sélectionnée, mais il ne rend pas le code tiers approuvé ni sûr.
  — <https://github.com/xai-org/plugin-marketplace>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-07-15 — La recommandation selon laquelle le harnais de Grok Build était indisponible pour l'inspection du code source ou la compilation locale est obsolète ; xAI a publié le code source de la CLI/TUI et du runtime de l'agent.
- 2026-08-19 — La restriction d'accès en bêta anticipée pour l'interface de création d'applications web et mobiles est obsolète ; xAI indique que cette interface est disponible sur tous les plans. Cela n'établit pas des conditions d'accès identiques pour la CLI en terminal.

## Points non établis {#still-unknown}

- Les champs demandés event_findings et new_events ne figurent pas dans le schéma de réponse fourni. Les ajouts de l'événement daté sont représentés dans Évolutions : l'annonce open source du 15 juillet et l'entrée de changelog v0.2.102 du 16 juillet.
- Grok Build désigne deux surfaces liées mais opérationnellement différentes : le dépôt GitHub couvre l'agent de codage en terminal, tandis que l'annonce d'août décrit un créateur d'applications web et mobiles pouvant exporter des projets vers GitHub et se poursuivre dans le terminal. xAI ne documente pas leur filiation d'implémentation partagée exacte.
- L'annonce d'août décrit la bêta anticipée web/mobile comme réservée à SuperGrok Heavy, alors que le lancement de la CLI en terminal en mai évoquait un accès en bêta anticipée pour SuperGrok et X Premium Plus. Nous ne devons pas traiter ces politiques d'accès comme un droit historique unique.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/xai-org/grok-build | xai-org/grok-build | 2026-09-05 |
| https://x.ai/news/grok-build-cli | Présentation de Grok Build | 2026-09-05 |
| https://x.ai/news/grok-plugin-marketplace | Marketplace de plugins Grok Build | 2026-09-05 |
| https://x.ai/news/grok-build-open-source | Grok Build est désormais open source | 2026-09-05 |
| https://x.ai/build/changelog | Journal des modifications de Grok Build | 2026-09-05 |
| https://x.ai/news/workflows | Workflows dans Grok Build | 2026-09-05 |
| https://x.ai/news/grok-build-for-everyone | Grok Build sur le web et mobile | 2026-09-05 |
| https://docs.x.ai/build/overview | Grok Build : l'agent de codage de SpaceXAI | 2026-09-05 |
| https://docs.x.ai/build/settings | Paramètres de Grok Build | 2026-09-05 |
| https://docs.x.ai/build/features/permissions | Permissions de Grok Build | 2026-09-05 |
| https://docs.x.ai/build/features/sandbox | Sandbox de Grok Build | 2026-09-05 |
| https://github.com/xai-org/plugin-marketplace | xai-org/plugin-marketplace | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:grok-build`, fil `grok-build`, 1 événement daté du 2026-07-16 au 2026-07-16.
- **Note pratique :** À partir du 2026-07-16, les praticiens doivent considérer le dépôt GitHub xAI lié comme la première référence publique pour Grok Build et vérifier son contenu avant de s'appuyer sur des détails d'implémentation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
