---
title: "TSANTSALIZE — Disponibilité publique du modèle"
category: projects
date: 2026-06-19
tags: [ltx_2_3, project, public-model-availability, tsantsalize]
aliases: ["TSANTSALIZE"]
level: 2
source_sha256: a623c9c229d820c65742abcf41b4b5646bd4940c8bd972a005035800256b3e07
translation: machine
translated_at: '2026-10-24'
---
# TSANTSALIZE — Disponibilité publique du modèle {#tsantsalize-public-model-availability}

**Ligne de développement :** `project:tsantsalize` · fil `public-model-availability`  
**Dernier événement :** 2026-06-19 · 1 événement daté depuis le 2026-06-19 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

TSANTSALIZE est un IC-LoRA vidéo-vers-vidéo pour LTX-2.3, destiné aux utilisateurs de ComfyUI qui souhaitent obtenir un effet délibéré de réduction de la tête sur un interprète qui parle.

- Remodèle le sujet parlant à partir d'un clip de référence.
- Laisse le traitement de la voix en dehors de l'adaptateur, dans un workflow audio fourni avec celui-ci.

## Ligne de développement {#development-line}

- **2026-06-19 — Enregistrement de la ressource de modèle TSANTSALIZE sur Hugging Face.** TSANTSALIZE a été mis en usage comme IC-LoRA pour LTX-2.3, afin de réduire la tête d'un sujet parlant. La note de version est datée du 2026-06-18 et précise un mode vidéo-vers-vidéo avec conditionnement sur la première image. La modification de la voix reste dans une chaîne audio côté workflow.

## Changements {#what-changed}

2026-06-19 : TSANTSALIZE a été mis en usage comme IC-LoRA pour LTX-2.3, afin de réduire la tête d'un sujet parlant. La note de version est datée du 2026-06-18 et précise un mode vidéo-vers-vidéo avec conditionnement sur la première image. La modification de la voix reste dans une chaîne audio côté workflow.

## Mode d'emploi {#how-to-use-this}

Consultez le dépôt Hugging Face lié pour vérifier la ressource de modèle TSANTSALIZE publique enregistrée le 2026-06-19, et contrôlez de façon indépendante ses fichiers, sa licence et ses instructions d'utilisation.

1. Téléchargez le checkpoint TSANTSALIZE ainsi que le workflow ComfyUI inclus depuis le dépôt du modèle.
  — <https://huggingface.co/TheBurgstall/tsantsalize>
2. Exécutez-le avec un workflow ComfyUI vidéo-vers-vidéo compatible LTX-2.3 et un clip de référence montrant une personne qui parle ; l'adaptateur ne transforme pas lui-même la voix.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
3. Pour une modification légère des proportions, utilisez une force de LoRA d'environ 0,5 ; pour l'effet visé, utilisez le réglage de 1,2 indiqué par le créateur. Ajoutez `tsantsalize` au prompt ; `tiny head` peut aider.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
4. Utilisez séparément les nœuds audio fournis lorsque vous souhaitez un son modifié : le workflow applique un décalage de hauteur, un traitement passe-haut de la voix et une séparation MelBand RoFormer.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
5. Avant de l'exécuter sur une installation LTX récente, vérifiez que l'adaptateur, le modèle de base, les nœuds et la version du workflow correspondent ; LTX documente la correspondance des versions comme une exigence pour les IC-LoRA.
  — <https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra>

## Bonnes pratiques {#best-practices}

- Commencez avec une seule personne qui parle face caméra. Le créateur signale des résultats nettement moins prévisibles sur d'autres séquences.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Maintenez la force à 1,2 ou en dessous pour obtenir l'effet complet, et utilisez environ 0,5 lorsque seul un petit ajustement est souhaité. Des valeurs supérieures à 1,2 ont entraîné une dérive d'identité dans les tests du créateur.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Ne considérez pas une force négative comme un moyen éprouvé d'agrandir les têtes : le créateur ne l'a pas testée pour cet adaptateur et signale qu'elle a échoué sur des IC-LoRA antérieurs.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Faites correspondre la résolution et la fréquence d'images de la vidéo de référence à celles de la génération, testez d'abord un clip simple, et comparez le résultat avec et sans l'adaptateur avant de vous attaquer à un plan complexe.
  — <https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Le nom exact du fichier de checkpoint, la licence, la révision immuable, le JSON du workflow et l'ensemble des dépendances de nœuds personnalisés n'ont pas pu être récupérés de manière indépendante depuis le dépôt du modèle.
- Aucun portage daté, successeur, benchmark ni test de compatibilité vérifié avec LTX-2.5 n'a été trouvé.
- Le réglage de force de LoRA à 1,2 indiqué par le créateur n'est pas démontrablement équivalent au contrôle `attention_strength` actuel de LTX-2.5, documenté sur une échelle de 0 à 1,0.
- La note de version est datée du 2026-06-18 alors que l'événement enregistré est daté du 2026-06-19 ; les éléments disponibles ne permettent pas d'établir si le 19 juin correspond à une révision distincte du modèle ou à une diffusion ultérieure de la même version.
- Les instantanés de recherche Hugging Face sont contradictoires : un instantané du catalogue de modèles indique TSANTSALIZE comme mis à jour le 2026-06-18, tandis qu'un instantané de profil indique une mise à jour cinq jours plus tôt, sans date calendaire ni révision. Cela ne suffit pas pour créer un événement daté ultérieur.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/TheBurgstall/tsantsalize | Dépôt de modèle TheBurgstall/tsantsalize | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/ | TSANTSALIZE — l'IC-LoRA le plus inutile que vous téléchargerez aujourd'hui | 2026-09-05 |
| https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra | IC-LoRA | Documentation LTX | 2026-09-05 |
| https://docs.ltx.io/open-source-model/integration-tools/ic-lo-ra-adapters | IC-LoRA Adapters | Documentation LTX | 2026-09-05 |
| https://huggingface.co/TheBurgstall | TheBurgstall | Hugging Face | 2026-09-05 |
| https://huggingface.co/TheBurgstall/models | Modèles de TheBurgstall | Hugging Face | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:tsantsalize`, fil `public-model-availability`, 1 événement daté du 2026-06-19 au 2026-06-19.
- **Note pratique :** À partir du 2026-06-19, les praticiens doivent consulter le dépôt Hugging Face lié comme ressource de modèle TSANTSALIZE publique enregistrée, tout en vérifiant de façon indépendante ses fichiers, sa licence et ses instructions d'utilisation actuels.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
