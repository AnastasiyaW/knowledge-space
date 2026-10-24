---
title: "Opérateurs Kubernetes"
category: concepts
tags: [kubernetes, operator, custom-resource, controller, automation]
level: 3
source_sha256: 163d4552c6a42431106a627155cafb9872e33b2e5b270c0a3a86e5b2d1138238
translation: machine
translated_at: '2026-10-24'
---
# Opérateurs Kubernetes {#kubernetes-operators}

Extensions logicielles qui utilisent des Custom Resources (CR) pour gérer les applications et leurs composants. Ils encodent les connaissances opérationnelles (installation, configuration, mise à jour, sauvegarde, bascule) dans du code.

## Points clés {#key-facts}

- Opérateur = Custom Resource Definition (CRD) + Contrôleur
- Le contrôleur surveille les CR et réconcilie l'état réel avec l'état souhaité
- Étend l'API Kubernetes avec des ressources spécifiques à un domaine
- Le pattern Operator a été introduit par CoreOS (2016) et est aujourd'hui un standard de l'industrie
- OperatorHub.io catalogue les opérateurs communautaires
- Operator Lifecycle Manager (OLM) gère l'installation et les mises à jour des opérateurs
- Niveaux de maturité : Installation de base -> Mises à jour transparentes -> Cycle de vie complet -> Analyses approfondies -> Pilote automatique

## Architecture {#architecture}

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

## Instance de Custom Resource {#custom-resource-instance}

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

## Logique du contrôleur (boucle de réconciliation) {#controller-logic-reconciliation-loop}

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

## Frameworks de développement d'opérateurs {#operator-development-frameworks}

| Framework | Langage | Maturité | Idéal pour |
|-----------|---------|----------|------------|
| Operator SDK | Go, Ansible, Helm | GA | Usage général |
| kubebuilder | Go | GA | Opérateurs natifs Go |
| KOPF | Python | Stable | Équipes Python |
| Metacontroller | Tout langage (webhooks) | Stable | Léger, tout langage |
| Shell-operator | Bash/scripts | Stable | Automatisation simple |

## Opérateurs populaires {#popular-operators}

| Opérateur | Gère | Fonctionnalités |
|-----------|------|-----------------|
| postgres-operator (Zalando) | PostgreSQL | HA, sauvegardes, pool de connexions |
| Strimzi | Apache Kafka | Gestion de clusters, topics, utilisateurs |
| Prometheus Operator | Pile de supervision | ServiceMonitor, AlertManager |
| Cert-Manager | Certificats TLS | Renouvellement automatique, ACME, Vault |
| ArgoCD | Déploiements GitOps | App-of-apps, sync waves |
| Rook | Stockage Ceph | Stockage bloc, objet, fichier |

## Choisir la stratégie de déploiement {#choosing-deployment-strategy}

```php
Plain YAML manifest     -> Simple, static deployment
      |
Helm chart              -> Templated config, versioned releases
      |
Operator                -> Lifecycle management, self-healing
      |
Operator + Custom Logic -> Domain-specific automation
```

Facteurs de décision :
- **YAML** : déploiements ponctuels, sans complexité opérationnelle
- **Helm** : déploiements paramétrables, charts communautaires disponibles
- **Operator** : applications avec état nécessitant sauvegarde/restauration, logique de mise à l'échelle, bascule

## Pièges courants {#gotchas}

- **Problème :** l'opérateur entre dans une boucle de réconciliation infinie (il crée une ressource, détecte un changement, la recrée) -> **Solution :** utiliser les owner references et vérifier si la ressource existe déjà avant de la créer. Définir `controllerutil.SetControllerReference()`.
- **Problème :** les modifications du schéma d'une CRD cassent les CR existantes -> **Solution :** utiliser des CRD versionnées (v1, v2) avec des webhooks de conversion. Ne jamais supprimer des champs obligatoires.
- **Problème :** l'opérateur dispose de permissions cluster-admin (risque de sécurité) -> **Solution :** appliquer le principe du moindre privilège : créer un ServiceAccount dédié avec un RBAC minimal. N'accorder l'accès qu'aux ressources gérées par l'opérateur.

## Voir aussi {#see-also}

- [[kubernetes-architecture]] - composants principaux de K8s
- [[helm-package-manager]] - alternative de packaging de déploiement
- [[kubernetes-workloads]] - StatefulSets, Deployments gérés par les opérateurs
- [[kubernetes-security]] - sécurisation des permissions des opérateurs
