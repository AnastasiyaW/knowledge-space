---
title: Knowledge Base
description: Browse 766+ technical articles across 26 domains. Dense references for LLM agents and engineers.
---

# Knowledge Base

766+ curated articles across 26 domains. Click any domain to explore.

---

<div id="data-science"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#a07ad0,#5a3a80);box-shadow:0 0 8px rgba(160,122,208,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Data Science & Machine Learning · 50 articles"

    **Foundations**

    - [[math-precalculus]] - Pre-calculus essentials for ML
    - [[math-logic]] - Mathematical logic and proofs
    - [[math-for-ml]] - Core math concepts for machine learning
    - [[math-linear-algebra]] - Vectors, matrices, eigenvalues
    - [[math-probability-statistics]] - Probability theory and distributions

    **Statistics & Probability**

    - [[descriptive-statistics]] - Central tendency, variance, distributions
    - [[probability-distributions]] - Normal, binomial, Poisson distributions
    - [[hypothesis-testing]] - t-tests, p-values, confidence intervals
    - [[causal-inference]] - Causal models, A/B testing, observational studies
    - [[bias-variance-tradeoff]] - Model complexity vs generalization

    **Tools & Languages**

    - [[python-for-ds]] - Python setup for data science workflows
    - [[numpy-fundamentals]] - Arrays, broadcasting, linear algebra
    - [[pandas-eda]] - DataFrames, groupby, merge, EDA patterns
    - [[data-visualization]] - Matplotlib, Seaborn, Plotly
    - [[sql-for-data-science]] - SQL for analytical queries

    **Classical Machine Learning**

    - [[linear-models]] - Linear/logistic regression, regularization
    - [[gradient-boosting]] - XGBoost, LightGBM, CatBoost
    - [[knn-and-classical-ml]] - KNN, SVM, decision trees, random forest
    - [[unsupervised-learning]] - Clustering, PCA, dimensionality reduction
    - [[bayesian-methods]] - Bayes theorem, naive Bayes, Bayesian inference

    **Deep Learning**

    - [[neural-networks]] - Perceptron, backpropagation, architectures
    - [[cnn-computer-vision]] - Convolutions, pooling, ResNet, detection
    - [[nlp-text-processing]] - Tokenization, word vectors, text classification
    - [[rnn-sequences]] - LSTM, GRU, sequence-to-sequence models
    - [[generative-models]] - GANs, VAEs, diffusion models
    - [[transfer-learning]] - Fine-tuning, domain adaptation
    - [[data-augmentation]] - Image/text augmentation strategies

    **Techniques & Evaluation**

    - [[feature-engineering]] - Feature creation, selection, encoding
    - [[model-evaluation]] - Metrics, cross-validation, confusion matrix
    - [[time-series-analysis]] - ARIMA, Prophet, seasonal decomposition
    - [[monte-carlo-simulation]] - Random sampling, Monte Carlo methods
    - [[recommender-systems]] - Collaborative filtering, content-based

    **Applied & Production**

    - [[ds-workflow]] - End-to-end data science project lifecycle
    - [[bi-dashboards]] - Building analytical dashboards
    - [[ml-production]] - Model deployment, monitoring, drift
    - [[financial-data-science]] - Quantitative finance, risk modeling
    - [[ai-video-production]] - AI video generation pipelines

---

