---
title: "Harmonisation de patchs de retouche pour des images avant/après appariées"
description: "Une conception de données d'entraînement pour l'inpainting de défauts qui préserve le domaine colorimétrique de l'image cible propre tout en injectant des détails de défaut localisés provenant d'une image avant alignée."
category: techniques
tags: [retouching, inpainting, image-harmonization, paired-data, frequency-separation, poisson-blending]
level: 3
source_sha256: 3c6735a7c815b2de698f6bdb0b85df99b3aff186b8a0d23617facf3b1b242e69
translation: machine
translated_at: '2026-10-24'
---
# Harmonisation de patchs de retouche pour des images avant/après appariées {#retouch-patch-harmonization-for-paired-beforeafter-images}

Utilisez cette construction lorsque les paires alignées `before`/`after` contiennent à la fois une suppression locale de défauts et des retouches plus globales de couleur ou de tonalité. L'objectif est l'inpainting de défauts, et non la reproduction de chaque modification apportée à l'image `after`. Construisez les entrées corrompues dans le domaine colorimétrique de l'image propre ; conservez l'image `after` propre comme cible.

## Périmètre du problème {#problem-boundary}

Soit `B` une image avant alignée, `A` l'image retouchée et `M` un masque de défauts. Une correspondance brute `B -> A` oblige un modèle à expliquer au moins deux transformations différentes :

- la suppression ou le remplacement de texture locale et de détails de défauts ;
- les étalonnages, l'éclairage, le lissage et les modifications de couleur, globaux ou locaux.

