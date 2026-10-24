---
title: "CNN et vision par ordinateur"
category: models
tags: [data-science, deep-learning, cnn, computer-vision, image-classification]
level: 4
source_sha256: 0abaa1ed448dbc1aba55baa2ddf043620908b9a5e820413eec929df0e723aa59
translation: machine
translated_at: '2026-10-24'
---
# CNN et vision par ordinateur {#cnns-and-computer-vision}

Les réseaux de neurones convolutifs exploitent la structure spatiale des images grâce à la détection de motifs locaux et à l'invariance par translation. De la classification à la génération, les CNN ont révolutionné la compréhension visuelle.

## L'image comme donnée {#image-as-data}

Image = tenseur 3D (hauteur x largeur x canaux). Niveaux de gris : 1 canal. RGB : 3 canaux. Chaque pixel = entier dans [0, 255].

Pour les modèles simples : aplatir en 1D (28x28 -> 784 variables). Problème : la structure spatiale est perdue. Les CNN résolvent ce problème.

## Couche de convolution {#convolution-layer}

Faire glisser un petit filtre (noyau) sur l'entrée. Chaque filtre détecte un motif (contour, texture, forme). La convolution se réduit à deux opérations : multiplication élément par élément, puis somme. Trois objets : l'image d'entrée, le filtre (noyau) et l'image de sortie (carte de caractéristiques).