<div id="kafka"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#d07870,#803830);box-shadow:0 0 8px rgba(208,120,112,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Kafka & Message Queues · 38 articles"

    **Core Concepts**

    - [[broker-architecture]] - Broker internals, partitions, replication
    - [[topics-and-partitions]] - Topic design, partition strategies
    - [[consumer-groups]] - Consumer coordination, rebalancing
    - [[kafka-replication-fundamentals]] - ISR, leader election, durability
    - [[kafka-fault-tolerance]] - Failure modes, recovery, partition rebalancing

    **Producers & Consumers**

    - [[kafka-producer-fundamentals]] - Batching, compression, idempotence
    - [[kafka-producer-advanced-patterns]] - Transactions, exactly-once semantics
    - [[idempotent-producer]] - Exactly-once producer semantics
    - [[consumer-configuration]] - Consumer tuning, polling, offsets
    - [[offsets-and-commits]] - Offset management, auto vs manual commit
    - [[delivery-semantics]] - At-most-once, at-least-once, exactly-once
    - [[rebalancing-deep-dive]] - Cooperative rebalancing, static membership

    **Stream Processing**

    - [[kafka-streams]] - KStreams, KTable, joins, aggregations
    - [[kafka-streams-windowing]] - Tumbling, hopping, session windows
    - [[kafka-streams-time-semantics]] - Event time vs processing time
    - [[kafka-streams-state-stores]] - RocksDB, queryable state
    - [[ksqldb]] - SQL over streams, push/pull queries

    **Integration**

    - [[kafka-connect]] - Source and sink connectors, transforms
    - [[schema-registry]] - Avro, Protobuf, JSON Schema evolution
    - [[spring-kafka]] - Spring Boot Kafka integration
    - [[confluent-rest-proxy]] - REST API for Kafka
    - [[alpakka-kafka]] - Akka Streams Kafka connector
    - [[zio-kafka]] - ZIO effect-based Kafka client

    **Patterns**

    - [[kafka-transactions]] - Transactional messaging patterns
    - [[transactional-outbox]] - Outbox pattern for consistency
    - [[event-sourcing]] - Event-driven architecture with Kafka
    - [[cqrs-pattern]] - Command Query Responsibility Segregation
    - [[saga-pattern]] - Distributed transaction coordination
    - [[messaging-models]] - Pub/sub vs queue, routing patterns
    - [[partitioning-strategies]] - Key-based, round-robin, custom

    **Operations**

    - [[kafka-cluster-management]] - Cluster management, rolling upgrades
    - [[kafka-monitoring-and-tuning]] - Observability, JMX metrics, tuning
    - [[kafka-backup-and-dr]] - Backup strategies, disaster recovery
    - [[kafka-monitoring]] - JMX metrics, consumer lag, alerts
    - [[kafka-security]] - SSL, SASL, ACLs, encryption
    - [[kafka-troubleshooting]] - Common issues and fixes
    - [[zero-copy-and-disk-io]] - Performance internals
    - [[docker-development-setup]] - Local Kafka with Docker
    - [[mirrormaker]] - Cross-cluster replication
    - [[kafka-queues-v4]] - KIP-932 queue semantics
    - [[nats-comparison]] - Kafka vs NATS comparison
    - [[admin-api]] - AdminClient API reference

---

<div id="devops"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#c88060,#784020);box-shadow:0 0 8px rgba(200,128,96,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>DevOps & Infrastructure · 35 articles"

    **Containers & Docker**

    - [[docker-fundamentals]] - Images, containers, registries
    - [[dockerfile-and-image-building]] - Multi-stage builds, layer caching
    - [[docker-compose]] - Multi-container orchestration
    - [[docker-for-ml]] - GPU containers, model serving

    **Kubernetes**

    - [[kubernetes-architecture]] - Control plane, nodes, API server
    - [[kubernetes-workloads]] - Deployments, StatefulSets, DaemonSets
    - [[kubernetes-services-and-networking]] - Services, Ingress, DNS
    - [[kubernetes-storage]] - PV, PVC, StorageClasses
    - [[kubernetes-resource-management]] - Requests, limits, HPA
    - [[kubernetes-on-aks]] - Azure Kubernetes Service
    - [[kubernetes-on-eks]] - Amazon EKS setup and management
    - [[helm-package-manager]] - Charts, values, templating

    **CI/CD & Automation**

    - [[cicd-pipelines]] - Pipeline design, stages, artifacts
    - [[jenkins-automation]] - Jenkinsfile, shared libraries
    - [[gitops-and-argocd]] - GitOps workflow, ArgoCD setup

    **Infrastructure as Code**

    - [[terraform-iac]] - HCL, state, modules, providers
    - [[ansible-configuration-management]] - Playbooks, roles, inventory

    **Cloud & Networking**

    - [[aws-cloud-fundamentals]] - EC2, S3, VPC, IAM
    - [[container-registries]] - ECR, GCR, Docker Hub
    - [[datacenter-network-design]] - Network topology, SDN

    **Monitoring & SRE**

    - [[monitoring-and-observability]] - Prometheus, Grafana, logging
    - [[sre-principles]] - SLIs, SLOs, error budgets
    - [[sre-incident-management]] - On-call, postmortems, escalation
    - [[sre-automation-and-toil]] - Toil reduction, automation
    - [[chaos-engineering-and-testing]] - Chaos Monkey, fault injection

    **Deployment & Architecture**

    - [[deployment-strategies]] - Blue-green, canary, rolling
    - [[service-mesh-istio]] - Istio, Envoy, traffic management
    - [[microservices-patterns]] - Service discovery, circuit breaker
    - [[devops-culture-and-sdlc]] - DevOps principles, SDLC
    - [[git-version-control]] - Git workflow, branching strategies
    - [[linux-server-administration]] - Server setup, hardening

