---
title: "Data Science et Machine Learning"
type: MOC
level: 4
source_sha256: 06947669b91d0bc68483b891d757b613dc8e87c2f77e805aeca06b63a235e5ed
translation: machine
translated_at: '2026-10-24'
---
# Data Science et Machine Learning {#data-science-machine-learning}

Référence complète couvrant les statistiques, le machine learning, le deep learning, la vision par ordinateur, le NLP et la data science appliquée, des fondements mathématiques jusqu'au déploiement en production.

## Fondements {#foundations}

- [[math-precalculus]] - systèmes de nombres, équations, fonctions, ensembles, combinatoire
- [[math-logic]] - logique propositionnelle, logique du premier ordre, techniques de preuve, calculabilité
- [[math-for-ml]] - calcul différentiel, optimisation, descente de gradient, rétropropagation
- [[math-linear-algebra]] - vecteurs, matrices, valeurs propres, SVD
- [[math-probability-statistics]] - théorie des probabilités, estimation, MLE, intervalles de confiance

## Statistiques et probabilités {#statistics-probability}

- [[descriptive-statistics]] - tendance centrale, dispersion, forme, corrélation, z-scores
- [[probability-distributions]] - Bernoulli, binomiale, Poisson, normale, exponentielle, TCL
- [[hypothesis-testing]] - tests A/B, tests statistiques, CUPED, conception d'expériences
- [[causal-inference]] - DiD, appariement par score de propension, contrôle synthétique, DAGs
- [[bias-variance-tradeoff]] - surapprentissage, sous-apprentissage, régularisation, compromis des ensembles

## Outils et langages {#tools-languages}

- [[python-for-ds]] - fondamentaux de Python pour la data science, Jupyter/Colab
- [[numpy-fundamentals]] - opérations sur les tableaux, algèbre linéaire, génération aléatoire
- [[pandas-eda]] - manipulation de DataFrames, groupby, filtrage, flux de travail EDA
- [[data-visualization]] - matplotlib, seaborn, plotly, choix des graphiques
- [[sql-for-data-science]] - requêtes, fonctions de fenêtrage, CTE, patterns analytiques

## Machine learning classique {#classical-machine-learning}

- [[linear-models]] - régression linéaire et logistique, descente de gradient, régularisation
- [[gradient-boosting]] - CatBoost, XGBoost, LightGBM, Random Forest, hyperparamètres
- [[knn-and-classical-ml]] - KNN, SVM, arbres de décision, guide de sélection d'algorithmes
- [[unsupervised-learning]] - K-Means, DBSCAN, PCA, t-SNE, UMAP, SVD
- [[bayesian-methods]] - théorème de Bayes, Naive Bayes, inférence bayésienne

## Deep learning {#deep-learning}

- [[neural-networks]] - architecture, entraînement, fonctions d'activation, optimiseurs, régularisation
- [[cnn-computer-vision]] - convolutions, architectures (ResNet, YOLO), détection, segmentation
- [[nlp-text-processing]] - tokenisation, TF-IDF, embeddings, transformers, BERT
- [[rnn-sequences]] - LSTM, GRU, bidirectionnel, séquence-à-séquence
- [[generative-models]] - GANs, VAEs, modèles de diffusion, CycleGAN
- [[transfer-learning]] - modèles pré-entraînés, stratégies de fine-tuning, adaptation de domaine
- [[data-augmentation]] - augmentation d'images, de texte et de données tabulaires, SMOTE

## Techniques et évaluation {#techniques-evaluation}

- [[feature-engineering]] - mise à l'échelle, encodage, imputation, sélection, pipelines
- [[model-evaluation]] - métriques (MAE, ROC AUC, F1), validation croisée, matrice de confusion
- [[time-series-analysis]] - stationnarité, ARIMA, saisonnalité, feature engineering pour les séries temporelles
- [[monte-carlo-simulation]] - simulation, optimisation de portefeuille, métriques de risque
- [[recommender-systems]] - filtrage collaboratif, filtrage basé sur le contenu, évaluation
- [[knowledge-tracing]] - modélisation de l'apprenant, BKT->DKT->SAKT->AKT->simpleKT, apprentissage adaptatif, FSRS

## Applications et production {#applied-production}

- [[ds-workflow]] - méthodologie de projet de bout en bout, pièges, reproductibilité
- [[bi-dashboards]] - systèmes BI, conception de tableaux de bord, KPI, SQL analytique
- [[ml-production]] - sérialisation de modèles, mise en service, monitoring, détection de dérive
- [[financial-data-science]] - théorie de portefeuille, produits dérivés, métriques de risque, ratios financiers
- [[ai-video-production]] - pipeline de vidéo IA, chaîne d'outils, prompt engineering pour la vidéo

## Liens transversaux {#cross-topic-links}

- [[python-for-ds]] - configuration de Python pour les workflows de data science
- [[sql-for-data-science]] - SQL pour les requêtes analytiques
- [[complexity-analysis]] - complexité algorithmique
- [[etl-elt-pipelines]] - infrastructure de pipelines de données
- [[prompt-engineering]] - prompt engineering pour les LLM

## Références complémentaires {#additional-references}

- [[anomaly-detection]] - identification des points de données qui s'écartent significativement du comportement normal
- [[attention-mechanisms]] - l'attention permet aux modèles de se concentrer sur les parties pertinentes de l'entrée lors de la production de chaque élément de sortie
- [[bayesian-inference]] - l'approche bayésienne traite les paramètres du modèle comme des distributions de probabilité, et non comme des estimations ponctuelles
- [[dimensionality-reduction]] - réduction du nombre de caractéristiques tout en préservant les informations importantes
- [[ensemble-methods]] - combinaison de plusieurs modèles pour produire de meilleures prédictions qu'un modèle unique
- [[graph-neural-networks]] - les GNN opèrent sur des données structurées en graphe, où les entités (nœuds) ont des relations (arêtes)
- [[hyperparameter-optimization]] - recherche systématique de la meilleure configuration de modèle
- [[image-similarity-pipeline]] - pipeline de similarité d'images de niveau production utilisant les backbones CLIP+CSD+DINOv3, apprentissage contrastif sur
- [[image-similarity-scaling]] - trajectoire de migration concrète et décisions d'infrastructure pour les systèmes de similarité d'images passant de
- [[imbalanced-data]] - lorsqu'une classe domine le jeu de données (par ex. 99 % négatifs, 1 % positifs), les classifieurs standards deviennent
- [[ml-system-design]] - conception de systèmes ML de bout en bout fonctionnant en production
- [[mlops-pipelines]] - le MLOps applique les principes du DevOps au machine learning : contrôle de version pour les données et les modèles, automatisation
- [[object-detection-yolo]] - la détection d'objets localise et classe plusieurs objets dans des images à l'aide de boîtes englobantes
- [[probabilistic-language-models]] - modèles n-grammes, techniques de lissage et évaluation par perplexité pour la génération de texte et le NLP
- [[reinforcement-learning]] - un agent apprend en interagissant avec un environnement, en recevant des récompenses/pénalités et en optimisant une
- [[spark-big-data]] - lorsque les données dépassent la mémoire d'une seule machine, Spark répartit le calcul sur des clusters
- [[text-summarization]] - techniques de résumé extractif et abstractif utilisant le scoring TF-IDF et des modèles transformers
- [[tipsv2-dense-spatial-prediction]] - modèle de Google DeepMind pour la prédiction dense de caractéristiques spatiales (profondeur, normales de surface, segmentation)
- [[yolo-object-detection]] - détection d'objets YOLO (You Only Look Once) - représentation par boîtes englobantes, IoU, NMS, évaluation
