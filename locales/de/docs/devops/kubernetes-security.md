---
title: "Kubernetes-Sicherheit"
category: concepts
tags: [kubernetes, security, rbac, pod-security, network-policy]
level: 3
source_sha256: ce54ed00217b20525b0c140116ef64cc977f2b2ee880c7784489b7b54983cf58
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes-Sicherheit {#kubernetes-security}

Mehrschichtige Verteidigung für Kubernetes-Cluster: Authentifizierung, Autorisierung, Admission Control, Network Policies, Pod-Sicherheit, Laufzeitschutz und Auditing.

## Wichtige Fakten {#key-facts}

- Sicherheit gilt auf jeder Ebene: Cluster, Node, Pod, Container, Netzwerk
- Authentifizierung: Wer bist du (Zertifikate, Tokens, OIDC)
- Autorisierung: Was darfst du tun (RBAC, ABAC, Webhook)
- Admission Control: Soll diese Anfrage erlaubt werden (Mutating- und Validating-Webhooks)
- Pod Security Standards (PSS): Privileged, Baseline, Restricted
- Pod Security Admission (PSA) hat PodSecurityPolicies ersetzt (in 1.25 entfernt)
- MITRE ATT&CK for Kubernetes ordnet bekannte Angriffstechniken Erkennung und Gegenmaßnahmen zu

## Authentifizierungsmethoden {#authentication-methods}

| Methode | Anwendungsfall | Sicherheitsniveau |
|--------|----------|---------------|
| Client-Zertifikate (X.509) | Service-zu-Service, Administratoren | Hoch |
| Service-Account-Tokens | Pod-zu-API-Server | Mittel (automatisch rotiert) |
| OIDC-Tokens | Menschliche Benutzer über IdP | Hoch |
| Bootstrap-Tokens | Cluster-Join | Niedrig (temporär) |
| Statische Tokens/Basic Auth | Legacy, nur Tests | Sehr niedrig |

### Authentifizierung mit Client-Zertifikaten {#client-certificate-authentication}

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

## RBAC {#rbac}

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

## Pod Security Standards {#pod-security-standards}

### Restricted (am sichersten) {#restricted-most-secure}

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

### Pod Security Admission Labels {#pod-security-admission-labels}

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

## Network Policies {#network-policies}

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

## Absicherung der Komponenten {#securing-components}

### API-Server {#api-server}

```bash
# Key flags
--anonymous-auth=false
--authorization-mode=RBAC,Node
--enable-admission-plugins=NodeRestriction,PodSecurity
--audit-policy-file=/etc/kubernetes/audit-policy.yaml
--encryption-provider-config=/etc/kubernetes/encryption.yaml
--tls-cert-file=/etc/kubernetes/pki/apiserver.crt
```

### etcd {#etcd}

```bash
# Always encrypt, always TLS, restrict access
--cert-file=/etc/kubernetes/pki/etcd/server.crt
--key-file=/etc/kubernetes/pki/etcd/server.key
--client-cert-auth=true
--trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
```

### kubelet {#kubelet}

```bash
--anonymous-auth=false
--authorization-mode=Webhook
--read-only-port=0
--protect-kernel-defaults=true
```

## Verwaltung von Secrets {#secrets-management}

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

Für Produktivumgebungen: externe Secrets-Verwaltung verwenden (HashiCorp Vault, AWS Secrets Manager usw.)

## Security Scanning {#security-scanning}

| Tool | Umfang | Verwendung |
|------|-------|-----|
| Trivy | Images, IaC, SBOM | Image-Scanning in CI/CD |
| Cosign | Image-Signierung | Supply-Chain-Sicherheit |
| kube-bench | CIS-Benchmark | Prüfung der Cluster-Härtung |
| Kubescape | NSA/CISA, MITRE | Umfassendes Scanning |
| Falco | Laufzeit | Erkennung von Anomalien |
| OPA/Gatekeeper | Admission | Durchsetzung von Richtlinien |

## Fallstricke {#gotchas}

- **Problem:** Standard-Service-Account hat zu viele Berechtigungen -> **Lösung:** Dedizierte Service Accounts pro Workload anlegen. `automountServiceAccountToken: false` setzen, wenn kein API-Zugriff benötigt wird.
- **Problem:** Network Policies haben keine Wirkung -> **Lösung:** Network Policies benötigen ein CNI-Plugin, das sie unterstützt (Calico, Cilium, Weave). Das Standard-Netzwerk kubenet erzwingt NetworkPolicy NICHT.
- **Problem:** Secrets werden in etcd als Base64 gespeichert (nicht verschlüsselt) -> **Lösung:** Verschlüsselung von etcd at Rest aktivieren. Besser: External Secrets Operator mit Vault verwenden (z. B. External Secrets Operator mit Vault).
- **Problem:** Container läuft standardmäßig als root -> **Lösung:** Immer `runAsNonRoot: true` und `runAsUser: <non-zero>` setzen. Distroless- oder Scratch-Basis-Images verwenden.

## Siehe auch {#see-also}

- [[kubernetes-architecture]] - Cluster-Komponenten
- [[kubernetes-services-and-networking]] - Service-Bereitstellung
- [[monitoring-and-observability]] - Sicherheitsüberwachung
- [[container-registries]] - Image-Sicherheit
