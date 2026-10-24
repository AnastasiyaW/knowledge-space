---
title: "FramePack Studio"
category: projects
date: 2025-07-04
tags: [framepack-studio, framepack-studio-development, framepack_studio, project]
aliases: ["FramePack Studio", "Framepack Studio"]
level: 3
source_sha256: 949bc07b72fdda500f02dbac84078e58d165fd5f90a89da25a43c8ce69888152
translation: machine
translated_at: '2026-10-24'
---
# FramePack Studio {#framepack-studio}

**Ligne de développement :** `project:framepack-studio` · fil `framepack-studio-development`  
**Dernier événement :** 2025-07-04 · 2 événements datés depuis 2025-05-05 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

FramePack Studio est une application locale construite sur FramePack, destinée aux créateurs qui ont besoin de la génération image-vers-vidéo Original et F1, ainsi que de l'extension de vidéo, sans avoir à assembler un workflow distinct.

- génération Original et par image de fin, génération F1 et extension de vidéo ;
- entrées de type texte, image, vidéo, LoRA, prompt horodaté et mélange de prompts ;
- files de tâches, préréglages, métadonnées reproductibles, upscaling, interpolation, filtres et bouclage.

Le minimum matériel est un GPU CUDA disposant d'au moins 8 Go de VRAM (16 Go recommandés), 16 Go de mémoire système et 80 Go de stockage. Le premier lancement télécharge environ 30 Go de modèles.

Pour un workflow GPU local, utilisez le dépôt FP-Studio et sa documentation. Ne le confondez pas avec le service navigateur sans rapport accessible à framepack.studio.

## Ligne de développement {#development-line}

- **2025-05-05 — le dépôt FramePack Studio a été relié.** Le 2025-05-05, des liens ont associé FramePack Studio au dépôt GitHub colinurbs/FramePack-Studio et à un élément GreenNeuralRobots. Les éléments disponibles n'identifient ni version, ni publication, ni fonctionnalité précise.
- **2025-07-04 — la documentation de FramePack Studio et le dépôt du projet ont été reliés.** Le 2025-07-04, des liens ont relié FramePack Studio au dépôt GitHub FP-Studio/FramePack-Studio et à son site de documentation. Ces liens ne permettent pas d'établir s'il s'agissait d'une publication, d'une migration ou d'un changement de fonctionnalité.

## Ce qui a changé {#what-changed}

FramePack Studio a déplacé son adresse publique, d'une URL de dépôt personnel vers le projet FP-Studio et sa documentation, tandis que la dernière version formelle trouvée reste la 0.5.1.

