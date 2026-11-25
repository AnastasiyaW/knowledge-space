---
title: "Base de connaissances"
description: "Parcourez plus de 851 articles techniques répartis en 26 domaines. Références denses pour les agents LLM et les ingénieurs."
level: 4
source_sha256: 61de659f9dfc26261b7e411c1fdb0ad71ea47087aef0fd45149fcee1986fb2ec
translation: machine
translated_at: '2026-10-24'
---
# Base de connaissances {#knowledge-base}

Plus de 851 articles sélectionnés répartis en 26 domaines. Cliquez sur un domaine pour l'explorer.

## Parcourir par domaine {#browse-by-domain}

Chaque domaine ci-dessous est repliable : développez-le pour voir la liste des articles. Les articles sont regroupés par thème au sein de chaque domaine.

---

<div id="data-science"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#a07ad0,#5a3a80);box-shadow:0 0 8px rgba(160,122,208,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Data Science & Machine Learning · 57 articles"

    **Fondations**

    - [[math-precalculus]] - Notions essentielles de précalcul pour le ML
    - [[math-logic]] - Logique mathématique et démonstrations
    - [[math-for-ml]] - Concepts mathématiques de base pour le machine learning
    - [[math-linear-algebra]] - Vecteurs, matrices, valeurs propres
    - [[math-probability-statistics]] - Théorie des probabilités et distributions

    **Statistiques & probabilités**

    - [[descriptive-statistics]] - Tendance centrale, variance, distributions
    - [[probability-distributions]] - Lois normale, binomiale, de Poisson
    - [[hypothesis-testing]] - Tests t, p-values, intervalles de confiance
    - [[causal-inference]] - Modèles causaux, tests A/B, études observationnelles
    - [[bias-variance-tradeoff]] - Complexité du modèle vs généralisation

    **Outils & langages**

    - [[python-for-ds]] - Configuration de Python pour les workflows de data science
    - [[numpy-fundamentals]] - Tableaux, broadcasting, algèbre linéaire
    - [[pandas-eda]] - DataFrames, groupby, merge, patterns d'EDA
    - [[data-visualization]] - Matplotlib, Seaborn, Plotly
    - [[sql-for-data-science]] - SQL pour les requêtes analytiques

    **Machine learning classique**

    - [[linear-models]] - Régression linéaire et logistique, régularisation
    - [[gradient-boosting]] - XGBoost, LightGBM, CatBoost
    - [[knn-and-classical-ml]] - KNN, SVM, arbres de décision, random forest
    - [[unsupervised-learning]] - Clustering, PCA, réduction de dimensionnalité
    - [[bayesian-methods]] - Théorème de Bayes, naive Bayes, inférence bayésienne

    **Deep learning**

    - [[neural-networks]] - Perceptron, rétropropagation, architectures
    - [[cnn-computer-vision]] - Convolutions, pooling, ResNet, détection
    - [[nlp-text-processing]] - Tokenisation, vecteurs de mots, classification de texte
    - [[rnn-sequences]] - LSTM, GRU, modèles séquence à séquence
    - [[generative-models]] - GAN, VAE, modèles de diffusion
    - [[transfer-learning]] - Fine-tuning, adaptation de domaine
    - [[data-augmentation]] - Stratégies d'augmentation d'images et de textes

    **Techniques & évaluation**

    - [[feature-engineering]] - Création, sélection et encodage de features
    - [[model-evaluation]] - Métriques, validation croisée, matrice de confusion
    - [[time-series-analysis]] - ARIMA, Prophet, décomposition saisonnière
    - [[monte-carlo-simulation]] - Échantillonnage aléatoire, méthodes de Monte Carlo
    - [[recommender-systems]] - Filtrage collaboratif, approches basées sur le contenu

    **Appliqué & production**

    - [[ds-workflow]] - Cycle de vie de bout en bout d'un projet de data science
    - [[bi-dashboards]] - Construction de tableaux de bord analytiques
    - [[ml-production]] - Déploiement, monitoring et drift des modèles
    - [[financial-data-science]] - Finance quantitative, modélisation des risques
    - [[ai-video-production]] - Pipelines de génération vidéo par IA

    **Autres**

    - [[anomaly-detection]] - Identification des points de données qui s'écartent significativement du comportement normal
    - [[attention-mechanisms]] - L'attention permet au modèle de se concentrer sur les parties pertinentes de l'entrée lors de la production de chaque élément de sortie
    - [[bayesian-inference]] - L'approche bayésienne traite les paramètres du modèle comme des distributions de probabilité, et non comme des estimations ponctuelles
    - [[dimensionality-reduction]] - Réduction du nombre de features tout en préservant l'information importante
    - [[ensemble-methods]] - Combinaison de plusieurs modèles pour produire de meilleures prédictions qu'un modèle unique
    - [[graph-neural-networks]] - Les GNN opèrent sur des données structurées en graphe, où des entités (nœuds) sont liées par des relations (arêtes)
    - [[hyperparameter-optimization]] - Recherche systématique de la meilleure configuration du modèle
    - [[image-similarity-pipeline]] - Pipeline de similarité d'images de niveau production utilisant les backbones CLIP+CSD+DINOv3, apprentissage contrastif sur
    - [[image-similarity-scaling]] - Chemin de migration concret et décisions d'infrastructure pour les systèmes de similarité d'images qui passent à l'échelle à partir de
    - [[imbalanced-data]] - Lorsqu'une classe domine le jeu de données (par ex. 99 % négatifs, 1 % positifs), les classifieurs standards deviennent
    - [[knowledge-tracing]] - Les modèles de knowledge tracing (KT) prédisent la probabilité qu'un apprenant réponde à une question
    - [[ml-system-design]] - Conception de systèmes ML de bout en bout fonctionnant en production
    - [[mlops-pipelines]] - Le MLOps applique les principes DevOps au machine learning : versionnement des données et des modèles, automatisation
    - [[object-detection-yolo]] - La détection d'objets localise et classe plusieurs objets dans des images à l'aide de boîtes englobantes
    - [[probabilistic-language-models]] - Modèles n-grammes, techniques de lissage et évaluation par perplexité pour la génération de texte et le NLP
    - [[reinforcement-learning]] - L'agent apprend en interagissant avec un environnement, en recevant des récompenses ou des pénalités, et en optimisant un
    - [[spark-big-data]] - Lorsque les données dépassent la mémoire d'une seule machine, Spark répartit le calcul sur des clusters
    - [[text-summarization]] - Techniques de résumé extractif et abstractif utilisant le scoring TF-IDF et les modèles transformers
    - [[tipsv2-dense-spatial-prediction]] - Modèle de Google DeepMind pour la prédiction dense de caractéristiques spatiales (profondeur, normales de surface, segmentation)
    - [[yolo-object-detection]] - Détection d'objets YOLO (You Only Look Once) : représentation par boîtes englobantes, IoU, NMS, évaluation

---

<div id="kafka"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#d07870,#803830);box-shadow:0 0 8px rgba(208,120,112,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Kafka & Message Queues · 43 articles"

    **Concepts fondamentaux**

    - [[broker-architecture]] - Fonctionnement interne des brokers, partitions, réplication
    - [[topics-and-partitions]] - Conception des topics, stratégies de partitionnement
    - [[consumer-groups]] - Coordination des consommateurs, rééquilibrage
    - [[kafka-replication-fundamentals]] - ISR, élection du leader, durabilité
    - [[kafka-fault-tolerance]] - Modes de défaillance, reprise, rééquilibrage des partitions

    **Producteurs & consommateurs**

    - [[kafka-producer-fundamentals]] - Batching, compression, idempotence
    - [[kafka-producer-advanced-patterns]] - Transactions, sémantique exactly-once
    - [[idempotent-producer]] - Sémantique exactly-once côté producteur
    - [[consumer-configuration]] - Réglage des consommateurs, polling, offsets
    - [[offsets-and-commits]] - Gestion des offsets, commit automatique vs manuel
    - [[delivery-semantics]] - At-most-once, at-least-once, exactly-once
    - [[rebalancing-deep-dive]] - Rééquilibrage coopératif, appartenance statique

    **Traitement de flux**

    - [[kafka-streams]] - KStreams, KTable, jointures, agrégations
    - [[kafka-streams-windowing]] - Fenêtres tumbling, hopping, de session
    - [[kafka-streams-time-semantics]] - Event time vs processing time
    - [[kafka-streams-state-stores]] - RocksDB, état interrogeable
    - [[ksqldb]] - SQL sur les flux, requêtes push/pull

    **Intégration**

    - [[kafka-connect]] - Connecteurs source et sink, transformations
    - [[schema-registry]] - Évolution des schémas Avro, Protobuf, JSON Schema
    - [[spring-kafka]] - Intégration de Kafka dans Spring Boot
    - [[confluent-rest-proxy]] - API REST pour Kafka
    - [[alpakka-kafka]] - Connecteur Kafka pour Akka Streams
    - [[zio-kafka]] - Client Kafka basé sur les effets ZIO

    **Patterns**

    - [[kafka-transactions]] - Patterns de messagerie transactionnelle
    - [[transactional-outbox]] - Pattern outbox pour la cohérence
    - [[event-sourcing]] - Architecture orientée événements avec Kafka
    - [[cqrs-pattern]] - Command Query Responsibility Segregation
    - [[saga-pattern]] - Coordination des transactions distribuées
    - [[messaging-models]] - Pub/sub vs file d'attente, patterns de routage
    - [[partitioning-strategies]] - Par clé, round-robin, personnalisée

    **Exploitation**

    - [[kafka-cluster-management]] - Gestion du cluster, mises à niveau progressives
    - [[kafka-monitoring-and-tuning]] - Observabilité, métriques JMX, optimisation
    - [[kafka-backup-and-dr]] - Stratégies de sauvegarde, reprise après sinistre
    - [[kafka-monitoring]] - Métriques JMX, retard des consommateurs, alertes
    - [[kafka-security]] - SSL, SASL, ACL, chiffrement
    - [[kafka-troubleshooting]] - Problèmes courants et corrections
    - [[zero-copy-and-disk-io]] - Fonctionnement interne et performances
    - [[docker-development-setup]] - Kafka local avec Docker
    - [[mirrormaker]] - Réplication inter-clusters
    - [[kafka-queues-v4]] - Sémantique de files d'attente KIP-932
    - [[nats-comparison]] - Comparaison Kafka vs NATS
    - [[admin-api]] - Référence de l'API AdminClient

    **Autres**

    - [[kafka-messaging-fundamentals]] - Garanties de livraison de Kafka, mécanique des groupes de consommateurs, stratégies de rééquilibrage et intégration

---

<div id="devops"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#c88060,#784020);box-shadow:0 0 8px rgba(200,128,96,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>DevOps & Infrastructure · 47 articles"

    **Conteneurs & Docker**

    - [[docker-fundamentals]] - Images, conteneurs, registres
    - [[dockerfile-and-image-building]] - Builds multi-étapes, mise en cache des couches
    - [[docker-compose]] - Orchestration multi-conteneurs
    - [[docker-for-ml]] - Conteneurs GPU, service de modèles

    **Kubernetes**

    - [[kubernetes-architecture]] - Plan de contrôle, nœuds, serveur d'API
    - [[kubernetes-workloads]] - Deployments, StatefulSets, DaemonSets
    - [[kubernetes-services-and-networking]] - Services, Ingress, DNS
    - [[kubernetes-storage]] - PV, PVC, StorageClasses
    - [[kubernetes-resource-management]] - Requests, limits, HPA
    - [[kubernetes-on-aks]] - Azure Kubernetes Service
    - [[kubernetes-on-eks]] - Configuration et gestion d'Amazon EKS
    - [[helm-package-manager]] - Charts, values, templating

    **CI/CD & automatisation**

    - [[cicd-pipelines]] - Conception des pipelines, étapes, artefacts
    - [[jenkins-automation]] - Jenkinsfile, bibliothèques partagées
    - [[gitops-and-argocd]] - Workflow GitOps, configuration d'ArgoCD

    **Infrastructure as Code**

    - [[terraform-iac]] - HCL, state, modules, providers
    - [[ansible-configuration-management]] - Playbooks, rôles, inventaire

    **Cloud & réseau**

    - [[aws-cloud-fundamentals]] - EC2, S3, VPC, IAM
    - [[container-registries]] - ECR, GCR, Docker Hub
    - [[datacenter-network-design]] - Topologie réseau, SDN

    **Monitoring & SRE**

    - [[monitoring-and-observability]] - Prometheus, Grafana, journalisation
    - [[sre-principles]] - SLI, SLO, budgets d'erreur
    - [[sre-incident-management]] - Astreinte, post-mortems, escalade
    - [[sre-automation-and-toil]] - Réduction du toil, automatisation
    - [[chaos-engineering-and-testing]] - Chaos Monkey, injection de pannes

    **Déploiement & architecture**

    - [[deployment-strategies]] - Blue-green, canary, rolling
    - [[service-mesh-istio]] - Istio, Envoy, gestion du trafic
    - [[microservices-patterns]] - Découverte de services, circuit breaker
    - [[devops-culture-and-sdlc]] - Principes DevOps, SDLC
    - [[git-version-control]] - Workflow Git, stratégies de branches
    - [[linux-server-administration]] - Mise en place et durcissement de serveurs

    **Autres**

    - [[comfyui-container-build]] - Patterns de construction d'images Docker ComfyUI de niveau production : résolution des conflits distutils, couches
    - [[container-security-scanning]] - Détection automatisée des vulnérabilités, des mauvaises configurations et des secrets dans les images de conteneurs, IaC
    - [[kubernetes-operators]] - Extensions logicielles qui utilisent des Custom Resources (CR) pour gérer les applications et leurs composants
    - [[kubernetes-security]] - Défense multicouche pour les clusters Kubernetes : authentification, autorisation, contrôle d'admission
    - [[kustomize]] - Personnalisation des configurations YAML de Kubernetes sans templates
    - [[libvirt-kvm-networking]] - Diagnostic et correction des coupures intermittentes de connexion sur les invités KVM utilisant le NAT de virbr0
    - [[observability-query-languages]] - Référence des trois principaux langages de requête d'observabilité : PromQL de Prometheus pour les métriques, Grafana
    - [[ois-multi-environment-task-monitoring-architecture]] - L'infrastructure OIS repose sur un déploiement monorepo uniforme entre staging et production
    - [[runpod-flash-gpu-serverless]] - RunPod Flash est un SDK Python open source (licence MIT, v1.16.0) qui permet le déploiement de
    - [[runpod-production]] - Référence pour le déploiement de charges GPU sur RunPod : choix du type de déploiement, niveaux de stratégie d'image
    - [[runpod-serverless-diagnostic-image]] - Les workers serverless meurent silencieusement
    - [[runpod-serverless-observability-limits]] - Les workers RunPod Serverless sont difficiles à déboguer non pas à cause d'une fonctionnalité manquante, mais parce que
    - [[runpod-serverless-python-silent-exit-1]] - Analyse et atténuation des plantages silencieux de workers (code de sortie 1) lors de la prise en charge d'une tâche sur RunPod
    - [[runpod-serverless-silent-worker-crashes-on-task-pickup]] - Les workers d'un environnement serverless peuvent apparaître « Ready », prendre une tâche, puis mourir silencieusement
    - [[runpod-serverless-stuck-queue-idle-workers]] - Symptôme : le endpoint de santé affiche idle > 0 ou ready > 0, la profondeur de file est positive, inProgress = 0, et
    - [[tunnel-architecture]] - Exposition sur Internet public de services hébergés sur VM ou derrière NAT, sans ouvrir de ports entrants sur le pare-feu

