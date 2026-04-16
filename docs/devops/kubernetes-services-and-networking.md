---
title: Kubernetes Services and Networking
category: concepts
tags: [devops, kubernetes, services, ingress, load-balancer, dns, networking]
---

# Kubernetes Services and Networking

Services provide stable network access to dynamic sets of pods. Since pod IPs change on restart/scaling, Services offer persistent DNS names and IP addresses for reliable communication.

## Service Types

| Type | Scope | Use Case |
|------|-------|----------|
| **ClusterIP** (default) | Internal cluster only | Inter-service communication |
| **NodePort** | External via node IP:port (30000-32767) | Development/testing |
| **LoadBalancer** | External via cloud LB | Production external access |
| **ExternalName** | CNAME to external DNS | Connect to external services |

### Service YAML

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-svc
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
  - port: 80           # service port
    targetPort: 8080    # container port
    protocol: TCP
```

### DNS Resolution

Format: `<service-name>.<namespace>.svc.cluster.local`

Example: `app1.dev.svc.cluster.local`

### Headless Service

`clusterIP: None` - no load balancing, DNS returns individual pod IPs. Required for StatefulSets:

```text
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

### ExternalName Service

Maps to external DNS:
```yaml
spec:
  type: ExternalName
  externalName: mydb.mysql.database.azure.com
```

Application connects to service name, Kubernetes resolves to external DNS.

## Ingress

Layer 7 HTTP/HTTPS routing. Requires an Ingress Controller (NGINX, Traefik, Kong, HAProxy).

### Path-Based Routing

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-path-based
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /app1
        pathType: Prefix
        backend:
          service:
            name: app1-svc
            port:
              number: 80
      - path: /app2
        pathType: Prefix
        backend:
          service:
            name: app2-svc
            port:
              number: 80
```

### Host-Based Routing

```yaml
spec:
  ingressClassName: nginx
  rules:
  - host: app1.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app1-svc
            port:
              number: 80
  - host: app2.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app2-svc
            port:
              number: 80
```

### TLS/SSL with cert-manager

```bash
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true
```

ClusterIssuer for Let's Encrypt:
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

Ingress with TLS:
```yaml
metadata:
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - app1.example.com
    secretName: app1-tls
```

Certificate auto-renewed 30 days before expiry.

### NGINX Ingress Controller

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-basic --create-namespace
```

Traffic flow: Internet -> Cloud LB -> NGINX Ingress Controller pods -> Ingress rules -> Backend services -> Application pods.

### AWS ALB Ingress Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:...
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-redirect: "443"
```

Target type `ip` routes directly to pod IPs (bypasses NodePort).

## ExternalDNS

Automatically creates DNS records when Ingress resources are created. Watches Ingress for host entries, creates/updates A records. Removes records on Ingress deletion.

## Gotchas

- NodePort range is fixed: 30000-32767
- LoadBalancer type on bare metal requires MetalLB or similar
- AWS creates Classic LB by default - use annotation `service.beta.kubernetes.io/aws-load-balancer-type: nlb` for NLB
- Internal load balancer (Azure): `service.beta.kubernetes.io/azure-load-balancer-internal: "true"`
- Ingress requires an Ingress Controller to be installed - it does nothing on its own
- Name ports in services for clarity: `name: http`

## See Also

- [[kubernetes-architecture]] - cluster components
- [[kubernetes-workloads]] - pods, deployments, StatefulSets
- [[kubernetes-on-aks]] - Azure-specific networking
- [[kubernetes-on-eks]] - AWS-specific networking
- [[helm-package-manager]] - deploying ingress controllers