---

<div id="architecture"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#7088c8,#303878);box-shadow:0 0 8px rgba(112,136,200,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Software Architecture · 32 articles"

    **Architecture Process**

    - [[solution-architecture-process]] - Architecture decision records
    - [[architecture-documentation]] - C4 model, arc42, diagrams
    - [[tech-lead-role]] - Technical leadership patterns
    - [[system-design-interviews]] - System design preparation

    **Styles & Patterns**

    - [[architectural-styles]] - Monolith, SOA, microservices, serverless
    - [[microservices-communication]] - Sync vs async, gRPC, messaging
    - [[design-patterns-gof]] - GoF patterns with modern examples
    - [[microfrontends]] - Micro-frontend architectures

    **Distributed Systems**

    - [[distributed-systems-fundamentals]] - CAP, consensus, clocks
    - [[queueing-theory]] - Little's law, capacity planning
    - [[quality-attributes-reliability]] - Availability, fault tolerance

    **API Design**

    - [[http-rest-fundamentals]] - HTTP methods, status codes, HATEOAS
    - [[rest-api-advanced]] - Pagination, versioning, rate limiting
    - [[graphql-api]] - Schema, resolvers, subscriptions
    - [[grpc-api]] - Protocol buffers, streaming, interceptors
    - [[soap-api]] - WSDL, SOAP envelope, WS-Security
    - [[json-rpc-api]] - JSON-RPC 2.0 specification
    - [[async-event-apis]] - WebSockets, SSE, webhooks
    - [[api-authentication-security]] - OAuth2, JWT, API keys
    - [[api-documentation-specs]] - OpenAPI, AsyncAPI, Swagger
    - [[api-testing-tools]] - Postman, curl, HTTPie

    **Data & Integration**

    - [[database-selection]] - Decision tree for database choice
    - [[data-serialization-formats]] - JSON, Protobuf, Avro, MessagePack
    - [[caching-and-performance]] - Redis, CDN, cache invalidation
    - [[enterprise-integration]] - EIP, middleware, ESB
    - [[message-broker-patterns]] - Pub/sub, fan-out, dead letter
    - [[kafka-architecture]] - Kafka from architecture perspective
    - [[rabbitmq-architecture]] - RabbitMQ exchanges and queues

    **Security & Operations**

    - [[security-architecture]] - Zero trust, defense in depth
    - [[devops-cicd]] - CI/CD from architecture perspective
    - [[testing-and-quality]] - Testing pyramid, quality gates
    - [[bigdata-ml-architecture]] - Big data and ML system design

---

