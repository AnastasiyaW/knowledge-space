---
title: "ComfyUI Skill Public — Dépôt public"
category: projects
date: 2026-05-14
tags: [comfyui-skill-public, comfyui_skill_public, project, public-repository]
aliases: ["ComfyUI Skill Public", "comfyui-skill-public"]
level: 3
source_sha256: ef9c3871e674d1af70cd0d254cf0c42307f1aab7df0e889adefd67a61b21c2a7
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Skill Public — Dépôt public {#comfyui-skill-public-public-repository}

**Ligne de développement :** `project:comfyui-skill-public` · fil `public-repository`  
**Dernier événement :** 2026-05-14 · 1 événement daté depuis 2026-05-14 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

comfyui-skill-public : un skill ComfyUI portable destiné aux agents et aux opérateurs travaillant sur des installations locales, distantes ou cloud qu'ils ne connaissent pas.

- Découvre les classes de nœuds et les valeurs de modèles avant de construire un workflow.
- Couvre le travail d'image avec FLUX 2, la vidéo avec LTX 2.3 et WAN 2.2, les prompts JoyCaption, l'entraînement de LoRA, les traitements par lots et la reprise après incident.
- Utilise REST et le suivi des jobs via WebSocket, sans interface graphique.

## Ligne de développement {#development-line}

- **2026-05-14 — Dépôt GitHub public de ComfyUI Skill référencé.** Le 2026-05-14, la fiche a enregistré un lien vers le dépôt GitHub de ComfyUI Skill Public. Les éléments disponibles établissent la référence au dépôt, mais n'établissent ni une version, ni une fonctionnalité, ni une modification de code précise.

## Modifications {#what-changed}

2026-03-28 — comfyui-skill-public : le premier paquet public portable a séparé les consignes de déclenchement et de routage de la configuration propre à chaque machine. 2026-04-11 — Ajout de consignes pour LTX 2.3, de la gestion et de la reprise de l'état des lots, d'implémentations de référence, de consignes sur les dépendances, de workflows de démonstration et d'un parcours d'entraînement LoRA. 2026-04-12 — Ajout de guides de prompts pour FLUX 2 et WAN 2.2, ainsi que d'un flux de décision pour la première configuration. 2026-04-25 — Ajout d'une procédure opérationnelle (SOP) de supervision et de reprise des lots. 2026-04-26 — Alignement de la documentation de configuration et de cron. 2026-05-14 — Une mention publique documentée décrivait le pilotage de OpenClaw en langage naturel ; aucune modification d'implémentation GitHub n'est visible pour cette date. 2026-06-03 — La v1.4.0 a ajouté un helper d'API portable, un starter de lots, une convention JoyCaption, des instructions de démarrage à froid pour les agents et davantage de cartes de nœuds ; la v1.4.1 a explicitement élargi la prise en charge au-delà d'OpenClaw et remplacé les consignes « démos prêtes à l'emploi » par des workflows apportés par l'utilisateur (bring-your-own API).

## Mode d'emploi {#how-to-use-this}

Au 2026-05-14, les praticiens peuvent utiliser le dépôt GitHub lié comme référence publique candidate pour le skill ComfyUI, tout en inspectant son contenu avant de s'appuyer sur une capacité ou une version particulière.

1. Clonez le dépôt, puis demandez à un agent IA de lire AGENTS.md ou SKILL.md en tant qu'opérateur ; installez les dépendances Python listées si vous utilisez son code d'aide.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
2. Pour une cible ComfyUI inconnue, collectez son URL, sa version, ses packs de nœuds, sa famille de modèles, ses limites matérielles et ses règles de sortie ; vérifiez d'abord system_stats, object_info, la file d'attente, le WebSocket et un prompt minimal exécuté jusqu'au bout.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/setup.md>
3. Exportez un workflow existant au format API de ComfyUI, puis inspectez ses nœuds, modèles, encodeurs et VAE requis via object_info.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
4. Copiez le workflow en profondeur, ne modifiez que les entrées propres à chaque job, soumettez-le à prompt, conservez l'ID du prompt, attendez la fin de l'exécution via WebSocket et vérifiez les sorties dans l'historique.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/api.md>
5. Pour un lot, réutilisez un même client ID et une même connexion WebSocket, persistez l'état de chaque job et ne reprenez que les jobs sans sortie vérifiée.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md>

## Bonnes pratiques {#best-practices}

- Découvrez les classes de nœuds, les noms de fichiers de modèles et les valeurs propres à chaque installation à l'exécution ; ne traitez pas les exemples comme des faits sur la machine cible.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/SKILL.md>
- Ne modifiez pas un workflow de base sur place ; copiez-le en profondeur et modifiez la copie.
  — <https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md>
- Ne lancez pas les prompts de lot en mode « lancer et oublier » : attendez la fin via WebSocket et vérifiez chaque ID de prompt dans l'historique.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md>
- Considérez les graphes de démonstration fournis comme de simples exemples ; privilégiez un workflow exporté depuis l'installation ComfyUI cible.
  — <https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/755d3f66f4ebb1072a75fc7d8d616489c97bacce>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-03 — Workflows de démonstration présentés comme prêts à installer : remplacés par les consignes de la v1.4.1, qui recommandent d'exporter et d'adapter le workflow au format API de l'utilisateur.
- 2026-06-03 — Hypothèses de contrôleur codées en dur, propres à OpenClaw et Discord : remplacées par les consignes de la v1.4.0, indépendantes du planificateur et configurées par l'environnement.

## Toujours inconnu {#still-unknown}

- Aucun commit first-party ni aucune GitHub Release n'est visible pour le 2026-05-14 ; l'événement est attesté comme une mention publique du même jour, et non comme une publication de code avérée.
- L'URL d'origine redirige désormais vers ComfyUI-Agent-Toolkit, mais la date et la raison du renommage ne sont pas exposées.
- GitHub ne publie aucune Release ; les numéros de version du changelog relèvent de la documentation, et non de la preuve d'un artefact publié.
- L'API GitHub était injoignable lors de cette vérification : les dates created_at et pushed_at du dépôt n'ont pas été vérifiées de manière indépendante.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/Zambav/comfyui-skill-public | GitHub - Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |
| https://nnets.ru/news/openclaw-skill-upravlenie-comfyui-komandami-na-estestvennom-yazyke | OpenClaw Skill : pilotage de ComfyUI par commandes en langage naturel. | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commits/main | Commits · Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/95fe0bc5ee9cdf9b64db983ea8983d68905dbc9c | v1.4.0 : améliorations du contrôleur portées + nouveau README d'accueil | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/commit/755d3f66f4ebb1072a75fc7d8d616489c97bacce | v1.4.1 : README élargi à « any agent » + « bring your own workflows » | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/README.md | README.md | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/SKILL.md | SKILL.md | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/setup.md | setup.md | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/api.md | ComfyUI-Agent-Toolkit/api.md at main | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/blob/main/batch-operations.md | ComfyUI-Agent-Toolkit/batch-operations.md at main | 2026-09-05 |
| https://raw.githubusercontent.com/Zambav/ComfyUI-Agent-Toolkit/main/changelog.md | changelog.md | 2026-09-05 |
| https://github.com/Zambav/ComfyUI-Agent-Toolkit/releases | Releases · Zambav/ComfyUI-Agent-Toolkit | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:comfyui-skill-public`, fil `public-repository`, 1 événement daté, du 2026-05-14 au 2026-05-14.
- **Note pratique :** Au 2026-05-14, les praticiens peuvent utiliser le dépôt GitHub lié comme référence publique candidate pour le skill ComfyUI, tout en inspectant son contenu avant de s'appuyer sur une capacité ou une version particulière.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
