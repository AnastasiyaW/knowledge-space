---
title: "Sécurité de Kubernetes"
category: concepts
tags: [kubernetes, security, rbac, pod-security, network-policy]
level: 3
source_sha256: ce54ed00217b20525b0c140116ef64cc977f2b2ee880c7784489b7b54983cf58
translation: machine
translated_at: '2026-10-24'
---
# Sécurité de Kubernetes {#kubernetes-security}

Défense multicouche pour les clusters Kubernetes : authentification, autorisation, contrôle d'admission, network policies, sécurité des pods, protection à l'exécution et audit.

## Points clés {#key-facts}

- La sécurité s'applique à chaque couche : cluster, nœud, pod, conteneur, réseau
- Authentification : qui êtes-vous (certificats, jetons, OIDC)
- Autorisation : que pouvez-vous faire (RBAC, ABAC, webhook)
- Contrôle d'admission : cette requête doit-elle être autorisée (webhooks de mutation + de validation)
- Pod Security Standards (PSS) : Privileged, Baseline, Restricted
- Pod Security Admission (PSA) a remplacé les PodSecurityPolicies (supprimées en 1.25)
- MITRE ATT&CK pour Kubernetes associe les techniques d'attaque connues à la détection et à l'atténuation

## Méthodes d'authentification {#authentication-methods}

| Méthode | Cas d'usage | Niveau de sécurité |
|---------|-------------|--------------------|
| Certificats client (X.509) | Service à service, administration | Élevé |
| Jetons de compte de service | Pod vers serveur API | Moyen (rotation automatique) |
| Jetons OIDC | Utilisateurs humains via un IdP | Élevé |
| Jetons d'amorçage | Adhésion au cluster | Faible (temporaire) |
| Jetons statiques / basic auth | Héritage, tests uniquement | Très faible |

### Authentification par certificat client {#client-certificate-authentication}

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

### Restricted (le plus sécurisé) {#restricted-most-secure}

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

### Labels Pod Security Admission {#pod-security-admission-labels}

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

## Sécurisation des composants {#securing-components}

### Serveur API {#api-server}

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

## Gestion des secrets {#secrets-management}

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

En production : utilisez une gestion externe des secrets (HashiCorp Vault, AWS Secrets Manager, etc.)

## Analyse de sécurité {#security-scanning}

| Outil | Périmètre | Usage |
|-------|-----------|-------|
| Trivy | Images, IaC, SBOM | Analyse des images en CI/CD |
| Cosign | Signature d'images | Sécurité de la chaîne d'approvisionnement |
| kube-bench | Benchmark CIS | Audit de durcissement du cluster |
| Kubescape | NSA/CISA, MITRE | Analyse complète |
| Falco | Exécution | Détection d'anomalies |
| OPA/Gatekeeper | Admission | Application des politiques |

## Pièges courants {#gotchas}

- **Problème :** Le compte de service par défaut dispose de trop de permissions -> **Correctif :** Créez un compte de service dédié par charge de travail. Définissez `automountServiceAccountToken: false` lorsque l'accès à l'API n'est pas nécessaire.
- **Problème :** Les network policies n'ont aucun effet -> **Correctif :** Les network policies nécessitent un plugin CNI qui les prend en charge (Calico, Cilium, Weave). Le kubenet par défaut n'applique PAS NetworkPolicy.
- **Problème :** Les secrets sont stockés en base64 dans etcd (non chiffrés) -> **Correctif :** Activez le chiffrement au repos pour etcd. Mieux : utilisez un opérateur de secrets externe (par exemple External Secrets Operator avec Vault).
- **Problème :** Le conteneur s'exécute en root par défaut -> **Correctif :** Définissez systématiquement `runAsNonRoot: true` et `runAsUser: <non nul>`. Utilisez des images de base distroless ou scratch.

## Voir aussi {#see-also}

- [[kubernetes-architecture]] - composants du cluster
- [[kubernetes-services-and-networking]] - exposition des services
- [[monitoring-and-observability]] - supervision de la sécurité
- [[container-registries]] - sécurité des images