<div id="data-engineering"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#8878b8,#483868);box-shadow:0 0 8px rgba(136,120,184,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Data Engineering · 33 articles"

    **Concepts & Architecture**

    - [[etl-elt-pipelines]] - ETL vs ELT, pipeline patterns
    - [[dwh-architecture]] - Data warehouse design, Kimball vs Inmon
    - [[data-modeling]] - Conceptual, logical, physical models
    - [[dimensional-modeling]] - Star schema, snowflake, facts/dimensions
    - [[data-vault]] - Data Vault 2.0 methodology
    - [[scd-patterns]] - Slowly changing dimensions (Type 1-6)
    - [[data-lake-lakehouse]] - Delta Lake, Iceberg, Hudi
    - [[data-quality]] - Data quality frameworks, great expectations
    - [[data-governance-catalog]] - Metadata management, data catalogs
    - [[data-lineage-metadata]] - Lineage tracking, impact analysis
    - [[file-formats]] - Parquet, ORC, Avro, CSV comparison

    **Distributed Processing**

    - [[apache-spark-core]] - RDDs, DAG, executors, partitions
    - [[pyspark-dataframe-api]] - PySpark DataFrame operations
    - [[spark-optimization]] - Broadcast, repartition, caching
    - [[spark-streaming]] - Structured Streaming, micro-batch
    - [[apache-kafka]] - Kafka for data engineering pipelines
    - [[mapreduce]] - MapReduce paradigm and implementations

    **Storage & Databases**

    - [[hadoop-hdfs]] - HDFS architecture, replication
    - [[apache-hive]] - HiveQL, partitions, bucketing
    - [[hbase]] - Column-family store, row key design
    - [[clickhouse]] - OLAP engine, MergeTree, materialized views
    - [[clickhouse-engines]] - ClickHouse engine types reference
    - [[greenplum-mpp]] - MPP architecture, distribution
    - [[postgresql-administration]] - PostgreSQL for data engineering
    - [[mongodb-nosql]] - Document model, aggregation pipeline

    **Infrastructure**

    - [[apache-airflow]] - DAGs, operators, scheduling
    - [[cloud-data-platforms]] - AWS/GCP/Azure data services
    - [[docker-for-de]] - Docker for data pipelines
    - [[kubernetes-for-de]] - K8s for Spark and Airflow
    - [[yarn-resource-management]] - YARN architecture, scheduling

    **Cross-Cutting**

    - [[mlops-feature-store]] - Feature stores, ML pipelines
    - [[sql-for-de]] - SQL patterns for data engineering
    - [[python-for-de]] - Python tools for data pipelines

---

<div id="llm-agents"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#c0b060,#706020);box-shadow:0 0 8px rgba(192,176,96,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>LLM & AI Agents · 32 articles"

    **Foundations**

    - [[transformer-architecture]] - Attention, multi-head, positional encoding
    - [[tokenization]] - BPE, WordPiece, SentencePiece
    - [[embeddings]] - Word2Vec, sentence embeddings, vector spaces
    - [[frontier-models]] - GPT-4, Claude, Gemini, Llama comparison

    **Prompting & Generation**

    - [[prompt-engineering]] - System prompts, few-shot, chain-of-thought
    - [[function-calling]] - Tool use, structured output
    - [[llm-api-integration]] - API patterns, streaming, error handling

    **RAG**

    - [[rag-pipeline]] - Retrieval-augmented generation architecture
    - [[chunking-strategies]] - Document splitting, overlap, semantic chunking
    - [[vector-databases]] - Pinecone, Weaviate, Chroma, pgvector

    **Agents**

    - [[agent-fundamentals]] - Agent loop, tool use, planning
    - [[agent-design-patterns]] - ReAct, MRKL, plan-and-execute
    - [[multi-agent-systems]] - Multi-agent orchestration, delegation
    - [[agent-memory]] - Short/long-term memory, context management
    - [[agent-security]] - Prompt injection, guardrails, sandboxing

    **Frameworks**

    - [[langchain-framework]] - Chains, agents, tools, callbacks
    - [[langgraph]] - Graph-based agent workflows
    - [[no-code-platforms]] - Low-code AI tools
    - [[spring-ai]] - Spring AI framework for Java
    - [[ai-coding-assistants]] - Copilot, Claude Code, Cursor

    **Operations**

    - [[fine-tuning]] - LoRA, QLoRA, full fine-tuning
    - [[model-optimization]] - Quantization, pruning, distillation
    - [[ollama-local-llms]] - Local model deployment
    - [[llmops]] - LLM monitoring, evaluation, versioning
    - [[production-patterns]] - Production deployment patterns

---

