---
title: "OpenBot — Développement du projet"
category: projects

tags: [openbot, project, project-development]
aliases: ["OpenBot"]
level: 3
source_sha256: e789842d3f733f893cf33d79fba67489c3d23ab8c418e7b70acc89789a185b3e
translation: machine
translated_at: '2026-10-24'
---
# OpenBot — Développement du projet {#openbot-project-development}

**Ligne de développement :** `project:openbot` · fil `project-development`  
**Dernier événement :** - · 0 événement daté depuis - · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

OpenBot est un modèle que les équipes clonent pour exploiter des coworkers AG-UI encadrés sur notre propre infrastructure, plutôt que d'utiliser un agent hébergé.

- Isolation des Bots : donne à chaque Bot son propre profil de navigateur, son propre système de fichiers et ses outils accordés.
- Passerelle de politiques : achemine les actions de navigateur, de fichiers et MCP à travers une vérification CEL à échec fermé et une piste d'audit.
- Prise en charge des agents : accepte des agents AG-UI personnalisés, ainsi que les Bots de preuve de concept et LangGraph livrés avec le projet.

Il s'agit toujours d'un logiciel en alpha, sans version hébergée ni paquet installable.

Utilisez-le lorsque notre équipe peut gérer Docker, PostgreSQL, les identifiants des modèles et la politique d'accès ; ne le considérez pas comme un service géré.

## Ligne de développement {#development-line}

- L'événement daté n'a pas encore fait l'objet d'une rédaction ; ce qui est connu figure ci-dessous.

## Évolutions {#what-changed}

- 2026-08-17 — La v0.0.1 a introduit l'alpha exécutable sur ordinateur portable, avec des ordinateurs isolés par Bot, des actions encadrées, la prise en charge d'AG-UI et les fils CopilotKit Intelligence.
- 2026-08-22 — Les versions v0.0.2 à v0.0.4 ont rendu l'accès aux outils utilisable à partir d'un clone frais tout en renforçant la frontière de sécurité : génération automatique et locale de AGENT_TOOL_TOKEN, sélection d'outils par compétences au-delà de 12 accords, visibilité de l'audit, routage compatible OpenAI corrigé, compétences empaquetées et refus d'une référence de page non résoluble.
- 2026-08-28 — La v0.0.5 a ajouté le transfert de Bot à Bot accordé par l'administrateur et l'escalade vers un humain, réparé les conversations bloquées sur un résultat d'outil, et ajouté la prise en charge du streaming de l'API Responses pour les modèles gpt-5.6-*.

## Mode d'emploi {#how-to-use-this}

Aucune évolution des pratiques de l'utilisateur final n'est enregistrée à la date du 2026-08-22. Consultez d'abord le dépôt lié et récupérez le message source pour établir ce qui a changé.

1. Clonez OpenBot et préparez Docker, Bun 1.3+, un projet CopilotKit Intelligence et un identifiant de modèle.
  — <https://github.com/CopilotKit/openbot>
2. Copiez .env.example vers .env, utilisez la CLI CopilotKit pour obtenir INTELLIGENCE_API_KEY, puis renseignez l'identifiant du modèle.
  — <https://github.com/CopilotKit/openbot>
3. Exécutez bun install, puis bash scripts/start.sh ; ouvrez http://localhost:3010 une fois les contrôles de santé validés.
  — <https://github.com/CopilotKit/openbot>
4. Remplacez le paquet de locataire d'exemple par brand.yaml, agents.yaml, channels.yaml, model.yaml et knowledge.yaml ; ajoutez skills.yaml si nécessaire.
  — <https://github.com/CopilotKit/openbot/blob/main/docs/configuration.md>
5. Créez ou connectez des coworkers depuis /agents, configurez les serveurs MCP et les accords sous /admin/plugins, puis définissez les règles navigateur/fichiers/MCP sous /admin/boundaries.
  — <https://github.com/CopilotKit/openbot>
6. Testez une action de navigateur contrôlée, ajoutez une règle de refus, relancez-la, puis inspectez l'action autorisée ou refusée dans /admin/audit.
  — <https://github.com/CopilotKit/openbot>

## Bonnes pratiques {#best-practices}

- Activez un fournisseur d'identité avant d'autoriser d'autres personnes : le mode mono-utilisateur par défaut traite chaque visiteur comme un administrateur.
  — <https://github.com/CopilotKit/openbot>
- Appliquez le moindre privilège aux outils. Les compétences déclarent les outils à proposer, mais n'accordent pas d'accès ; les accords de Bot restent la frontière effective.
  — <https://github.com/CopilotKit/openbot/releases>
- Conservez l'isolation par défaut de l'ordinateur de chaque Bot ; utilisez gVisor via COMPUTER_RUNTIME=runsc lorsque l'hôte le permet.
  — <https://github.com/CopilotKit/openbot>
- Considérez la politique et l'audit comme une boucle d'exploitation : testez une action refusée avant de l'accorder, puis examinez la piste d'audit obtenue.
  — <https://github.com/CopilotKit/openbot>
- Pour un déploiement publié, épinglez le digest du conteneur figurant dans container-images.json et vérifiez son attestation de provenance GitHub plutôt que de déployer une étiquette mutable.
  — <https://github.com/CopilotKit/openbot/blob/main/docs/releasing.md>

## Remplacé par cette version {#superseded-by-this}

- 2026-08-22 — Les clones frais sur ordinateur portable n'ont plus besoin de provisionner manuellement AGENT_TOOL_TOKEN lorsqu'ils sont démarrés avec scripts/start.sh ; les déploiements en dehors de ce script échouent toujours en mode fermé sans jeton.
- 2026-08-22 — La proposition de chaque outil accordé aux Bots disposant de plus de 12 outils est remplacée par des propositions correspondant aux compétences, ainsi que les outils accordés non revendiqués.
- 2026-08-22 — Une action de navigateur dont l'élément cité ne peut être résolu n'est plus autorisée ; le Bot doit prendre un nouvel instantané.
- 2026-08-28 — Les exécutions de Bots framework gpt-5.6-* qui ignoraient silencieusement les blocs de contenu de l'API Responses sont remplacées par une prise en charge des deux formes de streaming.

## Toujours inconnu {#still-unknown}

- L'élément du 2026-08-22 ne comporte que l'URL du dépôt ; sa version exacte visée ne peut donc pas être identifiée. GitHub enregistre les versions v0.0.2, v0.0.3 et v0.0.4 à cette date.
- OpenBot reste en alpha, et son README indique que le dépôt est un modèle et non un produit hébergé ; la maturité pour la production d'un déploiement donné exige donc sa propre revue de sécurité et d'exploitation.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://github.com/CopilotKit/openbot | README d'OpenBot | 2026-09-05 |
| https://github.com/CopilotKit/openbot/releases | Releases · CopilotKit/OpenBot | 2026-09-05 |
| https://github.com/CopilotKit/openbot/blob/main/docs/configuration.md | Configuration d'OpenBot | 2026-09-05 |
| https://github.com/CopilotKit/openbot/blob/main/docs/releasing.md | Guide de publication d'OpenBot | 2026-09-05 |

## Consigne pour l'agent {#agent-brief}

- **Sujet :** `project:openbot`, fil `project-development`, 0 événement daté - → -.
- **Note pratique :** Nous ne signalons aucune évolution des pratiques de l'utilisateur final à la date du 2026-08-22 ; consultez d'abord le dépôt lié et récupérez le message source pour établir ce qui a changé.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
