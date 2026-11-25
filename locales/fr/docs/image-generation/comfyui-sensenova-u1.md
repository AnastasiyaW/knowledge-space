---
title: "SenseNova U1 et ComfyUI"
description: "Référence sensible aux limites pour les artefacts officiels SenseNova U1/U1.5, les nœuds ComfyUI officiels et le wrapper tiers ComfyUI_SenseNova_U1."
level: 3
source_sha256: 08fa2483f3d9b1c6a935a0e5d419d1324ec93767dabad05893d0ddf3c88a42b9
translation: machine
translated_at: '2026-10-24'
---
# SenseNova U1 et ComfyUI {#sensenova-u1-and-comfyui}

SenseNova U1 est une famille officielle de génération et d'édition d'images. `smthemex/ComfyUI_SenseNova_U1` est un wrapper tiers distinct. Les nœuds officiels, les capacités officielles des modèles et les capacités du wrapper doivent être attribués indépendamment. Statut vérifié à partir des sources officielles en anglais et en chinois ainsi que du dépôt du wrapper, à la date du **27 août 2026**.

## Cartographie des artefacts actuels {#current-artifact-map}

| Surface | État vérifié |
|---|---|
| Dépôt officiel | `OpenSenseNova/SenseNova-U1`, Apache-2.0 |
| Révision officielle vérifiée | `022fa663d3f1a3c6822ec0b534e336a991bb7b0b` |
| Nœuds ComfyUI officiels | `OpenSenseNova/ComfyUI-SenseNova-U1` v0.3.0 ; miroir du registre de `SenseNova-U1/apps/comfyui` |
| Révision du miroir ComfyUI officiel | `fc90611ac6f9eecfbf0f6a5115b13f609683e202` |
| Wrapper tiers | `smthemex/ComfyUI_SenseNova_U1`, Apache-2.0 |
| Révision vérifiée du wrapper | `35f930a349aa38a94100529fd1ec7dd8b31f9ec9` |
| Formats du wrapper | U1.5 preview/formal, ainsi que les chemins GGUF, INT8, FP8 et BF16 décrits dans son README actuel |
| Chemin LoRA 8 étapes (ancien) | Barré dans le README du wrapper ; à conserver comme historique, pas comme valeur par défaut actuelle |

N'attribuez pas au wrapper tiers toutes les fonctionnalités officielles de U1/U1.5. Ne considérez pas le chemin quantifié du wrapper comme une preuve que le modèle officiel en pleine précision tient sur le même matériel.

## Historique de développement {#development-history}

| Date | Fil | Événement | Statut temporel |
|---|---|---|---|
| 2026-05-05 | wrapper tiers | Premier rapport sur le wrapper ComfyUI | Fondation historique |
| 2026-05-21 | projet officiel | Publication du code de fine-tuning complet | Capacité officielle actuelle |
| 2026-06-19 | wrapper/adaptateur | Rapport sur la LoRA infographique en huit étapes | Remplacé/barré dans la documentation actuelle du wrapper |
| 2026-08-24 | ComfyUI officiel | Préparation du miroir de registre v0.3.0 | Surface ComfyUI officielle actuelle |
| 2026-08-26 | wrapper | Révision actuelle vérifiée du wrapper | Point de terminaison actuel du wrapper |
| 2026-08-27 | projet officiel | Révision officielle actuelle vérifiée | Point de terminaison officiel actuel |

Le développement du modèle officiel et celui du wrapper tiers sont liés par l'intégration, non par la propriété. Représentez-les comme des sujets ou fils distincts, reliés par des liens explicites `integrates_with`, plutôt que par une fausse chaîne de prédécesseurs unique.

## Choix du matériel {#hardware-selection}

La FAQ officielle en chinois indique environ 36 Go pour le BF16 complet et précise qu'il faut plus de 36 Go de VRAM pour ce chemin. Pour les appareils contraints, elle recommande des choix GGUF plus légers ou équilibrés.

