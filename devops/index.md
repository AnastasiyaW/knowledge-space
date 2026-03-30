---
title: DevOps & Infrastructure - Knowledge Base Index
type: MOC
---
# DevOps & Infrastructure - Knowledge Base

Reference knowledge base for containers, orchestration, CI/CD, cloud platforms, IaC, SRE, and observability.

## Containers

- [[docker-images-containers]] - Dockerfile, multi-stage builds, image layers, registries, runtime
- [[docker-compose]] - multi-container YAML definition, services, volumes, healthchecks
- [[docker-networking]] - bridge, host, overlay networks, port mapping, DNS resolution

## Kubernetes

- [[kubernetes-pods]] - Pods, Deployments, ReplicaSets, StatefulSets, DaemonSets, kubectl
- [[kubernetes-services]] - ClusterIP, NodePort, LoadBalancer, Ingress, DNS, traffic routing
- [[kubernetes-config-secrets]] - ConfigMaps, Secrets, env vars, volume mounts, encryption at rest
- [[helm-charts]] - chart structure, values, templating, repositories, releases, rollback

## CI/CD & GitOps

- [[ci-cd-pipelines]] - GitHub Actions, GitLab CI, Jenkins, pipeline-as-code, artifacts
- [[gitops]] - ArgoCD, FluxCD, pull-based deployment, drift detection, App of Apps
- [[deployment-strategies]] - rolling update, blue-green, canary, Argo Rollouts, zero-downtime

## Infrastructure as Code

- [[terraform-iac]] - HCL, providers, state, modules, plan/apply, remote backends
- [[ansible-configuration]] - playbooks, roles, inventory, modules, idempotency, Jinja2

## Cloud Platforms

- [[aws-core-services]] - EC2, S3, IAM, VPC, RDS, EKS, ECR, ELB, Route53
- [[azure-aks]] - AKS, ACR, managed identity, node pools, Azure DevOps

## SRE & Operations

- [[sre-sli-slo-sla]] - SLI/SLO/SLA, error budgets, DORA metrics, toil
- [[monitoring-observability]] - Prometheus, Grafana, PromQL, alerting, USE/RED/Golden Signals
- [[incident-management]] - on-call, severity levels, postmortems, runbooks, MTTR

## Architecture

- [[microservices-architecture]] - service design, API gateway, service mesh, circuit breaker, saga

## Quick Reference by Task

| Task | Entry | Key Tools |
|------|-------|-----------|
| Build container image | [[docker-images-containers]] | `docker build`, Dockerfile |
| Run multi-container app | [[docker-compose]] | `docker compose up` |
| Deploy to Kubernetes | [[kubernetes-pods]] | `kubectl apply`, Deployment YAML |
| Expose service externally | [[kubernetes-services]] | Service, Ingress |
| Manage K8s config/secrets | [[kubernetes-config-secrets]] | ConfigMap, Secret |
| Package K8s manifests | [[helm-charts]] | `helm install/upgrade` |
| Automate build/test/deploy | [[ci-cd-pipelines]] | GitHub Actions, GitLab CI |
| Git-driven deployments | [[gitops]] | ArgoCD, FluxCD |
| Safe rollouts | [[deployment-strategies]] | Rolling, canary, blue-green |
| Provision infrastructure | [[terraform-iac]] | `terraform plan/apply` |
| Configure servers | [[ansible-configuration]] | `ansible-playbook` |
| AWS infrastructure | [[aws-core-services]] | `aws` CLI, EC2, S3, EKS |
| Azure Kubernetes | [[azure-aks]] | `az aks`, ACR |
| Define reliability targets | [[sre-sli-slo-sla]] | SLO, error budget |
| Monitor and alert | [[monitoring-observability]] | Prometheus, Grafana |
| Handle incidents | [[incident-management]] | On-call, postmortem |
| Design distributed systems | [[microservices-architecture]] | API gateway, service mesh |
