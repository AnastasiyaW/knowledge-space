---
title: "Kubernetes Operators"
category: concepts
tags: [kubernetes, operator, custom-resource, controller, automation]
level: 3
source_sha256: 163d4552c6a42431106a627155cafb9872e33b2e5b270c0a3a86e5b2d1138238
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes Operators {#kubernetes-operators}

Softwareerweiterungen, die Custom Resources (CRs) nutzen, um Anwendungen und deren Komponenten zu verwalten. Kodiert operatives Wissen (Installation, Konfiguration, Upgrade, Backup, Failover) in Code.

## Key Facts {#key-facts}

- Operator = Custom Resource Definition (CRD) + Controller
- Controller überwacht CRs und gleicht den tatsächlichen Zustand mit dem Soll-Zustand ab
- Erweitert die Kubernetes-API um domänenspezifische Ressourcen
- Operator-Muster von CoreOS geprägt (2016), inzwischen Industriestandard
- OperatorHub.io katalogisiert Community-Operatoren
- Operator Lifecycle Manager (OLM) verwaltet Installation und Upgrades von Operatoren
- Reifegradstufen: Basic Install -> Seamless Upgrades -> Full Lifecycle -> Deep Insights -> Auto Pilot

## Architektur {#architecture}

```sql
User creates/updates CR -> API Server stores CR -> Controller detects change
    -> Controller reconciles (create pods, update config, run backup, etc.)
    -> Controller updates CR status
```

## Custom Resource Definition {#custom-resource-definition}

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

## Custom-Resource-Instanz {#custom-resource-instance}

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

## Controller-Logik (Reconciliation Loop) {#controller-logic-reconciliation-loop}

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

## Frameworks zur Operator-Entwicklung {#operator-development-frameworks}

| Framework | Sprache | Reife | Geeignet für |
|-----------|----------|----------|----------|
| Operator SDK | Go, Ansible, Helm | GA | Allgemeiner Einsatz |
| kubebuilder | Go | GA | Go-native Operatoren |
| KOPF | Python | Stabil | Python-Teams |
| Metacontroller | Beliebig (Webhooks) | Stabil | Leichtgewichtig, beliebige Sprache |
| Shell-operator | Bash/Skripte | Stabil | Einfache Automatisierung |

## Beliebte Operatoren {#popular-operators}

| Operator | Verwaltet | Funktionen |
|----------|----------|----------|
| postgres-operator (Zalando) | PostgreSQL | HA, Backups, Connection Pooling |
| Strimzi | Apache Kafka | Clusterverwaltung, Topics, Benutzer |
| Prometheus Operator | Monitoring-Stack | ServiceMonitor, AlertManager |
| Cert-Manager | TLS-Zertifikate | Automatische Erneuerung, ACME, Vault |
| ArgoCD | GitOps-Deployments | App-of-Apps, Sync Waves |
| Rook | Ceph-Storage | Block-, Object- und File-Storage |

## Wahl der Deployment-Strategie {#choosing-deployment-strategy}

```php
Plain YAML manifest     -> Simple, static deployment
      |
Helm chart              -> Templated config, versioned releases
      |
Operator                -> Lifecycle management, self-healing
      |
Operator + Custom Logic -> Domain-specific automation
```

Entscheidungsfaktoren:
- **YAML**: einmalige Deployments, keine operative Komplexität
- **Helm**: parametrisierte Deployments, Community-Charts verfügbar
- **Operator**: zustandsbehaftete Anwendungen mit Bedarf an Backup/Restore, Skalierungslogik, Failover

## Fallstricke {#gotchas}

- **Problem:** Operator in endloser Reconciliation-Schleife (erstellt Ressource, erkennt Änderung, erstellt erneut) -> **Lösung:** Owner References verwenden und vor dem Erstellen prüfen, ob die Ressource bereits existiert. `controllerutil.SetControllerReference()` setzen.
- **Problem:** Schema-Änderungen an CRDs brechen bestehende CRs -> **Lösung:** Versionierte CRDs (v1, v2) mit Conversion Webhooks verwenden. Pflichtfelder niemals entfernen.
- **Problem:** Operator hat cluster-admin-Berechtigungen (Sicherheitsrisiko) -> **Lösung:** Least-Privilege-Prinzip befolgen: dedizierten ServiceAccount mit minimalen RBAC-Regeln anlegen. Nur Zugriff auf die vom Operator verwalteten Ressourcen gewähren.

## Siehe auch {#see-also}

- [[kubernetes-architecture]] - zentrale K8s-Komponenten
- [[helm-package-manager]] - alternative Paketierung für Deployments
- [[kubernetes-workloads]] - StatefulSets, Deployments, die Operatoren verwalten
- [[kubernetes-security]] - Absicherung der Operator-Berechtigungen
