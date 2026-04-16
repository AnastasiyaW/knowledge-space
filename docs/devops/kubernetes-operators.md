---
title: Kubernetes Operators
category: concepts
tags: [kubernetes, operator, custom-resource, controller, automation]
---

# Kubernetes Operators

Software extensions that use Custom Resources (CRs) to manage applications and their components. Encodes operational knowledge (install, configure, upgrade, backup, failover) in code.

## Key Facts

- Operator = Custom Resource Definition (CRD) + Controller
- Controller watches CRs and reconciles actual state with desired state
- Extends Kubernetes API with domain-specific resources
- Operator pattern coined by CoreOS (2016), now industry standard
- OperatorHub.io catalogs community operators
- Operator Lifecycle Manager (OLM) manages operator installation and upgrades
- Maturity levels: Basic Install -> Seamless Upgrades -> Full Lifecycle -> Deep Insights -> Auto Pilot

## Architecture

```sql
User creates/updates CR -> API Server stores CR -> Controller detects change
    -> Controller reconciles (create pods, update config, run backup, etc.)
    -> Controller updates CR status
```

## Custom Resource Definition

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.example.com
spec:
  group: example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                engine:
                  type: string
                  enum: ["postgres", "mysql"]
                version:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                storage:
                  type: string
            status:
              type: object
              properties:
                phase:
                  type: string
                ready:
                  type: boolean
      subresources:
        status: {}
  scope: Namespaced
  names:
    plural: databases
    singular: database
    kind: Database
    shortNames:
      - db
```

## Custom Resource Instance

```yaml
apiVersion: example.com/v1
kind: Database
metadata:
  name: my-postgres
  namespace: production
spec:
  engine: postgres
  version: "16"
  replicas: 3
  storage: 100Gi
```

## Controller Logic (Reconciliation Loop)

```go
// Simplified operator reconciliation in Go (Operator SDK / kubebuilder)
func (r *DatabaseReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. Fetch the CR
    db := &v1.Database{}
    if err := r.Get(ctx, req.NamespacedName, db); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // 2. Check current state
    existing := &appsv1.StatefulSet{}
    err := r.Get(ctx, types.NamespacedName{
        Name: db.Name, Namespace: db.Namespace,
    }, existing)

    if errors.IsNotFound(err) {
        // 3. Create resources if not found
        sts := r.buildStatefulSet(db)
        if err := r.Create(ctx, sts); err != nil {
            return ctrl.Result{}, err
        }
    } else {
        // 4. Update if spec changed
        if existing.Spec.Replicas != &db.Spec.Replicas {
            existing.Spec.Replicas = &db.Spec.Replicas
            if err := r.Update(ctx, existing); err != nil {
                return ctrl.Result{}, err
            }
        }
    }

    // 5. Update CR status
    db.Status.Phase = "Running"
    db.Status.Ready = true
    r.Status().Update(ctx, db)

    return ctrl.Result{}, nil
}
```

## Operator Development Frameworks

| Framework | Language | Maturity | Best for |
|-----------|----------|----------|----------|
| Operator SDK | Go, Ansible, Helm | GA | General purpose |
| kubebuilder | Go | GA | Go-native operators |
| KOPF | Python | Stable | Python teams |
| Metacontroller | Any (webhooks) | Stable | Lightweight, any language |
| Shell-operator | Bash/scripts | Stable | Simple automation |

## Popular Operators

| Operator | Manages | Features |
|----------|---------|----------|
| postgres-operator (Zalando) | PostgreSQL | HA, backups, connection pooling |
| Strimzi | Apache Kafka | Cluster management, topics, users |
| Prometheus Operator | Monitoring stack | ServiceMonitor, AlertManager |
| Cert-Manager | TLS certificates | Auto-renewal, ACME, Vault |
| ArgoCD | GitOps deployments | App-of-apps, sync waves |
| Rook | Ceph storage | Block, object, file storage |

## Choosing Deployment Strategy

```php
Plain YAML manifest     -> Simple, static deployment
      |
Helm chart              -> Templated config, versioned releases
      |
Operator                -> Lifecycle management, self-healing
      |
Operator + Custom Logic -> Domain-specific automation
```

Decision factors:
- **YAML**: one-off deployments, no operational complexity
- **Helm**: parameterized deployments, community charts available
- **Operator**: stateful apps needing backup/restore, scaling logic, failover

## Gotchas

- **Issue:** Operator in infinite reconciliation loop (creates resource, detects change, creates again) -> **Fix:** Use owner references and check if resource already exists before creating. Set `controllerutil.SetControllerReference()`.
- **Issue:** CRD schema changes break existing CRs -> **Fix:** Use versioned CRDs (v1, v2) with conversion webhooks. Never remove required fields.
- **Issue:** Operator has cluster-admin permissions (security risk) -> **Fix:** Follow least privilege: create dedicated ServiceAccount with minimal RBAC. Only grant access to resources the operator manages.

## See Also

- [[kubernetes-architecture]] - core K8s components
- [[helm-package-manager]] - alternative deployment packaging
- [[kubernetes-workloads]] - StatefulSets, Deployments operators manage
- [[kubernetes-security]] - securing operator permissions
