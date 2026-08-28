---
title: Data Science & Machine Learning
type: MOC
---

# Data Science & Machine Learning

Comprehensive reference covering statistics, machine learning, deep learning, computer vision, NLP, and applied data science. From mathematical foundations through production deployment.

## Foundations

- [[math-precalculus]] - number systems, equations, functions, sets, combinatorics
- [[math-logic]] - propositional logic, first-order logic, proof techniques, computability
- [[math-for-ml]] - calculus, optimization, gradient descent, backpropagation
- [[math-linear-algebra]] - vectors, matrices, eigenvalues, SVD
- [[math-probability-statistics]] - probability theory, estimation, MLE, confidence intervals

## Statistics & Probability

- [[descriptive-statistics]] - central tendency, spread, shape, correlation, z-scores
- [[probability-distributions]] - Bernoulli, binomial, Poisson, normal, exponential, CLT
- [[hypothesis-testing]] - A/B testing, statistical tests, CUPED, experiment design
- [[causal-inference]] - DiD, propensity score matching, synthetic control, DAGs
- [[bias-variance-tradeoff]] - overfitting, underfitting, regularization, ensemble tradeoffs

## Tools & Languages

- [[python-for-ds]] - Python fundamentals for data science, Jupyter/Colab
- [[numpy-fundamentals]] - array operations, linear algebra, random generation
- [[pandas-eda]] - DataFrame manipulation, groupby, filtering, EDA workflow
- [[data-visualization]] - matplotlib, seaborn, plotly, chart selection
- [[sql-for-data-science]] - queries, window functions, CTEs, analytics patterns

## Classical Machine Learning

- [[linear-models]] - linear/logistic regression, gradient descent, regularization
- [[gradient-boosting]] - CatBoost, XGBoost, LightGBM, Random Forest, hyperparameters
- [[knn-and-classical-ml]] - KNN, SVM, decision trees, algorithm selection guide
- [[unsupervised-learning]] - K-Means, DBSCAN, PCA, t-SNE, UMAP, SVD
- [[bayesian-methods]] - Bayes' theorem, Naive Bayes, Bayesian inference

## Deep Learning

- [[neural-networks]] - architecture, training, activation functions, optimizers, regularization
- [[cnn-computer-vision]] - convolutions, architectures (ResNet, YOLO), detection, segmentation
- [[nlp-text-processing]] - tokenization, TF-IDF, embeddings, transformers, BERT
- [[rnn-sequences]] - LSTM, GRU, bidirectional, sequence-to-sequence
- [[generative-models]] - GANs, VAEs, diffusion models, CycleGAN
- [[transfer-learning]] - pre-trained models, fine-tuning strategies, domain adaptation
- [[data-augmentation]] - image/text/tabular augmentation, SMOTE

## Techniques & Evaluation

- [[feature-engineering]] - scaling, encoding, imputation, selection, pipelines
- [[model-evaluation]] - metrics (MAE, ROC AUC, F1), cross-validation, confusion matrix
- [[time-series-analysis]] - stationarity, ARIMA, seasonality, feature engineering for time
- [[monte-carlo-simulation]] - simulation, portfolio optimization, risk metrics
- [[recommender-systems]] - collaborative filtering, content-based, evaluation
- [[knowledge-tracing]] - learner modeling, BKT->DKT->SAKT->AKT->simpleKT, adaptive learning, FSRS

## Applied & Production

- [[ds-workflow]] - end-to-end project methodology, pitfalls, reproducibility
- [[bi-dashboards]] - BI systems, dashboard design, KPIs, analytics SQL
- [[ml-production]] - model serialization, serving, monitoring, drift detection
- [[financial-data-science]] - portfolio theory, derivatives, risk metrics, financial ratios
- [[ai-video-production]] - AI video pipeline, tool chain, prompt engineering for video

## Cross-Topic Links

- [[python-for-ds]] - Python setup for data science workflows
- [[sql-for-data-science]] - SQL for analytical queries
- [[complexity-analysis]] - computational complexity
- [[etl-elt-pipelines]] - data pipeline infrastructure
- [[prompt-engineering]] - prompt engineering for LLMs

## Additional References

- [[anomaly-detection]] - Identifying data points that deviate significantly from normal behavior
- [[attention-mechanisms]] - Attention allows models to focus on relevant parts of the input when producing each output element
- [[bayesian-inference]] - Bayesian approach treats model parameters as probability distributions, not point estimates
- [[dimensionality-reduction]] - Reducing number of features while preserving important information
- [[ensemble-methods]] - Combining multiple models to produce better predictions than any single model
- [[graph-neural-networks]] - GNNs operate on graph-structured data where entities (nodes) have relationships (edges)
- [[hyperparameter-optimization]] - Systematic search for the best model configuration
- [[image-similarity-pipeline]] - Production-grade image similarity pipeline using CLIP+CSD+DINOv3 backbones, contrastive learning on
- [[image-similarity-scaling]] - Concrete migration path and infrastructure decisions for image similarity systems scaling from
- [[imbalanced-data]] - When one class dominates the dataset (e.g., 99% negative, 1% positive), standard classifiers become
- [[ml-system-design]] - Designing end-to-end ML systems that work in production
- [[mlops-pipelines]] - MLOps applies DevOps principles to machine learning: version control for data/models, automated
- [[object-detection-yolo]] - Object detection finds and classifies multiple objects in images with bounding boxes
- [[probabilistic-language-models]] - N-gram models, smoothing techniques, and perplexity evaluation for text generation and NLP
- [[reinforcement-learning]] - Agent learns by interacting with an environment, receiving rewards/penalties, and optimizing a
- [[spark-big-data]] - When data exceeds single-machine memory, Spark distributes computation across clusters
- [[text-summarization]] - Extractive and abstractive summarization techniques using TF-IDF scoring and transformer models
- [[tipsv2-dense-spatial-prediction]] - Google DeepMind model for dense spatial feature prediction (depth, surface normals, segmentation)
- [[yolo-object-detection]] - YOLO (You Only Look Once) object detection - bounding box representation, IoU, NMS, evaluation
