---
title: "DevOps & Infrastruktur"
type: MOC
level: 3
source_sha256: 3cf572791cbd9ea242c56c339f3aafee74141dfd3a365671b414f93c0685d186
translation: machine
translated_at: '2026-10-24'
---
# DevOps & Infrastruktur {#devops-infrastructure}

Umfassende Referenz zu Docker, Kubernetes, CI/CD, Terraform, Cloud-Plattformen, Monitoring, SRE-Praktiken und Rechenzentrumsnetzwerken.

## Containers & Docker {#containers-docker}

- [[docker-fundamentals]] - Container, Images, Volumes, Networking, Lebenszyklus
- [[dockerfile-and-image-building]] - Dockerfile-Syntax, Multi-Stage-Builds, Optimierung
- [[docker-compose]] - Orchestrierung mehrerer Container, Service Discovery
- [[docker-for-ml]] - ML-spezifische Docker-Muster, JupyterLab, MLflow, Model Runner

## Kubernetes {#kubernetes}

- [[kubernetes-architecture]] - Control Plane, Worker Nodes, CNI, Cluster-Deployment
- [[kubernetes-workloads]] - Pods, Deployments, StatefulSets, DaemonSets, ConfigMaps, Secrets
- [[kubernetes-services-and-networking]] - Services, Ingress, TLS, cert-manager, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass, CSI-Treiber, Cloud-Storage
- [[kubernetes-resource-management]] - Requests, Limits, QoS, Namespaces, Quotas, HPA, Autoscaling
- [[kubernetes-on-aks]] - Azure AKS, ACR, Azure AD, Monitoring, Virtual Nodes
- [[kubernetes-on-eks]] - AWS EKS, ECR, EBS/EFS, ALB Ingress Controller

## Paketverwaltung & Templating {#package-management-templating}

- [[helm-package-manager]] - Charts, Templates, Hooks, Releases, Repositories, Secrets

## CI/CD & Automatisierung {#cicd-automation}

- [[cicd-pipelines]] - GitHub Actions, Azure DevOps, Pipeline-Stufen, Multi-Environment
- [[jenkins-automation]] - Jenkinsfile, Shared Libraries, Docker-Agents, Credentials
- [[gitops-and-argocd]] - ArgoCD, Sync Waves, App-of-Apps, Sealed Secrets, Crossplane

## Infrastructure as Code {#infrastructure-as-code}

- [[terraform-iac]] - HCL, State, Module, Workspaces, Cloud-Provider
- [[ansible-configuration-management]] - Playbooks, Rollen, Inventory, Idempotenz

## Cloud-Plattformen {#cloud-platforms}

- [[aws-cloud-fundamentals]] - IAM, VPC, EC2, S3, CloudWatch, ECR, App Runner
- [[container-registries]] - Docker Hub, ECR, ACR, GAR, Nexus

## Monitoring & Observability {#monitoring-observability}

- [[monitoring-and-observability]] - Golden Signals, Prometheus, Grafana, Loki, Tempo, SLI/SLO/SLA

## SRE-Praktiken {#sre-practices}

- [[sre-principles]] - Kultur, Error Budgets, Toil, Team-Modelle
- [[sre-incident-management]] - Bereitschaftsdienst, Postmortems, Eskalation, Diagnose
- [[sre-automation-and-toil]] - Automatisierungsreife, Tools, Workflow-Automatisierung
- [[chaos-engineering-and-testing]] - Chaos Engineering, Lasttests, Game Days, Resilienzmuster

## Deployment & Release {#deployment-release}

- [[deployment-strategies]] - Rolling Update, Blue-Green, Canary, Feature Flags, 15-Factor-Methodik
- [[service-mesh-istio]] - Istio, Envoy, Traffic Management, mTLS, Observability

## Architekturmuster {#architecture-patterns}

- [[microservices-patterns]] - Spring Cloud, API Gateway, Service Discovery, ereignisgesteuert, OAuth2
- [[datacenter-network-design]] - CLOS/Leaf-Spine, VXLAN, EVPN, BGP, Multi-Site

## Grundlagen {#foundations}

- [[devops-culture-and-sdlc]] - DevOps-Prinzipien, Agile/Scrum, SDLC, Tool-Landschaft
- [[git-version-control]] - Git-Workflow, Branching-Strategien, Monorepo vs. Multirepo
- [[linux-server-administration]] - Dateisystem, Prozesse, Networking, SSH, systemd, Scripting

## Weitere Referenzen {#additional-references}

- [[comfyui-container-build]] - Muster für den Bau produktionsreifer ComfyUI-Docker-Images: Auflösung von distutils-Konflikten, Layer
- [[container-security-scanning]] - Automatisierte Erkennung von Schwachstellen, Fehlkonfigurationen und Secrets in Container-Images, IaC
- [[kubernetes-operators]] - Softwareerweiterungen, die Custom Resources (CRs) nutzen, um Anwendungen und deren Komponenten zu verwalten
- [[kubernetes-security]] - Mehrschichtige Verteidigung für Kubernetes-Cluster: Authentifizierung, Autorisierung, Admission Control
- [[kustomize]] - Templatefreie Anpassung von Kubernetes-YAML-Konfigurationen
- [[libvirt-kvm-networking]] - Diagnose und Behebung sporadischer Verbindungsabbrüche bei KVM-Gästen mit virbr0-NAT
- [[observability-query-languages]] - Referenz zu den drei wichtigsten Observability-Abfragesprachen: Prometheus PromQL für Metriken, Grafana
- [[ois-multi-environment-task-monitoring-architecture]] - Die OIS-Infrastruktur nutzt ein einheitliches Monorepo-Deployment für Staging und Produktion
- [[runpod-flash-gpu-serverless]] - RunPod Flash ist ein Open-Source-Python-SDK (MIT-Lizenz, v1.16.0), das die Bereitstellung von
- [[runpod-production]] - Referenz zur Bereitstellung von GPU-Workloads auf RunPod: Auswahl des Deploy-Typs, Image-Strategie-Stufen
- [[runpod-serverless-diagnostic-image]] - Serverless-Worker sterben stillschweigend
- [[runpod-serverless-observability-limits]] - RunPod-Serverless-Worker sind schwer zu debuggen, nicht wegen eines fehlenden Features, sondern weil
- [[runpod-serverless-python-silent-exit-1]] - Analyse und Gegenmaßnahmen für stille Worker-Abstürze (Exit-Code 1) bei der Task-Übernahme auf RunPod
- [[runpod-serverless-silent-worker-crashes-on-task-pickup]] - Worker in einer Serverless-Umgebung können als "Ready" starten, einen Task übernehmen und dann stillschweigend sterben
- [[runpod-serverless-stuck-queue-idle-workers]] - Symptom: Health-Endpoint zeigt idle > 0 oder ready > 0, Queue-Tiefe ist positiv, inProgress = 0, und
- [[tunnel-architecture]] - Veröffentlichung von VM-gehosteten oder NAT-ten Diensten im öffentlichen Internet, ohne eingehende Firewall-Ports zu öffnen
