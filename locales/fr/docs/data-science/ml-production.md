---
title: "ML en production"
category: practices
tags: [data-science, mlops, deployment, monitoring, api]
level: 3
source_sha256: 2bfd591ccd3fdc8ff788a13e22de204db37a8945a8fb5e52cd168b33283dcda9
translation: machine
translated_at: '2026-10-24'
---
# ML en production {#ml-in-production}

Faire passer un modèle du notebook à la production. Couvre la sérialisation des modèles, le service (serving), la surveillance (monitoring) et les préoccupations opérationnelles qui distinguent les prototypes des produits.

## Sérialisation des modèles {#model-serialization}

```python
# Pickle (sklearn, catboost)
import pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Joblib (better for large numpy arrays)
import joblib
joblib.dump(model, 'model.joblib')
model = joblib.load('model.joblib')

# PyTorch
torch.save(model.state_dict(), 'model.pth')
model.load_state_dict(torch.load('model.pth'))

# ONNX (framework-agnostic)
import torch.onnx
torch.onnx.export(model, dummy_input, 'model.onnx')
```

## Mise à disposition des modèles {#serving-models}

### Flask/FastAPI {#flaskfastapi}
```python
from fastapi import FastAPI
import pickle

app = FastAPI()
model = pickle.load(open('model.pkl', 'rb'))

@app.post("/predict")
def predict(features: dict):
    X = preprocess(features)
    prediction = model.predict(X)
    return {"prediction": prediction.tolist()}
```

### Prédiction par lots {#batch-prediction}
Pour les cas d'usage non temps réel : exécuter les prédictions selon un planning et stocker les résultats en base de données.

```python
# Batch scoring pipeline
predictions = model.predict(batch_features)
df['prediction'] = predictions
df.to_parquet('predictions.parquet')
```

## Surveillance {#monitoring}

### Dérive des données {#data-drift}
Les caractéristiques en production s'écartent de la distribution d'entraînement.

- Comparer les distributions des caractéristiques entre les données d'entraînement et de production
- Surveiller les tests statistiques (test de KS, PSI) pour détecter la dérive
- Déclencher une alerte lorsque la dérive dépasse le seuil

### Dégradation du modèle {#model-degradation}
Les performances diminuent au fil du temps à mesure que le contexte évolue.

- Surveiller les changements de distribution des prédictions
- Suivre les métriques métier corrélées aux sorties du modèle
- Mettre en place des déclencheurs de réentraînement (planifiés ou basés sur la dérive)

### Journalisation {#logging}
Journaliser chaque prédiction avec ses caractéristiques, son horodatage et la version du modèle, pour le débogage et le réentraînement.

## Tests A/B en production {#ab-testing-in-production}

1. Rediriger une fraction du trafic vers le nouveau modèle
2. Comparer les métriques métier entre le contrôle (ancien) et le test (nouveau)
3. Utiliser des tests statistiques pour confirmer l'amélioration
4. Augmenter progressivement le trafic vers la variante gagnante
5. Surveiller les régressions après le déploiement complet

## Automatisation du pipeline {#pipeline-automation}

- **Pipelines de caractéristiques** : calcul et stockage automatisés des caractéristiques
- **Pipelines d'entraînement** : réentraînement planifié avec les dernières données
- **Portes de validation** : contrôles automatisés avant le déploiement
- **Retour arrière (rollback)** : possibilité de revenir rapidement à la version précédente du modèle

## Pièges à éviter {#gotchas}
- Les fichiers pickle ne sont pas sécurisés : ne chargez jamais de pickles non fiables
- Le modèle et le prétraitement doivent être versionnés ensemble (un décalage de scaler = prédictions erronées)
- La prédiction par lots est plus simple et suffisante pour la plupart des cas d'usage : ne construisez pas de service temps réel sauf si nécessaire
- Une dérive des données n'implique pas toujours une dégradation du modèle : investiguez avant de réentraîner
- Exigences matérielles : le CPU suffit généralement pour l'inférence ; le GPU n'est utile que pour les grands réseaux de neurones

## Voir aussi {#see-also}
- [[ds-workflow]] - cycle de vie complet du projet
- [[model-evaluation]] - évaluation hors ligne avant le déploiement
- [[hypothesis-testing]] - tests A/B sur les modèles déployés
- [[gradient-boosting]] - modèles de production courants
