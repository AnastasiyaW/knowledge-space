---
title: "Services et réseau Kubernetes"
category: concepts
tags: [devops, kubernetes, services, ingress, load-balancer, dns, networking]
level: 3
source_sha256: 549f44f067cea4a91ba932178c7f8e20ac2f470e9207eeeade5925d50df2514e
translation: machine
translated_at: '2026-10-24'
---
# Services et réseau Kubernetes {#kubernetes-services-and-networking}

Les Services offrent un accès réseau stable à des ensembles dynamiques de pods. Les adresses IP des pods changeant à chaque redémarrage ou mise à l'échelle, les Services fournissent des noms DNS et des adresses IP persistants pour une communication fiable.

## Types de Service {#service-types}

| Type | Portée | Cas d'usage |
|------|-------|----------|
| **ClusterIP** (par défaut) | Interne au cluster uniquement | Communication inter-services |
| **NodePort** | Externe via IP:port du nœud (30000-32767) | Développement/tests |
| **LoadBalancer** | Externe via load balancer cloud | Accès externe en production |
| **ExternalName** | CNAME vers un DNS externe | Connexion à des services externes |

### YAML du Service {#service-yaml}

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

### Résolution DNS {#dns-resolution}

Format : `<service-name>.<namespace>.svc.cluster.local`

Exemple : `app1.dev.svc.cluster.local`

### Service headless {#headless-service}

`clusterIP: None` - pas d'équilibrage de charge, le DNS renvoie les adresses IP individuelles des pods. Requis pour les StatefulSets :

```text
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

### Service ExternalName {#externalname-service}

Correspondance avec un DNS externe :
```yaml
spec:
  type: ExternalName
  externalName: mydb.mysql.database.azure.com
```

L'application se connecte au nom du service, et Kubernetes le résout vers le DNS externe.

## Ingress {#ingress}

Routage HTTP/HTTPS de couche 7. Nécessite un contrôleur Ingress (NGINX, Traefik, Kong, HAProxy).

### Routage basé sur le chemin {#path-based-routing}

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

### Routage basé sur l'hôte {#host-based-routing}

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

### TLS/SSL avec cert-manager {#tlsssl-with-cert-manager}

```bash
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true
```

ClusterIssuer pour Let's Encrypt :
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

Ingress avec TLS :
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

Le certificat est renouvelé automatiquement 30 jours avant son expiration.

### Contrôleur Ingress NGINX {#nginx-ingress-controller}

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-basic --create-namespace
```

Flux de trafic : Internet -> Load balancer cloud -> pods du contrôleur Ingress NGINX -> règles Ingress -> services backend -> pods applicatifs.

### Contrôleur Ingress AWS ALB {#aws-alb-ingress-controller}

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

Le type de cible `ip` route directement vers les adresses IP des pods (contourne NodePort).

## ExternalDNS {#externaldns}

Crée automatiquement les enregistrements DNS lorsque des ressources Ingress sont créées. Surveille les Ingress pour les entrées d'hôte, crée et met à jour les enregistrements A. Supprime les enregistrements à la suppression de l'Ingress.

## Points d'attention {#gotchas}

- La plage NodePort est fixe : 30000-32767
- Le type LoadBalancer sur bare metal nécessite MetalLB ou un outil équivalent
- AWS crée un Classic LB par défaut - utilisez l'annotation `service.beta.kubernetes.io/aws-load-balancer-type: nlb` pour un NLB
- Load balancer interne (Azure) : `service.beta.kubernetes.io/azure-load-balancer-internal: "true"`
- Un Ingress nécessite l'installation d'un contrôleur Ingress - il ne fait rien seul
- Nommez les ports dans les services pour plus de clarté : `name: http`

## Voir aussi {#see-also}

- [[kubernetes-architecture]] - composants du cluster
- [[kubernetes-workloads]] - pods, deployments, StatefulSets
- [[kubernetes-on-aks]] - réseau spécifique à Azure
- [[kubernetes-on-eks]] - réseau spécifique à AWS
- [[helm-package-manager]] - déploiement des contrôleurs ingress