<div id="sql-databases"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#9888c0,#504070);box-shadow:0 0 8px rgba(152,136,192,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>SQL & Databases · 32 articles"

    **SQL Fundamentals**

    - [[select-fundamentals]] - SELECT, WHERE, ORDER BY, LIMIT
    - [[aggregate-functions-group-by]] - COUNT, SUM, AVG, GROUP BY, HAVING
    - [[joins-and-set-operations]] - INNER, LEFT, FULL, CROSS joins, UNION
    - [[subqueries-and-ctes]] - Subqueries, CTEs, recursive CTEs
    - [[window-functions]] - ROW_NUMBER, RANK, LAG, LEAD, frames
    - [[dml-insert-update-delete]] - INSERT, UPDATE, DELETE, MERGE

    **Schema & Modeling**

    - [[ddl-schema-management]] - CREATE, ALTER, constraints, indexes
    - [[data-types-and-nulls]] - Type selection, NULL handling
    - [[schema-design-normalization]] - 1NF-5NF, denormalization

    **Transactions & Concurrency**

    - [[transactions-and-acid]] - ACID properties, isolation levels
    - [[concurrency-and-locking]] - Locks, MVCC, deadlocks
    - [[distributed-transactions]] - 2PC, saga, eventual consistency

    **Internals & Performance**

    - [[database-storage-internals]] - Pages, B-trees, buffer pool
    - [[btree-and-index-internals]] - B-tree structure, index types
    - [[index-strategies]] - Composite, covering, partial indexes
    - [[query-optimization-explain]] - EXPLAIN plans, query tuning
    - [[database-cursors]] - Server-side cursors, pagination

    **PostgreSQL**

    - [[postgresql-mvcc-vacuum]] - MVCC, autovacuum, bloat
    - [[postgresql-configuration-tuning]] - shared_buffers, work_mem
    - [[postgresql-wal-durability]] - WAL, replication, recovery
    - [[postgresql-data-loading]] - COPY, bulk inserts, pg_dump

    **MySQL & HA**

    - [[mysql-innodb-engine]] - InnoDB internals, buffer pool
    - [[connection-pooling]] - PgBouncer, HikariCP
    - [[replication-fundamentals]] - Streaming, logical replication
    - [[postgresql-ha-patroni]] - Patroni HA cluster setup
    - [[backup-and-recovery]] - pg_dump, pg_basebackup, PITR

    **Scaling & Security**

    - [[partitioning-and-sharding]] - Table partitioning, sharding
    - [[distributed-databases]] - CockroachDB, YugabyteDB, Vitess
    - [[caching-redis-memcached]] - Redis, Memcached patterns
    - [[database-security]] - Roles, RLS, encryption
    - [[postgresql-docker-kubernetes]] - PostgreSQL in containers
    - [[infrastructure-as-code]] - Database IaC patterns

---

<div id="web-frontend"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#6090c8,#204078);box-shadow:0 0 8px rgba(96,144,200,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Web Frontend · 30 articles"

    **HTML & CSS**

    - [[html-fundamentals]] - Semantic HTML, accessibility
    - [[html-tables-and-forms]] - Forms, validation, tables
    - [[css-selectors-and-cascade]] - Specificity, cascade, inheritance
    - [[css-box-model-and-layout]] - Box model, positioning
    - [[css-flexbox]] - Flex container, items, alignment
    - [[css-grid]] - Grid template, areas, auto-fill
    - [[css-responsive-design]] - Media queries, mobile-first
    - [[css-animation-and-transforms]] - Transitions, keyframes, transforms
    - [[css-sass-and-methodology]] - SASS, BEM, CSS modules

    **JavaScript**

    - [[js-variables-and-types]] - var/let/const, types, coercion
    - [[js-control-flow]] - Loops, conditionals, error handling
    - [[js-strings-and-numbers]] - String methods, number precision
    - [[js-functions]] - Arrow functions, closures, IIFE
    - [[js-scope-closures-this]] - Scope chain, this binding
    - [[js-arrays]] - Array methods, functional patterns
    - [[js-objects-and-data]] - Objects, destructuring, spread
    - [[js-dom-and-events]] - DOM manipulation, event delegation
    - [[js-async-and-fetch]] - Promises, async/await, fetch API

    **TypeScript & React**

    - [[typescript-fundamentals]] - Types, interfaces, generics
    - [[typescript-advanced]] - Utility types, mapped types, conditional
    - [[react-components-and-jsx]] - Components, props, children
    - [[react-state-and-hooks]] - useState, useEffect, custom hooks
    - [[react-rendering-internals]] - Virtual DOM, reconciliation
    - [[react-styling-approaches]] - CSS-in-JS, Tailwind, modules

    **Build & Design**

    - [[npm-and-task-runners]] - npm scripts, package management
    - [[frontend-build-systems]] - Webpack, Vite, esbuild
    - [[git-and-github]] - Git workflow for frontend
    - [[figma-fundamentals]] - Figma basics for developers
    - [[figma-layout-and-components]] - Auto layout, components
    - [[figma-design-workflow]] - Design-to-code workflow

