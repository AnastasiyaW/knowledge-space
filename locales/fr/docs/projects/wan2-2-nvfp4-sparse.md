---
title: "Wan2.2-NVFP4-Sparse"
category: projects
date: 2026-06-05
tags: [project, wan, wan2-2-nvfp4-sparse, wan2-2-nvfp4-sparse-development]
aliases: ["Wan2.2-NVFP4-Sparse"]
level: 3
source_sha256: 91fef09886dce840d729573fcbe91cc227d6364644e8a1cd022fad6117b8ec67
translation: machine
translated_at: '2026-10-24'
---
# Wan2.2-NVFP4-Sparse {#wan22-nvfp4-sparse}

**Ligne de développement :** `project:wan2-2-nvfp4-sparse` · fil `wan2-2-nvfp4-sparse-development`  
**Dernier événement :** 2026-06-05 · 1 daté depuis le 2026-06-05 · **Recherche :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Wan2.2-NVFP4-Sparse, désigné dans la fiche sous le nom LightWan2.2-A14B depuis le 27 juillet, est une version de Wan2.2-T2V/I2V-A14B destinée aux détenteurs de cartes Blackwell qui veulent un générateur vidéo local en quatre étapes. Fonctionnalités : T2V ; I2V ; paires high/low NVFP4 ; dynamic sparse attention. Mesure et limite : le tableau de l'auteur sur RTX 5090 donne 9,1–26,7 s avec 4 étapes pour du 480p/720p, mais cette voie exige une RTX 50/Blackwell, T5/VAE et, pour I2V, un image encoder. Verdict : cela a du sens comme pipeline LightX2V spécialisé ; sur un autre matériel, ses avantages annoncés ne sont pas confirmés.

## Ligne de développement {#development-line}

- **2026-06-05 — Référence Hugging Face pour Wan2.2-NVFP4-Sparse.** Wan2.2-NVFP4-Sparse — des poids NVFP4 T2V/I2V high/low nommés, y compris les variantes Comfy, sont apparus et ont été réorganisés ; deux doublons ambigus ont été supprimés de la racine.

## Ce qui a changé {#what-changed}

2026-05-28 : Wan2.2-NVFP4-Sparse — le dépôt du modèle a été initialisé sur Hugging Face. 2026-05-29 : Wan2.2-NVFP4-Sparse — LightX2V a annoncé une variante Wan 2.2 14B pour T2V et I2V, avec distillation d'étapes tenant compte de la quantification NVFP4 et sparse attention pour Blackwell ; un gain supérieur à 50× sur une seule RTX 5090 est revendiqué. 2026-06-05 : Wan2.2-NVFP4-Sparse — des poids NVFP4 T2V/I2V high/low nommés, y compris les variantes Comfy, sont apparus et ont été réorganisés ; deux doublons ambigus ont été supprimés de la racine. 2026-06-09 : Wan2.2-NVFP4-Sparse — la fiche a formalisé I2V comme modèle de base et ajouté une voie de lancement distincte avec image encoder et image d'entrée. 2026-07-18 : Wan2.2-NVFP4-Sparse — les instructions sont passées du répertoire distill, désormais obsolète, aux scripts actuels wan22/extreme, et des variantes sequence parallel pour plusieurs GPU ont été ajoutées. 2026-07-27 : Wan2.2-NVFP4-Sparse — la fiche a été renommée LightWan2.2-A14B ; l'ancienne adresse redirige désormais vers la nouvelle.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-06-05, les praticiens doivent considérer le dépôt Hugging Face lié comme une source candidate pour Wan2.2-NVFP4-Sparse, et vérifier sa fiche de modèle, ses fichiers, sa licence et sa compatibilité avant toute utilisation.

1. Vérifiez la plateforme : cette voie exige une GPU NVIDIA de la série RTX 50 ou une autre architecture Blackwell ; sur un autre GPU, ne comptez pas sur le mode NVFP4 annoncé.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
2. Lancez le conteneur recommandé lightx2v/lightx2v:26052801-cu130-5090, ou compilez LightX2V et le noyau NVFP4 avec CUTLASS en suivant les instructions de la fiche.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
3. Téléchargez la paire high/low NVFP4 correspondant à la tâche T2V ou I2V, puis préparez Wan2.2 T5 et VAE ; pour I2V, préparez en plus l'image encoder et l'image source.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
4. Dans la configuration, renseignez les chemins des deux fichiers de checkpoint, high_noise_quantized_ckpt et low_noise_quantized_ckpt ; la configuration T2V de départ définit 4 étapes, 81 images, 480×832 et un ratio de sparse-attention de 0.9.
  — <https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json>
5. Pour T2V, renseignez lightx2v_path et model_path dans run_wan22_moe_t2v_extreme.sh actuel, puis lancez-le ; le script appelle model_cls wan2.2_moe avec la configuration T2V extreme.
  — <https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_t2v_extreme.sh>
6. Pour I2V, renseignez les mêmes chemins ainsi que image_path dans run_wan22_moe_i2v_extreme.sh ; le script utilise la configuration I2V extreme et enregistre le résultat au format MP4.
  — <https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_i2v_extreme.sh>

## Bonnes pratiques {#best-practices}

