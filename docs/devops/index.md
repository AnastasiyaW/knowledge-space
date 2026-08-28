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

## Additional References

- [[comfyui-container-build]] - Patterns for building production-grade ComfyUI Docker images: distutils conflict resolution, layer
- [[container-security-scanning]] - Automated detection of vulnerabilities, misconfigurations, and secrets in container images, IaC
- [[kubernetes-operators]] - Software extensions that use Custom Resources (CRs) to manage applications and their components
- [[kubernetes-security]] - Multi-layered defense for Kubernetes clusters: authentication, authorization, admission control
- [[kustomize]] - Template-free customization of Kubernetes YAML configurations
- [[libvirt-kvm-networking]] - Diagnosing and fixing intermittent connection drops on KVM guests using virbr0 NAT
- [[observability-query-languages]] - Reference for the three main observability query languages - Prometheus PromQL for metrics, Grafana
- [[ois-multi-environment-task-monitoring-architecture]] - The OIS infrastructure utilizes a uniform monorepo deployment across staging and production
- [[runpod-flash-gpu-serverless]] - RunPod Flash is an open-source Python SDK (MIT license, v1.16.0) that enables the deployment of
- [[runpod-production]] - Reference for deploying GPU workloads on RunPod: deploy type selection, image strategy tiers
- [[runpod-serverless-diagnostic-image]] - Serverless workers die silently
- [[runpod-serverless-observability-limits]] - RunPod Serverless workers are difficult to debug not because of one missing feature but because
- [[runpod-serverless-python-silent-exit-1]] - Analysis and mitigation of silent worker crashes (exit code 1) during task pickup on RunPod
- [[runpod-serverless-silent-worker-crashes-on-task-pickup]] - Workers in a serverless environment may spawn as "Ready," pick up a task, and then die silently
- [[runpod-serverless-stuck-queue-idle-workers]] - Symptom: health endpoint shows idle > 0 or ready > 0, queue depth is positive, inProgress = 0, and
- [[tunnel-architecture]] - Exposing VM-hosted or NAT-ed services to the public internet without opening inbound firewall ports
