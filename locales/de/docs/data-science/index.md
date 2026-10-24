---
title: "Data Science & Machine Learning"
type: MOC
level: 4
source_sha256: 06947669b91d0bc68483b891d757b613dc8e87c2f77e805aeca06b63a235e5ed
translation: machine
translated_at: '2026-10-24'
---
# Data Science & Machine Learning {#data-science-machine-learning}

Umfassendes Nachschlagewerk zu Statistik, Machine Learning, Deep Learning, Computer Vision, NLP und angewandter Data Science. Von mathematischen Grundlagen bis zum Produktionseinsatz.

## Grundlagen {#foundations}

- [[math-precalculus]] - Zahlensysteme, Gleichungen, Funktionen, Mengen, Kombinatorik
- [[math-logic]] - Aussagenlogik, Prädikatenlogik erster Stufe, Beweistechniken, Berechenbarkeit
- [[math-for-ml]] - Analysis, Optimierung, Gradientenabstieg, Backpropagation
- [[math-linear-algebra]] - Vektoren, Matrizen, Eigenwerte, SVD
- [[math-probability-statistics]] - Wahrscheinlichkeitstheorie, Schätzung, MLE, Konfidenzintervalle

## Statistik & Wahrscheinlichkeitsrechnung {#statistics-probability}

- [[descriptive-statistics]] - Lagemaße, Streuung, Form, Korrelation, z-Werte
- [[probability-distributions]] - Bernoulli, Binomial, Poisson, Normal, Exponential, CLT
- [[hypothesis-testing]] - A/B-Testing, statistische Tests, CUPED, Versuchsplanung
- [[causal-inference]] - DiD, Propensity-Score-Matching, Synthetic Control, DAGs
- [[bias-variance-tradeoff]] - Overfitting, Underfitting, Regularisierung, Ensemble-Abwägungen

## Werkzeuge & Sprachen {#tools-languages}

- [[python-for-ds]] - Python-Grundlagen für Data Science, Jupyter/Colab
- [[numpy-fundamentals]] - Array-Operationen, lineare Algebra, Zufallszahlenerzeugung
- [[pandas-eda]] - DataFrame-Manipulation, groupby, Filterung, EDA-Workflow
- [[data-visualization]] - matplotlib, seaborn, plotly, Auswahl von Diagrammtypen
- [[sql-for-data-science]] - Abfragen, Fensterfunktionen, CTEs, Analysemuster

## Klassisches Machine Learning {#classical-machine-learning}

- [[linear-models]] - Lineare/logistische Regression, Gradientenabstieg, Regularisierung
- [[gradient-boosting]] - CatBoost, XGBoost, LightGBM, Random Forest, Hyperparameter
- [[knn-and-classical-ml]] - KNN, SVM, Entscheidungsbäume, Leitfaden zur Algorithmenauswahl
- [[unsupervised-learning]] - K-Means, DBSCAN, PCA, t-SNE, UMAP, SVD
- [[bayesian-methods]] - Bayes-Theorem, Naive Bayes, Bayessche Inferenz

## Deep Learning {#deep-learning}

- [[neural-networks]] - Architektur, Training, Aktivierungsfunktionen, Optimierer, Regularisierung
- [[cnn-computer-vision]] - Faltungen, Architekturen (ResNet, YOLO), Detektion, Segmentierung
- [[nlp-text-processing]] - Tokenisierung, TF-IDF, Embeddings, Transformer, BERT
- [[rnn-sequences]] - LSTM, GRU, bidirektional, Sequence-to-Sequence
- [[generative-models]] - GANs, VAEs, Diffusionsmodelle, CycleGAN
- [[transfer-learning]] - vortrainierte Modelle, Fine-Tuning-Strategien, Domänenanpassung
- [[data-augmentation]] - Augmentierung von Bild-, Text- und tabellarischen Daten, SMOTE

## Techniken & Evaluation {#techniques-evaluation}

- [[feature-engineering]] - Skalierung, Kodierung, Imputation, Feature-Auswahl, Pipelines
- [[model-evaluation]] - Metriken (MAE, ROC AUC, F1), Kreuzvalidierung, Konfusionsmatrix
- [[time-series-analysis]] - Stationarität, ARIMA, Saisonalität, Feature-Engineering für Zeitreihen
- [[monte-carlo-simulation]] - Simulation, Portfoliooptimierung, Risikokennzahlen
- [[recommender-systems]] - kollaboratives Filtern, inhaltsbasierte Verfahren, Evaluation
- [[knowledge-tracing]] - Lernendenmodellierung, BKT->DKT->SAKT->AKT->simpleKT, adaptives Lernen, FSRS