- **Taille du noyau** : 3x3 et 5x5 sont courants. Empiler de petits noyaux = grand champ réceptif
- **Stride** : pas de déplacement. Un stride de 2 divise par deux les dimensions spatiales
- **Padding** : "same" conserve la taille, "valid" la réduit
- **Canaux** : les canaux d'entrée correspondent à la profondeur du filtre ; les canaux de sortie = nombre de filtres
- **Convolution 1x1** : combinaison linéaire des canaux (goulot d'étranglement, réduction de dimensionnalité)
- **Terme de biais** : chaque filtre possède un biais scalaire ajouté après la somme de convolution, avant l'activation

### La convolution comme détection de caractéristiques {#convolution-as-feature-detection}

Différents noyaux détectent différentes caractéristiques :
- **Noyau de flou** : le filtre moyenneur lisse l'image (réduction du bruit)
- **Détection de contours** : les filtres de type Sobel mettent en évidence les frontières entre régions
- **Noyau de netteté** : amplifie les différences entre pixels voisins

Dans un CNN entraîné, les noyaux ne sont pas conçus à la main : ils sont appris par rétropropagation. Les premières couches apprennent des détecteurs de contours et de textures ; les couches plus profondes apprennent des détecteurs de motifs complexes (yeux, roues, texte).

### Pooling {#pooling}

Réduction des dimensions spatiales (sous-échantillonnage). Le **max pooling** (maximum dans la fenêtre) est le plus courant. Typiquement : 2x2, stride 2.

- Pooling de taille 2 avec stride 2 : 100x100 -> 50x50 (division par deux de chaque dimension)
- Assure l'invariance par translation : de petits décalages de l'entrée ne modifient pas la sortie après pooling
- **Average pooling** : prend la moyenne au lieu du maximum. Utilisé dans certaines architectures (GoogLeNet)
- **Global Average Pooling** : réduit toute la carte de caractéristiques à une seule valeur par canal. Remplace le flatten + dense dans les architectures modernes (moins de paramètres, moins de surapprentissage)

### Architecture CNN en deux étapes {#cnn-two-stage-architecture}

Un CNN comporte deux étapes :

1. **Étape d'extraction de caractéristiques** : couches Conv + Pool alternées. Organisation hiérarchique : chaque couche détecte des caractéristiques à partir de la sortie de la couche précédente. Cette étape constitue un transformateur de caractéristiques d'image spécialisé
2. **Étape de classification** : couches denses (entièrement connectées) classiques qui prennent les caractéristiques extraites et effectuent la classification ou la régression

```php
Input -> [Conv -> BN -> ReLU -> Pool] x N -> Flatten -> Dense -> Output
```

Cette séparation explique pourquoi le transfer learning fonctionne : l'étape 1 apprend des caractéristiques générales de l'image (contours, textures, formes), tandis que l'étape 2 apprend la classification propre à la tâche.

## Évolution des architectures {#architecture-evolution}

| Architecture | Année | Innovation clé |
|-------------|------|----------------|
| **AlexNet** | 2012 | Premier CNN profond à remporter ImageNet. ReLU, dropout, augmentation de données |
| **VGG** | 2014 | Uniquement des convolutions 3x3 empilées en profondeur. Simple, uniforme |
| **GoogLeNet/Inception** | 2014 | Convolutions parallèles de tailles différentes, concaténées. Goulots 1x1 |
| **ResNet** | 2015 | Connexions résiduelles : sortie = F(x) + x. 50 à 152 couches |
| **DenseNet** | 2017 | Chaque couche est connectée à toutes les couches précédentes |
| **MobileNet** | 2017 | Convolutions séparables en profondeur pour mobile et edge |
| **EfficientNet** | 2019 | Mise à l'échelle composée (largeur, profondeur, résolution) |
| **ViT** | 2020 | Vision Transformer : application d'un transformer à des patchs d'image |

### Connexions résiduelles de ResNet {#resnet-skip-connections}

Résolvent le problème du gradient qui disparaît pour les réseaux profonds :
```php
input -> Conv -> BN -> ReLU -> Conv -> BN -> (+input) -> ReLU
```
La connexion d'identité permet aux gradients de traverser directement le réseau. ResNet a démontré qu'avec des connexions résiduelles, l'entraînement d'un réseau de 152 couches est réalisable et surpasse les alternatives moins profondes.

### Pourquoi étudier les études de cas d'architectures {#why-study-architecture-case-studies}

Les architectures de réseaux de neurones performantes sur une tâche de vision par ordinateur se transfèrent généralement à d'autres tâches. Principaux schémas de fertilisation croisée :
- **Les connexions résiduelles de ResNet** sont apparues dans les architectures transformer
- **Le traitement multi-échelle d'Inception** a influencé les feature pyramid networks
- **ViT a montré** que l'attention des transformers peut remplacer entièrement la convolution

La lecture d'articles sur les architectures développe une intuition comparable à celle qu'acquiert un programmeur en lisant le code d'autres développeurs.

## Transfer learning {#transfer-learning}

Utiliser un modèle pré-entraîné (ImageNet : 1,2 million d'images, 1000 classes) comme point de départ.

```python
import torchvision.models as models
import torch.nn as nn

model = models.resnet50(pretrained=True)

# Option A: Feature extraction (freeze everything, replace head)
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(2048, num_classes)

# Option B: Fine-tune last layers
for param in model.layer4.parameters():
    param.requires_grad = True
model.fc = nn.Linear(2048, num_classes)
```

**Règle empirique** : jeu de données plus petit = geler davantage de couches ; jeu de données plus grand = affiner davantage de couches.

## Détection d'objets {#object-detection}

Localiser des objets à l'aide de boîtes englobantes et d'étiquettes de classe.

### Détecteurs à deux étapes {#two-stage-detectors}
- **R-CNN** : propositions de régions (selective search) -> CNN par région -> classification
- **Fast R-CNN** : CNN appliqué à l'image entière, extraction des caractéristiques par région à partir de la carte de caractéristiques
- **Faster R-CNN** : Region Proposal Network (RPN) apprenant les propositions. Entièrement de bout en bout

### Détecteurs à une étape {#one-stage-detectors}
- **YOLO** : découpe l'image en grille SxS, chaque cellule prédit des boîtes et des classes. Une seule passe avant. Temps réel
- **SSD** : cartes de caractéristiques multi-échelles pour des objets de tailles différentes

### Métriques de détection {#detection-metrics}
- **IoU** : intersection / union de la boîte prédite et de la boîte de référence. >= 0,5 = correct
- **mAP@0.5** : précision moyenne (mean Average Precision) au seuil d'IoU de 0,5
- **mAP@0.5:0.95** : moyenne sur les seuils d'IoU de 0,5 à 0,95 (pas de 0,05)
- **NMS** (Non-Maximum Suppression) : suppression des détections qui se chevauchent, conservation de celle de confiance maximale

## Segmentation {#segmentation}

### Segmentation sémantique {#semantic-segmentation}
Classer chaque pixel. Pas de distinction entre instances.
- **FCN** : remplacer les couches FC par des convolutions, puis suréchantillonner
- **U-Net** : encodeur-décodeur avec connexions résiduelles. Excellent pour l'imagerie médicale
- **DeepLab** : convolutions atrous (dilatées) pour un champ réceptif plus large

### Segmentation d'instances {#instance-segmentation}
Détecter les objets ET délimiter leurs contours au niveau du pixel.
- **Mask R-CNN** : Faster R-CNN + branche de prédiction de masque par boîte détectée

### Métriques de segmentation {#segmentation-metrics}
- **mIoU** : IoU moyen sur les classes (métrique principale)
- **Coefficient de Dice** : 2*|A ∩ B| / (|A| + |B|). Équivalent au F1

## Modèles génératifs {#generative-models}

- **GAN** : entraînement adversarial générateur contre discriminateur. Difficultés : effondrement de modes, instabilité
- **VAE** : encodage vers une distribution latente, échantillonnage, décodage. Interpolation fluide
- **Diffusion** : débruitage itératif à partir d'un bruit pur. État de l'art actuel pour la qualité d'image
- **CycleGAN** : traduction d'image à image non appariée (transfert de style, adaptation de domaine)

## Vision 3D {#3d-vision}
- **Estimation de profondeur** : prédire la distance de chaque pixel à partir d'une image 2D
- **Traitement de nuages de points** : PointNet pour les données de points 3D
- **NeRF** : apprendre une scène 3D à partir d'images 2D, puis générer des vues inédites

## Convolution sur images couleur (noyaux 3D) {#convolution-on-color-images-3d-kernels}

Convolution en niveaux de gris : un filtre 2D glisse sur une image 2D. Images couleur : un **filtre 3D** glisse sur une entrée 3D (H x W x C).

- Entrée : (H, W, 3) pour du RGB. Noyau : (k, k, 3) - même profondeur que les canaux d'entrée
- Somme sur les trois canaux à chaque position -> une seule valeur scalaire en sortie
- Un noyau 3D agit comme un **détecteur de motifs couleur** : un filtre pour « cercle rouge » ne correspondra pas aux cercles bleus
- Plusieurs filtres -> plusieurs canaux de sortie : N filtres de (k, k, 3) produisent une sortie de (H', W', N)
- Chaque couche de convolution successive : canaux d'entrée = nombre de filtres de la couche précédente, et non 3

C'est pourquoi la première couche de convolution comporte peu de paramètres (3 canaux d'entrée), alors que les couches plus profondes en comportent beaucoup (64, 128, 256 canaux d'entrée, selon le nombre de filtres de la couche précédente).

## CNN pour la classification de séries temporelles {#cnns-for-time-series-classification}

Les CNN ne se limitent pas aux images : ils fonctionnent sur toute donnée présentant une structure locale spatiale ou temporelle.

### Convolution 1D pour les séries temporelles {#1d-convolution-for-time-series}

Forme d'entrée : (batch, pas de temps, variables) = (N, T, D). Utiliser Conv1D au lieu de Conv2D.

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, kernel_size=5, activation='relu',
                           input_shape=(128, 9)),  # T=128, D=9
    tf.keras.layers.MaxPooling1D(pool_size=3),
    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
    tf.keras.layers.GlobalMaxPooling1D(),  # alternatives: Flatten, GlobalAvgPooling1D
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
```

**Choix de la taille du noyau** : pour les séquences longues (T=128 et plus), utiliser des noyaux initiaux plus grands (5 à 7). Pour les séquences courtes (T~10), des noyaux plus petits (3). Un T plus grand justifie des noyaux plus grands, selon le même principe que pour les images de grande taille.

### Reconnaissance d'activité humaine (HAR) {#human-activity-recognition-har}

Application classique des CNN aux séries temporelles de capteurs. Entrée : mesures de l'accéléromètre et du gyroscope d'un smartphone (T=128 pas de temps, D=9 canaux pour x/y/z provenant de 3 capteurs).

**Architecture multi-entrées** : combiner le CNN sur séries temporelles avec des caractéristiques tabulaires (statistiques, caractéristiques FFT) par concaténation :

```python
# Time series branch
ts_input = tf.keras.Input(shape=(128, 9))
x = tf.keras.layers.Conv1D(32, 5, activation='relu')(ts_input)
x = tf.keras.layers.MaxPooling1D(3)(x)
x = tf.keras.layers.GlobalMaxPooling1D()(x)

# Tabular branch
tab_input = tf.keras.Input(shape=(num_tabular_features,))
y = tf.keras.layers.Dense(64, activation='relu')(tab_input)

# Combine
combined = tf.keras.layers.Concatenate()([x, y])
output = tf.keras.layers.Dense(num_classes, activation='softmax')(combined)
model = tf.keras.Model(inputs=[ts_input, tab_input], outputs=output)
```

### CNN pour la prévision de séries temporelles {#cnn-for-time-series-forecasting}

Utiliser le CNN comme extracteur de caractéristiques, puis une couche dense pour la prédiction. Remodeler la série univariée en entrée (T, 1).

```python
model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, kernel_size=3, activation='relu',
                           input_shape=(window_size, 1)),
    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)  # single step forecast
])
```

Remarque : les valeurs ne se divisent pas exactement après les couches de pooling ; vérifiez toujours `model.summary()` pour contrôler les formes de sortie à chaque couche.

## Pièges à éviter {#gotchas}
- Toujours normaliser les images (statistiques ImageNet : mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- L'augmentation de données est presque toujours bénéfique pour les tâches de vision
- Une résolution d'entrée plus élevée améliore la précision, mais le coût de calcul augmente de façon quadratique
- Les modèles pré-entraînés attendent des tailles d'entrée et une normalisation spécifiques
- Les versions de YOLO varient beaucoup : vérifiez la variante utilisée pour une comparaison équitable
- **Conv1D pour les séries temporelles** : le noyau glisse uniquement selon l'axe temporel, et non spatial. La forme d'entrée diffère de celle de Conv2D
- **GlobalMaxPooling vs Flatten** : GlobalMaxPooling réduit à une taille fixe quelle que soit la longueur d'entrée. Flatten exige une taille d'entrée fixe
- **Les modèles multi-entrées** nécessitent `tf.keras.Model` (API fonctionnelle), et non `Sequential`

## Voir aussi {#see-also}
- [[neural-networks]] - fondements généraux du deep learning
- [[transfer-learning]] - stratégies détaillées de pré-entraînement et d'affinage
- [[data-augmentation]] - techniques d'augmentation pour la vision
- [[generative-models]] - GAN, VAE et diffusion en détail
- [[time-series-analysis]] - modèles classiques de séries temporelles
- [[rnn-sequences]] - alternative RNN pour les données séquentielles
