---
title: Kubernetes ConfigMaps & Secrets
category: orchestration
tags: [kubernetes, configmap, secrets, configuration, environment-variables, volumes]
---
# Kubernetes ConfigMaps & Secrets

Managing application configuration and sensitive data in Kubernetes clusters.

## Key Facts

- **ConfigMap** = key-value store for non-sensitive configuration data
- **Secret** = key-value store for sensitive data; base64-encoded (NOT encrypted by default)
- Both can be consumed as environment variables or mounted as files in pods
- ConfigMaps: plain text configs, feature flags, connection strings (non-secret)
- Secrets types: `Opaque` (generic), `kubernetes.io/tls` (TLS certs), `kubernetes.io/dockerconfigjson` (registry auth)
- Secrets are base64-encoded in etcd by default; enable **encryption at rest** for actual security
- ConfigMap/Secret changes don't auto-restart pods; need rollout restart or use reloader controllers
- **Immutable** ConfigMaps/Secrets (`immutable: true`) prevent accidental changes and improve performance
- [[kubernetes-pods]] consume ConfigMaps and Secrets via `envFrom`, `valueFrom`, or volume mounts
- [[helm-charts]] commonly template ConfigMaps and Secrets from values
- **External Secrets Operator** syncs secrets from AWS Secrets Manager, Azure Key Vault, HashiCorp Vault
- Maximum size: ConfigMap and Secret data must be < 1 MiB

## Patterns

```yaml
# ConfigMap from literal values
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "postgres.default.svc.cluster.local"
  DATABASE_PORT: "5432"
  LOG_LEVEL: "info"
  config.yaml: |
    server:
      port: 8080
      timeout: 30s
    features:
      beta_enabled: true

---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:                    # plaintext (K8s auto-encodes to base64)
  DATABASE_PASSWORD: "s3cret!"
  API_KEY: "sk-abc123def456"

---
# Pod consuming both
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0
    # Individual env vars from ConfigMap/Secret
    env:
    - name: DB_HOST
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: DATABASE_HOST
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: DATABASE_PASSWORD
    # All keys as env vars
    envFrom:
    - configMapRef:
        name: app-config
    - secretRef:
        name: app-secrets
    # Mount as files
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
      readOnly: true
  volumes:
  - name: config-volume
    configMap:
      name: app-config
      items:
      - key: config.yaml
        path: config.yaml
```

```bash
# Create from command line
kubectl create configmap app-config \
  --from-literal=DB_HOST=postgres \
  --from-file=config.yaml=./config.yaml

kubectl create secret generic app-secrets \
  --from-literal=DB_PASSWORD=s3cret! \
  --from-file=tls.crt=./cert.pem

# View (secrets are base64 encoded in output)
kubectl get configmap app-config -o yaml
kubectl get secret app-secrets -o yaml
kubectl get secret app-secrets -o jsonpath='{.data.DB_PASSWORD}' | base64 -d

# Trigger pod restart after config change
kubectl rollout restart deploy/myapp
```

## Gotchas

- Secrets are base64-encoded, NOT encrypted; anyone with RBAC access to Secrets can decode them
- Enable etcd encryption at rest: `EncryptionConfiguration` in kube-apiserver for actual security
- Env vars from ConfigMap/Secret are set at pod creation; changes require pod restart
- Volume-mounted ConfigMaps auto-update (kubelet sync period ~1 min); env vars do NOT
- `stringData` in Secret manifests is convenient but gets converted to base64 `data` on apply
- Deleting a ConfigMap/Secret that pods reference = pods fail to start (mount error)
- Secrets in Git are a security risk; use Sealed Secrets, SOPS, or External Secrets Operator
- ConfigMap keys become filenames when volume-mounted; keys with `/` create subdirectories

## See Also

- [[kubernetes-pods]] - pod specs that consume configs
- [[helm-charts]] - templating ConfigMaps in charts
- [[gitops]] - secret management in GitOps workflows
- [[ci-cd-pipelines]] - injecting secrets in build pipelines
- K8s ConfigMaps: https://kubernetes.io/docs/concepts/configuration/configmap/
- K8s Secrets: https://kubernetes.io/docs/concepts/configuration/secret/