---

<div id="python"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#50b89a,#20684a);box-shadow:0 0 8px rgba(80,184,154,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Python · 30 articles"

    **Language Fundamentals**

    - [[variables-types-operators]] - Variables, types, operators
    - [[strings-and-text]] - String methods, formatting, regex
    - [[data-structures]] - Lists, dicts, sets, tuples
    - [[control-flow]] - Conditionals, loops, comprehensions

    **Functions & OOP**

    - [[functions]] - Args, kwargs, decorators, closures
    - [[decorators]] - Decorator patterns, functools
    - [[oop-fundamentals]] - Classes, inheritance, encapsulation
    - [[oop-advanced]] - Metaclasses, descriptors, ABC
    - [[magic-methods]] - Dunder methods, protocols

    **Error Handling & I/O**

    - [[error-handling]] - Exceptions, context managers
    - [[file-io]] - File operations, pathlib, CSV/JSON
    - [[regular-expressions]] - Regex patterns, re module

    **Standard Library & Advanced**

    - [[standard-library]] - collections, itertools, functools
    - [[iterators-and-generators]] - Generators, yield, lazy evaluation
    - [[type-hints]] - Type annotations, mypy, pydantic
    - [[async-programming]] - asyncio, coroutines, event loop
    - [[concurrency]] - Threading, multiprocessing, GIL
    - [[memory-and-internals]] - CPython internals, memory model

    **Performance & Testing**

    - [[profiling-and-optimization]] - cProfile, line_profiler, optimization
    - [[recursion-and-algorithms]] - Recursive patterns in Python
    - [[testing-with-pytest]] - pytest, fixtures, mocking
    - [[project-setup-and-tooling]] - venv, pip, poetry, pre-commit

    **FastAPI**

    - [[fastapi-fundamentals]] - Routes, dependency injection
    - [[fastapi-pydantic-validation]] - Pydantic models, validation
    - [[fastapi-database-layer]] - SQLAlchemy, async DB access
    - [[fastapi-auth-and-security]] - JWT, OAuth2, CORS
    - [[fastapi-deployment]] - Uvicorn, Docker, production
    - [[fastapi-caching-and-tasks]] - Redis cache, background tasks

    **Ecosystem**

    - [[web-frameworks-comparison]] - Flask vs Django vs FastAPI
    - [[data-analysis-basics]] - pandas, numpy quickstart

---

<div id="security"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#b87080,#683040);box-shadow:0 0 8px rgba(184,112,128,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Security & Cybersecurity · 29 articles"

    - [[information-security-fundamentals]] - CIA triad, risk management
    - [[cryptography-and-pki]] - Encryption, certificates, TLS
    - [[authentication-and-authorization]] - OAuth2, SAML, RBAC
    - [[web-application-security-fundamentals]] - OWASP Top 10
    - [[sql-injection-deep-dive]] - SQLi detection and prevention
    - [[burp-suite-and-web-pentesting]] - Web application testing
    - [[penetration-testing-methodology]] - Pentesting lifecycle
    - [[privilege-escalation-techniques]] - Linux/Windows privesc
    - [[active-directory-attacks]] - AD exploitation and defense
    - [[network-security-and-protocols]] - TLS, VPN, firewall rules
    - [[linux-system-hardening]] - OS hardening checklist
    - [[siem-and-incident-response]] - SIEM tools, IR process
    - [[browser-and-device-fingerprinting]] - Fingerprinting techniques
    - [[anti-fraud-behavioral-analysis]] - Fraud detection patterns

---

