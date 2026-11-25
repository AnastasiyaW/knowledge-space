---
title: "Unsloth"
description: "Référence tenant compte des artefacts pour Unsloth Core, Studio, Desktop et les recommandations de fine-tuning liées à une version."
level: 3
source_sha256: 2c9fb5a93260e2b66b6f772cad435351180aaffcb6835ecf37295c4cfc1c8fa0
translation: machine
translated_at: '2026-10-24'
---
# Unsloth {#unsloth}

Unsloth est une famille de surfaces locales de fine-tuning et d'inférence. Les recettes Core/bibliothèque, Studio et Desktop sont des produits apparentés, mais ne sont pas des environnements d'exécution interchangeables. Statut vérifié à partir des sources officielles en anglais et en chinois, le **2026-08-27**.

## Cartographie des surfaces actuelles {#current-surface-map}

| Surface | Rôle | Périmètre actuel |
|---|---|---|
| Unsloth Core/bibliothèque | Intégration Python pour l'entraînement et l'inférence | À utiliser pour les workflows en scripts et notebooks ; épingler le paquet et la recette du modèle |
| Unsloth Studio | Interface et workflow locaux | Ne pas supposer la même installation, le même ensemble de fonctionnalités ni le même rythme de publication que Core |
| Unsloth Desktop | Programmes d'installation de bureau pour Windows, macOS et Linux | Introduit dans la lignée de versions du 2026-08-13 ; les versions actuelles doivent être vérifiées séparément |
| Guides spécifiques aux modèles | Paramètres de fine-tuning et compatibilité | Les paramètres ne s'appliquent qu'à la famille de modèles nommée et à la révision du guide |

La page officielle des releases affichait `v0.1.803-beta` le 2026-08-25. Le dépôt documente les chemins CPU et multi-GPU pour NVIDIA, AMD, Intel et Mac, mais la profondeur du support varie selon le système d'exploitation, le backend, le modèle et le workflow.

## Historique de développement {#development-history}

| Date | Fil | Événement | Statut temporel |
|---|---|---|---|
| 2025-08-11 | guides d'entraînement de modèles | Recommandations de fine-tuning GPT-OSS signalées | Historique ; récupérer le guide actuel avant utilisation |
| 2026-03-11 | guides d'entraînement de modèles | Recommandations de fine-tuning Qwen3.5 signalées | Guide de famille actuel ; les paramètres restent spécifiques à la taille du modèle |
| 2026-04-08 | interface locale | Rapport de workflow local lié à Studio/Gemma | Branche produit historique |
| 2026-08-13 | interface locale | Introduction d'Unsloth Desktop | Branche produit actuelle |
| 2026-08-25 | ligne de releases | `v0.1.803-beta` observée | Version actuelle au moment de la vérification |

Les guides d'entraînement de modèles forment un seul historique. Studio et Desktop forment un historique distinct d'interface locale. Ne pas faire d'un article sur Studio le prédécesseur d'une recette de modèle sans rapport.

## Limites du fine-tuning de Qwen3.5 {#qwen35-fine-tuning-bounds}

Le guide officiel indique une mémoire approximative pour LoRA en bf16 selon la taille du modèle :

| Taille de Qwen3.5 | Mémoire LoRA bf16 indiquée |
|---|---:|
| 0,8B | 3 Go |
| 2B | 5 Go |
| 4B | 10 Go |
| 9B | 22 Go |
| 27B | 56 Go |
| 35B-A3B | 74 Go |

L'affirmation souvent répétée « 5 Go » concerne spécifiquement la recette **LoRA bf16 du modèle 2B**. Ce n'est pas une exigence mémoire universelle pour Qwen3.5 ni pour Unsloth.

Le guide exige Transformers v5 pour cette famille de modèles. Il déconseille également le QLoRA en 4 bits pour Qwen3.5, car son comportement de quantification diffère des recettes où le QLoRA en 4 bits constitue la valeur par défaut habituelle pour une faible consommation mémoire.

## Enregistrement d'exécution reproductible {#reproducible-run-record}

```yaml
unsloth_surface: core-or-studio-or-desktop
unsloth_version: <exact-release-or-package-version>
model_id: <exact-model-and-size>
model_revision: <immutable-revision>
transformers_version: <exact-version>
training_mode: bf16-lora-or-other
quantization: none-or-exact-format
gpu_backend: nvidia-or-amd-or-intel-or-mps-or-cpu
gpu_and_vram: <exact-device>
sequence_length: <integer>
batch_and_accumulation: <values>
measured_peak_memory: <value>
```

