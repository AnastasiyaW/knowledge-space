---
title: Kubernetes Security
category: concepts
tags: [kubernetes, security, rbac, pod-security, network-policy]
---

# Kubernetes Security

Multi-layered defense for Kubernetes clusters: authentication, authorization, admission control, network policies, pod security, runtime protection, and auditing.

## Key Facts

- Security applies at every layer: cluster, node, pod, container, network
- Authentication: who are you (certs, tokens, OIDC)
- Authorization: what can you do (RBAC, ABAC, webhook)
- Admission control: should this request be allowed (mutating + validating webhooks)
- Pod Security Standards (PSS): Privileged, Baseline, Restricted
- Pod Security Admission (PSA) replaced PodSecurityPolicies (removed in 1.25)
- MITRE ATT&CK for Kubernetes maps known attack techniques to detection/mitigation

## Authentication Methods

| Method | Use case | Security level |
|--------|----------|---------------|
| Client certificates (X.509) | Service-to-service, admin | High |
| Service account tokens | Pod-to-API server | Medium (auto-rotated) |
| OIDC tokens | Human users via IdP | High |
| Bootstrap tokens | Cluster join | Low (temporary) |
| Static tokens/basic auth | Legacy, testing only | Very low |

### Client Certificate Authentication

```bash
# Generate CSR for user
openssl genrsa -out user.key 2048
openssl req -new -key user.key -out user.csr -subj "/CN=username/O=group"

# Submit CSR to Kubernetes
kubectl certificate approve user-csr

# Configure kubeconfig
kubectl config set-credentials username \
  --client-certificate=user.crt \
  --client-key=user.key
```

## RBAC

```yaml
# Role: namespace-scoped permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]

---
# RoleBinding: grants Role to subject
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: production
  name: read-pods
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io

---
# ClusterRole + ClusterRoleBinding for cluster-wide permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
```

## Pod Security Standards

### Restricted (most secure)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
      requests:
        memory: "64Mi"
        cpu: "250m"
```

### Pod Security Admission Labels

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: production
spec:
  podSelector: {}  # applies to all pods
  policyTypes:
  - Ingress
  ingress: []  # empty = deny all

---
# Allow specific ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
```

## Securing Components

### API Server

```bash
# Key flags
--anonymous-auth=false
--authorization-mode=RBAC,Node
--enable-admission-plugins=NodeRestriction,PodSecurity
--audit-policy-file=/etc/kubernetes/audit-policy.yaml
--encryption-provider-config=/etc/kubernetes/encryption.yaml
--tls-cert-file=/etc/kubernetes/pki/apiserver.crt
```

### etcd

```bash
# Always encrypt, always TLS, restrict access
--cert-file=/etc/kubernetes/pki/etcd/server.crt
--key-file=/etc/kubernetes/pki/etcd/server.key
--client-cert-auth=true
--trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
```

### kubelet

```bash
--anonymous-auth=false
--authorization-mode=Webhook
--read-only-port=0
--protect-kernel-defaults=true
```

## Secrets Management

```yaml
# EncryptionConfiguration for etcd at-rest encryption
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    providers:
    - aescbc:
        keys:
        - name: key1
          secret: <base64-encoded-key>
    - identity: {}
```

For production: use external secrets management (HashiCorp Vault, AWS Secrets Manager, etc.)

## Security Scanning

| Tool | Scope | Use |
|------|-------|-----|
| Trivy | Images, IaC, SBOM | CI/CD image scanning |
| Cosign | Image signing | Supply chain security |
| kube-bench | CIS benchmark | Cluster hardening audit |
| Kubescape | NSA/CISA, MITRE | Comprehensive scanning |
| Falco | Runtime | Anomaly detection |
| OPA/Gatekeeper | Admission | Policy enforcement |

## Gotchas

- **Issue:** Default service account has too many permissions -> **Fix:** Create dedicated service accounts per workload. Set `automountServiceAccountToken: false` when API access not needed.
- **Issue:** Network policies have no effect -> **Fix:** Network policies require a CNI plugin that supports them (Calico, Cilium, Weave). Default kubenet does NOT enforce NetworkPolicy.
- **Issue:** Secrets stored as base64 in etcd (not encrypted) -> **Fix:** Enable etcd encryption at rest. Better: use external secrets operator (e.g., External Secrets Operator with Vault).
- **Issue:** Container running as root by default -> **Fix:** Always set `runAsNonRoot: true` and `runAsUser: <non-zero>`. Use distroless or scratch base images.

## See Also

- [[kubernetes-architecture]] - cluster components
- [[kubernetes-services-and-networking]] - service exposure
- [[monitoring-and-observability]] - security monitoring
- [[container-registries]] - image security