- 2025-05-05 — le lien du projet pointait vers colinurbs/FramePack-Studio ; il redirige désormais vers FP-Studio/framepack-studio. Le texte de l'annonce n'est pas disponible, aucun changement de fonctionnalité n'est donc attribué à cette date.
- 2025-06-30 (trouvé aujourd'hui) — la v0.5.0 a rendu MagCache cache par défaut, ajouté l'amélioration de prompt Granite et la description d'images Florence2, publié des images Docker et annoncé le site de documentation.
- 2025-07-04 — les liens du projet pointent vers le dépôt FP-Studio et la documentation officielle, ce qui confirme la même identité de projet et non un second FramePack Studio.
- 2025-07-14 (trouvé aujourd'hui) — la v0.5.1 a fait utiliser à Original l'image d'entrée comme première image, et corrigé l'ordre des arguments FFmpeg pour les boucles vidéo.
- 2025-11-14 (trouvé aujourd'hui) — la branche main a reçu des mises à jour de versions de paquets ; aucune version plus récente n'est répertoriée.
- 2026-03-07 (trouvé aujourd'hui) — une modification de journalisation sur develop a déclenché un workflow de publication Docker qui a échoué lors de l'installation des dépendances. Cela signale une fragilité de la voie Docker de développement ; cela ne prouve pas que la version 0.5.1 ne peut pas fonctionner.

La page publique des versions indique toujours 0.5.1 comme dernière version.

Le projet est resté actif après sa dernière publication, mais un déploiement actuel doit utiliser une version figée et testée, plutôt que de supposer que develop est publiable.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-07-04, consultez le dépôt FramePack Studio relié, ainsi que son site de documentation, lorsque vous évaluez ou utilisez le projet ; les seuls liens datés n'établissent pas de workflow propre à une version donnée.

1. Vérifiez que le GPU, la version CUDA/Torch, la mémoire et le stockage respectent les exigences documentées ; choisissez Pinokio, Docker, l'installation automatisée Windows ou une installation manuelle pour l'hôte.
  — <https://docs.framepackstudio.com/docs/get_started/>
2. Installez et démarrez l'application. Pour Docker, clonez le dépôt et exécutez docker compose ; pour une installation manuelle, créez un environnement virtuel, installez les dépendances et la version de Torch correspondant à CUDA, puis lancez studio.py.
  — <https://docs.framepackstudio.com/docs/get_started/>
3. Ouvrez l'interface locale à l'adresse http://localhost:7860 une fois le téléchargement initial des modèles terminé.
  — <https://docs.framepackstudio.com/docs/get_started/>
4. Choisissez Original pour une meilleure cohérence, Original with Endframe lorsque l'image finale compte, F1 pour un mouvement plus dynamique, ou un mode Video pour prolonger un clip existant ; fournissez l'entrée image ou vidéo correspondante.
  — <https://docs.framepackstudio.com/docs/user_guide/>
5. Rédigez un prompt précis avec le sujet, la scène, l'action, la caméra, l'éclairage et le cadrage ; utilisez des segments de prompt horodatés lorsque l'action doit évoluer dans le temps.
  — <https://docs.framepackstudio.com/docs/prompting_guide/>
6. Ajoutez des tâches à la file, inspectez les sorties et les métadonnées sauvegardées, puis envoyez les clips retenus au post-traitement pour des opérations telles que l'upscaling, l'interpolation, les filtres ou les boucles.
  — <https://docs.framepackstudio.com/docs/user_guide/>

## Bonnes pratiques {#best-practices}

- Faites correspondre la version CUDA de Torch au GPU et utilisez la procédure d'installation documentée pour l'hôte. Pinokio est la voie la plus simple pour une installation sans compétences techniques, mais il est explicitement plus difficile à dépanner.
  — <https://docs.framepackstudio.com/docs/get_started/>
- N'installez qu'une seule bibliothèque d'attention au maximum, et n'installez pas SageAttention, FlashAttention ou xFormers sur les GPU RTX de série 1000/2000, car la documentation avertit que cela peut provoquer des erreurs de génération.
  — <https://docs.framepackstudio.com/docs/get_started/>
- Choisissez le modèle en fonction du compromis : Original conserve généralement mieux la cohérence, tandis que F1 produit généralement un mouvement plus dynamique mais peut pulser entre les sections.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Gardez un prompt concret mais borné : nommez le sujet, la scène, l'action, la caméra, l'éclairage et la taille du plan ; le guide officiel suggère 60 à 100 mots et un enchaînement logique.
  — <https://docs.framepackstudio.com/docs/prompting_guide/>
- Sauvegardez le JSON des métadonnées et conservez la graine (seed) des exécutions prometteuses, afin de pouvoir restaurer et comparer les paramètres au lieu de les reconstituer de mémoire.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Considérez un CFG plus élevé et une mise en cache plus agressive comme des compromis qualité-vitesse : un CFG supérieur à 1 double le temps de génération et peut ajouter des artefacts ; des seuils MagCache plus bas ou une rétention plus faible peuvent être plus rapides, mais s'écartent davantage de la sortie sans cache.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Ne supposez pas que la voie Docker de develop est publiable : le dernier workflow de publication observé sur develop a échoué pendant l'installation des dépendances. Figez et testez la version choisie.
  — <https://github.com/FP-Studio/framepack-studio/actions/runs/22808835350>

## Remplacé par ceci {#superseded-by-this}

- 2025-05-05 — considérer colinurbs/FramePack-Studio comme une adresse de projet actuelle distincte ; cette adresse redirige vers FP-Studio/framepack-studio.
- 2025-06-30 — hypothèses antérieures à la v0.5 selon lesquelles MagCache n'était pas le cache par défaut, ou qu'aucun site de documentation n'existait.
- 2025-07-14 — hypothèses de l'époque de la v0.5.0 concernant la gestion de l'image d'entrée d'Original ; la v0.5.1 utilise l'image d'entrée comme première image.
- 2026-03-07 — considérer une image Docker issue de develop comme une voie de déploiement vérifiée ; l'exécution de publication observée a échoué.

## Toujours inconnu {#still-unknown}

- Le texte exact et les affirmations de fonctionnalités des annonces du 2025-05-05 et du 2025-07-04 ne sont pas disponibles ; leurs liens établissent l'identité du projet, et non une note de version précise.
- Les deux liens GitHub datés renvoient au même projet FP-Studio, ils n'indiquent donc pas deux sujets différents. Un service distinct orienté navigateur, accessible à framepack.studio, utilise le même nom et ne doit pas être assimilé à FP-Studio.
- Aucune documentation de première main en chinois simplifié, ni source confirmée de retours d'expérience en chinois, n'a été trouvée lors des recherches observées ; les résultats en chinois renvoyaient principalement à la collision de nom avec le service sans rapport.
- Il n'existe ici aucun retour de réussite d'installation propre ni de déploiement Docker actuel fonctionnel. La documentation, l'historique des versions, le rapport d'installation ouvert de mai 2026 et la tâche de publication develop échouée de mars 2026 montrent que l'état de l'installation et du packaging a pu diverger depuis la v0.5.1.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/colinurbs/FramePack-Studio/ | GitHub - FP-Studio/framepack-studio: Expanding FramePack into a multifunction video creation tool | 2026-09-04 |
| https://github.com/FP-Studio/FramePack-Studio/ | FP-Studio/framepack-studio repository | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio | GitHub - FP-Studio/framepack-studio: Expanding FramePack into a multifunction video creation tool | 2026-09-04 |
| https://github.com/FP-Studio/FramePack-Studio/releases | Releases · FP-Studio/framepack-studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/get_started/ | Getting Started | FP-Studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/user_guide/ | User Guide | FP-Studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/prompting_guide/ | Prompting Guide | FP-Studio | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/commits/main/ | Commits · FP-Studio/framepack-studio | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/actions/runs/22808835350 | finish logging implementation · FP-Studio/framepack-studio@648e34a | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/issues/382 | Installation Fail for FP-Studio · Issue #382 | 2026-09-04 |
| https://framepack.studio/zh | FramePack Studio | FramePack AI、FramePack Studio 及图像转视频工作流程 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Sujet :** `project:framepack-studio`, fil `framepack-studio-development`, 2 événements datés du 2025-05-05 au 2025-07-04.
- **Note pratique :** À partir du 2025-07-04, les praticiens doivent consulter le dépôt FramePack Studio relié, ainsi que son site de documentation, lorsqu'ils évaluent ou utilisent le projet ; les seuls liens datés n'établissent pas de workflow propre à une version donnée.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