Utiliser la mémoire de pointe mesurée comme donnée de référence pour le déploiement. Les tableaux du guide sont des bornes de planification, et non des garanties pour toutes les longueurs de séquence, tailles de lot, états de l'optimiseur et paramètres de déchargement.

## Choix de la plateforme {#platform-selection}

- Utiliser Core lorsque des scripts, des notebooks, de l'intégration continue ou un épinglage exact des dépendances sont requis.
- Utiliser Desktop lorsque l'exigence est une interface locale packagée et que son programme d'installation actuel prend en charge l'OS et le backend cibles.
- Utiliser Studio uniquement si son ensemble de fonctionnalités actuel correspond à la tâche ; ne pas le désigner comme Desktop.
- Privilégier le guide spécifique au modèle plutôt qu'une recette communautaire générique.
- Relancer une étape d'entraînement minimale après tout changement de paquet, de Transformers, de CUDA/backend, de modèle ou de quantification.

## Retours de la communauté {#community-reports}

- [Issue #7506](https://github.com/unslothai/unsloth/issues/7506) décrit un plantage de l'entraînement de Qwen3.5-0.8B en BF16 sur Tesla T4. Une suggestion de la communauté consistant à passer les indicateurs du trainer en FP16 n'a pas complètement résolu le problème, car le auteur du rapport observait toujours des poids chargés en BF16. Considérer l'entraînement de Qwen3.5 sur T4 comme un cas de compatibilité de types mixtes non résolu, et non comme un correctif par un simple indicateur.
- [Issue #9549](https://github.com/unslothai/unsloth/issues/9549) décrit Unsloth Studio/Desktop `v0.1.801-beta` sous Windows 10 avec des AMD W7900/W7500, où un modèle est chargé dans la RAM système malgré des options liées à la VRAM. Le rapport est postérieur au lancement de Desktop et reste ouvert ; vérifier à nouveau ce comportement sur la version actuelle avant de se fier à ces options.
- Ces rapports confirment que la prise en charge multiplateforme ne signifie pas une parité entre backends, et que les libellés de mémoire de l'interface ne sont pas des justificatifs d'allocation mesurée.

## Pièges courants {#gotchas}

- **Problème :** Répéter « Qwen3.5 s'entraîne en 5 Go » sans indiquer de taille de modèle → **Correctif :** lier l'affirmation au LoRA bf16 du modèle 2B et consigner les paramètres de séquence et de lot.
- **Problème :** Appliquer les recommandations génériques du QLoRA en 4 bits à Qwen3.5 → **Correctif :** suivre le guide de famille actuel, qui ne recommande pas cette voie.
- **Problème :** Traiter Core, Studio et Desktop comme une seule application versionnée → **Correctif :** consigner la surface exacte ainsi que son propre contrat de version et d'installation.
- **Problème :** Interpréter la prise en charge multiplateforme comme une parité fonctionnelle → **Correctif :** vérifier l'OS exact, le backend d'accélération, le modèle, la quantification et le workflow.
- **Problème :** Considérer `fp16=True` comme une solution éprouvée pour Qwen3.5 sur T4 → **Correctif :** reproduire une étape d'entraînement ; l'issue #7506 restait en types mixtes après ce changement.

## Statut temporel {#temporal-status}

- **Actuel :** branche produit Desktop ; `v0.1.803-beta` au moment de la vérification ; guidage Qwen3.5 avec Transformers v5 et LoRA bf16 spécifique à la taille du modèle.
- **Remplacé ou sensible à la révision :** anciennes copies des recettes GPT-OSS et des premières recettes Qwen3.5.
- **Inconnu tant que non testé :** parité exacte de matériel et de formats pour Desktop, et mémoire mesurée pour la configuration de séquence et de lot d'un utilisateur.

## Briefing pour agent {#agent-brief}

Identifier la surface demandée (`Core`, `Studio` ou `Desktop`) ainsi que le modèle exact avant de donner des instructions. Récupérer le guide officiel actuel dans la langue demandée, épingler toutes les versions, et garder séparées la mémoire de planification indiquée et la mémoire de pointe mesurée. Ne jamais généraliser le chiffre 2B/5 Go de Qwen3.5 ni recommander le QLoRA en 4 bits pour cette famille sans preuve officielle plus récente.

## Sources {#sources}

- Dépôt officiel : https://github.com/unslothai/unsloth
- Releases officielles : https://github.com/unslothai/unsloth/releases
- Documentation en anglais : https://unsloth.ai/docs
- Documentation en chinois : https://unsloth.ai/docs/zh/
- Rapport T4/Qwen3.5 à types mixtes : https://github.com/unslothai/unsloth/issues/7506
- Rapport Desktop/Studio sur la RAM système : https://github.com/unslothai/unsloth/issues/9549