---

<div id="architecture"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#7088c8,#303878);box-shadow:0 0 8px rgba(112,136,200,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Software Architecture · 37 articles"

    **Processus d'architecture**

    - [[solution-architecture-process]] - Architecture decision records
    - [[architecture-documentation]] - Modèle C4, arc42, diagrammes
    - [[tech-lead-role]] - Patterns de leadership technique
    - [[system-design-interviews]] - Préparation aux entretiens de conception de systèmes

    **Styles & patterns**

    - [[architectural-styles]] - Monolithe, SOA, microservices, serverless
    - [[microservices-communication]] - Synchrone vs asynchrone, gRPC, messagerie
    - [Design Patterns (GoF)](../architecture/design-patterns-gof.md) - Patterns GoF avec exemples modernes
    - [[microfrontends]] - Architectures micro-frontend

    **Systèmes distribués**

    - [[distributed-systems-fundamentals]] - CAP, consensus, horloges
    - [[queueing-theory]] - Loi de Little, dimensionnement des capacités
    - [[quality-attributes-reliability]] - Disponibilité, tolérance aux pannes

    **Conception d'API**

    - [[http-rest-fundamentals]] - Méthodes HTTP, codes de statut, HATEOAS
    - [[rest-api-advanced]] - Pagination, versionnement, limitation de débit
    - [[graphql-api]] - Schéma, resolvers, subscriptions
    - [[grpc-api]] - Protocol buffers, streaming, intercepteurs
    - [[soap-api]] - WSDL, enveloppe SOAP, WS-Security
    - [[json-rpc-api]] - Spécification JSON-RPC 2.0
    - [[async-event-apis]] - WebSockets, SSE, webhooks
    - [[api-authentication-security]] - OAuth2, JWT, clés d'API
    - [[api-documentation-specs]] - OpenAPI, AsyncAPI, Swagger
    - [[api-testing-tools]] - Postman, curl, HTTPie

    **Données & intégration**

    - [[database-selection]] - Arbre de décision pour le choix d'une base de données
    - [[data-serialization-formats]] - JSON, Protobuf, Avro, MessagePack
    - [[caching-and-performance]] - Redis, CDN, invalidation de cache
    - [[enterprise-integration]] - EIP, middleware, ESB
    - [[message-broker-patterns]] - Pub/sub, fan-out, dead letter
    - [[kafka-architecture]] - Kafka vu depuis l'architecture
    - [[rabbitmq-architecture]] - Échanges et files RabbitMQ

    **Sécurité & exploitation**

    - [[security-architecture]] - Zero trust, défense en profondeur
    - [[devops-cicd]] - CI/CD vu depuis l'architecture
    - [[testing-and-quality]] - Pyramide de tests, portes de qualité
    - [[bigdata-ml-architecture]] - Conception de systèmes big data et ML

    **Autres**

    - [[happyin-knowledge-space]] - Happyin Knowledge Space est une référence technique publique
    - [[news-development-graph]] - Le schéma 1.4 du système de news Happyin relie chaque enregistrement de news relu à un projet ou une organisation
    - [[news-research-knowledge-lifecycle]] - Une news n'est utile à un agent que lorsqu'elle mène à une connaissance pratique et versionnée
    - [[photoshop-plugin-architecture]] - Date : 2026-04-03 Contexte : Développement d'un plugin C++ d'inférence ML multiplateforme (Mac + Windows) pour
    - [[write-buffering-patterns]] - Patterns de durabilité et de débit pour absorber des écritures à haute fréquence avant un stockage lent ou

---

<div id="data-engineering"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#8878b8,#483868);box-shadow:0 0 8px rgba(136,120,184,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Data Engineering · 34 articles"

    **Concepts & architecture**

    - [[etl-elt-pipelines]] - ETL vs ELT, patterns de pipelines
    - [[dwh-architecture]] - Conception d'entrepôt de données, Kimball vs Inmon
    - [[data-modeling]] - Modèles conceptuel, logique, physique
    - [[dimensional-modeling]] - Schéma en étoile, flocon, faits/dimensions
    - [[data-vault]] - Méthodologie Data Vault 2.0
    - [[scd-patterns]] - Dimensions à évolution lente (types 1 à 6)
    - [[data-lake-lakehouse]] - Delta Lake, Iceberg, Hudi
    - [[data-quality]] - Frameworks de qualité des données, great expectations
    - [[data-governance-catalog]] - Gestion des métadonnées, catalogues de données
    - [[data-lineage-metadata]] - Suivi de la lignée, analyse d'impact
    - [[file-formats]] - Comparatif Parquet, ORC, Avro, CSV

    **Traitement distribué**

    - [[apache-spark-core]] - RDD, DAG, exécuteurs, partitions
    - [[pyspark-dataframe-api]] - Opérations sur les DataFrames PySpark
    - [[spark-optimization]] - Broadcast, repartitionnement, mise en cache
    - [[spark-streaming]] - Structured Streaming, micro-batch
    - [[apache-kafka]] - Kafka pour les pipelines de data engineering
    - [[mapreduce]] - Paradigme MapReduce et implémentations

    **Stockage & bases de données**

    - [[hadoop-hdfs]] - Architecture HDFS, réplication
    - [[apache-hive]] - HiveQL, partitions, bucketing
    - [[hbase]] - Stockage orienté colonnes, conception de la row key
    - [[clickhouse]] - Moteur OLAP, MergeTree, vues matérialisées
    - [[clickhouse-engines]] - Référence des types de moteurs ClickHouse
    - [[greenplum-mpp]] - Architecture MPP, distribution
    - [[postgresql-administration]] - PostgreSQL pour le data engineering
    - [[mongodb-nosql]] - Modèle document, pipeline d'agrégation

    **Infrastructure**

    - [[apache-airflow]] - DAG, opérateurs, ordonnancement
    - [[cloud-data-platforms]] - Services de données AWS/GCP/Azure
    - [[docker-for-de]] - Docker pour les pipelines de données
    - [[kubernetes-for-de]] - K8s pour Spark et Airflow
    - [[yarn-resource-management]] - Architecture YARN, ordonnancement

    **Transversal**

    - [[mlops-feature-store]] - Feature stores, pipelines ML
    - [[sql-for-de]] - Patterns SQL pour le data engineering
    - [[python-for-de]] - Outils Python pour les pipelines de données

    **Autres**

    - [[vector-search-at-scale]] - Passage à l'échelle de la recherche de similarité par embeddings, de quelques dizaines de milliers à plusieurs millions de vecteurs

---

<div id="llm-agents"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#c0b060,#706020);box-shadow:0 0 8px rgba(192,176,96,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>LLM & AI Agents · 70 articles"

    **Fondations**

    - [[transformer-architecture]] - Guide pratique, tenant compte des versions, sur la structure des transformers à attention, le décodage autorégressif, l'information de position et les limites de configuration en production.
    - [[tokenization]] - BPE, WordPiece, SentencePiece
    - [[embeddings]] - Word2Vec, embeddings de phrases, espaces vectoriels
    - [[frontier-models]] - Comparatif GPT-4, Claude, Gemini, Llama

    **Prompting & génération**

    - [[prompt-engineering]] - Prompts système, few-shot, chain-of-thought
    - [[function-calling]] - Utilisation d'outils, sortie structurée
    - [[llm-api-integration]] - Patterns d'API, streaming, gestion des erreurs

    **RAG**

    - [[rag-pipeline]] - Architecture de génération augmentée par la récupération
    - [[chunking-strategies]] - Découpage des documents, chevauchement, chunking sémantique
    - [[vector-databases]] - Construire la recherche vectorielle autour d'embeddings versionnés, de filtres de métadonnées autorisés, de la provenance, de l'évaluation du rappel et d'une migration sûre, plutôt que de classements de produits statiques.

    **Agents**

    - [[agent-fundamentals]] - Boucle d'agent, utilisation d'outils, planification
    - [[agent-design-patterns]] - ReAct, MRKL, plan-and-execute
    - [[multi-agent-systems]] - Coordonner plusieurs agents à travers des contrats de tâche, la propriété, l'autorité, l'état et les frontières de preuve ; n'ajouter des agents que lorsqu'une décomposition mesurée en a besoin.
    - [[agent-memory]] - Mémoire court et long terme, gestion du contexte
    - [[agent-security]] - Injection de prompt, garde-fous, sandboxing

    **Frameworks**

    - [[langchain-framework]] - Guide tenant compte des versions du harnais d'agent actuel de LangChain, des intégrations de fournisseurs, des middlewares, de l'état et des limites de production.
    - [[langgraph]] - Workflows d'agents basés sur des graphes
    - [[no-code-platforms]] - Outils d'IA low-code
    - [[spring-ai]] - Framework Spring AI pour Java
    - [[ai-coding-assistants]] - Exploiter les assistants de code IA à travers des frontières explicites de périmètre, de données, d'outils, d'approbation et de preuve, plutôt que des classements de produits ou une confiance accordée au code généré.

    **Exploitation**

    - [[fine-tuning]] - LoRA, QLoRA, fine-tuning complet
    - [[model-optimization]] - Quantification, élagage, distillation
    - [[ollama-local-llms]] - Déploiement de modèles en local
    - [[llmops]] - Monitoring, évaluation, versionnement des LLM
    - [[production-patterns]] - Patterns de déploiement en production

    **Autres**

    - [[adaptive-learning-systems]] - Patterns d'architecture pour les systèmes éducatifs pilotés par l'IA qui s'adaptent à chaque apprenant
    - [[adaptive-patterns-for-autonomous-agents]] - Utiliser un état de tâche explicite, des hooks bornés, des sous-agents à capacités restreintes et des portes fondées sur des preuves, plutôt que des déclencheurs par mots-clés opaques ou des scores d'ambiguïté arbitraires.
    - [[agent-architectures]] - Structurer le flux de contrôle et la gestion d'état d'un agent LLM au-delà des patterns individuels
    - [[agent-deployment]] - Faire passer les agents du prototype à la production
    - [[agent-evaluation]] - Évaluer le comportement d'un agent avec des fixtures de tâches versionnées, des validateurs déterministes, des contrôles d'effets de bord maîtrisés et des preuves reproductibles, plutôt qu'un score de benchmark unique.
    - [[agent-observability-dashboards]] - Observabilité en temps réel pour les systèmes multi-agents et sous-agents : télémétrie basée sur les hooks, événement
    - [[agent-orchestration]] - Coordonner appels de modèles, outils, transferts, approbations, relances et preuves via un état de tâche explicite, plutôt qu'une boucle d'agent propre à un framework.
    - [[agent-safety-alignment]] - Construire la sécurité des agents comme des frontières explicites d'autorité, de données, d'outils, d'approbation et de preuve, plutôt que comme une simple promesse au niveau du prompt.
    - [[agent-scope-evasion]] - Les agents de code entraînés à réduire la complaisance présentent un mode de défaillance documenté : face à
    - [[agent-self-improvement]] - Techniques permettant aux agents d'améliorer leurs propres performances par la réflexion, la récompense au niveau des étapes
    - [[agentic-rl-competitive-programming]] - GrandCode (2026) atteint des performances de niveau grand maître sur des problèmes de programmation compétitive grâce à
    - [[agentic-security-2026]] - Guide de modélisation des menaces et de contrôles pour les agents utilisant des outils, les intégrations MCP, la mémoire persistante et les effets irréversibles. Périmètre vérifié le 2026-09-03.
    - [[agentic-systems-landscape-2026]] - Protocoles multi-agents, comparatif des SDK, patterns d'orchestration et agents de code réels
    - [[ai-adaptive-learning-systems]] - Architecture tenant compte des versions pour les preuves d'apprentissage, la planification déterministe, le tutorat LLM contraint, l'évaluation et les garde-fous sur les données des apprenants.
    - [[ai-agent-ide-features]] - Concevoir et évaluer des environnements de codage assistés par IA autour de l'isolation des espaces de travail, des permissions explicites, des artefacts de tâche durables, de la vérification et de la revue.
    - [[autonomous-agent-evolution]] - Remplacer la recherche évolutionnaire figée (agents sans état) par des agents autonomes de longue durée
    - [[chinese-ai-coding-ecosystem]] - Outils, patterns et pratiques communautaires des assistants de code IA chinois : Trae, OpenSpec, MetaGPT, GLM-5
    - [[claude-adaptive-thinking]] - Configurer et évaluer l'effort de raisonnement de Claude sans se fier à une sagesse populaire figée et propre à chaque modèle.
    - [[claude-code-degradation-2026]] - Méthode fondée sur des preuves tangibles pour diagnostiquer les changements de qualité, de configuration, de coût et de disponibilité d'un agent de code, sans inventer d'incident chez le fournisseur.
    - [[claude-code-ecosystem]] - Utiliser les plugins, skills, hooks, instructions de projet et sous-agents de Claude Code comme surfaces de gouvernance explicites et versionnées ; vérifier leur schéma actuel et leur portée effective avant tout déploiement.
    - [[claude-code-harness-patterns]] - Une frontière pratique entre instructions, outils, portes déterministes, revue et preuves durables pour le travail d'un agent de code.
    - [[claude-desktop-session-management]] - Utiliser les contrôles d'export, de compte et d'extension supportés plutôt que de s'appuyer sur les détails internes non versionnés du cache local pour la reprise de conversations ou la synchronisation entre appareils.
    - [[claude-managed-agents]] - Définir des sous-agents Claude Code gérés par l'organisation avec un périmètre explicite, une priorité, des limites d'outils et une vérification, plutôt que de traiter la configuration gérée comme un runtime d'exécution dans le cloud.
    - [[context-engineering]] - Traiter le contexte du modèle comme une entrée de travail bornée, et conserver l'état de la tâche, les preuves, l'autorité et la provenance de la récupération dans des artefacts versionnés plutôt que dans des allocations fixes de tokens.
    - [[gradio-llm-interfaces]] - Prototypage rapide d'interfaces de chat avec streaming, rendu markdown et comparaison multi-modèles
    - [[handoff-rollup-pattern]] - Comment créer une synthèse bornée et auditable d'un travail d'agent de longue durée, sans prétendre qu'un résumé est sans perte.
    - [[kv-cache-compression]] - Réduire la mémoire du cache KV pendant l'inférence des LLM pour permettre des contextes plus longs et davantage de requêtes concurrentes
    - [[llm-fine-tuning-practical]] - Guide de bout en bout du fine-tuning via API frontier et QLoRA, avec un cadre de décision sur le moment où l'utiliser
    - [[llm-persona-design-and-engineering]] - Concevoir la persona d'un LLM comme une politique comportementale versionnée, avec des frontières explicites d'autorité, de confidentialité, d'escalade et d'évaluation, plutôt que comme une personnalité supposée du modèle.
    - [[managed-agents]] - Guide tenant compte des versions du harnais d'agents gérés d'Anthropic : configuration des agents, environnements, sessions, événements, politiques de permission et frontières de données.
    - [[multi-agent-messaging]] - Patterns de communication inter-agents pour les sessions Claude Code : Agent Teams intégrés, basés sur les hooks
    - [[multi-agent-systems-architectures-2026]] - Les systèmes multi-agents (MAS) se sont scindés en deux grandes écoles architecturales : basées sur les rôles
    - [[multi-session-coordination]] - Patterns de coordination durables pour plusieurs sessions d'agents de code : worktrees isolés, manifestes, preuves en ajout seul, baux sur les ressources exclusives et intégration vérifiée.
    - [[notebooklm-integration]] - Utiliser Google NotebookLM comme backend de recherche gratuit pour Claude Code, avec des workflows économes en tokens
    - [[oh-my-claudecode-omc-architecture]] - Comment adopter le plugin OMC, en évolution rapide, sans confondre commandes tierces, routage de modèles ou état généré avec une frontière stable de sécurité ou de release.
    - [[persona-adaptive-llm]] - Un cadre de décision pour les champs de profil, la mémoire de récupération et la personnalisation par adaptateurs, avec isolation des locataires, évaluation, consentement et frontières de suppression.
    - [[qwen-code]] - Installation, authentification, diagnostics et historique de projet tenant compte des versions pour Qwen Code
    - [[scaling-laws-and-benchmarks]] - Loi de scaling de Chinchilla, benchmarks standards (ARC, DROP, HellaSwag) et lignes directrices de sélection de modèles
    - [[social-media-mcp-tools]] - Conception indépendante du fournisseur, avec approbation préalable, pour utiliser MCP afin de rédiger, valider et publier du contenu sur les réseaux sociaux sans traiter une publication comme une action réversible dans un chat.
    - [[swarm-based-review-and-multisampling-in-agentic-workflows]] - Générer des candidats indépendants, valider les preuves et sélectionner les sorties d'agents via des critères d'acceptation explicites, plutôt que par des nombres de votes figés ou la confiance du modèle.
    - [[telegram-managed-bots]] - Guide orienté production sur le modèle de bots gestionnaires de Telegram : création, rotation des tokens, paramètres d'accès, isolation d'état et reçus de cycle de vie.
    - [[token-optimization]] - Réduire la consommation de tokens dans les systèmes d'agents sans dégrader les performances de la tâche
    - [[tool-use-patterns]] - Comment concevoir, exposer et gérer les outils pour les agents LLM
    - [[uml-driven-agent-development]] - Utiliser de petits diagrammes de séquence, d'état et de frontières de confiance, versionnés, pour clarifier les workflows d'agents, puis les valider dans le moteur de rendu et la cible CI qui les publieront.
    - [[unsloth]] - Référence tenant compte des artefacts pour Unsloth Core, Studio, Desktop et les recommandations de fine-tuning liées à une version

