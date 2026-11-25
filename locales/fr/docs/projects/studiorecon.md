---
title: "StudioRecon"
category: projects

tags: [project, studiorecon]
aliases: ["StudioRecon"]
level: 2
source_sha256: e6a073f296ab7738e33f346848c18586f1c4ad4b773bed025caeb83f19d1b2fe
translation: machine
translated_at: '2026-10-24'
---
# StudioRecon {#studiorecon}

**Ligne de développement :** `project:studiorecon` · fil `studiorecon`  
**Dernier événement :** - · 0 daté depuis - · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

StudioRecon reconstruit des scènes 4D dynamiques à partir de captures vidéo éparses à faible recouvrement.

- Séparation de la scène : construit des représentations gaussiennes distinctes pour l'arrière-plan et pour chaque personne.
- Synthèse de nouveaux points de vue : génère des trajectoires de caméra en orbite, en travelling et statiques, avec une option sans amélioration.
- Affinement temporel : applique une amélioration par diffusion sur l'ensemble des images.
- Entrée de capture : nécessite au moins quatre vidéos synchronisées à faible recouvrement.

La pile hors ligne exige plusieurs environnements Conda, CUDA et environ 110 Go pour télécharger les poids de GEN3C, Cosmos et T5. Il s'agit de code de recherche reproductible, et non d'un outil de production rapide.

## Ligne de développement {#development-line}

- L'événement daté n'a pas encore fait l'objet d'une rédaction ; les informations connues figurent dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-15 — StudioRecon a été présenté comme une méthode de reconstruction 4D pour SIGGRAPH 2026, à partir de vidéos éparses à faible recouvrement. L'article initial v1, daté du 2026-07-10, précise les composants du pipeline. GEN3C génère des centaines de vues synthétiques de l'arrière-plan, tandis que CoMotion/DWPose et NLF/SMPL suivent les personnes. La méthode construit des représentations gaussiennes distinctes et applique DiFiX pour l'amélioration temporelle.

## Comment l'utiliser {#how-to-use-this}

Aucune modification du workflow pratique ne peut être établie à partir du seul lien daté vers la page du projet ; consultez la page liée ou la publication source avant de considérer cela comme une étape de développement de StudioRecon.

1. Clonez le dépôt avec ses sous-modules et initialisez les sources tierces.
  — <https://github.com/sisyphm/StudioRecon>
2. Créez des environnements Conda distincts pour le pipeline principal, SAM3, GEN3C, CoMotion, Segment Anything et DiFiX, en utilisant des versions épinglées de Torch et CUDA.
  — <https://github.com/sisyphm/StudioRecon/blob/master/docs/INSTALL.md>
3. Téléchargez les poids requis, demandez à l'avance l'accès à SAM3 (accès restreint), et vérifiez les chemins pour NLF, SMPL, SAM et GEN3C.
  — <https://github.com/sisyphm/StudioRecon/blob/master/docs/CHECKPOINTS.md>
4. Préparez une scène à partir d'un jeu de données pris en charge, testez d'abord le pipeline avec --dry-run, puis exécutez la configuration de la scène sur les GPU attribués.
  — <https://github.com/sisyphm/StudioRecon>
5. Effectuez le rendu de la scène entraînée avec scripts/render.sh ; utilisez --no-enhance pour obtenir le rendu gaussien brut, sans DiFiX.
  — <https://github.com/sisyphm/StudioRecon>

## Bonnes pratiques {#best-practices}

- Gardez les dépendances de DiFiX séparées de l'environnement principal, afin que des versions épinglées incompatibles de Torch, CUDA et diffusers n'entrent pas en conflit.
  — <https://github.com/sisyphm/StudioRecon/blob/master/docs/INSTALL.md>
- Lancez un --dry-run et un test de fumée avant de télécharger les gros modèles ; vérifiez les fichiers de points de contrôle obligatoires et la somme de contrôle de NLF une fois téléchargés.
  — <https://github.com/sisyphm/StudioRecon/blob/master/docs/INSTALL.md>
- Demandez l'approbation manuelle pour SAM3 avant de commencer ; conservez les poids d'exécution dans les chemins documentés ou spécifiez-les explicitement dans le YAML de la scène.
  — <https://github.com/sisyphm/StudioRecon/blob/master/docs/CHECKPOINTS.md>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- L'exécution indépendante de bout en bout sur une infrastructure tierce n'est pas vérifiée ; les articles et le dépôt ne confirment que la méthode et le code.
- Les résultats publiés ne couvrent que leurs protocoles à quatre caméras, ce qui laisse les performances non démontrées pour des caméras, des scènes ou un nombre de personnes quelconques, ou pour un fonctionnement en temps réel.
- La structure du dépôt et les instructions sont disponibles dès maintenant, mais les dates de commit individuelles et les dates de publication ne peuvent pas être extraites de façon fiable ; nous ne pouvons pas les considérer comme des événements de développement datés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://sisyphm.github.io/studiorecon-page/ | StudioRecon : reconstruction 4D humain-scène à partir de captures à faible recouvrement | 2026-09-05 |
| https://arxiv.org/abs/2607.09125 | Reconstruction 4D humain-scène à partir de captures à faible recouvrement | 2026-09-05 |
| https://github.com/sisyphm/StudioRecon | sisyphm/StudioRecon | 2026-09-05 |
| https://github.com/sisyphm/StudioRecon/blob/master/docs/INSTALL.md | Guide d'installation de StudioRecon | 2026-09-05 |
| https://github.com/sisyphm/StudioRecon/blob/master/docs/CHECKPOINTS.md | Points de contrôle et poids des modèles de StudioRecon | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:studiorecon`, fil `studiorecon`, 0 événement daté - → -.
- **Note pratique :** Aucune modification du workflow pratique ne peut être établie à partir du seul lien daté vers la page du projet ; consultez la page liée ou la publication source avant de considérer cela comme une étape de développement de StudioRecon.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