<div id="algorithms"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#80a0d0,#305080);box-shadow:0 0 8px rgba(128,160,208,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Algorithms & Data Structures · 29 articles"

    - [[complexity-analysis]] - Big-O notation, time/space complexity
    - [[amortized-analysis]] - Average cost per operation
    - [[sorting-algorithms]] - Comparison of all sorts with code
    - [[searching-algorithms]] - Binary search, KMP matching
    - [[dynamic-programming-fundamentals]] - Memoization vs tabulation
    - [[graph-traversal-bfs-dfs]] - DFS, BFS, grid problems
    - [[shortest-path-algorithms]] - Dijkstra, Bellman-Ford, Floyd-Warshall
    - [[trees-and-binary-trees]] - Tree traversals, BST operations
    - [[hash-tables]] - Hash functions, collision handling
    - [[heap-priority-queue]] - Binary heap, priority queue
    - [[union-find]] - Disjoint set union, path compression

---

<div id="image-generation"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#c8a058,#785018);box-shadow:0 0 8px rgba(200,160,88,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Image Generation · 27 articles"

    - ACE++ - Advanced image editing model
    - ATI - AI texture generation
    - Flow Matching - Flow-based generative models
    - FLUX Kontext - Context-aware image generation
    - LaMa - Large mask inpainting
    - LoRA Fine-Tuning for Editing Models - LoRA training for image editing
    - MARBLE - Multi-aspect image restoration
    - MMDiT - Multi-modal diffusion transformer
    - SANA - Efficient text-to-image architecture
    - Tiled Inference - Memory-efficient large image generation
    - Transformers v5 - HuggingFace Transformers for image gen

---

<div id="cpp"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#7090c0,#304070);box-shadow:0 0 8px rgba(112,144,192,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>C++ · 25 articles"

    - [[cmake-build-systems]] - CMake, build configuration
    - [[smart-pointers]] - unique_ptr, shared_ptr, weak_ptr
    - [[move-semantics]] - Rvalue references, std::move
    - [[raii-resource-management]] - RAII pattern, resource safety
    - [[templates-and-concepts]] - Template metaprogramming
    - [[stl-containers]] - vector, map, set, unordered_map
    - [[stl-algorithms]] - std::sort, std::find, ranges
    - [[concurrency]] - std::thread, mutex, atomic
    - [[error-handling]] - Exceptions, std::expected
    - [[lambda-expressions]] - Lambda syntax, captures
    - [[modern-cpp-features]] - C++17/20/23 features

---

<div id="java-spring"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#68b080,#286038);box-shadow:0 0 8px rgba(104,176,128,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Java & Spring · 25 articles"

    - [[java-type-system-fundamentals]] - Primitives, generics, records
    - [[kotlin-language-features]] - Kotlin for JVM developers
    - [[spring-boot-configuration]] - Properties, profiles, auto-config
    - [[spring-data-jpa-hibernate]] - JPA entities, repositories, queries
    - [[spring-security]] - Authentication, authorization, filters
    - [[spring-mvc-rest]] - REST controllers, error handling
    - [[android-fundamentals-ui]] - Android UI basics
    - [[android-architecture-mvvm]] - MVVM, ViewModel, LiveData

---

<div id="bi-analytics"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#70a0b0,#205060);box-shadow:0 0 8px rgba(112,160,176,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>BI & Analytics · 23 articles"

    - [[product-analytics-fundamentals]] - Analytics frameworks
    - [[product-metrics-framework]] - North Star, AARRR, KPIs
    - [[tableau-fundamentals]] - Worksheets, dashboards, data sources
    - [[tableau-calculations]] - Calculated fields, table calculations
    - [[powerbi-fundamentals]] - Power BI reports, DAX basics
    - [[dashboard-design-patterns]] - Dashboard layout, UX principles
    - [[sql-for-analytics]] - Analytical SQL patterns
    - [[web-marketing-analytics]] - GA4, UTM, attribution models

---

<div id="linux-cli"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#a08878,#584030);box-shadow:0 0 8px rgba(160,136,120,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Linux & Command Line · 27 articles"

    - [[terminal-basics]] - Shell, terminal emulators, navigation
    - [[file-operations]] - cp, mv, rm, find, permissions
    - [[file-search-and-grep]] - grep, find, locate, fd
    - [[text-processing]] - awk, sed, cut, sort, uniq
    - [[bash-scripting]] - Variables, loops, functions, scripts
    - [[systemd-and-services]] - Service management, journald
    - [[process-management]] - ps, top, kill, nohup, screen
    - [[ssh-remote-access]] - SSH keys, tunnels, config
    - [[linux-security]] - Users, permissions, firewalls
    - [[docker-basics]] - Docker from Linux perspective