---

<div id="sql-databases"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#9888c0,#504070);box-shadow:0 0 8px rgba(152,136,192,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>SQL et bases de données · 33 articles"

    **Fondamentaux SQL**

    - [[select-fundamentals]] - SELECT, WHERE, ORDER BY, LIMIT
    - [[aggregate-functions-group-by]] - COUNT, SUM, AVG, GROUP BY, HAVING
    - [[joins-and-set-operations]] - Jointures INNER, LEFT, FULL, CROSS, UNION
    - [[subqueries-and-ctes]] - Sous-requêtes, CTE, CTE récursives
    - [[window-functions]] - ROW_NUMBER, RANK, LAG, LEAD, cadres (frames)
    - [[dml-insert-update-delete]] - INSERT, UPDATE, DELETE, MERGE

    **Schéma et modélisation**

    - [[ddl-schema-management]] - CREATE, ALTER, contraintes, index
    - [[data-types-and-nulls]] - Choix des types, gestion des NULL
    - [[schema-design-normalization]] - 1NF à 5NF, dénormalisation

    **Transactions et concurrence**

    - [[transactions-and-acid]] - Propriétés ACID, niveaux d'isolation
    - [[concurrency-and-locking]] - Verrous, MVCC, interblocages
    - [[distributed-transactions]] - 2PC, saga, cohérence à terme

    **Internes et performance**

    - [[database-storage-internals]] - Pages, B-trees, buffer pool
    - [[btree-and-index-internals]] - Structure des B-trees, types d'index
    - [[index-strategies]] - Index composites, couvrants, partiels
    - [[query-optimization-explain]] - Plans EXPLAIN, optimisation des requêtes
    - [[database-cursors]] - Curseurs côté serveur, pagination

    **PostgreSQL**

    - [[postgresql-mvcc-vacuum]] - MVCC, autovacuum, bloat
    - [[postgresql-configuration-tuning]] - shared_buffers, work_mem
    - [[postgresql-wal-durability]] - WAL, réplication, reprise
    - [[postgresql-data-loading]] - COPY, insertions en masse, pg_dump

    **MySQL et HA**

    - [[mysql-innodb-engine]] - Internes d'InnoDB, buffer pool
    - [[connection-pooling]] - PgBouncer, HikariCP
    - [[replication-fundamentals]] - Streaming, réplication logique
    - [[postgresql-ha-patroni]] - Mise en place d'un cluster HA Patroni
    - [[backup-and-recovery]] - pg_dump, pg_basebackup, PITR

    **Montée en charge et sécurité**

    - [[partitioning-and-sharding]] - Partitionnement de tables, sharding
    - [[distributed-databases]] - CockroachDB, YugabyteDB, Vitess
    - [[caching-redis-memcached]] - Motifs Redis, Memcached
    - [Sécurité des bases de données](../sql-databases/database-security.md) - Rôles, RLS, chiffrement
    - [[postgresql-docker-kubernetes]] - PostgreSQL en conteneurs
    - [[infrastructure-as-code]] - Motifs IaC pour les bases de données

    **Plus**

    - [[advanced-patterns]] - Motifs SQL avancés au-delà du CRUD de base - fonctions de fenêtrage pour l'analytique, sous-requêtes corrélées

---

<div id="web-frontend"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#6090c8,#204078);box-shadow:0 0 8px rgba(96,144,200,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Frontend web · 36 articles"

    **HTML et CSS**

    - [[html-fundamentals]] - HTML sémantique, accessibilité
    - [[html-tables-and-forms]] - Formulaires, validation, tableaux
    - [[css-selectors-and-cascade]] - Spécificité, cascade, héritage
    - [[css-box-model-and-layout]] - Modèle de boîte, positionnement
    - [[css-flexbox]] - Conteneur flex, éléments, alignement
    - [[css-grid]] - Grid template, zones, auto-fill
    - [[css-responsive-design]] - Media queries, approche mobile-first
    - [[css-animation-and-transforms]] - Transitions, keyframes, transformations
    - [[css-sass-and-methodology]] - SASS, BEM, modules CSS

    **JavaScript**

    - [[js-variables-and-types]] - var/let/const, types, coercition
    - [[js-control-flow]] - Boucles, conditionnelles, gestion des erreurs
    - [[js-strings-and-numbers]] - Méthodes de chaînes, précision des nombres
    - [[js-functions]] - Fonctions fléchées, fermetures, IIFE
    - [[js-scope-closures-this]] - Chaîne de portée, liaison de this
    - [[js-arrays]] - Méthodes de tableaux, motifs fonctionnels
    - [[js-objects-and-data]] - Objets, déstructuration, spread
    - [[js-dom-and-events]] - Manipulation du DOM, délégation d'événements
    - [[js-async-and-fetch]] - Promesses, async/await, API fetch

    **TypeScript et React**

    - [[typescript-fundamentals]] - Types, interfaces, génériques
    - [[typescript-advanced]] - Types utilitaires, types mappés, types conditionnels
    - [[react-components-and-jsx]] - Composants, props, enfants
    - [[react-state-and-hooks]] - useState, useEffect, hooks personnalisés
    - [[react-rendering-internals]] - DOM virtuel, réconciliation
    - [[react-styling-approaches]] - CSS-in-JS, Tailwind, modules

    **Build et design**

    - [[npm-and-task-runners]] - Scripts npm, gestion des paquets
    - [[frontend-build-systems]] - Webpack, Vite, esbuild
    - [[git-and-github]] - Flux de travail Git pour le frontend
    - [[figma-fundamentals]] - Bases de Figma pour les développeurs
    - [[figma-layout-and-components]] - Auto layout, composants
    - [[figma-design-workflow]] - Flux de travail du design au code

    **Plus**

    - [[3d-browser-libs-for-video]] - Comparaison de Three.js, React Three Fiber, Spline, Lottie et autres bibliothèques 3D/animation pour
    - [[dom-free-text-layout]] - Mesure et mise en page du texte sans déclencher de reflow du DOM par le navigateur
    - [[javascript-async-event-loop]] - Référence complète de la programmation asynchrone en JavaScript - des callbacks jusqu'à
    - [[javascript-concurrency-primitives]] - Coordination asynchrone avancée en JavaScript - sémaphores, mutex, files et pools asynchrones, worker
    - [[remotion-programmatic-video]] - Créer des démos produit, vidéos marketing et decks de présentation sous forme de composants React - rendu en MP4 avec
    - [[video-motion-design-rules]] - Valeurs concrètes pour la durée, les easings, les niveaux audio, la composition et la narration dans les vidéos produit

---

<div id="python"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#50b89a,#20684a);box-shadow:0 0 8px rgba(80,184,154,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Python · 33 articles"

    **Fondamentaux du langage**

    - [[variables-types-operators]] - Variables, types, opérateurs
    - [[strings-and-text]] - Méthodes de chaînes, formatage, regex
    - [[data-structures]] - Listes, dictionnaires, ensembles, tuples
    - [[control-flow]] - Conditionnelles, boucles, compréhensions

    **Fonctions et POO**

    - [[functions]] - Arguments, kwargs, décorateurs, fermetures
    - [[decorators]] - Motifs de décorateurs, functools
    - [[oop-fundamentals]] - Classes, héritage, encapsulation
    - [[oop-advanced]] - Métaclasses, descripteurs, ABC
    - [[magic-methods]] - Méthodes dunder, protocoles

    **Gestion des erreurs et E/S**

    - [Gestion des erreurs et gestionnaires de contexte](../python/error-handling.md) - Exceptions, gestionnaires de contexte
    - [[file-io]] - Opérations sur fichiers, pathlib, CSV/JSON
    - [[regular-expressions]] - Motifs regex, module re

    **Bibliothèque standard et avancé**

    - [[standard-library]] - collections, itertools, functools
    - [[iterators-and-generators]] - Générateurs, yield, évaluation paresseuse
    - [[type-hints]] - Annotations de types, mypy, pydantic
    - [[async-programming]] - asyncio, coroutines, boucle d'événements
    - [Concurrence - threading et multiprocessing](../python/concurrency.md) - Threading, multiprocessing, GIL
    - [[memory-and-internals]] - Internes de CPython, modèle mémoire

    **Performance et tests**

    - [[profiling-and-optimization]] - cProfile, line_profiler, optimisation
    - [[recursion-and-algorithms]] - Motifs récursifs en Python
    - [[testing-with-pytest]] - pytest, fixtures, mocking
    - [[project-setup-and-tooling]] - venv, pip, poetry, pre-commit

    **FastAPI**

    - [[fastapi-fundamentals]] - Routes, injection de dépendances
    - [[fastapi-pydantic-validation]] - Modèles Pydantic, validation
    - [[fastapi-database-layer]] - SQLAlchemy, accès asynchrone à la base de données
    - [[fastapi-auth-and-security]] - JWT, OAuth2, CORS
    - [[fastapi-deployment]] - Uvicorn, Docker, production
    - [[fastapi-caching-and-tasks]] - Cache Redis, tâches en arrière-plan

    **Écosystème**

    - [[web-frameworks-comparison]] - Flask vs Django vs FastAPI
    - [[data-analysis-basics]] - Démarrage rapide avec pandas, numpy

    **Plus**

    - [[django-rest-framework]] - Motifs de sérialiseurs Django REST Framework, gestion des relations, validation et ORM avancé
    - [[stdlib-patterns]] - Structures de données de la bibliothèque standard Python et outils de programmation fonctionnelle - module collections
    - [[web-scraping]] - Motifs de scraping web avec BeautifulSoup - méthodes de recherche d'éléments, extraction de données, pagination, tableaux

---

