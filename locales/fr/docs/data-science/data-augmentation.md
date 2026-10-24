---
title: "Augmentation des données"
category: techniques
tags: [data-science, deep-learning, augmentation, computer-vision, regularization]
level: 3
source_sha256: b7fb3b3293f938e022594a9b131f8435fae1a087eb6bec35231c32b76378e89d
translation: machine
translated_at: '2026-10-24'
---
# Augmentation des données {#data-augmentation}

Augmenter artificiellement les données d'entraînement en appliquant des transformations aléatoires. Réduit le surapprentissage et améliore la généralisation. Gain de performance pratiquement sans coût pour les tâches de vision et de NLP.

## Augmentation d'images {#image-augmentation}

### Transformations de base {#basic-transforms}

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Validation: NO augmentation (except resize + normalize)
val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

### Techniques avancées {#advanced-techniques}

- **Cutout/Random Erasing** : masquer aléatoirement des régions rectangulaires
- **Mixup** : mélanger deux images et leurs étiquettes : x = lambda*x1 + (1-lambda)*x2
- **CutMix** : coller un fragment d'une image sur une autre, et mélanger les étiquettes au prorata des surfaces
- **AutoAugment** : politiques d'augmentation apprises

## Augmentation de texte {#text-augmentation}

- **Remplacement par synonymes** : remplacer des mots par leurs synonymes
- **Rétrotraduction (back-translation)** : traduire dans une autre langue, puis retraduire dans la langue d'origine
- **Insertion/suppression/permutation aléatoires** : perturber l'ordre des mots
- **Augmentation contextuelle** : utiliser un modèle de langue pour remplacer des mots

## Augmentation de données tabulaires {#tabular-data-augmentation}

- **SMOTE** : générer des échantillons synthétiques de la classe minoritaire pour les classes déséquilibrées
- **Injection de bruit** : ajouter un bruit gaussien aux variables
- **Mixup** : mélanger les vecteurs de caractéristiques et leurs étiquettes

```python
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X_train, y_train)
```

## Principes {#principles}

- Appliquer l'augmentation **uniquement aux données d'entraînement**, jamais à la validation ni au test
- Les augmentations doivent préserver l'étiquette (retourner un « 6 » peut donner un « 9 »)
- Adapter au domaine : ne pas retourner horizontalement du texte, ne pas faire pivoter des images médicales si l'orientation compte
- Augmenter plus agressivement pour les petits jeux de données
- Combiner plusieurs augmentations pour un effet maximal

## Pièges à éviter {#gotchas}

- Une augmentation trop agressive peut nuire aux performances (le modèle apprend à gérer le bruit au lieu du signal)
- Les retournements verticaux sont rarement pertinents (la plupart des images naturelles ont une notion de gravité)
- L'augmentation colorimétrique peut détruire une information couleur importante (imagerie médicale)
- SMOTE génère des points synthétiques dans l'espace des caractéristiques, qui peuvent correspondre à des échantillons irréalistes
- L'augmentation allonge le temps d'entraînement : évaluer le bénéfice par rapport au coût

## Voir aussi {#see-also}
- [[cnn-computer-vision]] - principal bénéficiaire de l'augmentation d'images
- [[nlp-text-processing]] - techniques d'augmentation de texte
- [[feature-engineering]] - SMOTE pour les données tabulaires
- [[model-evaluation]] - mesurer l'impact de l'augmentation