La même FAQ met en garde : un chemin Q6 complet sur 8 Go n'est pas sûr et peut provoquer un OOM. Ne transformez pas « GGUF disponible » en « tous les niveaux GGUF tiennent sur 8 Go ».

```yaml
surface: official-nodes-or-third-party-wrapper
official_revision: 022fa663d3f1a3c6822ec0b534e336a991bb7b0b
wrapper_revision: 35f930a349aa38a94100529fd1ec7dd8b31f9ec9
model: U1-or-exact-U1.5-artifact
format: BF16-or-FP8-or-INT8-or-exact-GGUF
adapter: <exact-hash-or-none>
comfyui_revision: <exact-revision>
gpu_and_vram: <exact-device>
steps: <integer>
resolution: <width>x<height>
peak_vram: <measured-value>
```

## Choix pratique {#practical-selection}

- Privilégiez les nœuds officiels du registre lorsque le contrat d'exécution de l'artefact officiel correspond à la tâche. Le paquet officiel actuel est `ComfyUI-SenseNova-U1` v0.3.0 ; il nécessite l'API de nœuds v3 de ComfyUI (`comfy_api.latest`).
- Installez le paquet officiel via ComfyUI Manager/Registry ou épinglez la révision de son miroir. Son README désigne `OpenSenseNova/SenseNova-U1/apps/comfyui` comme source de référence.
- N'utilisez le wrapper tiers que si son chemin exact de quantification ou de modèle est requis, et épinglez à la fois le wrapper et le modèle.
- Supprimez ou désactivez un répertoire `ComfyUI_SenseNova_U1` hérité, copié manuellement, avant d'activer le paquet officiel. Les deux implémentations enregistrent des identifiants de nœuds qui se chevauchent : les garder ensemble ferait dépendre le code exécuté de l'ordre de chargement.
- Utilisez le BF16 complet uniquement avec une marge mesurée supérieure à l'exigence documentée.
- Sur 8 Go, partez d'une quantification légère ou équilibrée documentée et validez un workflow minimal ; ne sélectionnez pas le Q6 complet sur la seule base de son nom.
- Pour la génération d'infographies, consignez la langue, les échecs de texte répété, le comportement de l'arrière-plan, le hash de l'adaptateur, le nombre d'étapes et la résolution.

## Frontière d'entraînement {#training-boundary}

Le projet officiel a publié le code de fine-tuning complet le 21 mai 2026. La FAQ officielle décrit le code d'entraînement LoRA comme prévu, et non comme équivalent au chemin de fine-tuning complet déjà publié. Vérifiez à nouveau ce statut avant d'affirmer la prise en charge de l'entraînement LoRA, car il évolue dans le temps.

Les surfaces locales et les API peuvent exposer des modèles, des valeurs par défaut, des limites et des comportements de sortie différents. Ne mélangez pas les résultats d'API avec les benchmarks de workflows locaux, sauf si le point de terminaison exact est l'objet de l'étude.

## Limites des retours de la communauté {#community-evidence-boundary}

Le rapport plus ancien sur la LoRA infographique en huit étapes est utile comme historique du projet, mais ce n'est pas une valeur par défaut actuelle : la documentation même du wrapper barre désormais ce chemin. Des problèmes précis du wrapper apportent du contexte :