<div id="security"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#b87080,#683040);box-shadow:0 0 8px rgba(184,112,128,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Sécurité et cybersécurité · 61 articles"

    - [[information-security-fundamentals]] - Triade CIA, gestion des risques
    - [[cryptography-and-pki]] - Chiffrement, certificats, TLS
    - [[authentication-and-authorization]] - OAuth2, SAML, RBAC
    - [[web-application-security-fundamentals]] - OWASP Top 10
    - [[sql-injection-deep-dive]] - Détection et prévention des injections SQL
    - [[burp-suite-and-web-pentesting]] - Tests de applications web avec Burp Suite
    - [[penetration-testing-methodology]] - Cycle de vie du test d'intrusion
    - [[privilege-escalation-techniques]] - Élévation de privilèges sous Linux/Windows
    - [[active-directory-attacks]] - Exploitation et défense d'Active Directory
    - [[network-security-and-protocols]] - TLS, VPN, règles de pare-feu
    - [[linux-system-hardening]] - Liste de contrôle du durcissement du système d'exploitation
    - [[siem-and-incident-response]] - Outils SIEM, processus de réponse aux incidents
    - [[browser-and-device-fingerprinting]] - Techniques de fingerprinting
    - [[anti-fraud-behavioral-analysis]] - Motifs de détection de fraude

    **Plus**

    - [[adobe-piracy-patterns]] - Date : 2026-04-03 Contexte : recherche en sécurité défensive
    - [[ai-agent-production-disasters]] - Analyse des défaillances critiques en production causées par des agents de codage IA autonomes entre 2025 et 2026
    - [[ai-powered-vulnerability-detection-april-2026]] - L'état de l'art de l'audit de sécurité automatisé est passé du SAST basé sur des motifs à des approches hybrides
    - [[ai-vulnerability-detection]] - Date : 2026-04-14 Contexte : état de l'art de l'analyse de sécurité assistée par IA en avril 2026
    - [[anti-piracy-legal]] - Date : 2026-04-03 Contexte : produit d'inférence ML de bureau
    - [[claude-mythos-leak-and-ai-supply-chain-security]] - L'accès non autorisé à l'aperçu Claude Mythos (avril 2026) sert de référence pour la sécurité de la chaîne d'approvisionnement de l'IA
    - [[compliance-and-regulations]] - Cadres réglementaires et exigences de conformité : ISO 27001, NIST Cybersecurity Framework, PCI
    - [[computation-obfuscation]] - Date : 2026-04-03 Contexte : produit d'inférence ML de bureau
    - [[cwe-079-xss]] - CWE-79 : données contrôlées par un attaquant insérées dans le DOM/HTML sans échappement
    - [[cwe-089-sql-injection]] - CWE-89 : injection SQL - des données non fiables modifient la structure de la requête
    - [[cwe-125-oob-read]] - CWE-125 : lecture hors limites - les lectures au-delà des bornes du tampon divulguent des secrets, des clés et le tas adjacent
    - [[cwe-190-integer-overflow]] - CWE-190 : une opération arithmétique produit un résultat hors plage, avec repliement ou troncature
    - [[cwe-400-resource-consumption]] - CWE-400 : un attaquant déclenche une consommation incontrôlée de CPU, mémoire, disque ou descripteurs de fichiers via un DoS par regex, hachage
    - [[cwe-416-use-after-free]] - CWE-416 : Use After Free - l'accès à une mémoire libérée permet une exécution de code à distance, une divulgation d'informations ou un DoS
    - [[cwe-434-file-upload]] - CWE-434 : téléversement non restreint de types de fichiers dangereux - les fichiers téléversés s'exécutent sur le serveur
    - [[cwe-502-deserialization]] - CWE-502 : la désérialisation de données contrôlées par un attaquant permet l'exécution de code arbitraire via des chaînes de gadgets
    - [[cwe-787-oob-write]] - CWE-787 : écriture hors limites - corruption de la mémoire par des écritures au-delà des bornes du tampon
    - [[cwe-918-ssrf]] - CWE-918 : le serveur effectue des requêtes HTTP/de protocole vers des URL contrôlées par un attaquant, exposant des ressources internes
    - [Sécurité des bases de données](../security/database-security.md) - Sécurité des bases de données SQL et NoSQL : gestion des privilèges utilisateurs, chiffrement au repos et en transit
    - [[deepfake-and-document-forensics]] - Détection et analyse de contenus falsifiés : technologies de deepfake vidéo/audio et méthodes de détection
    - [[disposable-email-detection]] - Référence backend pour la détection des adresses e-mail jetables et des abus multi-comptes lors de l'inscription
    - [[email-reputation-services]] - Catégories de signaux, compromis entre services de fournisseurs et pile MVP « faire soi-même » pour bloquer les risques élevés
    - [[firewall-and-ids-ips]] - Contrôles de sécurité des couches réseau et applicative : iptables/ufw pour les pare-feu Linux, Windows Defender
    - [[hkdf-personalized-weights]] - Date : 2026-04-03 Contexte : application de bureau C++, inférence ONNX Runtime
    - [[licensing-implementation-cpp]] - Date : 2026-04-03 Contexte : application de bureau C++ (Mac + Windows), serveur de licences auto-hébergé, modèles ONNX
    - [[linux-os-fundamentals]] - Fondements internes de Linux pertinents pour la sécurité : hiérarchie du système de fichiers, modèle utilisateur, noyau vs
    - [[lora-weight-protection]] - Date : 2026-04-03 Contexte : génération d'images de bureau/serveur avec adaptateurs LoRA propriétaires sur
    - [[model-weight-encryption]] - Date : 2026-04-03 Contexte : application de bureau C++ (Mac + Windows)
    - [[network-traffic-analysis]] - Capture et analyse de paquets avec tcpdump et Wireshark, scan de ports avec nmap, et réseau
    - [[onnx-model-protection]] - Date : 2026-04-03 Contexte : application de bureau C++ (Mac + Windows), inférence ONNX Runtime, protection de
    - [[osint-and-reconnaissance]] - Techniques de renseignement en sources ouvertes : recherche d'infrastructures avec Shodan/Censys, Google Dorking, métadonnées
    - [[output-scrambling-antipiracy]] - Date : 2026-04-03 Contexte : application de bureau C++ avec inférence ONNX
    - [[piracy-economics]] - Date : 2026-04-03 Contexte : produits d'inférence ML de bureau
    - [[python-for-security]] - Script Python pour les professionnels de la sécurité : programmation par sockets pour le scan de ports et la récupération de bannières
    - [[remote-kill-switch]] - Date : 2026-04-03 Contexte : application de retouche de bureau C++ (Mac + Windows)
    - [[retouch4me-competitive-analysis]] - Date : 2026-04-03 Contexte : analyse architecturale et produit pour la construction d'un concurrent de retouche
    - [[secure-backend-development]] - Patterns de sécurité pour le développement backend avec Node.js/NestJS/Express : validation des entrées
    - [[security-solutions-architecture]] - Catégories de solutions de sécurité d'entreprise et leur mise en œuvre : EDR (Endpoint Detection and Response)
    - [[security-telemetry]] - Date : 2026-04-03 Contexte : application de bureau avec serveur de licences en ligne
    - [[social-engineering-and-phishing]] - Vecteurs d'attaque ciblant l'humain : hameçonnage (spear, whaling, vishing), prétexting, usurpation d'e-mail
    - [[tamper-resistant-counters]] - Date : 2026-04-03 Contexte : C++, Windows + macOS
    - [[threat-modeling]] - Processus systématique d'identification, d'évaluation et de documentation des menaces potentielles pour un
    - [[tls-fingerprinting-and-network-identifiers]] - Techniques d'identification au niveau réseau : classification et réputation des adresses IP, géolocalisation
    - [[vulnerability-scanning-and-management]] - Gestion du cycle de vie des vulnérabilités : analyse avec Nessus et OpenVAS, scoring CVE/CVSS
    - [[watermarking-encrypted-models]] - Date : 2026-04-03 Contexte : application de retouche de bureau C++
    - [[web-server-security]] - Configuration sécurisée des serveurs web : hôtes virtuels Apache et Nginx, mise en place de TLS/SSL avec Let's
    - [[windows-security-and-powershell]] - Internes de sécurité Windows : stockage des identifiants (SAM, LSASS), PowerShell pour les opérations de sécurité

---

<div id="algorithms"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#80a0d0,#305080);box-shadow:0 0 8px rgba(128,160,208,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Algorithmes et structures de données · 33 articles"

    - [[complexity-analysis]] - Notation de Landau (grand O), complexité en temps et en espace
    - [[amortized-analysis]] - Coût moyen par opération
    - [[sorting-algorithms]] - Comparaison de tous les tris avec code
    - [[searching-algorithms]] - Recherche dichotomique, recherche de motifs KMP
    - [[dynamic-programming-fundamentals]] - Mémoïsation vs tabulation
    - [[graph-traversal-bfs-dfs]] - DFS, BFS, problèmes sur grille
    - [[shortest-path-algorithms]] - Dijkstra, Bellman-Ford, Floyd-Warshall
    - [[trees-and-binary-trees]] - Parcours d'arbres, opérations sur les ABR
    - [[hash-tables]] - Fonctions de hachage, gestion des collisions
    - [[heap-priority-queue]] - Tas binaire, file de priorité
    - [[union-find]] - Union-find (ensembles disjoints), compression de chemin

    **Plus**

    - [[backtracking]] - Exploration systématique de l'espace des solutions en construisant des candidats progressivement et en abandonnant
    - [[bit-manipulation]] - Opérations sur les bits individuels des entiers
    - [[complexity-classes]] - Les classes de complexité regroupent les problèmes de décision selon les ressources de calcul nécessaires pour les résoudre ou
    - [[data-structures-fundamentals]] - Opérations de base sur les structures de données et analyse de complexité - tableaux, tableaux triés avec recherche dichotomique
    - [[dp-grid-problems]] - Problèmes de programmation dynamique sur grille et combinatoires : problème de partition, plus grand carré, comptage de voyelles triées
    - [[dp-optimization-problems]] - Problèmes classiques d'optimisation par programmation dynamique : voleur de maisons, rendu de monnaie, sac à dos 0-1, somme de sous-ensembles, découpe de barre
    - [[dp-sequence-problems]] - Programmation dynamique sur séquences et chaînes : plus longue sous-séquence commune (LCS), distance d'édition
    - [[dynamic-programming]] - Fondements de la récursivité, mémoïsation (top-down), tabulation bottom-up et reconnaissance de la programmation dynamique
    - [[eulerian-hamiltonian-paths]] - Les chemins eulériens visitent chaque ARÊTE exactement une fois
    - [[graph-coloring]] - La coloration de graphe attribue des couleurs aux sommets de sorte que deux sommets adjacents ne partagent jamais la même couleur
    - [[graph-representation]] - Les graphes peuvent être représentés par des listes d'arêtes, des listes d'adjacence ou des matrices d'adjacence
    - [[greedy-algorithms]] - Construire des solutions progressivement en faisant à chaque étape le choix localement optimal
    - [[minimum-spanning-trees]] - Un arbre couvrant minimal (MST) d'un graphe non orienté connexe pondéré est un arbre couvrant avec
    - [[network-flow]] - Les algorithmes de flot dans un réseau trouvent le flot maximal réalisable de la source vers le puits dans un graphe orienté pondéré
    - [[problem-patterns]] - Approche systématique des problèmes algorithmiques - le processus d'entretien en 7 étapes, motifs courants
    - [[recursion-fundamentals]] - Fonction qui s'appelle elle-même pour résoudre des instances plus petites du même problème
    - [[sliding-window]] - Maintenir une fenêtre (sous-tableau/sous-chaîne contigu) qui glisse sur l'entrée, en s'étendant et se rétrécissant
    - [[string-algorithms]] - Algorithmes de recherche, de correspondance et de manipulation de chaînes
    - [[topological-sort]] - Un ordre topologique d'un DAG (graphe orienté acyclique) est un ordre linéaire des sommets tel que
    - [[traveling-salesman-problem]] - Trouver le trajet le plus court qui visite chaque ville exactement une fois et revient à l'origine
    - [[trees-and-graphs]] - Arbres binaires de recherche, tas/files de priorité, tries (arbres de préfixes), représentation de graphes et
    - [[two-pointer-technique]] - La technique des deux pointeurs utilise deux indices pour parcourir des structures de données (généralement des tableaux), réduisant

---

