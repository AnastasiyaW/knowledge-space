---
title: "Kubernetes-Services und Networking"
category: concepts
tags: [devops, kubernetes, services, ingress, load-balancer, dns, networking]
level: 3
source_sha256: 549f44f067cea4a91ba932178c7f8e20ac2f470e9207eeeade5925d50df2514e
translation: machine
translated_at: '2026-10-24'
---
# Kubernetes-Services und Networking {#kubernetes-services-and-networking}

Services bieten stabilen Netzwerkzugriff auf dynamische Mengen von Pods. Da sich Pod-IPs bei Neustarts und Skalierung ändern, stellen Services dauerhafte DNS-Namen und IP-Adressen für zuverlässige Kommunikation bereit.

## Service-Typen {#service-types}

| Typ | Geltungsbereich | Anwendungsfall |
|------|-------|----------|
| **ClusterIP** (Standard) | Nur innerhalb des Clusters | Kommunikation zwischen Services |
| **NodePort** | Extern über Node-IP:Port (30000-32767) | Entwicklung/Tests |
| **LoadBalancer** | Extern über Cloud-LB | Externer Zugriff in Produktion |
| **ExternalName** | CNAME auf externen DNS-Eintrag | Anbindung externer Services |

### Service-YAML {#service-yaml}

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

### DNS-Auflösung {#dns-resolution}

Format: `<service-name>.<namespace>.svc.cluster.local`

Beispiel: `app1.dev.svc.cluster.local`

### Headless Service {#headless-service}

`clusterIP: None` - kein Load Balancing, DNS liefert die einzelnen Pod-IPs zurück. Für StatefulSets erforderlich:

```text
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

### ExternalName-Service {#externalname-service}

Verweist auf einen externen DNS-Namen:
```yaml
spec:
  type: ExternalName
  externalName: mydb.mysql.database.azure.com
```

Die Anwendung verbindet sich mit dem Service-Namen, Kubernetes löst ihn auf den externen DNS-Namen auf.

## Ingress {#ingress}

HTTP/HTTPS-Routing auf Layer 7. Erfordert einen Ingress Controller (NGINX, Traefik, Kong, HAProxy).

### Pfadbasiertes Routing {#path-based-routing}

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

### Hostbasiertes Routing {#host-based-routing}

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

### TLS/SSL mit cert-manager {#tlsssl-with-cert-manager}

```bash
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true
```

ClusterIssuer für Let's Encrypt:
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

Ingress mit TLS:
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

Das Zertifikat wird 30 Tage vor Ablauf automatisch erneuert.

### NGINX Ingress Controller {#nginx-ingress-controller}

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-basic --create-namespace
```

Traffic-Fluss: Internet -> Cloud-LB -> NGINX-Ingress-Controller-Pods -> Ingress-Regeln -> Backend-Services -> Application-Pods.

### AWS ALB Ingress Controller {#aws-alb-ingress-controller}

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

Der Zieltyp `ip` leitet Anfragen direkt an Pod-IPs weiter (umgeht NodePort).

## ExternalDNS {#externaldns}

Erstellt DNS-Einträge automatisch, sobald Ingress-Ressourcen angelegt werden. Überwacht Ingress-Ressourcen auf Host-Einträge und erstellt bzw. aktualisiert A-Records. Entfernt die Einträge beim Löschen des Ingress wieder.

## Stolpersteine {#gotchas}

- Der NodePort-Bereich ist fest: 30000-32767
- Der Typ LoadBalancer auf Bare-Metal erfordert MetalLB oder ein ähnliches Werkzeug
- AWS erstellt standardmäßig einen Classic LB - für einen NLB die Annotation `service.beta.kubernetes.io/aws-load-balancer-type: nlb` verwenden
- Interner Load Balancer (Azure): `service.beta.kubernetes.io/azure-load-balancer-internal: "true"`
- Ingress benötigt einen installierten Ingress Controller - allein bewirkt er nichts
- Ports in Services zur besseren Übersicht benennen: `name: http`

## Siehe auch {#see-also}

- [[kubernetes-architecture]] - Cluster-Komponenten
- [[kubernetes-workloads]] - Pods, Deployments, StatefulSets
- [[kubernetes-on-aks]] - Azure-spezifisches Networking
- [[kubernetes-on-eks]] - AWS-spezifisches Networking
- [[helm-package-manager]] - Deployment von Ingress Controllern
