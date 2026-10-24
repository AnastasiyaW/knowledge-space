---
title: "Data2Story — Storytelling agentique à partir de données"
category: projects
date: 2026-06-16
tags: [agentic-data-storytelling, agentic_data_storytelling, data2story, project]
aliases: ["Data2Story"]
level: 2
source_sha256: 215eecd4d399fe72596b19705b057ab188bb3f21c4be64ce41dc2dd90a1a9308
translation: machine
translated_at: '2026-10-24'
---
# Data2Story — Storytelling agentique à partir de données {#data2story-agentic-data-storytelling}

**Ligne de développement :** `project:data2story` · fil `agentic-data-storytelling`  
**Dernier événement :** 2026-06-16 · 1 daté depuis 2026-06-16 · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Data2Story transforme un CSV, un dossier de données, un article scientifique ou une idée dans Pro en un récit HTML autonome. Il génère des graphiques et des médias accompagnés d'une visionneuse de preuves.

- Sept rôles de rédaction structurent le pipeline de rédaction canonique.
- La traçabilité des affirmations relie chaque assertion et chaque visuel aux données, au code ou aux citations.
- Pro ajoute un workflow de 14 agents et le recalcul dans la page.

L'article évalue 18 articles auprès de 53 participants.
Utilisez-le lorsque la traçabilité des preuves est une exigence de livraison, et non pour remplacer le jugement éditorial.

## Ligne de développement {#development-line}

- **2026-06-16 — Data2Story a été publiquement relié à son site web et à son dépôt GitHub.** Le 2026-06-16, des liens publics ont relié Data2Story à son site web de projet et au dépôt GitHub data2story-skill. Cela fixe le point de référence de la ligne de storytelling agentique à partir de données, sans affirmer de fonctionnalités non vérifiées.

## Ce qui a changé {#what-changed}

- 2026-05-11 — Data2Story a été accepté comme article Spotlight à l'atelier ACM Conference on AI and Agentic Systems.
- 2026-06-09 — L'article et le dépôt ont été publiés. L'implémentation canonique a établi une rédaction séquentielle à sept rôles et évalué 18 articles auprès de 53 participants.
- 2026-06-16 — Data2Story a été présenté publiquement comme un workflow allant du jeu de données à un récit vérifiable. L'Inspector trace chaque affirmation et chaque visuel jusqu'aux données, au code ou aux références.
- 2026-06 — La version 0.1.0 a optimisé les effets visuels. Le dépôt identifie data2story-pro comme l'implémentation plus riche, aux côtés de la skill à sept rôles reproductible selon l'article.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-16, utilisez le site web du projet et le dépôt GitHub comme références de départ pour le storytelling agentique à partir de données.

1. Clonez ou ouvrez le dépôt, puis utilisez la skill canonique `data2story` pour reproduire le pipeline à sept rôles de l'article.
  — <https://github.com/QinghongLin/data2story-skill>
2. Fournissez un CSV, un fichier JSON, un dossier de données, un article scientifique ou, dans Pro, une idée ou une URL ; lancez l'orchestrateur sur cette entrée.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story-pro/README.md>
3. Ouvrez `index.html` pour l'article et inspectez les affirmations via `viewer.html` dans la skill canonique, ou via l'inspecteur intégré à la page dans Pro.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story/SKILL.md>

## Bonnes pratiques {#best-practices}

- Exécutez les étapes fixes dans l'ordre et n'avancez pas tant que l'artefact précédent n'est pas complet.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story/SKILL.md>
- Archivez les skills exactes utilisées pour chaque exécution afin qu'un résultat puisse être tracé et revérifié.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story/SKILL.md>
- N'utilisez le mode idée de Pro que s'il peut acquérir et valider un jeu de données réel ; il s'arrête plutôt que de fabriquer des données à l'appui.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story-pro/README.md>
- Considérez la durée publiée de Pro comme une estimation de planification : `--fast` est indiqué à environ 15–25 minutes et le mode premium à environ 2 heures 40–50 minutes.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story-pro/README.md>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points restant inconnus {#still-unknown}

- Les notes de mise à jour du dépôt ne donnent que le mois de la version 0.1.0, de sorte que le jour exact de sa publication n'est pas vérifié.
- Aucune source de première main n'établit le coût d'exploitation en production, les valeurs par défaut de génération de médias propres à un modèle, ni un journal des modifications formel pour Data2Story Pro.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://data2story.github.io/ | Data Journalist Agent (Data2Story) | 2026-09-05 |
| https://github.com/QinghongLin/data2story-skill | Dépôt QinghongLin/data2story-skill | 2026-09-05 |
| https://arxiv.org/abs/2606.11176 | Data Journalist Agent: Transforming Data into Verifiable Multimodal Stories | 2026-09-05 |
| https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story/SKILL.md | Orchestrateur de la skill canonique Data2Story | 2026-09-05 |
| https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story-pro/README.md | README de Data2Story Pro | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:data2story`, fil `agentic-data-storytelling`, 1 événement daté du 2026-06-16 au 2026-06-16.
- **Note pratique :** Au 2026-06-16, les praticiens peuvent utiliser le site web du projet et le dépôt GitHub fournis comme références de départ lorsqu'ils évaluent Data2Story pour des travaux de storytelling agentique à partir de données.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