<div id="image-generation"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#c8a058,#785018);box-shadow:0 0 8px rgba(200,160,88,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Génération d'images · 79 articles"

    - [ACE++](../image-generation/ACE++.md) - ACE++ permet la création et l'édition d'images guidées par des références, via des workflows LoRA spécifiques à chaque tâche et un modèle FFT généraliste ; utilisez l'appariement de modèle de base publié et vérifiez ses conditions d'utilisation.
    - [[ATI]] - ATI ajoute un contrôle du mouvement par trajectoires (objet, zone locale et caméra) à son workflow image-vers-vidéo basé sur Wan2.1 ; conservez les limites publiées concernant le modèle, le checkpoint et l'éditeur en localhost.
    - [[flow-matching]] - Le flow matching entraîne un champ vectoriel continu le long d'un chemin de probabilité choisi ; le scheduler, le chemin et les paramètres d'inférence sont propres à chaque checkpoint et ne constituent pas des valeurs par défaut universelles de la diffusion.
    - [[flux-kontext]] - Génération d'images tenant compte du contexte
    - [[LaMa]] - LaMa est un modèle d'inpainting à convolutions de Fourier, adapté aux masques de grande taille et à la généralisation en résolution ; utilisez-le avec un checkpoint compatible et testez séparément la continuité des textures par rapport à la restauration sémantique d'objets.
    - [[lora-fine-tuning-for-editing-models]] - Un LoRA d'édition n'est compatible qu'avec son checkpoint de base exact, son architecture, son runtime et son format d'adaptateur ; entraînez-le à partir de paires de données autorisées, explorez la capacité et le calendrier d'entraînement sur des éditions tenues à l'écart, et prouvez à la fois le changement demandé et la préservation du reste avant toute mise en production.
    - [[MARBLE]] - MARBLE réalise le transfert de matériaux, le mélange et les modifications paramétriques de matériaux via des contrôles dans l'espace CLIP sur un générateur d'images pré-entraîné ; validez la géométrie des objets, l'éclairage et les licences des artefacts pour chaque workflow.
    - [[MMDiT]] - MMDiT est le patron de transformeur multimodal de Stable Diffusion 3 : des représentations propres à chaque modalité participent à une attention conjointe ; les API d'implémentation et les noms de cibles LoRA varient selon la révision du modèle.
    - [[SANA]] - Architecture efficace de génération d'images à partir de texte
    - [[tiled-inference]] - L'inférence par tuiles est une stratégie haute résolution liée au modèle ; le partitionnement, le recouvrement, le mélange, le contexte global, la correspondance des coordonnées et la revue des sorties doivent être évalués ensemble sur le pipeline épinglé, tandis que les tuiles de détection et les tuiles génératives ou de retouche restent des contrats distincts.
    - [[transformers-v5]] - Transformers v5 déplace la conversion des checkpoints dans le chargeur, mais chaque intégration doit être épinglée à une version installée, à un contrat de runtime, à un checkpoint et à un test d'adaptateur ; les API de la branche principale actuelle ne garantissent pas une compatibilité universelle.

    **Plus**

    - [[anatomy-correction-diffusion]] - La correction d'anatomie est un workflow diagnostiquer-masquer-conditionner-inpaint ; utilisez des méthodes de recherche tenant compte de la géométrie et des outils d'édition adaptés au modèle, puis vérifiez visuellement chaque main ou membre modifié par rapport à la source.
    - [[block-causal-linear-attention]] - L'attention linéaire causale par blocs est le mécanisme entraîné de SANA-Video pour la vidéo longue, avec un état d'attention cumulatif de taille fixe ; ce n'est pas un module interchangeable pour un pavage d'images arbitraire ni pour des DiT quelconques.
    - [[Calligrapher]] - Calligrapher personnalise des images de texte à partir de références de style via FLUX.1-Fill-dev, SigLIP, des masques et des poids de projet ; traitez l'exactitude typographique et la licence comme des critères d'acceptation distincts.
    - [[color-checker-and-white-balance]] - La correction par mire de couleurs et balance des blancs exige une mire physique mesurée ou un estimateur validé séparément ; la sortie d'un détecteur et une mire générée ne constituent pas une vérité terrain colorimétrique.
    - [[color-correction-by-numbers]] - La correction des couleurs n'est valide que par rapport à une cible de mesure déclarée, un illuminant, une caméra ou un profil, un espace de travail et une transformation de visualisation ; les échantillons neutres et les patches de mire sont des preuves lorsque leur provenance est connue, alors que les moyennes de scène et les rapports de couleur de peau ne sont pas une vérité universelle.
    - [[color-space-and-gamma-reference]] - La gestion des couleurs est une chaîne versionnée : interprétation de l'entrée, espace de travail, transformations créatives, transformation d'affichage ou de visualisation, puis encodage de sortie ; les étiquettes de caméra ou de conteneur et les règles génériques de gamma sont insuffisantes sans le profil exact, la version de transformation, la politique de métadonnées et l'écran de validation.
    - [[color-theory-for-ml]] - Les recommandations de couleur pour le ML constituent un contrat de représentation et de preuve propre à la tâche : précisez l'encodage source, les hypothèses d'illuminant ou de visualisation, la transformation cible, l'intention de palette et l'objectif de revue humaine ; l'harmonie artistique, les étiquettes spectrales et les associations psychologiques sont des hypothèses, et non des étiquettes universelles ou des contrôles de modèle.
    - [[comfyui-flux2klein-enhancer]] - Référence de workflow épinglé pour le conditionnement par référence et l'amélioration d'identité et de détails avec FLUX.2
    - [[comfyui-sensenova-u1]] - Référence tenant compte des limites pour les artefacts officiels SenseNova U1/U1.5, les nœuds ComfyUI officiels et le
    - [[comfyui-wan-vace-video-joiner]] - La jonction vidéo ComfyUI Wan VACE est un workflow communautaire lié à une version, et non un nœud de transition générique ; épinglez sa révision de workflow, ses dépendances ComfyUI, nœuds personnalisés et modèles, les contrats d'entrée (images, horodatages, couleurs), la politique de pont généré et de boucle, les artefacts intermédiaires, ainsi qu'une revue visuelle et audio avant de publier un clip assemblé.
    - [[DC-AE]] - Utilisez DC-AE uniquement avec un modèle de diffusion et un contrat latent pour lesquels il a été entraîné ; une forte compression réduit le travail sur les tokens latents, mais ne en fait pas un remplacement direct de VAE.
    - [[defect-detection-small-objects]] - La détection de défauts et de petits objets produit des candidats soumis à revue, et non une vérité automatique de qualité ; liez le modèle, le protocole de capture, la politique d'annotation ou de référence normale, le découpage ou la correspondance de fusion, les seuils et une évaluation disjointe par source avant toute décision d'inspection ou de workflow.
    - [[denoise-architectures-2026]] - Une architecture de débruitage se choisit en fonction d'une cible de dégradation et de fidélité déclarée, et non d'un classement ou d'un nom de famille ; liez les hypothèses de capture et de bruit, le modèle et le checkpoint, le chemin de prétraitement, de tuilage et de couleur, les découpages autorisés entraînement/évaluation, les métriques de tâche et de préservation, ainsi qu'une revue visuelle avant d'accepter des détails générés ou restaurés.
    - [[diffusion-distillation-cdm]] - La Continuous-Time Distribution Matching (CDM) est une méthode de recherche pour la distillation de diffusion en peu d'étapes, et non un simple interrupteur de vitesse ; liez l'article, le code, le checkpoint et sa licence, la paramétrisation et le calendrier enseignant/élève, le runtime d'entraînement et distribué, une évaluation qualité, diversité et préservation disjointe par source, et des éléments de service prêts pour un retour arrière avant toute utilisation.
    - [[diffusion-inference-acceleration]] - L'accélération de la diffusion est un compromis propre au modèle et au runtime ; mesurez la latence à chaud et en régime établi, la mémoire, la fidélité des sorties et la reproductibilité pour le checkpoint et le workflow exacts.
    - [[diffusion-lora-training]] - L'entraînement LoRA de diffusion est une expérience d'adaptateur liée à une version ; liez le checkpoint de base exact, l'architecture, le runtime, le format d'adaptateur, les données autorisées et le découpage d'évaluation, et ne choisissez le rang, le calendrier, les cibles et l'optimiseur qu'à partir du comportement mesuré sur des données tenues à l'écart, et non à partir de recettes copiées.
    - [[edge-softness-and-compositing]] - Mesurez le contour au lieu de le choisir : largeur de transition 10-90 %, ajustement robuste du contour
    - [[face-beautify-edit-lora]] - Un LoRA d'édition de visage est une tâche d'entraînement d'édition locale appariée et respectueuse du consentement ; liez l'adaptateur à son modèle de base exact et validez la correction demandée séparément de la préservation de l'identité.
    - [[face-detection-filtering-pipeline]] - Le filtrage des visages est un pipeline de sélection de candidats préservant la provenance ; les boîtes et points de repère du détecteur facilitent la revue, mais n'établissent ni l'identité, ni le consentement, ni le réalisme de l'image, ni son aptitude à l'entraînement.
    - [[FLAIR]] - FLAIR est un cadre d'échantillonnage a posteriori basé sur les flux, sans entraînement, pour l'imagerie inverse ; utilisez sa configuration publiée et vérifiez la fidélité, la cohérence avec les données observées et les conditions du modèle de base sur la tâche visée.
    - [[flowinone-unified-multimodal-generation-via-image-flow]] - FlowInOne est une version de recherche pour le flow matching image-vers-image guidé par prompt visuel ; liez l'article exact, le checkpoint, le code et le runtime, la licence, le contrat de tâche et de rendu d'entrée, ainsi qu'une évaluation de tâche et de préservation disjointe par source, et ne généralisez pas les résultats des articles en capacité de production ni en affirmation d'usage commercial.
    - [[flux-attention-manipulation]] - Les interventions sur l'attention dans les DiT de la famille FLUX dépendent de la recherche et de l'implémentation ; utilisez le chemin d'attention exposé par le modèle exact, préservez son contrat de conditionnement et validez la composition, plutôt que de traiter les cartes comme une preuve causale.
    - [[flux-klein-9b-architecture]] - Les affirmations sur l'architecture de FLUX.2 [klein] doivent être liées à la version officielle nommée et à son artefact ; la famille publique prend en charge la génération à partir de texte et l'édition par référence, mais les agencements internes de blocs, le câblage des encodeurs, la quantification et la compatibilité des adaptateurs ne peuvent pas être déduits d'une variante ou d'un runtime à l'autre.
    - [[flux-klein-9b-inference]] - L'inférence de FLUX.2 [klein] 9B doit suivre la variante de modèle, le checkpoint, le scheduler et la licence publiés ; mesurez le workflow exact de texte ou d'édition au lieu de reprendre des règles génériques de sampler, de VRAM ou de LoRA.
    - [[flux-klein-capability-map]] - Une capacité de FLUX.2 [klein] n'est utilisable que lorsque la variante exacte, le checkpoint, la licence, le runtime ou l'endpoint du fournisseur, le contrat d'entrée et la revue de sortie sont attestés au moment de l'exécution ; le support de génération et d'édition au niveau de la famille n'autorise pas chaque adaptateur, service, usage commercial ou résultat d'édition.
    - [[flux-klein-character-lora]] - Un LoRA d'identité est un adaptateur sensible, lié à une version, entraîné uniquement à partir d'images autorisées pour un objectif défini ; liez le consentement, le checkpoint de base et le format d'adaptateur, la politique de données et de suppression, ainsi qu'une revue de ressemblance et de préservation disjointe par source, et ne considérez jamais une correspondance d'identité générée comme une identité vérifiée.
    - [[flux-klein-jewelry-photography]] - L'imagerie de bijoux est un workflow produit à source contrôlée : préservez l'actif approuvé, les preuves de matière et de géométrie, le pipeline colorimétrique et les limites de droits, puis ne publiez qu'après un contrôle qualité visuel et factuel.
    - [[flux-klein-style-lora-system]] - Un LoRA de style FLUX.2 [klein] est un workflow de données et d'évaluation lié à une version ; séparez les données de style de celles de sujet, préservez les droits et la provenance, et validez le transfert sur du contenu tenu à l'écart.
    - [[fp8-quantization-optimization-for-e4m3]] - La quantification FP8 E4M3 est un contrat numérique propre à la version et au backend ; liez le format des tenseurs, la recette de mise à l'échelle, les opérations et le matériel pris en charge, les preuves de calibration ou d'amax, le chemin de sérialisation et d'exécution, ainsi que les mesures de qualité, latence et mémoire, et ne remplacez jamais silencieusement par un écrêtage ou un autre format.
    - [[frequency-decomposition-editing]] - La décomposition fréquentielle est une transformation déclarée, et non une carte d'édition sémantique ; consignez le domaine colorimétrique, la transformation ou le filtre, la politique de bord et de reconstruction, les masques d'édition et la revue des sorties, et distinguez le signal reconstruit mathématiquement des détails générés ou visuellement plausibles.
    - [[grayscale-overlay-nn-architectures]] - La prédiction de superposition en niveaux de gris est une tâche de retouche appariée et alignée au pixel près ; préservez le contrat de mélange et la base de référence sans modification, liez chaque paire source/cible et chaque masque, et évaluez l'image composite ainsi que la carte avant de publier un ajustement automatisé.
    - [[image-restoration-survey]] - La restauration d'image doit déclarer la dégradation et la cible de fidélité ; choisissez une méthode déterministe ou de diffusion compatible avec la tâche, puis validez la récupération mesurée séparément des détails plausibles mais inventés.
    - [[in-context-segmentation]] - La segmentation en contexte transfère un masque de référence fourni via un modèle de vision nommé ; sa sortie est un masque candidat, et non une vérité terrain, et nécessite la provenance de la référence, une revue de la cible, la gestion de l'incertitude et une validation disjointe par source.
    - [[in-context-segmentation-with-insid3-and-dinov3]] - INSID3 avec DINOv3 transfère un masque de référence fourni via une version nommée de backbone gelé, sous forme de segmentation candidate et non de vérité terrain ; liez les révisions du dépôt et du modèle, la licence et l'accès, la provenance des références et des masques, le prétraitement et la résolution, la configuration du biais positionnel, la politique d'incertitude et une revue disjointe par source avant utilisation.
    - [[intrinsic-decomposition]] - La décomposition intrinsèque est une estimation de la réflectance et de l'éclairage bornée par l'ambiguïté, et non une vérité terrain ; liez les hypothèses de formation de l'image, le modèle et sa version, le domaine colorimétrique, la politique de résidu, les preuves sources et une revue propre à la tâche avant d'utiliser ses sorties d'albédo ou d'ombrage pour l'édition ou le relighting.
    - [[krea-2-anygles]] - Krea 2 Anygles recalcule une personne nette sous un nouveau lacet, une nouvelle élévation ou une nouvelle distance de caméra, via un Control-LoRA piloté par une carte de normales SAM 3D Body ; il nécessite son propre chargeur et une étape de préparation isolée et contrôlée.
    - [[krea-2-prompting]] - Les poids ouverts de Krea 2 lisent un paragraphe unique en anglais, avec le médium placé tôt et la lumière décrite ; convertissez le guidage (cfg ComfyUI = 1 + g de Krea), ne vous attendez à aucun prompt négatif sur Turbo, restez sous 507 tokens et utilisez des prompts propres à chaque adaptateur pour les éditions et les mises en page par boîtes.
    - [[lora-auxiliary-losses]] - Les pertes auxiliaires LoRA sont des objectifs propres à chaque expérience, et non une recette portable ; liez le modèle de base, le format d'adaptateur, les droits sur les données, l'implémentation de la perte, la plage de recherche des pondérations, le découpage de validation et l'évaluation de tâche et de préservation, et traitez les pertes d'identité ou de masque comme des contrôles sensibles, et non comme une preuve de ressemblance.
    - [[lora-identity-disentanglement-in-flux2-klein-9b]] - Un LoRA d'identité FLUX.2 [klein] 9B est une expérience d'adaptateur liée à une version, aux données et aux droits ; liez la version officielle de base et ses conditions, le format d'adaptateur et de runtime, les références d'identité autorisées, la politique de labels, de légendes et de préservation, une évaluation de l'identité et des cas non ciblés disjointe par source, ainsi qu'une revue avant tout usage.
    - [[low-vram-inference-strategies]] - L'inférence en faible VRAM est une configuration d'exécution mesurée, et non une promesse liée à une catégorie de matériel ; épinglez le modèle et le backend, ne sélectionnez que les chemins de quantification, de déchargement ou de tuilage documentés, et consignez le pic de mémoire, la latence, la fidélité des sorties et le comportement en cas d'échec sur le périphérique réel.
    - [[MACRO]] - MACRO est un jeu de données structuré à références multiples, un benchmark et un ensemble d'actifs de fine-tuning spécifiques à des modèles ; validez le modèle de base compatible et les conditions des artefacts avant tout déploiement.
    - [[megastyle-flux-style-transfer]] - MegaStyle est une publication de recherche (code, modèle et jeu de données) pour le transfert de style d'image ; liez la révision exacte du dépôt ou de l'artefact et sa licence, la dépendance au modèle de base et au runtime, la provenance des références et des prompts, le contrat de rendu et de sortie, une évaluation disjointe par source du style, du contenu et de la préservation, ainsi qu'une revue humaine avant de publier ou d'entraîner sur les résultats.
    - [[object-removal-inpainting]] - La suppression d'objet est une modification contrainte : liez l'actif source, l'objet autorisé, le masque, le contrat du modèle et les zones protégées, puis validez la continuité de la scène et la préservation des éléments factuels avant publication.
    - [[paired-training-for-restoration]] - L'entraînement à la restauration appariée apprend une correspondance déclarée entre dégradé et cible ; il nécessite des paires alignées sur la source et dont les droits sont purgés, un chemin de conditionnement compatible avec le modèle, des jeux de validation séparés par source, et une évaluation qui distingue la récupération mesurée de l'invention plausible.
    - [[perspective-calibration-for-compositing]] - Un cadre de décision local pour estimer la géométrie de la caméra, la valider à l'aide d'indices de la scène, et
    - [[pixel-art-generation]] - La génération de pixel art est un workflow d'actifs contraint, et non un simple prompt de style ; liez la grille logique, la palette, le contrat alpha et d'animation ou de sprite, la provenance et les droits d'entraînement, la version de l'outil de modèle ou de rendu raster, le chemin d'export déterministe et la revue humaine de la lisibilité, de la géométrie et des détails factuels avant livraison.
    - [[PixelSmile]] - PixelSmile est un projet d'édition d'expressions faciales lié à une version publiée ; épinglez son aperçu humain publié, le modèle de base, le runtime patché, l'image source consentie et la revue d'expression, plutôt que de considérer les chiffres de benchmark ou les adaptateurs comme des garanties générales.
    - [[plugin-inference-ux]] - L'UX d'inférence de plugin ML est un contrat explicite entre l'hôte et l'état de la tâche : épinglez l'API de l'hôte, documentez les versions du snapshot et des modèles, le comportement d'annulation et de progression, les clés de cache et d'invalidation, la provenance des aperçus, la validation non destructive et la latence mesurée, plutôt que de promettre une réactivité universelle.
    - [[qwen-image]] - Référence tenant compte des versions pour la génération et l'édition Qwen-Image, les checkpoints 2511/2512 et le
    - [[RealRestorer]] - RealRestorer est un workflow de restauration à partir d'un grand modèle d'édition d'image, couvrant neuf types de dégradation documentés ; utilisez le runtime local patché du dépôt et évaluez la fidélité séparément des scores de benchmark.
    - [[recurrent-depth-transformer]] - Les transformeurs à profondeur récurrente réutilisent un bloc partagé propre à une version à travers les itérations ; liez l'architecture publiée, le checkpoint et le runtime, le budget de récurrence, le comportement de cache et de terminaison, ainsi que le rapport qualité/coût mesuré, et ne déduisez pas le raisonnement latent, la sortie anticipée, la stabilité ou la capacité de déploiement à partir du nom de la famille.
    - [[retouch-patch-harmonization]] - Une conception de données d'entraînement pour l'inpainting de défauts qui préserve le domaine colorimétrique de l'image cible propre
    - [[rights-first-text-to-mask-training]] - Un contrat d'entraînement et d'évaluation à contrôle de provenance pour les requêtes textuelles en russe, l'ancrage visuel
    - [[sana-denoiser-architecture]] - Un restaurateur basé sur SANA est une proposition de recherche, et non un pipeline implémenté ; il nécessite un conditionnement compatible avec le modèle, des bases de référence sur données appariées, une évaluation de fidélité et des tests séparés en haute résolution avant déploiement.
    - [[segmentation-dataset-preparation]] - La préparation d'un jeu de données de segmentation est un contrat de provenance et de supervision : liez la source et les droits, la politique d'annotation et la sémantique des masques, les découpages disjoints par groupe, le comportement d'augmentation et d'interpolation, la couverture des classes et les métriques de publication, et échouez en fermé en cas de fuite, de labels non relus ou de cibles incompatibles.
    - [[skin-retouch-pipeline]] - La retouche de la peau est un workflow de correction à portée limitée, respectueux du consentement ; préservez l'identité, la texture et les traits protégés, rendez chaque masque et chaque modification auditables, et exigez la revue de toute la peau modifiée.
    - [[spatialedit-16b-geometric-control-for-diffusion-based-image-editing]] - SpatialEdit-16B est une version de recherche pour l'édition d'images pilotée par la géométrie ; liez l'artefact exact de code et de modèle et ses conditions, l'autorité sur les actifs source et cible, le contrat de transformation des objets et de la caméra et des coordonnées, le prétraitement et le runtime, l'évaluation prenant en compte la géométrie et la préservation, ainsi qu'une revue humaine avant usage.
    - [[Step1X-Edit]] - Step1X-Edit est une famille multimodale d'édition d'images de StepFun avec des pipelines propres à chaque version ; associez chaque checkpoint à sa branche Diffusers documentée et vérifiez indépendamment les conditions du modèle et de l'artefact.
    - [[style-reference-ux]] - L'UX des références de style doit séparer l'influence temporaire de l'entraînement sauvegardé, le style du contenu et de la structure, et les données locales du traitement par des tiers, tout en rendant visibles pour l'utilisateur l'intensité et la provenance.
    - [[synthetic-dataset-pipeline]] - Les données de détection synthétiques forment un corpus candidat étiqueté, et non une vérité terrain automatique ; préservez la provenance du générateur et des sources, relisez les annotations, empêchez les fuites entre découpages et validez sur des données réelles tenues à l'écart.
    - [[temporal-tiling]] - Le tuilage temporel est une expérience de recherche propre à un modèle, visant la cohérence entre tuiles, et non une simple réutilisation de la mémoire vidéo ; liez le plan de tuilage et l'état du runtime, comparez à une base de recouvrement, et validez les coutures, la composition et le coût sur des images tenues à l'écart.
    - [[Text-to-LoRA]] - Text-to-LoRA est un hypernetwork de Sakana AI qui crée des adaptateurs de tâche pour des familles de LLM cibles documentées à partir de descriptions textuelles de tâches ; ce n'est pas un générateur interchangeable de LoRA pour modèles de diffusion.
    - [[textual-latent-interpolation]] - L'interpolation latente textuelle est une expérience de conditionnement propre à un modèle : préservez les entrées non ciblées, liez-la à un encodeur et un adaptateur exacts, balayez la plage demandée et prouvez la contrôlabilité et la préservation au lieu de supposer une linéarité sémantique.
    - [[tile-position-encoding]] - L'encodage de position des tuiles est un contrat spatial propre à un modèle, et non une recette de canal universelle ; liez le repère de coordonnées de l'image complète, la politique de recadrage, de recouvrement et de remplissage, la famille d'encodage et le point d'injection, la version du modèle et la distribution d'entraînement, ainsi qu'une évaluation des coutures et de la géométrie avant de considérer les sorties tuilées comme globalement cohérentes.
    - [[upscaler-evaluation]] - Choisissez un upscaler selon la fidélité mesurée sur la classe de source réelle, et non selon des étiquettes de benchmark ou une valeur par défaut universelle ; préservez la provenance des sources et des sorties, évaluez les artefacts et les détails factuels, et gardez les sorties génératives hors des cibles factuelles d'entraînement.
    - [[videomama-diffusion-based-video-matting]] - VideoMaMa est une version de recherche de détourage vidéo guidé par masque ; liez le code exact, le checkpoint, les conditions du modèle vidéo de base et de la licence, la provenance autorisée de la vidéo source et du masque grossier, le contrat frame/alpha/export, une évaluation temporelle et des bords disjointe par source, ainsi qu'une revue humaine avant publication ou composition des sorties.
    - [[watermark-removal]] - La restauration de filigrane visible n'est permise que pour les éléments que l'opérateur est autorisé à modifier ; liez la propriété ou l'autorisation écrite, l'actif source et le type de superposition, les versions de détection/masque et de restauration, les zones protégées et la gestion de la provenance, la divulgation des sorties et la revue humaine, et ne considérez jamais une reconstruction plausible comme un contenu original récupéré.
    - [[X-Dub]] - X-Dub est une version publique de doublage visuel basée sur Wan2.2-TI2V-5B ; validez le recadrage à une seule personne, l'identité, la stabilité temporelle, les droits audio et les conditions du modèle sur chaque vidéo cible.

