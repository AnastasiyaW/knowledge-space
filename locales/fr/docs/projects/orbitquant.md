---
title: "OrbitQuant"
category: projects

tags: [orbitquant, orbitquant-development, project]
aliases: ["OrbitQuant"]
level: 2
source_sha256: 06dc973b0cb9edbc56d558c03b2cba91fdcae53fb431eba981063183605cf35a
translation: machine
translated_at: '2026-10-24'
---
# OrbitQuant {#orbitquant}

**Ligne de développement :** `project:orbitquant` · fil `orbitquant-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherché le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

OrbitQuant — bibliothèque Python et méthode de quantification post-entraînement pour les diffusion transformers d'image et de vidéo. Fonctionnalités : rotation RPBH, codebook Lloyd–Max partagé, recettes W2A4–W4A6, intégrations Transformers/Diffusers/PyTorch et exécution packed CUDA, Triton et Metal. Limite : pour une architecture inconnue, la couverture des modules ne prouve pas la préservation de la qualité ; le résultat doit donc être mesuré avant publication de l'artefact. Verdict : c'est une voie pratique vers une inférence low-bit sans données (data-free), mais elle ne remplace pas une vérification de la qualité pour un modèle donné.

## Ligne de développement {#development-line}

- The dated line is not written up yet; what is known stands in the sections below.

## Ce qui a changé {#what-changed}

2026-07-07 — publication de la page de la méthode OrbitQuant pour la quantification weight-and-activation sans calibration des diffusion transformers d'image et de vidéo. 2026-07-09 — sortie sur PyPI de la première série de paquets OrbitQuant 0.1.0–0.1.6. 2026-07-10 — sortie des versions 0.2.0–0.3.1. 2026-07-11 — sortie de la version 0.4.0. 2026-07-12 — sortie de la version 0.5.0. 2026-07-14 — sortie des versions 0.6.0–0.9.0. 2026-08-04 — publication de la version 0.9.2, actuelle d'après le registre vérifié.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-07, considérez OrbitQuant comme une référence de projet non recherchée et vérifiez son objet, ses capacités et son statut avant de l'utiliser en pratique.

1. Installez l'intégration pour Hugging Face : `pip install "orbitquant[hf]"`.
  — <https://github.com/iamwavecut/OrbitQuant>
2. Avant la conversion, chargez le modèle et vérifiez la couverture lisible par machine via `inspect_linear_module_policy()` ; examinez séparément les modules ignorés et non pris en charge.
  — <https://github.com/iamwavecut/OrbitQuant>
3. Pour Transformers, passez `OrbitQuantConfig(target_policy="auto")` à `from_pretrained()`, puis sauvegardez l'artefact packed via `save_pretrained()`.
  — <https://github.com/iamwavecut/OrbitQuant>
4. Pour Diffusers, créez `build_diffusers_pipeline_quantization_config(...)`, quantifiez le composant `transformer` et chargez le pipeline en BF16.
  — <https://github.com/iamwavecut/OrbitQuant>
5. Dans ComfyUI, connectez le loader OrbitQuant correspondant au pipeline Diffusers d'origine, indiquez le `artifact_path` local et utilisez le pipeline renvoyé plus loin dans le graphe.
  — <https://pypi.org/project/comfyui-orbitquant/>

## Bonnes pratiques {#best-practices}

- Ne mettez pas à jour Triton séparément de PyTorch : le paquet utilise le Triton des wheels Linux de PyTorch comme solution de repli CUDA.
  — <https://github.com/iamwavecut/OrbitQuant>
- Pour les architectures inconnues, vérifiez d'abord la couverture de la policy et mesurez la qualité de génération ; la détection automatique des modules ne garantit pas la qualité.
  — <https://github.com/iamwavecut/OrbitQuant>
- Utilisez `auto_fused` pour le runtime packed, et `dequant_bf16` uniquement comme chemin explicite de compatibilité/débogage.
  — <https://pypi.org/project/comfyui-orbitquant/>
- Avant de charger un artefact ComfyUI, vérifiez le manifest, les checksums, les métadonnées de source, les réglages de bits et la target policy.
  — <https://pypi.org/project/comfyui-orbitquant/>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-04 — les versions d'OrbitQuant antérieures à 0.9.2 ne correspondent pas à la version actuelle dans l'historique de publication PyPI vérifié.
- 2026-07-09 — la première série 0.1.0–0.1.6 a été remplacée par les versions suivantes ; pour une nouvelle installation, vérifiez la version actuelle sur PyPI.

## Toujours inconnu {#still-unknown}

- La page de la méthode et l'article décrivent OrbitQuant en tant que recherche, tandis que l'implémentation PyPI/GitHub est présentée comme une implémentation clean-room ; leurs interfaces pratiques et les notes de version tardives ne doivent pas être attribuées à la publication originale du 2026-07-07.
- Aucun changelog primaire daté expliquant les différences de fond entre toutes les versions de paquets 0.1.0–0.9.2 n'a été trouvé ; les dates et numéros de versions sont confirmés, mais pas le périmètre complet modification par modification.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://saurabhcantina.github.io/orbitquant/ | OrbitQuant: Data-Agnostic Quantization for Image and Video Diffusion Transformers | 2026-09-05 |
| https://arxiv.org/abs/2607.02461 | OrbitQuant: Data-Agnostic Quantization for Image and Video Diffusion Transformers | 2026-09-05 |
| https://github.com/iamwavecut/OrbitQuant | iamwavecut/OrbitQuant | 2026-09-05 |
| https://pypi.org/project/orbitquant/ | orbitquant · PyPI | 2026-09-05 |
| https://pypi.org/project/comfyui-orbitquant/ | comfyui-orbitquant · PyPI | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:orbitquant`, thread `orbitquant-development`, 0 dated events - → -.
- **Practical note:** As of 2026-07-07, treat OrbitQuant as an unresearched project reference and verify its purpose, capabilities, and status before using it in practice.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