---

<div id="testing-qa"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#9090b8,#404068);box-shadow:0 0 8px rgba(144,144,184,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Testing & QA · 22 articles"

    - [[pytest-fundamentals]] - Test discovery, assertions, markers
    - [[pytest-fixtures-advanced]] - Fixtures, scope, parameterize
    - [[selenium-webdriver]] - Browser automation, locators
    - [[playwright-testing]] - Playwright API, auto-waiting
    - [[api-testing-requests]] - REST API testing patterns
    - [[page-object-model]] - POM pattern for UI tests
    - [[test-architecture]] - Testing pyramid, strategy
    - [[ci-cd-test-automation]] - Tests in CI/CD pipelines
    - [[allure-reporting]] - Allure test reports

---

<div id="rust"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#d89848,#784808);box-shadow:0 0 8px rgba(216,152,72,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Rust · 22 articles"

    - [[ownership-and-move-semantics]] - Ownership rules, moves
    - [[borrowing-and-references]] - Shared and mutable references
    - [[lifetimes]] - Lifetime annotations, elision
    - [[traits]] - Trait definitions, implementations, bounds
    - [[error-handling]] - Result, Option, ? operator
    - [[async-await]] - Tokio, async runtime, futures
    - [[concurrency]] - Arc, Mutex, channels, Send/Sync
    - [[smart-pointers]] - Box, Rc, RefCell patterns

---

<div id="ios-mobile"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#b080b0,#603060);box-shadow:0 0 8px rgba(176,128,176,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>iOS & Mobile · 21 articles"

    - [[swift-fundamentals]] - Swift syntax, types, optionals
    - [[swiftui-views-and-modifiers]] - View hierarchy, modifiers
    - [[swiftui-state-and-data-flow]] - @State, @Binding, ObservableObject
    - [[swiftui-navigation]] - NavigationStack, sheets, alerts
    - [[swiftdata-persistence]] - SwiftData models, queries
    - [[kotlin-android-fundamentals]] - Kotlin for Android

---

<div id="seo-marketing"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#80b868,#386020);box-shadow:0 0 8px rgba(128,184,104,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>SEO & Digital Marketing · 20 articles"

    - [[keyword-research-semantic-core]] - Keyword research methodology
    - [[technical-seo-audit]] - Technical SEO checklist
    - [[site-structure-urls]] - URL structure, canonicalization
    - [[link-building-strategy]] - Link acquisition tactics
    - [[core-web-vitals-performance]] - CWV optimization
    - [[seo-tools-workflow]] - Ahrefs, Semrush, GSC workflow

---

<div id="nodejs"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#58c098,#187048);box-shadow:0 0 8px rgba(88,192,152,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>Node.js · 16 articles"

    - [[event-loop-and-architecture]] - Event loop, libuv, phases
    - [[async-patterns]] - Callbacks, promises, async/await
    - [[streams]] - Readable, writable, transform streams
    - [[modules-and-packages]] - CommonJS, ESM, npm
    - [[error-handling]] - Error handling patterns
    - [[performance-optimization]] - Profiling, clustering

---

<div id="php"></div>

??? note "<span class="ks-planet" style="background:radial-gradient(circle at 35% 35%,rgba(255,255,255,0.4),transparent 60%),radial-gradient(circle at 50% 50%,#7090c0,#304070);box-shadow:0 0 8px rgba(112,144,192,0.5),inset 0 -2px 4px rgba(0,0,0,0.3)"></span>PHP & Laravel · 15 articles"

    - [[php-type-system]] - PHP 8 type system, enums
    - [[php-oop-fundamentals]] - Classes, interfaces, traits
    - [[laravel-architecture]] - Service container, providers
    - [[laravel-eloquent-orm]] - Models, relationships, queries
    - [[laravel-routing]] - Routes, middleware, controllers
    - [[laravel-authentication]] - Auth scaffolding, guards