- Utilisez l'image Docker recommandée et les scripts extreme officiels : ils constituent la voie documentée pour ce modèle, et non un simple widget générique du Hub Diffusers.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
- Gardez les poids high- et low-noise en paire et renseignez les deux chemins explicites dans la configuration ; ne revenez pas aux noms de fichiers génériques high_nvfp4/low_nvfp4 supprimés.
  — <https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json>
- Appliquez sparse attention surtout en haute résolution ; n'activez le CPU offload qu'en cas de manque de mémoire, car la fiche signale une baisse de débit.
  — <https://huggingface.co/lightx2v/LightWan2.2-A14B>
- Avant tout usage en production, comparez votre propre jeu de prompts avec la base FP8 sur le respect du prompt : un issue ouvert, mais non clos, signale un moins bon respect du prompt avec FP4, sans que cela constitue une régression générale de qualité confirmée.
  — <https://github.com/ModelTC/LightX2V/issues/1147>

## Remplacé par ceci {#superseded-by-this}

- {"claim":"Les instructions faisant référence aux fichiers génériques high_nvfp4.safetensors et low_nvfp4.safetensors sont obsolètes : ces deux fichiers ont été supprimés du dépôt.","obsolete_since":"2026-06-05","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/0191e9d9499dfc0bc7fcfbc24b678e94b918c405"}
- {"claim":"Les instructions utilisant les chemins scripts/wan22/distill/run_wan22_moe_*_extreme.sh sont obsolètes : la fiche a déplacé le lancement vers scripts/wan22/extreme et ajouté les variantes sequence-parallel.","obsolete_since":"2026-07-18","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/3eef5caddabe719c0a96fd8f3f703f5f1f235f8b"}
- {"claim":"Wan2.2-NVFP4-Sparse comme nom actuel de la fiche est obsolète : la fiche l'a remplacé par LightWan2.2-A14B ; l'ancienne URL est conservée comme redirection.","obsolete_since":"2026-07-27","source_url":"https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/27213d1d4a6cfb1ecd9c60d214764c917d0f6c45"}

## Points encore inconnus {#still-unknown}

- L'entrée de blog LightX2V du 19 juillet 2026, citée dans le README du projet, a renvoyé une erreur 404 lors de la vérification ; elle n'est donc pas utilisée comme preuve d'une mise à jour du modèle ou de l'environnement d'exécution.
- Les temps sur RTX 5090 et l'affirmation d'un gain supérieur à 50× sont rapportés par l'auteur ; aucune reproduction indépendante sur Blackwell n'a été effectuée ici.
- L'issue #1147 signale un moins bon respect du prompt par rapport à une comparaison FP8, mais elle n'est assignée à personne et n'a ni réponse des mainteneurs ni benchmark reproductible ; elle ne prouve donc pas une régression générale de qualité.
- Le Hub affiche un exemple de code Diffusers générique, mais aucune exécution n'a permis de vérifier qu'il remplace la configuration LightX2V documentée, avec des chemins de checkpoint high/low explicites et des noyaux NVFP4.
- Le 27 juillet confirme le renommage de la fiche et le fait que l'ancienne URL redirige actuellement, mais l'horodatage exact de la redirection du dépôt Hugging Face n'a pas été exposé.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/lightx2v/Wan2.2-NVFP4-Sparse | URL historique Wan2.2-NVFP4-Sparse, redirigeant vers LightWan2.2-A14B | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B | Fiche de modèle LightWan2.2-A14B | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commits/main | Historique des commits de LightWan2.2-A14B | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/0191e9d9499dfc0bc7fcfbc24b678e94b918c405 | Suppression des fichiers safetensors NVFP4 en trop | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/4dbf88dc61135c02943f3f54c99acee05ed856db | Mise à jour de la fiche ajoutant la voie I2V | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/3eef5caddabe719c0a96fd8f3f703f5f1f235f8b | Mise à jour de la fiche passant aux scripts extreme et sequence-parallel | 2026-09-06 |
| https://huggingface.co/lightx2v/LightWan2.2-A14B/commit/27213d1d4a6cfb1ecd9c60d214764c917d0f6c45 | Mise à jour de la fiche renommant LightWan2.2-A14B | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/README.md | README anglais de LightX2V et journal des versions datées | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/README_zh.md | README de LightX2V en chinois simplifié et journal des versions datées | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/configs/wan22/extreme/wan_moe_t2v_distill_nvfp4_sparse_attn.json | Configuration T2V sparse-attention NVFP4 | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_t2v_extreme.sh | Script de lancement T2V extreme | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/blob/main/scripts/wan22/extreme/run_wan22_moe_i2v_extreme.sh | Script de lancement I2V extreme | 2026-09-06 |
| https://lightx2v-en.readthedocs.io/en/latest/getting_started/model_structure.html | Guide du format de modèle et du chargement dans LightX2V | 2026-09-06 |
| https://github.com/ModelTC/LightX2V/issues/1147 | Signalement communautaire ouvert sur le respect du prompt en NVFP4 | 2026-09-06 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:wan2-2-nvfp4-sparse`, fil `wan2-2-nvfp4-sparse-development`, 1 événement daté du 2026-06-05 au 2026-06-05.
- **Note pratique :** à partir du 2026-06-05, les praticiens doivent considérer le dépôt Hugging Face lié comme une source candidate pour Wan2.2-NVFP4-Sparse, et vérifier sa fiche de modèle, ses fichiers, sa licence et sa compatibilité avant toute utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