- [Issue #12](https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/12) signale une modification d'un fichier `SenseNova-U1-8B-MoT-8step-Q8_0.gguf` de 18,6 Go sur une carte NVIDIA de 16 Go : une allocation GPU de 4,92 Go a été journalisée et le prompt en huit étapes a pris 42,19 secondes, ce qui indique un déchargement important ou une sous-utilisation. Un autre utilisateur a mesuré 37 Go de mémoire GPU et partagée combinée pour une exécution en 2K sur RTX 4090 et suggéré de tester `prefetch_count=0`. Ce sont des observations propres à un workflow donné, non une garantie de capacité.
- [Issue #17](https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/17) signale des résultats dégradés pour les fine-tunes Interleaved/Infographic en Q4, tandis que le même utilisateur a trouvé le Q6 acceptable. Conservez la quantification GGUF exacte avant de diagnostiquer la qualité de l'adaptateur.
- Une [fiche modèle GGUF U1.5](https://huggingface.co/realrebelai/SenseNova-U1.5-8B_GGUFs) communautaire existe, mais ce n'est pas une fiche officielle et elle ne peut pas annuler l'avertissement officiel concernant plus de 36 Go pour le BF16 et le Q6 sur 8 Go.

## Pièges {#gotchas}

- **Problème :** Qualifier le wrapper tiers de « ComfyUI officiel de SenseNova ». **Correction :** nommez le propriétaire du dépôt et gardez les nœuds officiels du registre séparés.
- **Problème :** Installer le paquet officiel v0.3.0 à côté du répertoire tiers hérité. **Correction :** désactivez ou supprimez d'abord la copie héritée ; des identifiants de nœuds en double rendent l'implémentation active dépendante de l'ordre d'analyse.
- **Problème :** Charger le paquet officiel v0.3.0 sur un runtime ComfyUI ancien à nœuds v1. **Correction :** mettez à jour vers une version exposant `comfy_api.latest`, ou conservez la surface tierce compatible épinglée.
- **Problème :** Supposer que le Q6 tient sur un GPU de 8 Go. **Correction :** suivez l'avertissement officiel et sélectionnez puis testez une quantification documentée plus légère.
- **Problème :** Recommander l'ancienne LoRA en huit étapes parce qu'un article historique le faisait. **Correction :** marquez-la comme remplacée/barrée et vérifiez le chemin d'adaptateur actuel.
- **Problème :** Affirmer l'entraînement LoRA officiel à partir du code de fine-tuning complet publié. **Correction :** traitez-les comme des capacités distinctes et revérifiez la FAQ.
- **Problème :** Diagnostiquer la qualité d'une infographie sans connaître le niveau GGUF. **Correction :** consignez Q4/Q6/Q8 et la révision de l'adaptateur ; l'issue #17 signale des résultats sensiblement différents entre Q4 et Q6.

## Statut temporel {#temporal-status}

- **Actuel :** dépôt officiel U1 et nœuds du registre ; surface actuelle du wrapper U1.5/quantification ; code de fine-tuning complet publié.
- **Remplacé mais conservé :** anciennes instructions de LoRA infographique en huit étapes du wrapper, désormais barrées.
- **Prévu/instable :** statut du code d'entraînement LoRA officiel.
- **Généralisation dangereuse :** Q6 complet sur 8 Go.

## Synthèse pour agent {#agent-brief}

Commencez par distinguer les nœuds officiels v0.3.0 du wrapper `smthemex`, puis U1 de l'artefact exact U1.5 et de sa quantification. Épinglez les deux dépôts lorsque le wrapper est utilisé, et ne chargez jamais les deux implémentations de nœuds ensemble. Considérez les anciennes instructions d'adaptateur comme remplacées lorsque la documentation actuelle les barre. Préservez l'attribution officiel/communauté et ne promettez jamais une compatibilité 8 Go sans une configuration exacte mesurée.

## Sources {#sources}

- Dépôt officiel : https://github.com/OpenSenseNova/SenseNova-U1
- FAQ officielle en chinois : https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/FAQ_CN.md
- Miroir officiel du registre ComfyUI : https://github.com/OpenSenseNova/ComfyUI-SenseNova-U1
- Métadonnées officielles de ComfyUI v0.3.0 : https://github.com/OpenSenseNova/ComfyUI-SenseNova-U1/blob/main/pyproject.toml
- Wrapper tiers : https://github.com/smthemex/ComfyUI_SenseNova_U1
- Présence officielle du projet : https://www.sensenova.cn/
- Article : https://arxiv.org/abs/2605.12500
- Rapport chinois sur la VRAM et le déchargement : https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/12
- Rapport sur les artefacts Q4 versus Q6 : https://github.com/smthemex/ComfyUI_SenseNova_U1/issues/17
