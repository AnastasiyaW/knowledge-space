---
title: "Qwen-Image"
description: "Référence tenant compte des versions pour la génération et l'édition avec Qwen-Image, les checkpoints 2511/2512, et la surface de service distincte Qwen-Image 2.0."
level: 3
source_sha256: d1f97016e48185c7fccd93691baf57684ffc3d729c310339f9c4b45f110f631d
translation: machine
translated_at: '2026-10-24'
---
# Qwen-Image {#qwen-image}

Qwen-Image est une famille de projets comprenant des checkpoints distincts pour la génération et l'édition. Cette page distingue les artefacts ouverts exécutables en local des annonces ultérieures de produits hébergés. Statut vérifié auprès de sources officielles à la date du **2026-08-27**.

## Cartographie des artefacts actuels {#current-artifact-map}

| Artefact | Statut officiel | Usage |
|---|---|---|
| Qwen-Image | Publié dans le dépôt officiel le 2025-08-04 | Génération texte-vers-image de base |
| Qwen-Image-Edit | Publié le 2025-08-18 | Édition d'images par instruction |
| Qwen-Image-Edit-2511 | Poids annoncés le 2025-12-23 | Checkpoint d'édition ultérieur |
| Qwen-Image-2512 | Poids annoncés le 2025-12-31 | Checkpoint de génération ultérieur |
| Qwen-Image 2.0 | Annoncé le 2026-02-10 via le blog officiel et la surface Qwen Chat | Génération de produit hébergé actuelle ; aucun poids ouvert 2.0 identifié dans le dépôt officiel |
| Qwen-Image 2.0 Pro | Libellé produit/actualité hébergé observé plus tard en 2026 | Ne pas le traiter comme un alias des poids ouverts 2512 |

La valeur par défaut sûre pour un workflow de génération ouvert en local est l'exemple officiel **2512**. La valeur par défaut sûre pour un workflow d'édition ouvert en local est l'exemple officiel **Edit-2511**. Vérifiez à nouveau le dépôt avant de supposer que Qwen-Image 2.0 est téléchargeable.

## Historique de développement {#development-history}

| Date | Fil | Événement | Statut temporel |
|---|---|---|---|
| 2025-08-04 | génération | Publication initiale de Qwen-Image | Remplacé par 2512 pour les exemples locaux actuels |
| 2025-08-18 | édition | Publication de Qwen-Image-Edit | Remplacé par Edit-2511 pour les exemples locaux actuels |
| 2025-12-23 | édition | Publication des poids Edit-2511 | Checkpoint d'édition ouvert actuel dans les exemples officiels |
| 2025-12-31 | génération | Publication des poids 2512 | Checkpoint de génération ouvert actuel dans les exemples officiels |
| 2026-02-10 | génération/produit | Annonce de Qwen-Image 2.0 | Branche produit hébergé actuelle ; statut de l'artefact ouvert non vérifié |
| 2026-04-26 | génération/produit | Rapport sur Qwen-Image 2.0 Pro observé | Événement produit ultérieur, ne constitue pas une preuve de poids ouverts |

La génération et l'édition sont des branches de projet apparentées, et non une chaîne de prédécesseurs unique. Conservez les deux historiques et ne reliez que les événements appartenant à la même branche lorsque vous construisez un graphe d'actualités.

## Utilisation pratique {#practical-use}

### Génération en local {#local-generation}

```bash
git clone https://github.com/QwenLM/Qwen-Image.git
cd Qwen-Image
git rev-parse HEAD
```

Utilisez ensuite l'exemple de génération 2512 à partir de cette révision épinglée. Consignez l'identifiant du modèle, la révision du dépôt, les versions de Diffusers et de l'environnement d'exécution, le dtype, le GPU, la graine, les dimensions, le nombre d'étapes et toute quantification ou déchargement (offload).

### Édition en local {#local-editing}

Utilisez l'exemple Edit-2511 du même dépôt épinglé. Conservez l'image source et l'instruction d'édition ensemble dans l'enregistrement de l'exécution. Pour l'édition multi-images, consignez également l'ordre des entrées, car les références positionnelles peuvent modifier l'interprétation.

### 2.0 hébergé {#hosted-20}

Utilisez la documentation actuelle et officielle de Qwen Chat/API et précisez le point de terminaison ou le modèle exact. Ne présentez pas la latence, les limites ou le comportement des sorties hébergés comme des propriétés du checkpoint local 2512.

## Surface d'exécution et d'intégration {#runtime-and-integration-surface}

Le dépôt officiel recense des chemins d'intégration pour Diffusers et mentionne la prise en charge dans LightX2V, vLLM-Omni et SGLang. Il s'agit de runtimes distincts, dont les contrats de batching, de quantification et d'API diffèrent.

Pour chaque déploiement, consignez :

```yaml
artifact: Qwen-Image-2512-or-Qwen-Image-Edit-2511
source_revision: <40-character-commit>
runtime: <diffusers-or-serving-runtime>
runtime_version: <exact-version>
dtype: <bf16-fp16-fp8-int8-other>
gpu: <exact-model-and-vram>
resolution: <width>x<height>
steps: <integer>
seed: <integer>
```