---

<div id="cpp"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#7090c0,#304070);box-shadow:0 0 8px rgba(112,144,192,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>C++ · 29 articles"

    - [[cmake-build-systems]] - CMake, configuration de la compilation
    - [Smart Pointers and Memory Management](../cpp/smart-pointers.md) - unique_ptr, shared_ptr, weak_ptr
    - [[move-semantics]] - Références rvalue, std::move
    - [[raii-resource-management]] - Patron RAII, sécurité des ressources
    - [[templates-and-concepts]] - Métaprogrammation par templates
    - [[stl-containers]] - vector, map, set, unordered_map
    - [[stl-algorithms]] - std::sort, std::find, ranges
    - [Concurrency - Threads, Async, Atomics](../cpp/concurrency.md) - std::thread, mutex, atomic
    - [Error Handling - Exceptions and Alternatives](../cpp/error-handling.md) - Exceptions, std::expected
    - [[lambda-expressions]] - Syntaxe des lambdas, captures
    - [[modern-cpp-features]] - Fonctionnalités de C++17/20/23

    **Plus**

    - [[concepts-and-constraints]] - Exigences nommées sur les paramètres de template, remplaçant SFINAE par une écriture lisible et vérifiée par le compilateur
    - [[const-and-type-safety]] - const exprime l'intention, prévient les mutations accidentelles et permet les optimisations du compilateur
    - [[coroutines]] - Multitâche coopératif avec co_yield, co_return et co_await pour les générateurs paresseux et les E/S asynchrones
    - [[cross-platform-cpp-desktop-app]] - Référence sur les différences de plateforme lors de la création d'applications de bureau C++ (avec inférence ML) ciblant
    - [[cross-platform-ml-inference]] - Référence pour la création d'applications de bureau C++ avec inférence ML ciblant à la fois Windows et macOS
    - [[design-patterns-cpp]] - Patrons GoF classiques adaptés au C++ moderne avec templates, pointeurs intelligents, lambdas et sémantique de valeur
    - [[external-heartbeat-monitoring-for-native-process-crashes]] - Les gestionnaires d'exceptions en cours de processus échouent souvent à capturer les plantages « silencieux » causés par des erreurs bas niveau
    - [[file-io-streams]] - E/S par flux (<fstream>, <iostream>) et opérations sur le système de fichiers (<filesystem>)
    - [[function-pointers-and-callbacks]] - Pointeurs de fonction de style C, std::function et lambdas pour l'invocation indirecte et les patrons de callback
    - [[inheritance-and-polymorphism]] - Polymorphisme à l'exécution via fonctions virtuelles et hiérarchies d'héritage
    - [[manual-memory-management]] - new/delete bruts, pile vs tas, et les trois modes de défaillance qui motivent les pointeurs intelligents et RAII
    - [[object-lifetime]] - Construction, destruction et formes d'initialisation des objets, et élision de copie
    - [[operator-overloading]] - Définir un comportement personnalisé pour les opérateurs sur des types définis par l'utilisateur
    - [Performance Optimization](../cpp/performance-optimization.md) - Fondamentaux de performance en C++ : efficacité du cache, sémantique de déplacement, stratégies d'allocation, compilateur
    - [[ranges-and-views]] - Pipelines paresseux composables pour le traitement de séquences avec l'opérateur pipe et les adaptateurs de ranges
    - [[scope-and-lifetime]] - Règles de portée au niveau bloc, masquage de noms et ordre de destruction déterministe, prérequis pour
    - [[string-handling]] - std::string, std::string_view, formatage, conversion et recherche
    - [[winhttp-async-client]] - Notifications de fin vs de progression, attentes bornées et sémantique d'annulation pour WinHTTP dans

---

