---
title: DevOps & Infrastructure
type: MOC
---

# DevOps & Infrastructure

Comprehensive reference covering Docker, Kubernetes, CI/CD, Terraform, cloud platforms, monitoring, SRE practices, and data center networking.

## Containers & Docker

- [[docker-fundamentals]] - containers, images, volumes, networking, lifecycle
- [[dockerfile-and-image-building]] - Dockerfile syntax, multi-stage builds, optimization
- [[docker-compose]] - multi-container orchestration, service discovery
- [[docker-for-ml]] - ML-specific Docker patterns, JupyterLab, MLflow, Model Runner

## Kubernetes

- [[kubernetes-architecture]] - control plane, worker nodes, CNI, cluster deployment
- [[kubernetes-workloads]] - Pods, Deployments, StatefulSets, DaemonSets, ConfigMaps, Secrets
- [[kubernetes-services-and-networking]] - Services, Ingress, TLS, cert-manager, DNS
- [[kubernetes-storage]] - PV, PVC, StorageClass, CSI drivers, cloud storage
- [[kubernetes-resource-management]] - requests, limits, QoS, namespaces, quotas, HPA, autoscaling
- [[kubernetes-on-aks]] - Azure AKS, ACR, Azure AD, monitoring, virtual nodes
- [[kubernetes-on-eks]] - AWS EKS, ECR, EBS/EFS, ALB Ingress Controller

## Package Management & Templating

- [[helm-package-manager]] - charts, templates, hooks, releases, repositories, secrets

## CI/CD & Automation

- [[cicd-pipelines]] - GitHub Actions, Azure DevOps, pipeline stages, multi-environment
- [[jenkins-automation]] - Jenkinsfile, shared libraries, Docker agents, credentials
- [[gitops-and-argocd]] - ArgoCD, sync waves, app-of-apps, Sealed Secrets, Crossplane

## Infrastructure as Code

- [[terraform-iac]] - HCL, state, modules, workspaces, cloud providers
- [[ansible-configuration-management]] - playbooks, roles, inventory, idempotency

## Cloud Platforms

- [[aws-cloud-fundamentals]] - IAM, VPC, EC2, S3, CloudWatch, ECR, App Runner
- [[container-registries]] - Docker Hub, ECR, ACR, GAR, Nexus

## Monitoring & Observability

- [[monitoring-and-observability]] - Golden Signals, Prometheus, Grafana, Loki, Tempo, SLI/SLO/SLA

## SRE Practices

- [[sre-principles]] - culture, error budgets, toil, team models
- [[sre-incident-management]] - on-call, postmortems, escalation, diagnostics
- [[sre-automation-and-toil]] - automation maturity, tools, workflow automation
- [[chaos-engineering-and-testing]] - chaos engineering, load testing, game days, resilience patterns

## Deployment & Release

- [[deployment-strategies]] - rolling update, blue-green, canary, feature flags, 15-factor methodology
- [[service-mesh-istio]] - Istio, Envoy, traffic management, mTLS, observability

## Architecture Patterns

- [[microservices-patterns]] - Spring Cloud, API Gateway, service discovery, event-driven, OAuth2
- [[datacenter-network-design]] - CLOS/leaf-spine, VXLAN, EVPN, BGP, multi-site

## Foundations

- [[devops-culture-and-sdlc]] - DevOps principles, Agile/Scrum, SDLC, tools landscape
- [[git-version-control]] - Git workflow, branching strategies, monorepo vs multirepo
- [[linux-server-administration]] - filesystem, processes, networking, SSH, systemd, scripting