Aucune matrice VRAM/latence actuelle, officielle et versionnée n'a été retenue lors de la recherche bornée. Mesurez l'usage des ressources en local au lieu de recopier un chiffre issu de la communauté.

## Limites des preuves {#evidence-boundaries}

- Le dépôt officiel fait autorité pour les artefacts téléchargeables et les exemples locaux.
- Le blog officiel 2.0 fait autorité pour l'annonce, mais ne prouve pas à lui seul l'existence d'un checkpoint ouvert.
- La documentation officielle chinoise de l'API est utile pour le comportement de l'édition hébergée ; elle ne prouve pas la compatibilité locale de 2512.
- Les exemples communautaires sont utiles pour détecter des défaillances, mais pas pour établir l'identité d'un artefact ni des paramètres universels.

## Retours de la communauté {#community-reports}

- [Issue #26](https://github.com/QwenLM/Qwen-Image/issues/26) documente une exécution initiale de Qwen-Image avec Diffusers qui consomme 44,24 GiB et échoue sur une carte annoncée à 48 GB. Des réponses de la communauté indiquent que `enable_model_cpu_offload()` réduit efficacement la mémoire, au prix d'une perte de vitesse ; le seul tiling VAE dépassait néanmoins 50 GB pour un des rapporteurs. Ces mesures concernent l'artefact de base 2025, et non 2512/Edit-2511.
- [Issue #54](https://github.com/QwenLM/Qwen-Image/issues/54) compare une même invite d'infographie officielle sur Qwen hébergé, Diffusers et ComfyUI en BF16. Plusieurs utilisateurs ont signalé que la valeur par défaut de 20 étapes de ComfyUI donnait de moins bons résultats que l'exemple du dépôt à 50 étapes ; 50 étapes amélioraient la lisibilité sans garantir un texte parfait selon l'invite. Les sorties de Diffusers et de ComfyUI n'étaient pas interchangeables, même avec des poids nominalement similaires.
- La leçon opérationnelle est de conserver le runtime et le nombre d'étapes dans les comparaisons. Ne présentez pas un exemple hébergé comme une garantie du checkpoint local.

## Pièges à éviter {#gotchas}

- **Problème :** appeler chaque artefact « Qwen-Image 2.0 » -> **Correctif :** conservez l'identifiant exact du modèle : base, Edit, Edit-2511, 2512, ou 2.0/2.0 Pro hébergé.
- **Problème :** supposer qu'un blog ou un lancement sur Qwen Chat signifie des poids ouverts -> **Correctif :** exigez un artefact officiel dans le dépôt ou une fiche de modèle avant de décrire 2.0 comme téléchargeable localement.
- **Problème :** relier des événements d'édition comme prédécesseurs d'événements de génération -> **Correctif :** conservez des fils de développement `generation` et `editing` distincts.
- **Problème :** publier une consommation VRAM ou une vitesse issues de la communauté comme valeurs universelles -> **Correctif :** épinglez le runtime, le dtype, la quantification, les dimensions, le nombre d'étapes et le GPU, puis mesurez.
- **Problème :** comparer une exécution ComfyUI à 20 étapes avec l'exemple Diffusers à 50 étapes du dépôt -> **Correctif :** alignez d'abord les paramètres du runtime, et prévoyez tout de même des différences de sortie propres au backend.

## Statut temporel {#temporal-status}

- **Actuel :** exemple de génération locale 2512 ; exemple d'édition locale Edit-2511 ; surface produit hébergée Qwen-Image 2.0.
- **Remplacé mais conservé :** exemples initiaux de génération et d'édition de base de 2025, lorsque des checkpoints officiels ultérieurs existent.
- **Inconnu :** disponibilité, licence et contrat d'exécution local d'un éventuel checkpoint ouvert Qwen-Image 2.0.

## Consigne pour l'agent {#agent-brief}

Déterminez l'intention de l'utilisateur parmi `génération locale`, `édition locale` ou `2.0 hébergé` avant de formuler toute recommandation. Pour un travail local, consultez le dépôt officiel actuel et citez une révision immuable ainsi que l'identifiant exact du modèle. Pour un travail hébergé, citez la documentation actuelle du point de terminaison. Ne faites jamais correspondre « 2.0 Pro » à `2512` sans preuve primaire. Renvoyez les anciens événements avec leur statut temporel plutôt que de les supprimer.

## Sources {#sources}

- Dépôt officiel : https://github.com/QwenLM/Qwen-Image
- Annonce de Qwen-Image 2.0 : https://qwen.ai/blog?id=qwen-image-2.0
- Documentation chinoise de l'édition hébergée : https://docs.qwencloud.com/developer-guides/image-generation/image-editing
- Article de recherche : https://arxiv.org/abs/2605.10730
- Discussion sur la mémoire du modèle de base (zh-CN/EN) : https://github.com/QwenLM/Qwen-Image/issues/26
- Discussion sur la reproduction hébergé/Diffusers/ComfyUI : https://github.com/QwenLM/Qwen-Image/issues/54