## Anwendung & Produktion {#applied-production}

- [[ds-workflow]] - durchgängige Projektmethodik, typische Fallstricke, Reproduzierbarkeit
- [[bi-dashboards]] - BI-Systeme, Dashboard-Design, KPIs, Analyse-SQL
- [[ml-production]] - Modell-Serialisierung, Serving, Monitoring, Drift-Erkennung
- [[financial-data-science]] - Portfoliotheorie, Derivate, Risikokennzahlen, Finanzkennzahlen
- [[ai-video-production]] - KI-Videopipeline, Werkzeugkette, Prompt-Engineering für Video

## Themenübergreifende Verweise {#cross-topic-links}

- [[python-for-ds]] - Python-Einrichtung für Data-Science-Workflows
- [[sql-for-data-science]] - SQL für analytische Abfragen
- [[complexity-analysis]] - Komplexität von Berechnungen
- [[etl-elt-pipelines]] - Infrastruktur für Datenpipelines
- [[prompt-engineering]] - Prompt-Engineering für LLMs

## Weitere Referenzen {#additional-references}

- [[anomaly-detection]] - Erkennung von Datenpunkten, die deutlich vom normalen Verhalten abweichen
- [[attention-mechanisms]] - Attention ermöglicht es Modellen, sich bei jedem Ausgabeelement auf die relevanten Teile der Eingabe zu konzentrieren
- [[bayesian-inference]] - Der Bayes-Ansatz behandelt Modellparameter als Wahrscheinlichkeitsverteilungen statt als Punktschätzungen
- [[dimensionality-reduction]] - Reduktion der Anzahl der Merkmale unter Erhalt der wichtigen Informationen
- [[ensemble-methods]] - Kombination mehrerer Modelle, um bessere Vorhersagen zu erzielen als jedes einzelne Modell
- [[graph-neural-networks]] - GNNs arbeiten auf graphstrukturierten Daten, in denen Entitäten (Knoten) Beziehungen (Kanten) haben
- [[hyperparameter-optimization]] - Systematische Suche nach der besten Modellkonfiguration
- [[image-similarity-pipeline]] - Produktionsreife Pipeline zur Bildähnlichkeit mit CLIP+CSD+DINOv3-Backbones, kontrastives Lernen auf
- [[image-similarity-scaling]] - Konkreter Migrationspfad und Infrastrukturentscheidungen für Bildähnlichkeitssysteme, die skaliert werden von
- [[imbalanced-data]] - Wenn eine Klasse den Datensatz dominiert (z. B. 99 % negativ, 1 % positiv), werden Standardklassifikatoren
- [[ml-system-design]] - Entwurf durchgängiger ML-Systeme, die im Produktivbetrieb funktionieren
- [[mlops-pipelines]] - MLOps überträgt DevOps-Prinzipien auf Machine Learning: Versionskontrolle für Daten/Modelle, automatisierte
- [[object-detection-yolo]] - Objektdetektion findet und klassifiziert mehrere Objekte in Bildern mit Bounding Boxes
- [[probabilistic-language-models]] - N-Gramm-Modelle, Glättungstechniken und Perplexitätsevaluation für Textgenerierung und NLP
- [[reinforcement-learning]] - Ein Agent lernt durch Interaktion mit einer Umgebung, erhält Belohnungen/Strafen und optimiert eine
- [[spark-big-data]] - Wenn Daten den Arbeitsspeicher einer einzelnen Maschine übersteigen, verteilt Spark die Berechnung auf Cluster
- [[text-summarization]] - Extraktive und abstrakte Zusammenfassungstechniken mit TF-IDF-Bewertung und Transformer-Modellen
- [[tipsv2-dense-spatial-prediction]] - Google-DeepMind-Modell zur Vorhersage dichter räumlicher Merkmale (Tiefe, Oberflächennormalen, Segmentierung)
- [[yolo-object-detection]] - YOLO (You Only Look Once) Objektdetektion - Darstellung von Bounding Boxes, IoU, NMS, Evaluation
