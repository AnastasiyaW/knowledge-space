---
title: "Krea2-realism — LoRA Krea2"
category: projects
date: 2026-07-04
tags: [krea2-loras, krea2-realism, project]
aliases: ["Krea2-realism"]
level: 2
source_sha256: f8add336247b196f6cf4261cde724b26766d8cbb3f92378d128c88bd96929348
translation: machine
translated_at: '2026-10-24'
---
# Krea2-realism — LoRA Krea2 {#krea2-realism-krea2-loras}

**Ligne de développement :** `project:krea2-realism` · fil `krea2-loras`  
**Dernier événement :** 2026-07-04 · 1 daté depuis le 2026-07-04 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

Krea2-realism est une ligne de LoRA communautaires pour le modèle text-to-image Krea 2 Turbo, dont l'accès est restreint.

- La V1 cible des sujets photoréalistes SFW et NSFW.
- La V2 cible l'expression faciale, la texture, l'éclairage, la composition et la compatibilité avec les LoRA de personnage.
- Génération et aide à l'image-to-image, et non un modèle d'édition d'images.

Le guide de la V2 maintenu recommande un prompt en langage naturel de 4 à 5 phrases et une force de LoRA de 1,5 à 2,0.

Nous utilisons la V2 pour tout nouveau travail avec Krea 2, en particulier lorsqu'un LoRA de personnage doit conserver son visage. Nous ne conservons la V1 que pour reproduire une configuration existante.

## Ligne de développement {#development-line}

- **2026-07-04 — Références de modèles propres à la version Krea2 Realism v1 enregistrées.** Le 2026-07-04, la ligne de développement Krea2-realism a enregistré deux références Civitai propres à la version pour Krea2 Realism v1. Les liens identifient des artefacts de versions de modèle distincts, 3066973 et 3090634 ; nous suivons donc les versions disponibles dans l'historique du projet.

## Historique des modifications {#what-changed}

- 2026-06-24 — Krea2-realism-V1, version de modèle 3066973, est arrivé comme LoRA de réalisme pour Krea 2, pour la génération SFW et NSFW.
- 2026-07-02 — Krea2-realism-V2, version de modèle 3090634, a remplacé la V1 comme révision active. Elle apporte des visages plus naturels, une texture, un éclairage et une composition améliorés, ainsi qu'une meilleure coexistence avec les LoRA de personnage.
- 2026-07-04 — Les liens des versions de modèle V1 et V2 ont été collectés ensemble. Il ne s'agit pas d'une version datée indépendamment.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-04, nous épinglons Krea2 Realism v1 par son modelVersionId Civitai exact et nous consignons laquelle des deux versions référencées a été utilisée, plutôt que de traiter la page du modèle comme un artefact unique sans version.

1. Demander l'accès à Krea 2 Turbo et accepter sa licence communautaire avant de télécharger ou d'exécuter le modèle de base.
  — <https://huggingface.co/krea/Krea-2-Turbo>
2. Télécharger Krea2-realism-V2, la révision actuelle de cette ligne de LoRA.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>
3. Dans ComfyUI, placer le fichier LoRA dans `ComfyUI/models/loras/` et le sélectionner avec un nœud Load LoRA dans un workflow Krea 2.
  — <https://note.com/yasashii_maou/n/naf58ef9a48fb?hl=en>
4. Partir du workflow V1 si disponible, en remplaçant uniquement le LoRA par la V2. Utiliser l'image-to-image plutôt que de le traiter comme un éditeur dédié.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>
5. Décrire la scène dans un court paragraphe en langage naturel. Ajuster le poids du LoRA en fonction du sujet choisi et du LoRA de personnage.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>

## Bonnes pratiques {#best-practices}

- Privilégier la V2 à la V1 lorsqu'on empile un LoRA de personnage : la V2 ne modifie pas les visages fournis par d'autres LoRA de personnage.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>
- Utiliser une description de scène de 4 à 5 phrases plutôt qu'un empilement de tags. Commencer autour de la force 1,0 pour une comparaison contrôlée, puis tester 1,5 à 2,0 si le résultat nécessite un effet plus marqué.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>
- Considérer la V2 comme un composant de génération d'images ou d'image-to-image, et non comme un éditeur d'images sémantique.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>

## Remplacé par {#superseded-by-this}

- 2026-06-24 — Krea2-realism-V1 (version de modèle 3066973) est remplacée, pour les nouveaux travaux, par Krea2-realism-V2 (version de modèle 3090634, publiée le 2026-07-02). Le workflow V1 reste utilisable en remplaçant le LoRA.

## Points encore inconnus {#still-unknown}

- Les points de terminaison Civitai d'origine étaient inaccessibles ; les métadonnées du modèle, la disponibilité des téléchargements et les conditions de licence de ces pages n'ont pas pu être vérifiées.
- Le miroir Hugging Face de la V2 déclare la licence MIT, alors que le modèle de base Krea 2 est soumis à la Krea 2 Community License. Les conditions de distribution et d'utilisation applicables au workflow combiné doivent être confirmées sur la page du modèle d'origine.
- Aucune source ne documente une publication le 2026-07-04 elle-même. Cette date enregistre les deux liens de version plutôt qu'une nouvelle modification du modèle.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://civitai.red/models/2728365/krea2-realism-v1?modelVersionId=3066973 | Krea2-realism-V1, version de modèle 3066973 | 2026-09-05 |
| https://civitai.red/models/2728365/krea2-realism-v1?modelVersionId=3090634 | Krea2-realism-V2, version de modèle 3090634 | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ueq9au/one_lora_for_krea_2_sfw_and_not_sfw_realism/ | One LoRA for Krea 2. SFW and Not SFW Realism. | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/ | Krea2-realism-V2 is finally here! Things got a little wild (in the best way possible) | 2026-09-05 |
| https://huggingface.co/RudySen/Krea2-realism-V2 | RudySen/Krea2-realism-V2 | 2026-09-05 |
| https://huggingface.co/krea/Krea-2-Turbo | krea/Krea-2-Turbo | 2026-09-05 |
| https://note.com/yasashii_maou/n/naf58ef9a48fb?hl=en | [ComfyUI] A memo on using the realistic LoRA 'realism-V2' for Krea 2. With images | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:krea2-realism`, fil `krea2-loras`, 1 événement daté du 2026-07-04 → 2026-07-04.
- **Note pratique :** À partir du 2026-07-04, nous épinglons Krea2 Realism v1 par son modelVersionId Civitai exact et nous consignons laquelle des deux versions référencées a été utilisée, plutôt que de traiter la page du modèle comme un artefact unique sans version.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