<div id="java-spring"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#68b080,#286038);box-shadow:0 0 8px rgba(104,176,128,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Java et Spring · 25 articles"

    - [[java-type-system-fundamentals]] - Types primitifs, génériques, records
    - [[kotlin-language-features]] - Kotlin pour les développeurs JVM
    - [[spring-boot-configuration]] - Propriétés, profils, auto-configuration
    - [[spring-data-jpa-hibernate]] - Entités JPA, repositories, requêtes
    - [[spring-security]] - Authentification, autorisation, filtres
    - [[spring-mvc-rest]] - Contrôleurs REST, gestion des erreurs
    - [[android-fundamentals-ui]] - Bases de l'interface Android
    - [[android-architecture-mvvm]] - MVVM, ViewModel, LiveData

    **Plus**

    - [[algorithms-data-structures]] - Algorithmes fondamentaux (tri, recherche), structures de données de base (pile, file, liste chaînée, arbre
    - [[android-activity-lifecycle]] - Callbacks du cycle de vie d'Activity, Intents explicites et implicites, transmission de données entre Activities
    - [[android-data-storage]] - Persistance locale des données sur Android : SharedPreferences pour les paramètres, SQLite brut, ORM Room
    - [[android-dependency-injection]] - Hilt (basé sur Dagger) comme framework d'injection de dépendances recommandé pour Android
    - [[android-firebase]] - Intégration de Firebase pour Android : Authentication (email/mot de passe), Cloud Firestore (NoSQL
    - [[android-fragments-navigation]] - Cycle de vie des Fragments, communication entre Fragments via un ViewModel partagé, Jetpack Navigation Component, Safe
    - [[android-jetpack-compose]] - Boîte à outils déclarative moderne d'Android : fonctions composables, gestion d'état, mise en page
    - [[android-networking-retrofit]] - Réseau HTTP sous Android avec Retrofit (client HTTP typé), OkHttp, sérialisation Gson
    - [[android-recyclerview]] - RecyclerView pour les listes défilantes efficaces, patron Adapter/ViewHolder, LayoutManagers, DiffUtil
    - [[database-migrations]] - Évolution du schéma de base de données contrôlée et versionnée avec Flyway (basé sur SQL) et Liquibase
    - [[java-collections-streams]] - Hiérarchie du Java Collections Framework, choix de la bonne collection et traitement de données de style fonctionnel
    - [[java-concurrency]] - Modèle de threads Java, primitives de synchronisation, pools de threads, CompletableFuture et concurrent
    - [[kotlin-coroutines]] - Coroutines Kotlin pour la programmation asynchrone : fonctions suspend, dispatchers, scopes, structured
    - [[spring-data-access-evolution]] - Évolution de l'accès aux données dans Spring : JDBC brut -> PreparedStatement -> JdbcTemplate ->
    - [[spring-ioc-beans]] - Principe d'inversion de contrôle (IoC), types d'injection de dépendances, portées des beans, callbacks de cycle de vie
    - [[spring-nosql-databases]] - Abstractions Spring Data pour les bases NoSQL : Cassandra (familles de colonnes), MongoDB (documents), Redis
    - [[spring-validation]] - Annotations Bean Validation (Jakarta Validation), patron DTO pour séparer les modèles de domaine des

---

<div id="bi-analytics"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#70a0b0,#205060);box-shadow:0 0 8px rgba(112,160,176,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>BI et analytique · 23 articles"

    - [[product-analytics-fundamentals]] - Cadres d'analyse produit
    - [[product-metrics-framework]] - North Star, AARRR, KPI
    - [[tableau-fundamentals]] - Feuilles de calcul, tableaux de bord, sources de données
    - [[tableau-calculations]] - Champs calculés, calculs de tableau
    - [[powerbi-fundamentals]] - Rapports Power BI, bases de DAX
    - [[dashboard-design-patterns]] - Mise en page des tableaux de bord, principes UX
    - [[sql-for-analytics]] - Modèles SQL analytiques
    - [[web-marketing-analytics]] - GA4, UTM, modèles d'attribution

    **Plus**

    - [[app-store-optimization]] - L'ASO est l'optimisation du référencement naturel dans les boutiques d'applications : l'objectif est d'apparaître dans les premiers résultats pour
    - [[bi-development-process]] - Le processus de développement BI couvre le cycle de vie complet, depuis le recueil des besoins jusqu'à
    - [[bi-tools-comparison]] - Comparaison des principales plateformes BI, dont Tableau, Power BI, Apache Superset, DataLens (Yandex)
    - [[cohort-retention-analysis]] - L'analyse de cohortes regroupe les utilisateurs selon une caractéristique commune à un instant donné et suit leur
    - [[color-theory-visualization]] - La couleur est l'un des attributs d'encodage les plus puissants et les plus souvent mal utilisés dans les données
    - [[funnel-analysis]] - L'analyse de tunnel visualise et mesure la progression des utilisateurs dans un parcours en plusieurs étapes vers un
    - [[mobile-analytics-platforms]] - Les plateformes d'analyse mobile collectent les données comportementales des utilisateurs d'applications mobiles via l'intégration de SDK
    - [[mobile-attribution-fraud]] - L'attribution mobile détermine quelle source publicitaire (campagne, réseau, créatif) a provoqué chaque installation d'application
    - [[pandas-data-analysis]] - pandas est la bibliothèque Python de référence pour la manipulation et l'analyse de données tabulaires
    - [[powerbi-advanced-features]] - Fonctionnalités avancées de Power BI, dont les thèmes personnalisés, les visuels d'AppSource et les paramètres What-If
    - [[python-for-analytics]] - Bases de Python pour les analystes de données : syntaxe de base, NumPy pour les opérations numériques, et
    - [[tableau-chart-types]] - Choisir le bon type de graphique est une compétence BI essentielle
    - [[tableau-lod-expressions]] - Les expressions Level of Detail (LOD) calculent des agrégations à un grain différent de celui
    - [[tableau-performance-optimization]] - L'optimisation des performances dans Tableau porte sur quatre couches : charge serveur, source de données, calculs et
    - [[unit-economics]] - L'unit economics est une méthode de modélisation économique permettant de déterminer la rentabilité d'une activité en évaluant

---

<div id="linux-cli"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#a08878,#584030);box-shadow:0 0 8px rgba(160,136,120,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Linux et ligne de commande · 29 articles"

    - [[terminal-basics]] - Shell, émulateurs de terminal, navigation
    - [[file-operations]] - cp, mv, rm, find, permissions
    - [[file-search-and-grep]] - grep, find, locate, fd
    - [[text-processing]] - awk, sed, cut, sort, uniq
    - [[bash-scripting]] - Variables, boucles, fonctions, scripts
    - [[systemd-and-services]] - Gestion des services, journald
    - [[process-management]] - ps, top, kill, nohup, screen
    - [[ssh-remote-access]] - Clés SSH, tunnels, configuration
    - [[linux-security]] - Utilisateurs, permissions, pare-feux
    - [[docker-basics]] - Docker du point de vue Linux

    **Plus**

    - [[cron-and-scheduling]] - cron gère les tâches planifiées récurrentes
    - [[disk-data-recovery]] - Récupération de disques défaillants ou de grande capacité (16 To et plus) au niveau bloc : imagerie, réparation de partitions/GPT
    - [[disks-and-filesystems]] - Cette entrée couvre le nommage des périphériques disque, le partitionnement, le formatage, le montage et le fonctionnement interne des systèmes de fichiers
    - [[ffmpeg-encoding]] - Encodeur multimédia en ligne de commande
    - [[file-permissions]] - Chaque fichier et répertoire Linux a un propriétaire, un groupe et des bits de permission pour trois catégories
    - [[filesystem-hierarchy]] - Linux suit la Filesystem Hierarchy Standard (FHS)
    - [[firewall-and-iptables]] - iptables configure le framework de filtrage de paquets netfilter du noyau Linux
    - [[io-redirection-and-pipes]] - Chaque processus Linux dispose de trois flux standard : stdin (0), stdout (1) et stderr (2)
    - [[links-and-inodes]] - Chaque fichier Linux possède un inode, une structure de données qui stocke les métadonnées et les pointeurs vers les blocs de données
    - [[linux-kernel-and-boot]] - Le noyau est le cœur du système d'exploitation, qui assure la médiation entre le matériel et les programmes utilisateur
    - [[linux-os-structure]] - L'architecture Linux sépare l'espace noyau de l'espace utilisateur et utilise les fichiers comme abstractions universelles
    - [[logging-and-journald]] - La journalisation sous Linux couvre les événements système, la sortie des services, les pistes d'audit de sécurité et les journaux applicatifs
    - [[monitoring-and-performance]] - Outils de supervision du CPU, de la mémoire, des E/S disque et du réseau
    - [[package-management]] - Les logiciels Linux sont distribués sous forme de paquets : archives contenant des binaires, des bibliothèques, des configurations et
    - [[powershell-basics]] - PowerShell est un shell et un langage de script multiplateforme reposant sur .NET
    - [[python-and-node-cli]] - Installation et exécution de Python et Node.js en ligne de commande, gestion des paquets avec pip/npm
    - [[text-editors]] - nano est adapté aux débutants
    - [[users-and-groups]] - Linux est un système multi-utilisateur
    - [[wsl]] - WSL exécute des distributions Linux au sein de Windows

---

<div id="testing-qa"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#9090b8,#404068);box-shadow:0 0 8px rgba(144,144,184,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Tests et QA · 25 articles"

    - [[pytest-fundamentals]] - Découverte des tests, assertions, marqueurs
    - [[pytest-fixtures-advanced]] - Fixtures, portée, parametrize
    - [[selenium-webdriver]] - Automatisation de navigateur, localisateurs
    - [[playwright-testing]] - API Playwright, attente automatique
    - [[api-testing-requests]] - Modèles de tests d'API REST
    - [[page-object-model]] - Modèle POM pour les tests d'interface
    - [[test-architecture]] - Pyramide de tests, stratégie
    - [[ci-cd-test-automation]] - Tests dans les pipelines CI/CD
    - [[allure-reporting]] - Rapports de tests Allure

    **Plus**

    - [[browser-test-automation]] - Geb est une bibliothèque Groovy au-dessus de Selenium WebDriver pour l'automatisation des tests de navigateur
    - [[database-testing]] - Interroger directement les bases de données depuis les tests : vérifier l'intégrité des données après des appels d'API, préparer
    - [[docker-test-environments]] - Exécuter les services testés dans des conteneurs Docker : fichiers compose pour les environnements locaux, testcontainers
    - [[fastapi-test-services]] - Construire des microservices FastAPI testables et écrire des tests pour ceux-ci
    - [[grpc-testing]] - Tester les services gRPC : compilation protobuf, génération de clients, intercepteurs pour la journalisation, Allure
    - [[kafka-async-testing]] - Tester des microservices asynchrones communiquant via Apache Kafka
    - [[mobile-testing]] - Les tests d'interface Android utilisent Kaspresso (DSL Kotlin au-dessus d'Espresso et UI Automator)
    - [[negative-controls-for-verification]] - Un contrôle au vert ne prouve rien tant qu'il n'a pas été démontré qu'il peut passer au rouge
    - [[oauth-testing]] - Tester les API qui exigent OAuth 2.0, OIDC, JWT ou une authentification par session
    - [[pydantic-test-models]] - Utiliser des modèles Pydantic pour valider les réponses d'API, générer des données de test et faire respecter les contrats
    - [[selene-python]] - Selene est un port Python de Selenide (Java) : un wrapper concis et à attente automatique au-dessus de Selenium WebDriver
    - [[soap-testing]] - Tester les services web SOAP/XML avec requests (XML brut) et zeep (client compatible WSDL)
    - [[test-data-management]] - Stratégies de création, de gestion et de nettoyage des données de test dans les différents environnements
    - [[test-logging-secrets]] - Journalisation structurée dans les frameworks de test, masquage des données sensibles dans les journaux et rapports, et DevTools
    - [[test-parallelization]] - Exécuter les tests en parallèle avec pytest-xdist
    - [[three-state-check-aggregation]] - PASS / FAIL / UNKNOWN au lieu de réussite-échec : contrats de codes de sortie, agrégation fail-closed

---

<div id="rust"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#d89848,#784808);box-shadow:0 0 8px rgba(216,152,72,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Rust · 22 articles"

    - [[ownership-and-move-semantics]] - Règles de propriété, déplacements
    - [[borrowing-and-references]] - Références partagées et mutables
    - [[lifetimes]] - Annotations de durée de vie, élision
    - [[traits]] - Définitions de traits, implémentations, bornes
    - [Error Handling](../rust/error-handling.md) - Result, Option, opérateur ?
    - [[async-await]] - Tokio, runtime asynchrone, futures
    - [Concurrency](../rust/concurrency.md) - Arc, Mutex, canaux, Send/Sync
    - [Smart Pointers](../rust/smart-pointers.md) - Modèles Box, Rc, RefCell

    **Plus**

    - [[closures]] - Les closures sont des fonctions anonymes pouvant capturer des variables de leur portée englobante
    - [[collections]] - Les collections de la bibliothèque standard de Rust stockent les données sur le tas et croissent dynamiquement
    - [[dynamic-dispatch]] - Le dispatch dynamique utilise des objets trait (dyn Trait) pour appeler des méthodes via une vtable à l'exécution
    - [[enums-and-pattern-matching]] - Les enums Rust sont des types de données algébriques : chaque variante peut contenir des données différentes (unité, tuple ou
    - [[generics-and-monomorphization]] - Les génériques permettent d'écrire du code fonctionnant avec tout type satisfaisant des bornes de traits
    - [[interior-mutability]] - Modèle permettant la mutation de données derrière des références partagées (&T)
    - [[iterators]] - Les itérateurs Rust sont paresseux, composables et sans surcoût
    - [[macros]] - Les macros Rust génèrent du code à la compilation
    - [[modules-and-visibility]] - Le système de modules de Rust contrôle l'organisation du code et la visibilité
    - [[rust-gui]] - Panorama du développement d'interfaces graphiques en Rust : frameworks natifs, bindings vers des boîtes à outils établies et
    - [[rust-tooling]] - Rust fournit une chaîne d'outils unifiée : cargo (build/dépendances/tests), clippy (lint), rustfmt (formatage)
    - [[send-sync]] - Traits marqueurs qui encodent les garanties de sûreté des threads au niveau des types
    - [[sized-and-dst]] - Les types Rust se divisent en Sized (taille connue à la compilation) et en Dynamically Sized Types (DST, taille
    - [[structs-and-methods]] - Les structs sont le principal moyen qu'offre Rust pour créer des types de données personnalisés

---

<div id="ios-mobile"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#b080b0,#603060);box-shadow:0 0 8px rgba(176,128,176,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>iOS et mobile · 31 articles"

    - [[swift-fundamentals]] - Syntaxe Swift, types, optionnels
    - [[swiftui-views-and-modifiers]] - Hiérarchie des vues, modificateurs
    - [[swiftui-state-and-data-flow]] - @State, @Binding, ObservableObject
    - [[swiftui-navigation]] - NavigationStack, feuilles modales, alertes
    - [[swiftdata-persistence]] - Modèles et requêtes SwiftData
    - [[kotlin-android-fundamentals]] - Kotlin pour Android

    **Plus**

    - [[android-dagger-dependency-injection]] - Dagger 2 génère le code d'injection de dépendances à la compilation, sans réflexion ni surcoût à l'exécution
    - [[android-mvvm-architecture]] - MVVM (Model-View-ViewModel) est l'architecture recommandée pour les applications Android
    - [[android-retrofit-networking]] - Retrofit est le client HTTP standard pour Android, convertissant les définitions d'API REST en Kotlin
    - [[android-room-database]] - Room est la couche d'abstraction SQLite d'Android, offrant une vérification SQL à la compilation, LiveData
    - [[android-sparkle-filter]] - Implémentation d'effets de scintillement en temps réel sur les vêtements dans l'aperçu caméra en direct sous Android
    - [[avkit-audio-and-haptics]] - AVKit fournit la lecture audio pour la musique de fond et les effets sonores
    - [[core-data-persistence]] - Core Data est le framework de persistance mature d'Apple, disponible sur toutes les versions d'iOS
    - [[graph-algorithms-swift]] - Graphes en listes d'adjacence, parcours BFS/DFS et algorithmes de plus court chemin avec exemples de cartographie
    - [[mapkit-integration]] - L'intégration MapKit de SwiftUI fournit des vues de carte natives avec annotations, contrôle de la caméra
    - [[refactoring-view-controllers]] - Décomposition systématique de view controllers volumineux en composants testables par extraction
    - [[storekit-in-app-purchases]] - StoreKit 2 est l'API moderne d'Apple pour les achats intégrés
    - [[swift-collections-beyond-arrays]] - Ensembles et dictionnaires en Swift : caractéristiques de performance, opérations ensemblistes et modes d'accès
    - [[swift-enums-and-optionals]] - Les enums définissent un ensemble fini de cas nommés
    - [[swift-generics]] - Fonctions et types réutilisables et sûrs grâce à des paramètres génériques, contraintes et types associés
    - [[swift-macros]] - Génération de code à la compilation via des macros attachées et autonomes, reposant sur la transformation d'AST en Swift
    - [[swift-phantom-types]] - Paramètres de type existant uniquement à la compilation, pour imposer des machines à états, la sûreté des unités et des contraintes de domaine
    - [[swift-structs-and-classes]] - Les structs et les classes sont des modèles pour les types personnalisés en Swift
    - [[swiftui-animations]] - Les animations SwiftUI sont pilotées par les propriétés : on bascule un Bool, on attache des modificateurs qui réagissent à celui-ci, on encapsule le
    - [[swiftui-forms-and-input]] - Les formulaires regroupent les contrôles de saisie pour les écrans de saisie de données
    - [[swiftui-layout-testing]] - Fuzzing basé sur les propriétés pour vérifier les moteurs de mise en page personnalisés par rapport au rendu natif SwiftUI d'Apple
    - [[swiftui-lists-and-grids]] - List, ForEach, LazyVGrid et ScrollView sont les conteneurs principaux pour afficher des collections de
    - [[swiftui-networking]] - Le réseau dans SwiftUI utilise async/await de Swift avec URLSession pour les requêtes HTTP et
    - [[type-safe-modeling]] - Utiliser enums, structs et génériques pour éliminer les états impossibles et rendre les API auto-documentées
    - [[wrapping-c-libraries]] - Intégration de fonctions C en Swift avec sûreté de types, gestion automatique de la mémoire via deinit et gestion des erreurs
    - [[xcode-project-setup]] - Xcode est l'IDE requis pour le développement iOS

---

<div id="seo-marketing"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#80b868,#386020);box-shadow:0 0 8px rgba(128,184,104,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>SEO et marketing digital · 25 articles"

    - [[keyword-research-semantic-core]] - Méthodologie de recherche de mots-clés
    - [[technical-seo-audit]] - Checklist du SEO technique
    - [[site-structure-urls]] - Structure des URL, canonicalisation
    - [[link-building-strategy]] - Tactiques d'acquisition de liens
    - [[core-web-vitals-performance]] - Optimisation des Core Web Vitals
    - [[seo-tools-workflow]] - Flux de travail avec Ahrefs, Semrush, GSC

    **Plus**

    - [[behavioral-factors-ctr]] - Analyse des facteurs comportementaux, optimisation des extraits pour le CTR et mise en œuvre des micro-données Schema.org
    - [[commercial-ranking-factors]] - Les facteurs commerciaux évaluent la qualité de service telle que perçue par les moteurs de recherche
    - [[filters-and-penalties]] - Référence complète des filtres Yandex et Google, de leurs déclencheurs, symptômes, diagnostics et
    - [[internal-linking]] - Système de liens internes entre les pages
    - [[link-quality-assessment]] - Critères d'évaluation de la qualité des donneurs, méthodologie de prospection, usage des PBN (Private Blog Network), drop
    - [[llm-discoverability-ai-search]] - Optimisation du contenu web pour apparaître dans les réponses générées par l'IA, ChatGPT Search, Perplexity, Google AI
    - [[mkdocs-material-seo]] - Configuration SEO pour les sites MkDocs Material : sitemap, URL canoniques, plugins, Schema.org
    - [[multilingual-discovery-layer]] - Rendre un site statique en anglais uniquement (MkDocs, Hugo, Jekyll sur GitHub Pages) découvrable en plusieurs
    - [[niche-content-audit]] - Processus d'identification des principales caractéristiques de présentation du contenu dans une niche
    - [[ranking-algorithms-history]] - Chronologie des grandes mises à jour des algorithmes des moteurs de recherche, pour Yandex et Google, y compris le
    - [[regional-seo]] - Stratégies de promotion multirégionale, méthodes de ciblage géographique et différences entre moteurs de recherche pour
    - [[robots-txt-sitemaps-indexation]] - Couverture détaillée de la configuration de robots.txt, des exigences de sitemap.xml, de l'analyse d'indexation, du crawl
    - [[search-engine-mechanics]] - Comment les moteurs de recherche découvrent, traitent et classent les documents web
    - [[seo-analytics-reporting]] - Système de pilotage de projet : métriques KPI, structure du reporting mensuel, surveillance par méta-scanner
    - [[seo-client-management]] - Protocoles de communication client, modèles de tarification, définition du périmètre de travail, gestion de projet, juridique
    - [[seo-strategy-by-site-type]] - Approches SEO différenciées pour les sites e-commerce, les sites de services, les sites informationnels et les agrégateurs
    - [[technical-content-seo-strategy]] - Architecture de contenu et approche SEO pour les bases de connaissances techniques, la documentation développeur et
    - [[text-optimization]] - Zones de texte d'un document, règles des balises meta, scoring de pertinence textuelle (TF-IDF, BM25), flux de travail de l'analyseur de texte
    - [[twitter-x-content-strategy-and-ranking-factors]] - L'itération 2026 de l'algorithme de X (propulsé par Grok-v3) privilégie la profondeur conversationnelle et

---

<div id="nodejs"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#58c098,#187048);box-shadow:0 0 8px rgba(88,192,152,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Node.js · 16 articles"

    - [[event-loop-and-architecture]] - Boucle d'événements, libuv, phases
    - [[async-patterns]] - Callbacks, promesses, async/await
    - [[streams]] - Flux lisibles, inscriptibles, de transformation
    - [[modules-and-packages]] - CommonJS, ESM, npm
    - [Error Handling](../nodejs/error-handling.md) - Modèles de gestion des erreurs
    - [Performance Optimization](../nodejs/performance-optimization.md) - Profilage, clustering

    **Plus**

    - [[application-architecture]] - L'architecture d'une application Node.js repose sur la séparation en couches, l'abstraction du transport et le contexte
    - [[closures-and-scope]] - Une closure est une fonction qui conserve une référence aux variables de la portée de sa fonction externe, même
    - [Concurrency Patterns](../nodejs/concurrency-patterns.md) - La concurrence en Node.js dépasse async/await avec le modèle Actor, les CRDT pour l'état distribué
    - [[data-access-patterns]] - La couche d'accès aux données (DAL) sépare la logique métier du stockage physique en fournissant des CRUD abstraits
    - [[dependency-injection]] - Un couplage survient dès qu'un module appelle des méthodes, crée des instances ou lit/écrit des propriétés de
    - [Design Patterns (GoF) in JavaScript](../nodejs/design-patterns-gof.md) - Les patterns du Gang of Four s'appliquent différemment en JavaScript que dans les langages à classes
    - [[middleware-and-http]] - La gestion HTTP dans Node.js va des serveurs Node.js purs aux approches basées sur des frameworks (Fastify
    - [[security-and-sandboxing]] - La sécurité de Node.js englobe le hachage de mots de passe avec sel, l'authentification par jetons, le code en bac à sable
    - [[solid-and-grasp]] - Les principes SOLID et GRASP guident l'organisation du code en JavaScript, mais leur application diffère
    - [[v8-optimization]] - V8 compile JavaScript en code machine par compilation JIT à plusieurs niveaux d'optimisation

---

<div id="php"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#7090c0,#304070);box-shadow:0 0 8px rgba(112,144,192,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>PHP et Laravel · 15 articles"

    - [[php-type-system]] - Système de types PHP 8, enums
    - [[php-oop-fundamentals]] - Classes, interfaces, traits
    - [[laravel-architecture]] - Conteneur de services, fournisseurs
    - [[laravel-eloquent-orm]] - Modèles, relations, requêtes
    - [[laravel-routing]] - Routes, middleware, contrôleurs
    - [[laravel-authentication]] - Scaffolding d'authentification, gardes

    **Plus**

    - [[laravel-blade-templates]] - Blade est le moteur de templates de Laravel, qui fournit l'héritage de templates, les sections, les composants et
    - [[laravel-file-storage]] - L'abstraction de système de fichiers de Laravel (Flysystem) fournit une API unifiée pour le disque local, S3 et d'autres
    - [[laravel-middleware]] - Le middleware filtre les requêtes HTTP avant qu'elles n'atteignent les contrôleurs
    - [[laravel-migrations]] - Les migrations constituent le contrôle de version du schéma de base de données
    - [[laravel-validation]] - Laravel fournit une validation de requêtes intégrée avec plus de 90 règles et une redirection automatique en cas d'échec
    - [[mvc-framework]] - Construire un framework MVC à partir de zéro en PHP permet de comprendre l'architecture web de base : le Router distribue les URL
    - [[php-arrays]] - Les tableaux PHP sont des maps ordonnées : ils servent de tableaux, listes, tables de hachage, dictionnaires, piles et
    - [[php-control-structures]] - Les structures de contrôle PHP comprennent if/elseif/else, switch, match (PHP 8), for/foreach/while
    - [[php-pdo-and-sessions]] - PDO (PHP Data Objects) fournit une interface cohérente d'accès aux bases de données avec des requêtes préparées

---

<div id="audio-voice"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#e0a878,#805828);box-shadow:0 0 8px rgba(224,168,120,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Voix et audio · 14 articles"

    - [[ace-step-1-5]] - Référence tenant compte des artefacts et du matériel pour la génération musicale ACE-Step 1.5, base/SFT/turbo, et XL
    - [[asr-stt-compression]] - Méthodes de compression du cache KV pour l'inférence ASR/TTS et le contexte des LLM en 2026 : TriAttention
    - [[audio-flamingo]] - Référence tenant compte des versions pour Audio Flamingo 3, Music Flamingo et la compréhension audio d'Audio Flamingo Next
    - [[audio-generation]] - La génération audio couvre la synthèse musicale, la création d'effets sonores et la synchronisation vidéo-audio
    - [[audio-omni-unified-model]] - Modèle unique pour la compréhension, la génération et l'édition audio via un raisonnement LLM figé et des
    - [[lemas-tts-and-speech-editing]] - Modèles TTS multilingues open source LEMAS et édition de parole au niveau du mot : architecture
    - [[podcast-processing]] - Les pipelines de traitement de podcasts de bout en bout gèrent la diarisation des locuteurs (qui a parlé et quand), la transcription
    - [[speech-recognition]] - La reconnaissance automatique de la parole (ASR) convertit un signal audio parlé en texte
    - [[tts-fine-tuning-infrastructure]] - Comparatif de plateformes de location de GPU et modèles de déploiement pour le fine-tuning et le service de modèles TTS de 2B à 4B
    - [[tts-models]] - Le TTS moderne est passé des approches concaténatives et paramétriques à des modèles neuronaux de bout en bout
    - [[voice-agent-pipelines]] - Construire des systèmes d'IA vocale en temps réel : choix du framework, optimisation de la latence, configuration du VAD
    - [[voice-cloning]] - Le clonage vocal reproduit les caractéristiques vocales d'un locuteur cible (timbre, hauteur, rythme) à partir d'un
    - [[voice-conversion]] - La conversion vocale (VC) transforme l'identité du locuteur dans un audio existant tout en préservant la dimension linguistique
    - [[voice-design]] - Création de voix synthétiques uniques à partir de descriptions textuelles, morphing vocal, benchmarks de naturalité

---

<div id="go"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#5ec0d8,#1a6880);box-shadow:0 0 8px rgba(94,192,216,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Go · 9 articles"

    - [Go Concurrency - Goroutines, Channels, and Sync](../go/concurrency-patterns.md) - Modèle de concurrence de Go : l'ordonnanceur GMP, les canaux, select, les primitives de synchronisation et
    - [[database-patterns]] - Patterns de bases de données en production avec Go : PostgreSQL avec pgx, MongoDB avec le driver officiel, Redis
    - [Error Handling](../go/error-handling.md) - Go utilise des retours d'erreur explicites au lieu d'exceptions
    - [[fundamentals]] - Fonctionnalités de base du langage Go : système de types, slices, maps, pointeurs, interfaces, closures et gestion des erreurs
    - [[goroutines-channels]] - Le modèle de concurrence de Go repose sur les goroutines (threads légers gérés par le runtime Go) et les
    - [[http-servers]] - Le package net/http de Go fournit un serveur HTTP/2 de qualité production avec prise en charge de TLS d'emblée
    - [[interfaces-composition]] - Go utilise des interfaces pour le polymorphisme et l'embedding pour la composition
    - [[microservices]] - Patterns de microservices Go en production : gRPC avec protobuf, couches d'architecture propre, injection de dépendances
    - [[modules-packages]] - Les modules Go sont l'unité de gestion des dépendances, et les packages sont l'unité d'organisation du code

---

<div id="llm-memory"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#b898e0,#584878);box-shadow:0 0 8px rgba(184,152,224,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Mémoire des LLM · 13 articles"

    - [[context-window-management]] - Stratégies de gestion de ce qui entre dans la fenêtre de contexte du LLM et du moment
    - [[forgetting-strategies]] - Quand et comment retirer des informations de la mémoire d'un agent LLM
    - [[knowledge-base-as-memory]] - Utiliser une base de connaissances markdown structurée comme mémoire à long terme de l'agent
    - [[knowledge-graph-memory]] - Modèles de graphes de connaissances persistants pour agents d'IA : résolution d'entités, étapes du pipeline, notes d'agent
    - [[memory-architectures]] - Approches structurelles pour organiser les connaissances persistantes des agents LLM
    - [[memory-priority-enforcement]] - Modèle de structuration de la mémoire d'un agent en niveaux à chargement permanent (critique) et à la demande (référence)
    - [[memory-retrieval-patterns]] - Comment les agents retrouvent les informations pertinentes dans leur mémoire
    - [[memory-transfer-learning]] - Transfert de mémoire inter-domaines pour les agents de codage
    - [[session-persistence]] - Comment préserver les connaissances, décisions et avancées entre les sessions d'un agent LLM
    - [[shared-knowledge-layers]] - Lorsque plusieurs agents travaillent en parallèle, ils ont besoin d'un moyen structuré de partager leurs découvertes sans
    - [[temporal-memory]] - Gérer la dimension temporelle des connaissances stockées
    - [[verbatim-retrieval-vs-extraction]] - Pourquoi le stockage brut en verbatim surpasse l'extraction par LLM pour la récupération en mémoire d'agent : benchmarks, MemPalace
    - [[verbatim-vs-extraction]] - Faut-il stocker le texte brut ou des faits extraits par LLM en mémoire

---

<div id="writing"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#d8b0c8,#785068);box-shadow:0 0 8px rgba(216,176,200,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Langage naturel et rédaction · 14 articles"

    - [[4-layer-content-quality-framework]] - Approche systématique de la rédaction technique qui filtre le bruit linguistique, impose la couche informationnelle
    - [[ai-text-detection]] - Méthodes et travaux de recherche pour identifier les textes générés par IA
    - [[automated-video-production-and-post-production-toolkits]] - Les flux de production vidéo modernes utilisent des boîtes à outils pilotées par l'IA pour automatiser la génération de scènes, le montage
    - [[cognitive-memory-mechanics-for-course-design]] - L'optimisation des contenus pédagogiques exige d'aligner la diffusion sur les contraintes biologiques de
    - [[editing-checklist]] - Liste de contrôle pratique pour relire un texte avant publication
    - [[llm-writing-antipatterns]] - Motifs de texte IA détectables : vocabulaire surutilisé, antipatterns structurels, burstiness/perplexité
    - [[natural-writing-style]] - Ce qui fait qu'un texte paraît rédigé par un humain, et techniques pour obtenir une voix naturelle dans la documentation technique et
    - [[overused-words-phrases]] - Référence complète des mots et expressions qui signalent un texte généré par IA
    - [[publishing-platforms]] - Où publier des articles techniques, avec les profils d'audience, les exigences de mise en forme et
    - [[seo-for-articles]] - Comment optimiser des articles techniques pour la recherche sans dégrader leur qualité
    - [[structural-antipatterns]] - Le texte généré par IA possède une « forme » reconnaissable, indépendante du vocabulaire
    - [[technical-article-structure]] - Comment structurer des articles techniques qui sont lus, partagés et mis en favoris
    - [[video-demo-skills-ecosystem]] - Collections de skills Claude Code et bibliothèques pour créer des démonstrations vidéo programmatiques, des présentations
    - [[video-narrative-design-and-scripting-pipelines]] - Une production vidéo performante exige de dépasser l'écriture manuelle des scripts au profit de pipelines automatisés
