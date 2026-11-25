---
title: "DevOps et infrastructure"
type: MOC
level: 3
source_sha256: 3cf572791cbd9ea242c56c339f3aafee74141dfd3a365671b414f93c0685d186
translation: machine
translated_at: '2026-10-24'
---
# DevOps et infrastructure {#devops-infrastructure}

Référence complète couvrant Docker, Kubernetes, CI/CD, Terraform, les plateformes cloud, la supervision, les pratiques SRE et la conception des réseaux de datacenter.

## Conteneurs et Docker {#containers-docker}

- [[docker-fundamentals]] - conteneurs, images, volumes, réseau, cycle de vie
- [[dockerfile-and-image-building]] - syntaxe des Dockerfile, builds multi-étapes, optimisation
- [[docker-compose]] - orchestration multi-conteneurs, découverte de services
- [[docker-for-ml]] - patterns Docker spécifiques au ML, JupyterLab, MLflow, Model Runner

## Kubernetes {#kubernetes}

- [[kubernetes-architecture]] - plan de contrôle, nœuds workers, CNI, déploiement de cluster
- [[kubernetes-workloads]] - Pods, Deployments, StatefulSets, DaemonSets, ConfigMaps, Secrets
- [[kubernetes-services-and-networking]] - Services, Ingress, TLS, cert-manager, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass, pilotes CSI, stockage cloud
- [[kubernetes-resource-management]] - requests, limits, QoS, namespaces, quotas, HPA, autoscaling
- [[kubernetes-on-aks]] - Azure AKS, ACR, Azure AD, supervision, nœuds virtuels
- [[kubernetes-on-eks]] - AWS EKS, ECR, EBS/EFS, ALB Ingress Controller

## Gestion de paquets et templating {#package-management-templating}

- [[helm-package-manager]] - charts, templates, hooks, releases, dépôts, secrets

## CI/CD et automatisation {#cicd-automation}

- [[cicd-pipelines]] - GitHub Actions, Azure DevOps, étapes de pipeline, multi-environnements
- [[jenkins-automation]] - Jenkinsfile, bibliothèques partagées, agents Docker, identifiants
- [[gitops-and-argocd]] - ArgoCD, sync waves, app-of-apps, Sealed Secrets, Crossplane

## Infrastructure as Code {#infrastructure-as-code}

- [[terraform-iac]] - HCL, state, modules, workspaces, fournisseurs cloud
- [[ansible-configuration-management]] - playbooks, rôles, inventaire, idempotence

## Plateformes cloud {#cloud-platforms}

- [[aws-cloud-fundamentals]] - IAM, VPC, EC2, S3, CloudWatch, ECR, App Runner
- [[container-registries]] - Docker Hub, ECR, ACR, GAR, Nexus

## Supervision et observabilité {#monitoring-observability}

- [[monitoring-and-observability]] - Golden Signals, Prometheus, Grafana, Loki, Tempo, SLI/SLO/SLA

## Pratiques SRE {#sre-practices}

- [[sre-principles]] - culture, budgets d'erreur, toil, modèles d'équipe
- [[sre-incident-management]] - astreinte, post-mortems, escalade, diagnostic
- [[sre-automation-and-toil]] - maturité de l'automatisation, outils, automatisation des workflows
- [[chaos-engineering-and-testing]] - chaos engineering, tests de charge, game days, patterns de résilience

## Déploiement et mise en production {#deployment-release}

- [[deployment-strategies]] - rolling update, blue-green, canary, feature flags, méthodologie 15-factor
- [[service-mesh-istio]] - Istio, Envoy, gestion du trafic, mTLS, observabilité

## Patterns d'architecture {#architecture-patterns}

- [[microservices-patterns]] - Spring Cloud, API Gateway, découverte de services, event-driven, OAuth2
- [[datacenter-network-design]] - CLOS/leaf-spine, VXLAN, EVPN, BGP, multi-site

## Fondations {#foundations}

- [[devops-culture-and-sdlc]] - principes DevOps, Agile/Scrum, SDLC, panorama des outils
- [[git-version-control]] - workflow Git, stratégies de branchement, monorepo vs multirepo
- [[linux-server-administration]] - système de fichiers, processus, réseau, SSH, systemd, scripting

## Références complémentaires {#additional-references}

- [[comfyui-container-build]] - Patterns pour construire des images Docker ComfyUI de niveau production : résolution des conflits distutils, couches
- [[container-security-scanning]] - Détection automatisée des vulnérabilités, des mauvaises configurations et des secrets dans les images de conteneurs, IaC
- [[kubernetes-operators]] - Extensions logicielles qui utilisent des Custom Resources (CR) pour gérer les applications et leurs composants
- [[kubernetes-security]] - Défense multicouche pour les clusters Kubernetes : authentification, autorisation, contrôle d'admission
- [[kustomize]] - Personnalisation des configurations YAML Kubernetes sans templates
- [[libvirt-kvm-networking]] - Diagnostic et correction des coupures de connexion intermittentes sur les invités KVM utilisant le NAT virbr0
- [[observability-query-languages]] - Référence des trois principaux langages de requête d'observabilité - PromQL de Prometheus pour les métriques, Grafana
- [[ois-multi-environment-task-monitoring-architecture]] - L'infrastructure OIS utilise un déploiement monorepo uniforme entre staging et production
- [[runpod-flash-gpu-serverless]] - RunPod Flash est un SDK Python open source (licence MIT, v1.16.0) qui permet le déploiement de
- [[runpod-production]] - Référence pour le déploiement de charges GPU sur RunPod : choix du type de déploiement, niveaux de stratégie d'image
- [[runpod-serverless-diagnostic-image]] - Les workers serverless meurent silencieusement
- [[runpod-serverless-observability-limits]] - Les workers RunPod Serverless sont difficiles à déboguer non pas à cause d'une fonctionnalité manquante, mais parce que
- [[runpod-serverless-python-silent-exit-1]] - Analyse et atténuation des crashs silencieux de workers (code de sortie 1) lors de la prise en charge d'une tâche sur RunPod
- [[runpod-serverless-silent-worker-crashes-on-task-pickup]] - Les workers d'un environnement serverless peuvent démarrer en "Ready", prendre une tâche, puis mourir silencieusement
- [[runpod-serverless-stuck-queue-idle-workers]] - Symptôme : le endpoint de santé affiche idle > 0 ou ready > 0, la profondeur de file est positive, inProgress = 0, et
- [[tunnel-architecture]] - Exposition de services hébergés sur VM ou derrière NAT sur l'internet public, sans ouvrir de ports entrants sur le pare-feu
