---
title: "RealFusion"
category: projects
date: 2023-03-03
tags: [code_release, project, realfusion, realfusion-development]
aliases: ["RealFusion"]
level: 2
source_sha256: 0ce5d87fa10dbce7431800b2a42b955434b705c345eda904d599aeea75515881
translation: machine
translated_at: '2026-10-24'
---
# RealFusion {#realfusion}

**Ligne de développement :** `project:realfusion` · fil `realfusion-development`  
**Dernier événement :** 2023-03-03 · 1 événement daté depuis le 2023-03-03 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

RealFusion reconstruit un objet plausible à 360 degrés à partir d'une seule image masquée, en combinant une inversion textuelle sur image unique (single-image textual inversion), la distillation de score de Stable Diffusion et un NeRF de type Instant-NGP.

- inversion de jeton : apprend un jeton propre à l'image
- champ de radiance : optimisé à partir de l'image d'entrée et du prior de diffusion
- export de maillage : exporte optionnellement un maillage texturé

La géométrie non observée est inférée, et non reconstruite ; les échecs de convergence et les visages dupliqués de type Janus restent des modes de défaillance documentés.

Utilisez-le comme base de reproductibilité ou comme workflow de recherche paramétrable, et non comme produit clé en main actuel de conversion image vers 3D.

## Ligne de développement {#development-line}

- **2023-03-03 — Code de RealFusion et ressources du projet publiés.** Le 2023-03-03, la ligne de développement de RealFusion a enregistré une entrée de publication de code, avec des liens vers la page publique du projet et le dépôt GitHub. Cela fixe un point de référence public daté, mais aucune version, aucun commit ni aucune modification technique précise n'est identifié.

## Changements {#what-changed}

2023-03-03 — La page publique du projet RealFusion et la publication du code ont rendu le workflow inversion textuelle sur image unique plus NeRF exécutable en dehors de l'implémentation du papier. 2023-04-08 — La référence ultérieure renvoie à la publication du 2023-03-03 ; ce lien n'atteste aucune mise à jour distincte du code, du modèle ou de la méthode de RealFusion.

## Mode d'emploi {#how-to-use-this}

À partir du 2023-03-03, les praticiens pouvaient utiliser la page projet datée de RealFusion et les liens vers le dépôt comme point de départ pour localiser les ressources de publication de code publiquement référencées.

1. Installez les dépendances Python, PyTorch séparément et les extensions CUDA ; installez nvdiffrast uniquement pour exporter un maillage texturé.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
2. Préparez une image RGBA carrée contenant l'objet et son masque ; utilisez le script d'extraction de masque fourni si vous partez d'une image non masquée.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
3. Lancez l'inversion textuelle sur image unique avec Stable Diffusion v1.5 pour créer l'embedding appris de l'objet.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
4. Lancez la reconstruction avec `python main.py --O`, l'image RGBA, l'embedding appris et le checkpoint Stable Diffusion correspondant.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
5. Inspectez les vues novatrices et ajustez la pose de caméra, les rayons de caméra, les pertes et les graines aléatoires pour l'image considérée avant d'accepter un résultat.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>

## Bonnes pratiques {#best-practices}

- Partez d'une image propre de l'objet masqué ; le contrat d'entrée documenté est une image RGBA carrée.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Utilisez `--O` : le dépôt indique que son chemin de raymarching CUDA a été développé et testé avec ce bundle d'optimisation.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Faites correspondre `pose_angle` au point de vue de la caméra et réglez `radius_rot` légèrement au-dessus du maximum du rayon d'entraînement.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Lancez plusieurs graines et sélectionnez les résultats après inspection ; les paramètres par défaut ne sont explicitement pas aussi bons pour tous les exemples.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Considérez les faces arrière comme des extrapolations plausibles, et rejetez les champs transparents, les flottants, les géométries incorrectes ou les résultats à faces dupliquées plutôt que de les présenter comme une géométrie reconstruite.
  — <https://arxiv.org/abs/2302.10663>

## Ce qui a été remplacé {#superseded-by-this}

- 2023-03-03 — La version refactorisée du dépôt public a remplacé le recours aux détails d'implémentation d'origine du papier ; son mainteneur indique que certaines parties diffèrent du code du papier.
- 2023-04-08 — Considérer la référence ultérieure comme une publication distincte est obsolète : elle renvoie à l'élément antérieur du 2023-03-03 au lieu de documenter une nouvelle publication.

## Points non établis {#still-unknown}

- Aucune publication, aucun checkpoint, aucun test de compatibilité ni aucune annonce de méthode successeure datés et émanant des auteurs n'ont été trouvés pour la référence du 2023-04-08 ; il semble s'agir d'un pointeur rétrospectif vers l'élément antérieur, et non d'une étape de développement distincte.
- Le dépôt actuel documente un workflow de recherche dépendant de CUDA, mais n'apporte aucune preuve de compatibilité avec les versions actuelles de PyTorch, CUDA, Diffusers ou de l'écosystème Stable Diffusion.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://lukemelas.github.io/realfusion/ | Page du projet RealFusion | 2026-09-05 |
| https://github.com/lukemelas/realfusion | lukemelas/realfusion | 2026-09-05 |
| https://github.com/lukemelas/realfusion/blob/main/README.md | README de RealFusion | 2026-09-05 |
| https://arxiv.org/abs/2302.10663 | RealFusion: 360° Reconstruction of Any Object from a Single Image | 2026-09-05 |
| https://cvpr.thecvf.com/virtual/2023/poster/21294 | CVPR 2023 poster: RealFusion: 360° Reconstruction of Any Object From a Single Image | 2026-09-05 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:realfusion`, fil `realfusion-development`, 1 événement daté du 2023-03-03 au 2023-03-03.
- **Note pratique :** À partir du 2023-03-03, les praticiens pouvaient utiliser la page projet datée de RealFusion et les liens vers le dépôt comme point de départ pour localiser ses ressources de publication de code publiquement référencées.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
