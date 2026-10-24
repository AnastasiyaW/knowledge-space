---
title: "Conception de systèmes de ML"
category: patterns
tags: [data-science, system-design, architecture, scalability, production-ml]
level: 4
source_sha256: 4f78f3275069647f2db4f49dd0e3bf7c8846d3a2f6c12e590656d7cc4b3e1ee6
translation: machine
translated_at: '2026-10-24'
---
# Conception de systèmes de ML {#ml-system-design}

Conception de systèmes de ML de bout en bout fonctionnant en production. Couvre le cadrage du problème, le pipeline de données, le choix du modèle, l'architecture de service et la supervision. Le modèle représente généralement < 10 % de la complexité totale du système.

## Cadrage du problème {#problem-framing}

Avant toute modélisation, définissez :

1. **Objectif métier** : quelle métrique fait réellement bouger les choses (chiffre d'affaires, engagement, coût) ?
2. **Objectif ML** : que prédit le modèle ? (classification, classement, régression)
3. **Disponibilité des données** : quelles données étiquetées existent ? Peut-on générer des étiquettes ?
4. **Contraintes** : budget de latence, budget de calcul, exigences d'équité
5. **Référence de base** : quelle solution non ML existe ? (règles, heuristiques)

**Cadrages courants :**
- Détection de spam -> classification binaire
- Classement de résultats de recherche -> learning to rank (par paires ou par listes)
- Recommandation -> filtrage collaboratif + approche basée sur le contenu, servie sous forme de classement
- Fraude -> détection d'anomalies + classification supervisée
- Prédiction de l'ETA -> régression avec intervalles de confiance

## Architecture du pipeline de données {#data-pipeline-architecture}

```php
Raw Data -> Ingestion -> Validation -> Feature Engineering -> Feature Store
                                                                |
Training Pipeline <-------- Historical Features ----------------+
    |                                                           |
Model Registry                                                  |
    |                                                           |
Serving Pipeline <--------- Online Features --------------------+
    |
Predictions -> Logging -> Monitoring -> Feedback Loop
```

### Validation des données {#data-validation}

```python
import great_expectations as gx

# Define expectations
suite = gx.ExpectationSuite(name="transaction_data")
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="amount")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount", min_value=0, max_value=1000000
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfUniqueValuesToBeBetween(
        column="user_id", min_value=0.01  # not too many duplicates
    )
)
```

## Patrons de feature engineering {#feature-engineering-patterns}

### Caractéristiques temporelles {#temporal-features}

```python
# Time-based aggregations
def build_temporal_features(df, entity_col, time_col, value_col):
    features = {}
    for window in ['7d', '30d', '90d']:
        rolled = df.set_index(time_col).groupby(entity_col)[value_col].rolling(window)
        features[f'{value_col}_mean_{window}'] = rolled.mean()
        features[f'{value_col}_std_{window}'] = rolled.std()
        features[f'{value_col}_count_{window}'] = rolled.count()
    return pd.DataFrame(features)
```

### Caractéristiques d'interaction {#interaction-features}

```python
# Ratios, differences, products between features
df['price_per_sqft'] = df['price'] / df['sqft']
df['income_to_debt'] = df['income'] / (df['debt'] + 1)
df['recency_x_frequency'] = df['days_since_last'] * df['purchase_count']
```

### Target encoding (pour les variables catégorielles à forte cardinalité) {#target-encoding-for-high-cardinality-categoricals}

```python
from category_encoders import TargetEncoder

te = TargetEncoder(cols=['zip_code', 'merchant_id'], smoothing=10)
X_encoded = te.fit_transform(X_train, y_train)
# Use same encoder on test: te.transform(X_test)
```

## Arbre de décision pour le choix du modèle {#model-selection-decision-tree}

```php
Tabular data?
  Yes -> Start with CatBoost/XGBoost
    Need uncertainty? -> Bayesian methods or conformal prediction
    Need interpretability? -> SHAP on tree model or linear model
  No -> What modality?
    Text -> Pretrained transformer (fine-tune or embed)
    Image -> Pretrained CNN/ViT (fine-tune)
    Sequence/Time -> LSTM, Transformer, or specialized (Prophet, N-BEATS)
    Graph -> GNN (PyG)

Data size < 1000?
  Yes -> Simple model (logistic regression, small RF) + strong regularization
  Data size > 1M?
  Yes -> Consider online learning, distributed training, or sampling
```

## Architectures de service {#serving-architectures}

### Service en ligne (temps réel) {#online-serving-real-time}

- Latence < 100 ms par requête
- API REST (FastAPI, Flask) ou gRPC
- Modèle chargé en mémoire, features précalculées issues d'un feature store
- Mise à l'échelle horizontale derrière un répartiteur de charge

### Service par lots (batch) {#batch-serving}

- Traitement périodique de l'ensemble des données (toutes les heures / chaque jour)
- Moins coûteux, plus simple, débit plus élevé
- À utiliser pour les recommandations, le ciblage d'e-mails, la génération de rapports
- Stocker les prédictions dans une base de données ou un cache pour consultation

### Streaming (quasi temps réel) {#streaming-near-real-time}

- Traitement des événements à leur arrivée (Kafka/Flink)
- Pour la détection de fraude, la personnalisation en temps réel
- Modèle déployé sous forme de processeur de flux

## Tests A/B des modèles de ML {#ab-testing-ml-models}

```python
# Traffic splitting
import hashlib

def get_variant(user_id, experiment_id, traffic_pct=0.1):
    hash_key = f"{experiment_id}:{user_id}"
    hash_val = int(hashlib.md5(hash_key.encode()).hexdigest(), 16)
    bucket = hash_val % 1000

    if bucket < traffic_pct * 1000:
        return "treatment"  # new model
    return "control"        # existing model
```

**Puissance statistique** : il faut suffisamment d'échantillons pour obtenir des résultats fiables. Pour de petites tailles d'effet (< 1 % de gain), il peut être nécessaire de disposer de millions d'observations. Utilisez des tests séquentiels pour arrêter le test plus tôt si les résultats sont clairs.

## Boucles de rétroaction {#feedback-loops}

- **Retour direct** : l'utilisateur clique / ne clique pas -> étiquette disponible en quelques minutes
- **Retour différé** : fraude confirmée des jours ou des semaines plus tard
- **Retour implicite** : absence de signal négatif (l'utilisateur ne s'est pas plaint ne signifie pas qu'il est satisfait)
- **Danger de boucle de rétroaction** : le modèle influence les données qu'il observe. Un modèle de recommandation qui ne montre jamais l'article X n'apprendra jamais si X est pertinent

## Liste de contrôle pour la supervision {#monitoring-checklist}

| Quoi | Comment | Alerte si |
|------|---------|-----------|
| Qualité des données d'entrée | Validation de schéma, contrôles de valeurs nulles | Violation de schéma, taux de valeurs nulles > seuil |
| Dérive des features | Test de KS, PSI sur les distributions des features | p-value < 0,001 ou PSI > 0,2 |
| Dérive des prédictions | Distribution des sorties du modèle | Décalage de la moyenne ou de la variance au-delà de 2 sigma |
| Performance du modèle | Valeurs réelles vs prédites (lorsque les étiquettes sont disponibles) | Métrique en baisse de plus de 5 % par rapport à la référence |
| Latence | Temps de réponse P50/P95/P99 | P99 > SLA |
| Débit | Requêtes par seconde | Baisse de plus de 20 % par rapport à la normale |

## Pièges courants {#gotchas}

- **Le skew entre entraînement et service est le bug n°1 en production en ML** : une feature calculée différemment hors ligne (SQL sur l'historique complet) et en ligne (temps réel avec des données partielles). Utilisez un feature store ou du code de feature engineering partagé. Testez en comparant les prédictions hors ligne avec les prédictions de production sur les mêmes entrées
- **Biais de boucle de rétroaction** : si un modèle de détection de fraude bloque des transactions, vous ne voyez jamais le résultat de celles qui ont été bloquées. Entraîner sur des données biaisées renforce les biais existants. Laissez passer aléatoirement un faible pourcentage de cas signalés (exploration) ou utilisez des techniques d'inférence causale
- **Optimisation prématurée** : commencez par le modèle le plus simple susceptible de fonctionner (régression logistique, arbre unique). Établissez des métriques de référence. Les modèles complexes ne se justifient que lorsque les modèles simples sont clairement insuffisants. De nombreux systèmes en production reposent sur une régression logistique

## Voir aussi {#see-also}

- [[mlops-pipelines]]
- [[ml-production]]
- [[feature-engineering]]
- [[model-evaluation]]
