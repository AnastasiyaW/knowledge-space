---
title: Kubernetes Services & Ingress
category: orchestration
tags: [kubernetes, services, ingress, clusterip, nodeport, loadbalancer, networking]
---
# Kubernetes Services & Ingress

Service types, DNS resolution, Ingress controllers, and traffic routing in Kubernetes.

## Key Facts

- **Service** = stable network endpoint that routes traffic to a set of pods (selected by labels)
- **ClusterIP** (default) = internal cluster IP; reachable only within the cluster
- **NodePort** = exposes service on each node's IP at a static port (30000-32767)
- **LoadBalancer** = provisions cloud load balancer (AWS ELB, Azure LB, GCP LB); superset of NodePort
- **ExternalName** = maps service to external DNS name (CNAME record)
- Kubernetes DNS: `service-name.namespace.svc.cluster.local` resolves to ClusterIP
- **Ingress** = HTTP/HTTPS routing rules (path-based, host-based); requires an Ingress Controller
- Popular Ingress controllers: NGINX Ingress, Traefik, AWS ALB Ingress, Istio Gateway
- **Endpoints** object auto-populated with pod IPs matching the Service selector
- Services use `kube-proxy` (iptables/IPVS mode) for load balancing across pods
- [[kubernetes-pods]] define the labels that Services select on
- [[helm-charts]] commonly template Service and Ingress resources
- **Headless Service** (`clusterIP: None`) = no load balancing; returns pod IPs directly (for StatefulSets)

## Patterns

```yaml
# ClusterIP Service (internal only)
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
  - port: 80            # Service port
    targetPort: 8080     # Container port
    protocol: TCP

---
# LoadBalancer Service (external access)
apiVersion: v1
kind: Service
metadata:
  name: web-public
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 443
    targetPort: 8443

---
# Ingress with path-based routing
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

```bash
# Service operations
kubectl get svc
kubectl describe svc api-service
kubectl get endpoints api-service      # see which pods are backing the service

# Test service DNS from within cluster
kubectl run test --rm -it --image=busybox -- nslookup api-service
kubectl run test --rm -it --image=busybox -- wget -qO- http://api-service:80/health

# Port forward for local debugging
kubectl port-forward svc/api-service 8080:80

# Ingress operations
kubectl get ingress
kubectl describe ingress app-ingress
```

## Gotchas

- Service selector must match pod labels exactly; typo in label = no endpoints = no traffic
- NodePort range is limited (30000-32767); cannot use standard ports like 80/443
- LoadBalancer creates cloud resources that cost money; clean up with `kubectl delete svc`
- Ingress does nothing without an Ingress Controller installed in the cluster
- `targetPort` can be a port name (from pod spec), not just a number - useful for avoiding port conflicts
- DNS resolution uses `namespace` - cross-namespace access: `service.other-namespace.svc.cluster.local`
- Session affinity (`sessionAffinity: ClientIP`) needed for stateful connections; default is round-robin
- ExternalName services don't support ports - they just create DNS CNAME records

## See Also

- [[kubernetes-pods]] - workloads that Services route to
- [[microservices-architecture]] - service-to-service communication
- [[deployment-strategies]] - traffic shifting for canary/blue-green
- [[monitoring-observability]] - service-level metrics
- K8s Services: https://kubernetes.io/docs/concepts/services-networking/service/
- K8s Ingress: https://kubernetes.io/docs/concepts/services-networking/ingress/
