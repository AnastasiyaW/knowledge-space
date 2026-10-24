---
title: "LTX-2.3"
category: projects
date: 2026-07-30
tags: [ltx-video, project]
aliases: ["LTX Video", "LTX-2.3"]
level: 3
source_sha256: 38d216683489406a70db0179a5706d6f9895ebb94ac526e49131f6a3f05635c6
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.3 {#ltx-23}

**Ligne de développement :** `project:ltx-video` · fil `ltx-video`  
**Dernier événement :** 2026-07-30 · 3 entrées datées depuis le 2026-03-05 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

LTX-2.3 est un modèle de fondation audio-vidéo basé sur un DiT de 22B, destiné aux équipes qui génèrent localement de la vidéo et de l'audio synchronisés, dans ComfyUI ou via l'API LTX.

- Génération : text-to-video et image-to-video.
- Fonctions Pro : audio-to-video, Retake, Extend et Reframe.
- Voies de poids : checkpoints dev, distilled, fp8 et latent upscaler.

22B paramètres ; le dépôt Hugging Face actuel fait 156 Go et le checkpoint dev seul fait 46,1 Go. Nous le conservons pour les intégrations existantes et les adaptateurs spécifiques à la 2.3 ; les nouveaux travaux sur le multi-plans, l'édition de séquences ou le fine-tuning poussé doivent débuter sur LTX-2.5.

## Ligne de développement {#development-line}

- **2026-03-05 — LTX-2.3 a été présenté avec sa documentation et un playground text-to-video.** Fast gérait le text-to-video et l'image-to-video, tandis que Pro ajoutait audio-to-video, Retake et Extend ; les poids dev/distilled 22B et les latent upscalers ont été publiés.
- **2026-03-05 — Les fichiers du modèle LTX-2.3 et un workflow ComfyUI text-to-video ont été liés.** Fast gérait le text-to-video et l'image-to-video, tandis que Pro ajoutait audio-to-video, Retake et Extend ; les poids dev/distilled 22B et les latent upscalers ont été publiés.
- **2026-07-30 — Un LoRA IC 22B de LTX-2.3 pour le relighting a été publié.** Le 2026-07-30, une ressource Hugging Face nommée LTX-2.3-22B-IC-LoRA-Relight a été liée. Il s'agit d'une extension notable de la lignée LTX-2.3, car elle ajoute une capacité spécialisée de relighting via une ressource LoRA.

## Évolutions {#what-changed}

- **2026-03-05** — LTX-2.3 est devenu le modèle par défaut de l'API : Fast gérait le text-to-video et l'image-to-video, tandis que Pro ajoutait audio-to-video, Retake et Extend ; les poids dev/distilled 22B et les latent upscalers ont été publiés.
- **2026-04-23** — La conversion HDR asynchrone a ajouté la sortie SDR vers EXR.
- **2026-05-03** — Async V2 a été étendu au text-to-video, à l'image-to-video, à l'audio-to-video, à Retake et à Extend.
- **2026-07-02** — LTX-2 a été déprécié, avec un routage automatique temporaire vers LTX-2.3.
- **2026-07-07** — Le reframe vidéo asynchrone a ajouté un remplissage généré pour un nouveau format d'image.
- **2026-07-30** — LTX-2.3-22B-IC-LoRA-Relight a ajouté le relighting contrôlé de vidéos en extérieur, à partir d'un clip source et d'une sphère indiquant la direction de la lumière.
- **2026-08-02** — Le text-to-video et l'image-to-video de LTX-2.3 ont reçu un palier 720p.
- **2026-08-11** — LTX-2.5 a ajouté Fast jusqu'en 4K, Pro en 720p/1080p, le mouvement de caméra, l'image-to-video à partir de la dernière image et la durée automatique ; il constitue désormais le point de départ recommandé.
- **2026-08-16** — Les identifiants de modèle de l'API LTX-2 ont cessé de fonctionner ; les cibles de migration restantes sont LTX-2.3 et LTX-2.5.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-05, les praticiens peuvent utiliser LTX-2.3 via sa route text-to-video documentée ou le workflow ComfyUI lié ; à partir du 2026-07-30, ils doivent évaluer le LoRA IC 22B dédié au relighting lorsque celui-ci est nécessaire.

1. Conservez LTX-2.3 pour une intégration en production ou un adaptateur spécifique à la 2.3 ; sélectionnez LTX-2.5 pour un nouveau projet.
  — <https://ltx.io/model/ltx-2-3>
2. Créez une clé API dans la Developer Console, puis soumettez une requête text-to-video ou image-to-video.
  — <https://docs.ltx.video/quickstart>
3. Utilisez `ltx-2-3-fast` pour les aperçus text/image ; utilisez `ltx-2-3-pro` lorsque le workflow nécessite audio-to-video, Retake, Extend ou Reframe.
  — <https://docs.ltx.io/models/ltx-2-3>
4. En production, soumettez une tâche asynchrone V2, conservez son identifiant de tâche, interrogez jusqu'à la fin et téléchargez l'URL du résultat.
  — <https://docs.ltx.io/async-jobs>
5. Pour une exécution locale, clonez LTX-2, exécutez `uv sync`, téléchargez LTX-2.3 ainsi que Gemma 3 12B, puis choisissez le pipeline distilled pour la vitesse ou le pipeline HQ en deux étapes pour la qualité.
  — <https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md>
6. Dans ComfyUI, mettez d'abord ComfyUI à jour, chargez le workflow text-to-video fourni, et placez son checkpoint fp8, ses LoRA et son spatial upscaler dans les dossiers de modèles indiqués.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json>
7. Pour le relighting de vidéos en extérieur, utilisez le graphe officiel en une seule étape avec le Relight IC-LoRA à un poids de 1.0 et un clip source comportant la sphère indiquant la direction de la lumière.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight>

## Bonnes pratiques {#best-practices}

- Considérez la largeur et la hauteur divisibles par 32, ainsi que le nombre d'images divisible par 8+1, comme un contrat d'entrée ; sinon, complétez avec -1 puis recadrez après la génération.
  — <https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md>
- Rédigez un plan unique, ciblé et chronologique, avec une action, une caméra, un éclairage et un audio explicites ; réécrivez les prompts issus d'autres modèles vidéo au lieu de copier leurs balises ou listes de plans telles quelles.
  — <https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide>
- Utilisez Fast pour la génération itérative text/image et réservez Pro à l'ensemble d'endpoints qui l'exige.
  — <https://docs.ltx.io/models/ltx-2-3>
- Utilisez les tâches asynchrones pour les charges de production plutôt que de maintenir une connexion synchrone longue.
  — <https://docs.ltx.io/async-jobs>
- Pour Relight, restez sur des séquences filmées en extérieur, alignez la référence de la sphère sur le clip cible, utilisez le prompt de direction minimal, et évitez le véritable chemin en deux étapes, car l'étape 2 supprime le conditionnement.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight>
- Lors d'une migration depuis LTX-2, réentraînez les LoRA personnalisés pour l'espace latent de LTX-2.3 au lieu de supposer une compatibilité directe.
  — <https://ltx.io/model/ltx-2-3>

## Remplacé par {#superseded-by-this}

- 2026-03-05 — « Les LoRA LTX-2 personnalisés fonctionnent sans modification sur LTX-2.3 » est obsolète ; un réentraînement est nécessaire pour l'espace latent 2.3.
- 2026-08-11 — « LTX-2.3 est le point de départ recommandé pour un nouveau projet » est remplacé par LTX-2.5 ; LTX-2.3 reste pris en charge pour les intégrations existantes.
- 2026-08-16 — « `ltx-2-fast` et `ltx-2-pro` restent des identifiants de modèle API valides » est obsolète ; ces requêtes renvoient des erreurs.

## Points non élucidés {#still-unknown}

- L'élément du 2026-07-30 est une publication d'adaptateur IC-LoRA de première partie, et non un nouveau checkpoint de base LTX-2.3 ; les sources disponibles ne permettent pas de dire si chaque publication d'adaptateur relève de l'historique du modèle principal.
- La fiche du modèle Relight n'affiche pas de date de publication indépendante ; sa chronologie est donc ancrée au 2026-07-30, tandis que son périmètre technique est vérifié par la source de première partie.
- L'URL d'origine du text-to-video Studio redirige désormais vers la page d'accueil de Studio ; sans instantané daté, son interface et sa disponibilité exactes au 2026-03-05 ne peuvent pas être reconstituées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://ltx.io/model/ltx-2-3 | LTX-2.3: Previous Generation AI Video Model | LTX | 2026-09-04 |
| https://docs.ltx.video/quickstart | Quick Start | LTX Documentation | 2026-09-04 |
| https://app.ltx.studio/ltx-2-playground/t2v | AI video production | LTX | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/tree/main | Lightricks/LTX-2.3 at main | 2026-09-04 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json | workflow_templates/templates/video_ltx2_3_t2v.json at main · Comfy-Org/workflow_templates · GitHub | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Relight | Lightricks/LTX-2.3-22b-IC-LoRA-Relight · Hugging Face | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/commits/main | Commits · Lightricks/LTX-2.3 | 2026-09-04 |
| https://huggingface.co/Lightricks/LTX-2.3/blob/main/README.md | README.md · Lightricks/LTX-2.3 at main | 2026-09-04 |
| https://docs.ltx.io/models/ltx-2-3 | LTX-2.3 | LTX Documentation | 2026-09-04 |
| https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide | Prompting Guide | LTX Documentation | 2026-09-04 |
| https://docs.ltx.io/async-jobs | Async Jobs | LTX Documentation | 2026-09-04 |
| https://docs.ltx.io/api-changelog | API Changelog | LTX Documentation | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ltx-video`, fil `ltx-video`, 3 événements datés du 2026-03-05 au 2026-07-30.
- **Note pratique :** À partir du 2026-03-05, les praticiens peuvent utiliser LTX-2.3 via sa route text-to-video documentée ou le workflow ComfyUI lié ; à partir du 2026-07-30, ils doivent évaluer le LoRA IC 22B dédié au relighting lorsque celui-ci est nécessaire.
- **Confiance :** moyenne. Les mentions « remplacé par » datées font foi quant à ce qui est obsolète.
