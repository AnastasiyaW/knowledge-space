---
title: "OmniScientist"
category: projects

tags: [omniscientist, project]
aliases: ["OmniScientist"]
level: 3
source_sha256: 94746c7fc9adc8632e2927706d74473661eb05c54bb6b1a68a2d60e06d69dc83
translation: machine
translated_at: '2026-10-24'
---
# OmniScientist {#omniscientist}

**Ligne de développement :** `project:omniscientist` · fil `omniscientist`  
**Dernier événement :** - · 0 daté depuis - · **Recherché le :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

OmniScientist est un flux de travail de recherche local et ouvert, destiné aux personnes qui souhaitent transformer un dossier de données brutes et une question ouverte en un article candidat traçable.

- Entrées : lit les images, formes d'onde, audio, vidéo, nuages de points, trajectoires, tableaux et formules.
- Étapes : exécute les étapes d'idéation, d'expérimentation et de rédaction, avec des traces de code et d'artefacts.
- Sorties : produit une sortie TeX/PDF dont les nombres sont liés aux exécutions enregistrées.

Les auteurs rapportent 36 cas sur données réelles. Le moteur de référence autorise par défaut deux retours arrière automatiques de réidéation. Nous l'utilisons comme échafaudage de recherche computationnelle auditable, et non comme preuve qu'une affirmation scientifique générée est correcte.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; les éléments connus figurent dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

- 2026-08-13 — Le rapport technique a été soumis pour la première fois sur arXiv.
- 2026-08-16 — La v0.1.0 a publiquement diffusé l'atelier de bureau, l'agent terminal et la compétence Claude Code.
- 2026-08-18 — La v0.1.1 a ajouté la vérification SHA256SUMS à l'échelle de la version.
- 2026-08-21 — Il ne s'agit pas d'une date de version ou de commit vérifiée : l'historique officiel passe du 2026-08-20 au 2026-08-22 ; la v0.1.1 était alors la version étiquetée la plus récente.
- 2026-08-23 — La v0.1.2 a ajouté la prise en charge de DeepSeek V4 Flash Vision et corrigé le rendu de la relecture PDF.
- 2026-08-24 — La v0.1.3 a ajouté la prise en charge de l'espace de travail et des pages multilingues.
- 2026-08-25 — La v0.1.6 a été publiée avec les paquets bureau, terminal et compétence.
- 2026-08-28 — La v0.2.0 a livré les paquets bureau sous forme d'installateur Windows, d'archive ZIP macOS et de paquet DEB Linux.
- 2026-09-02 — La v0.2.1 est devenue la dernière version vérifiée ; les consignes actuelles du README retirent la CLI autonome au profit de l'application de bureau ou de la compétence.

## Comment l'utiliser {#how-to-use-this}

1. Téléchargez le paquet bureau v0.2.1 correspondant à votre plateforme, ou décompressez omnisci-skill.zip dans ~/.claude/skills. Vérifiez la somme de contrôle de la version avant l'installation.
  — <https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1>
2. Donnez à l'espace de travail de bureau ou à la compétence installée un dossier de données brutes et une direction de recherche ouverte. Utilisez l'espace de travail local pour inspecter le journal d'exécution et les artefacts produits.
  — <https://omni-scientist.github.io/>
3. Définissez les données et la direction ouverte dans series.json pour une exécution scriptable du moteur de référence. Lancez agentic.py avec --stage run plutôt qu'une étape isolée.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>
4. Configurez séparément le socle de raisonnement et un modèle de perception capable de traiter les images lorsque vous utilisez le moteur de référence.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>

## Bonnes pratiques {#best-practices}

- Utilisez --stage run pour une véritable exécution du moteur. Les étapes isolées servent au débogage et n'effectuent pas de retour arrière automatique.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>
- Commencez par une direction ouverte et réfutable, et inspectez les preuves brutes avant de choisir une méthode d'analyse.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md>
- Enregistrez chaque nombre rapporté à partir de la sortie standard du script, utilisez des références réellement récupérées, et considérez qu'un contrôle numérique réussi constitue une preuve de provenance et non une validation scientifique.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md>
- Vérifiez les fichiers de publication téléchargés par rapport à SHA256SUMS avant l'installation.
  — <https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1>

## Remplacé par ceci {#superseded-by-this}

- 2026-09-02 — Les consignes d'installation de la CLI autonome issues de la ligne v0.1.x sont obsolètes pour une nouvelle installation : le README actuel indique que l'édition terminal a été abandonnée dans la v0.2.1.
- 2026-09-02 — La v0.2.0 est remplacée par la v0.2.1 comme dernière version vérifiée.

## Toujours inconnu {#still-unknown}

- Le libellé exact et l'affirmation visée de l'annonce du 2026-08-21 ne sont pas disponibles ; elle ne peut donc être classée plus précisément qu'comme une référence au projet officiel.
- Le site officiel utilise des actualités d'août au niveau du mois, tandis que GitHub conserve la chronologie précise des versions ; GitHub fait foi pour les dates de version.
- La documentation de première partie présente un décalage : la prose de la version v0.2.1 mentionne encore un agent terminal, alors que le README actuel indique que la CLI autonome est abandonnée et que les actifs de la v0.2.1 ne contiennent que les paquets bureau et la compétence.
- Aucun rapport d'exploitation en chinois simplifié, de première partie ou reproductible indépendamment, n'a été trouvé pour une recommandation de pratique en langue chinoise.
- Les résultats d'évaluation du rapport technique sont rapportés par les auteurs ; aucune réplication indépendante n'a été vérifiée ici.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://omni-scientist.github.io/ | OmniScientist: An Omni-Modal Omni-Discipline AI Scientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist | Dépôt Omni-Scientist/OmniScientist et README actuel | 2026-09-07 |
| https://arxiv.org/abs/2608.13558 | OmniScientist: An Omni-Modal Omni-Discipline AI Scientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.0 | Version 0.1.0 d'OmniScientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.1 | Version 0.1.1 d'OmniScientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/commits/main | Historique des commits de la branche main d'OmniScientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.2 | Version 0.1.2 d'OmniScientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.3 | Version 0.1.3 d'OmniScientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.6 | Version 0.1.6 d'OmniScientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.0 | Version 0.2.0 d'OmniScientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1 | Version 0.2.1 d'OmniScientist | 2026-09-07 |
| https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md | Guide d'utilisation d'OmniScientist | 2026-09-07 |
| https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md | Instructions de la compétence agent d'OmniScientist | 2026-09-07 |

## Agent brief {#agent-brief}

- **Sujet :** `project:omniscientist`, fil `omniscientist`, 0 événement daté - → -.
- **Note pratique :** Voir les sections d'utilisation et de pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
