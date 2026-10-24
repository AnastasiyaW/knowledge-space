---
title: "Supervision et observabilité"
category: concepts
tags: [devops, monitoring, observability, prometheus, grafana, alerting, sli, golden-signals]
level: 3
source_sha256: 18d9986c7530f89ac571c3b66ccac62fd667ae124127a2f1532e217d118ad469
translation: machine
translated_at: '2026-10-24'
---
# Supervision et observabilité {#monitoring-and-observability}

La supervision répond à « qu'est-ce qui est cassé ? » (symptômes) et « pourquoi ? » (causes). L'observabilité consiste à construire un système sur lequel on peut poser n'importe quelle question et découvrir de nouvelles corrélations. Objectif : maximiser le signal, minimiser le bruit.

## Quatre signaux d'or {#four-golden-signals}

1. **Latence** - temps nécessaire pour traiter les requêtes. Distinguer la latence des requêtes réussies de celle des requêtes échouées
2. **Trafic** - charge subie par le système (requêtes/s, transactions/s)
3. **Erreurs** - taux de requêtes échouées (erreurs 5xx explicites + réponses lentes implicites)
4. **Saturation** - niveau de « remplissage » du service (CPU, mémoire, E/S, profondeur des files d'attente)

### Mesurer la saturation {#measuring-saturation}

- Déterminer un seuil de latence acceptable (par ex. 200 ms)
- La saturation peut être causée par la dégradation du matériel, et pas seulement par la charge
- Motif en dents de scie : une saturation périodique (par ex. la fusion d'index Elasticsearch) provoque des chutes de débit suivies de pics

## Trois piliers de l'observabilité {#three-pillars-of-observability}

| Pilier | Contenu | Outils |
|--------|---------|--------|
| **Journalisation** | Ce qui s'est passé | Loki, ELK, CloudWatch Logs |
| **Métriques** | Performance du système | Prometheus, CloudWatch, Datadog |
| **Traçage** | Parcours des requêtes entre services | Jaeger, Tempo, Zipkin |

## Prometheus {#prometheus}

Collecte de métriques de séries temporelles en mode pull :

```yaml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
```

Requêtes PromQL : `rate(http_server_requests_seconds_count[5m])`, `jvm_memory_used_bytes{area="heap"}`

Découverte de services : Kubernetes, Consul, basée sur des fichiers. Alertmanager gère le routage, le regroupement et la mise en sourdine des alertes.

## Grafana {#grafana}

Plateforme de visualisation pour les données de Prometheus, Loki, Tempo et Elasticsearch :

- Importer des tableaux de bord prêts à l'emploi (par ex. Node Exporter Full : ID 1860)
- Panneaux : graphique, statistique, jauge, tableau
- Variables de tableau de bord pour le filtrage
- Règles d'alerte avec points de contact (e-mail, Slack, PagerDuty)

### Grafana + Loki (journalisation centralisée) {#grafana-loki-centralized-logging}

Loki n'indexe que les labels (et non le contenu), ce qui le rend bien plus léger qu'ELK :

```yaml
LogQL: {container_name="accounts"} |= "error"
Rate:  rate({container_name="accounts"}[5m])
```

L'agent Promtail lit les fichiers de logs sur chaque nœud et les envoie à Loki.

### Grafana Tempo (traçage distribué) {#grafana-tempo-distributed-tracing}

Reçoit les traces via OTLP. Visualise le parcours des requêtes sous forme de diagramme en cascade. Lien depuis les logs Loki vers les traces Tempo grâce à la corrélation par traceId.

## OpenTelemetry {#opentelemetry}

Standard d'instrumentation indépendant des fournisseurs pour les traces, les métriques et les logs. Chaque requête reçoit :
- **traceId** - unique pour toute la chaîne de requêtes
- **spanId** - unique pour chaque saut entre services

L'en-tête W3C Trace Context est propagé automatiquement entre les services.

## SLI, SLO, SLA {#sli-slo-sla}

### SLI (Service Level Indicator) {#sli-service-level-indicator}
Mesure quantitative : latence p95/p99, disponibilité en %, taux d'erreurs, débit. Mesurée à la frontière exposée à l'utilisateur.

### SLO (Service Level Objective) {#slo-service-level-objective}
Cible pour un SLI : « 99,9 % des requêtes en moins de 200 ms sur 30 jours ». Objectif interne d'ingénierie.

### SLA (Service Level Agreement) {#sla-service-level-agreement}
SLO + conséquences (remboursements, avoirs). Généralement moins exigeant que le SLO.

### Budget d'erreur {#error-budget}
`100 % - SLO = budget d'erreur`. SLO de 99,9 % = budget de 0,1 %, soit 43,2 min/mois. Budget épuisé : geler les mises en production et se concentrer sur la fiabilité. Budget restant : déployer plus rapidement.

## Cycle de vie d'un problème {#problem-lifecycle}

`OK -> Soft -> Hard -> Notify -> Escalate -> Acknowledge -> Resolve`

- Chaque notification doit mener à une action
- Alertes via différents canaux : e-mail, SMS, messagerie instantanée (livraison hors bande)
- Le contexte doit être joint à chaque alerte

## Philosophie d'alerte {#alerting-philosophy}

- Alerter sur les **symptômes**, et non sur les causes (impact utilisateur, et non utilisation du CPU)
- Chaque alerte doit être **actionnable**
- Chaque astreinte doit exiger une **intervention humaine** pour être résolue
- Distinguer ce qui relève d'un ticket de ce qui justifie une astreinte
- Multi-fenêtres, multi-taux de consommation : consommation rapide = astreinte, consommation lente = ticket

## Sources de données pour les SLI {#data-sources-for-sli}

- **Métriques applicatives** : implémentées dans le code. Elles entrent en concurrence avec les tâches principales pour les ressources
- **API d'infrastructure** : cloud, WAF, équipements réseau. Très détaillées, avec des données historiques. Elles ignorent la logique applicative
- **Supervision tierce** : perspective externe. Utile pour valider les SLA
- **Sondes synthétiques** : contrôles en boîte noire simulant le comportement de l'utilisateur

## Supervision spécifique au cloud {#cloud-specific-monitoring}

### AWS CloudWatch {#aws-cloudwatch}

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "HighCPU" \
  --metric-name "CPUUtilization" \
  --namespace "AWS/EC2" \
  --statistic "Average" \
  --period 300 --threshold 80 \
  --comparison-operator "GreaterThanThreshold" \
  --alarm-actions arn:aws:sns:us-east-1:123456:alert-topic
```

### Azure Monitor (Container Insights) {#azure-monitor-container-insights}

Requêtes KQL sur les logs de conteneurs, les métriques et les données de performance. Agent OMS déployé en DaemonSet sur chaque nœud.

## Pièges {#gotchas}

- Supervision != observabilité. La supervision vérifie les problèmes connus ; l'observabilité permet de découvrir les inconnues
- Préférer les percentiles (p50, p95, p99) aux moyennes pour la latence, car les moyennes masquent les valeurs extrêmes
- APDEX (Application Performance Index) standardise la satisfaction des utilisateurs : Satisfait (<T), Tolérant (T-4T), Frustré (>4T)
- Spring Boot : `spring-boot-starter-actuator` + `micrometer-registry-prometheus` pour `/actuator/prometheus`
- Le taux de consommation du budget d'erreur mesure la vitesse à laquelle le budget est consommé ; un seul incident peut consommer plusieurs minutes de budget

## Voir aussi {#see-also}

- [[sre-principles]] - philosophie SRE qui guide les choix de supervision
- [[sre-incident-management]] - astreinte, escalade, post-mortems
- [[kubernetes-resource-management]] - metrics server pour le HPA
- [[service-mesh-istio]] - observabilité au niveau du maillage