Cette séparation relève d'un choix de conception du jeu de données, et non d'un résultat revendiqué par les articles cités. Elle suit la formulation de l'harmonisation d'images, selon laquelle un premier plan doit être rendu compatible avec le domaine de son arrière-plan. DoveNet formule l'harmonisation de cette façon et s'entraîne sur des composites synthétiques associés à des images réelles ; ses données iHarmony4 sont construites à partir de COCO, Adobe5k, Flickr et des sources day2night [DoveNet / iHarmony4, CVPR 2020](https://openaccess.thecvf.com/content_CVPR_2020/html/Cong_DoveNet_Deep_Image_Harmonization_via_Domain_Verification_CVPR_2020_paper.html).

## Construction de paires recommandée {#recommended-pair-construction}

1. Alignez géométriquement `B` sur `A` ; rejetez les paires présentant un déplacement visible de repères, de cheveux ou de pose à l'intérieur du masque élargi.
2. Estimez les détails supprimables à partir d'une décomposition passe-haut multi-échelle.
3. Partez de `A`, et non de `B`, pour chaque entrée synthétique.
4. Injectez uniquement les résidus de défauts/détails sélectionnés provenant de `B` à l'intérieur d'un masque élargi `M+`.
5. Harmonisez la frontière collée avec la toile `A` environnante.
6. Entraînez le modèle contre la cible `A` inchangée ; fournissez `M` comme canal d'entrée lorsque le contrat du modèle le permet.

```text
input  = harmonize(A, inject(A, defect_residual(B, A), M+), M+)
target = A
model_input = concat(input, M)  # optional but explicit conditioning
```

Cette approche demande volontairement au modèle de supprimer une incohérence locale insérée, plutôt que d'inférer une retouche globale inverse.

## Décomposition fréquentielle et colorimétrique {#frequency-and-colour-decomposition}

Pour un opérateur de flou `G_sigma`, définissez un résidu à l'échelle `sigma` :

```text
low_sigma(I)    = G_sigma(I)
detail_sigma(I) = I - low_sigma(I)
```

Un résidu de défaut prudent s'écrit :

```text
D = M * max(0, detail_sigma(B) - detail_sigma(A))
X0 = clip(A + D, 0, 1)
```

Évaluez-le à plusieurs échelles de flou, par exemple `sigma in {2, 4, 8}` pixels après normalisation de la résolution. La formule est une règle de synthèse pratique, et non une garantie du détecteur : ne sélectionnez les composantes connexes qu'après avoir vérifié qu'elles correspondent à des détails supprimés, et non à une erreur d'alignement ou à une réduction volontaire de texture.

Pour les taches spécifiques à la couleur, ajoutez un résidu chromatique local borné dans un espace colorimétrique perceptuel :

```text
delta_ab = clamp(ab(B) - ab(A), -c, c)
X0_lab[M+] = A_lab[M+] + [0, delta_ab]
```

Gardez séparés les contrôles de luminance et de chrominance. HDRNet montre que des modifications photographiques entre entrée et sortie appariées peuvent être approximées par des transformations affines locales de couleur dans l'espace bilatéral, y compris des modifications photographiques dépendantes du contenu ; il n'établit pas qu'une transformation inverse globale unique restitue l'image originale du retoucheur [Page du projet et article HDRNet](https://groups.csail.mit.edu/graphics/hdrnet/).

## Options d'harmonisation des bords {#boundary-harmonization-options}

### Référence par statistiques locales {#local-statistics-baseline}

Faites correspondre les statistiques du patch à un anneau situé immédiatement à l'extérieur de `M+`, par canal ou dans Lab. Pour un patch source `P` et un anneau de destination `R` :

```text
P' = (P - mean(P)) * std(R) / max(std(P), epsilon) + mean(R)
```

N'appliquez cette étape qu'aux canaux destinés à l'harmonisation ; ne laissez pas une passe de statistiques locales effacer le signal de défaut injecté. Le transfert de couleur global est une référence de diagnostic utile, mais la méthode classique transfère les statistiques d'apparence globale de l'image et n'encode pas les décisions d'éclairage spatialement locales [Color Transfer Between Images](https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf).

### Référence dans le domaine des gradients {#gradient-domain-baseline}

L'édition de Poisson résout un problème d'appariement de gradients contraint par la frontière. Pour des valeurs inconnues du patch `f`, un champ de guidage `v` et une frontière de destination `f*` :

```text
min_f integral_Ω ||grad(f) - v||², subject to f|∂Ω = f*|∂Ω
```

De manière équivalente :

```text
Laplacian(f) = div(v) in Ω, with f|∂Ω = f*|∂Ω
```

Utilisez les gradients source comme guidage lorsque la préservation de la structure injectée importe ; utilisez des gradients mixtes lorsque la texture de destination doit dominer. Il s'agit d'une référence de contrôle de couture, et non d'une preuve que le mélange de Poisson produit un inpainting sémantiquement correct. La méthode d'origine prend explicitement en charge le clonage sans couture et les modifications locales de texture, d'éclairage et de couleur [Poisson Image Editing](https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf).

## Référence exécutable : injection de détails + contrôle de couture de Poisson {#runnable-reference-detail-injection-poisson-seam-control}

Nécessite Python 3.10+, NumPy et OpenCV. Les entrées doivent déjà être alignées au pixel près ; `before.png`, `after.png` et `mask.png` doivent avoir les mêmes dimensions spatiales ; les pixels non nuls du masque marquent les défauts.

```python
from pathlib import Path

import cv2
import numpy as np

root = Path(".")
before = cv2.imread(str(root / "before.png"), cv2.IMREAD_COLOR)
after = cv2.imread(str(root / "after.png"), cv2.IMREAD_COLOR)
mask = cv2.imread(str(root / "mask.png"), cv2.IMREAD_GRAYSCALE)
if (before is None or after is None or mask is None
        or before.shape != after.shape or mask.shape != after.shape[:2]):
    raise ValueError("aligned before/after/mask inputs are required")

mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)[1]
expanded = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
blur_b = cv2.GaussianBlur(before, (0, 0), sigmaX=4)
blur_a = cv2.GaussianBlur(after, (0, 0), sigmaX=4)
detail_b = before.astype(np.int16) - blur_b.astype(np.int16)
detail_a = after.astype(np.int16) - blur_a.astype(np.int16)
removed = np.maximum(detail_b - detail_a, 0)

candidate = after.astype(np.int16)
inside = expanded > 0
candidate[inside] += removed[inside]
candidate = np.clip(candidate, 0, 255).astype(np.uint8)

ys, xs = np.where(expanded > 0)
if len(xs) == 0:
    raise ValueError("mask contains no defect pixels")
center = (int(xs.mean()), int(ys.mean()))
input_image = cv2.seamlessClone(candidate, after, expanded, center, cv2.MIXED_CLONE)
cv2.imwrite(str(root / "synthetic-input.png"), input_image)
```

`cv2.seamlessClone` n'est utilisé ici que pour construire une corruption avec une couture contrôlée. La cible d'entraînement reste `after.png`.

## Périmètre de la perte et de l'évaluation {#loss-and-evaluation-boundary}

Un objectif de reconstruction masqué rend explicite la région visée :

```text
L = lambda_m * mean(M * |prediction - A|)
  + lambda_b * mean(ring(M) * |prediction - A|)
  + lambda_u * mean((1 - M) * |prediction - input|)
```

Le terme hors masque est facultatif et doit être choisi en fonction de la portée de modification souhaitée pour le modèle. Ne rapportez pas les chiffres de référence de l'harmonisation d'images comme des résultats de retouche de la peau : iHarmony4 se compose de paires composites synthétiques et d'images réelles, et non de paires d'images de retouche clinique ou cosmétique. Évaluez séparément la qualité de l'alignement, la précision du masque résiduel, la visibilité des coutures, la préservation de la texture et les modifications indésirables en dehors de `M`.

## Limites {#limitations}

- Les paires d'images présentant des changements de pose, d'expression, de mise au point ou d'éclairage violent l'hypothèse du résidu au pixel près ; les erreurs de recalage deviennent des défauts synthétiques.
- Un résidu flouté ne permet pas de distinguer une lésion indésirable d'une suppression intentionnelle de texture, d'un maquillage, d'un débruitage ou d'une retouche d'éclairage. Utilisez un générateur de masques relu et conservez les cas rejetés.
- Les méthodes de Poisson imposent une compatibilité de frontière, mais peuvent décaler la couleur basse fréquence ou préserver des gradients source inadaptés ; inspectez l'intérieur des patchs autant que les coutures.
- L'appariement local moyenne/écart-type suppose que l'anneau environnant est représentatif. Il échoue en présence d'occultations, d'ombres marquées, de frontières peau/cheveux et de fortes zones spéculaires.
- Une distribution de corruptions synthétiques peut être plus étroite que les défauts réels de production. Elle ne prouve pas que le modèle entraîné généralisera à de nouveaux appareils, à d'autres teintes de peau ou à d'autres styles de retouche.

## Pièges courants {#gotchas}

- **Problème : appliquer un retour arrière global de couleur de `before` vers `after` avant la synthèse.** Cela modifie le domaine de la cible et peut réintroduire un étalonnage sans rapport avec la tâche de défauts. **Correction :** utilisez ce retour arrière uniquement comme diagnostic ; créez l'entrée corrompue sur la toile `after`.
- **Problème : injecter des pixels `before` bruts.** Les patchs bruts portent des différences d'éclairage basse fréquence, de lissage et de balance des blancs, ce qui fait dominer la tâche de couture sur le signal de défaut. **Correction :** partez d'un résidu haute fréquence ; n'ajoutez un résidu chromatique borné séparément que pour des classes de taches relues.
- **Problème : utiliser un masque non dilaté pour le contrôle de couture.** La frontière de mélange peut se situer sur le bord du défaut et laisser un anneau ou un halo. **Correction :** dilatez la région d'injection/de mélange tout en conservant le masque de défauts d'origine pour la perte principale et l'évaluation.
- **Problème : traiter le clonage sans couture comme une vérité terrain d'inpainting.** Le mélange dans le domaine des gradients peut rendre une frontière continue tout en préservant le mauvais détail. **Correction :** ne l'utilisez que comme référence de corruption d'entrée, et conservez l'image `after` propre vérifiée comme cible.

## Voir aussi {#see-also}

- [[skin-retouch-pipeline]] - détection de défauts, dilatation des masques et routage de retouche préservant la texture
- [[object-removal-inpainting]] - sélection de modèles et frontières d'inpainting basé sur masque
- [[frequency-decomposition-editing]] - concepts d'édition d'image par séparation de fréquences
- [[color-space-and-gamma-reference]] - gestion des espaces colorimétriques et de la lumière linéaire
