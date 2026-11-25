---
title: "Deployment-Strategien"
category: concepts
tags: [devops, deployment, blue-green, canary, rolling-update, feature-flags, release-management]
level: 3
source_sha256: 97d120745594f5362e0120b2a5ac4687a5ffa52ebca3ea7f0518d7bd53410a4c
translation: machine
translated_at: '2026-10-24'
---
# Deployment-Strategien {#deployment-strategies}

Deployment-Strategien steuern, wie neue Anwendungsversionen alte ersetzen. Die Wahl beeinflusst Ausfallzeiten, Rollback-Geschwindigkeit, Ressourcenkosten und das Risiko.

## Rolling Update (Kubernetes-Standard) {#rolling-update-kubernetes-default}

Ersetzt alte Pods schrittweise durch neue. Ohne Ausfallzeit, sofern Health Checks konfiguriert sind.

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%         # max extra pods during update
    maxUnavailable: 25%   # max pods unavailable during update
```

```bash
kubectl set image deployment/app app=app:2.0
kubectl rollout status deployment/app
kubectl rollout undo deployment/app         # rollback
```

## Blue-Green-Deployment {#blue-green-deployment}

Zwei identische Umgebungen. Deployment in die inaktive Umgebung, Traffic nach der Validierung umschalten.

- **Blue** = aktuell stabile Version
- **Green** = neue Version
- Rollback = Traffic zurück auf die alte Umgebung leiten
- In K8s: zwei Deployments, der Selector des Service wechselt zwischen ihnen

**Vorteile**: sofortiger Rollback, vollständiges Testen vor dem Umschalten
**Nachteile**: doppelte Infrastrukturkosten

## Canary-Deployment {#canary-deployment}

Einen kleinen Prozentsatz des Traffics auf die neue Version leiten. Beobachten und dann schrittweise erhöhen.

Mit Kubernetes + Istio:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
spec:
  http:
  - route:
    - destination:
        host: app
        subset: v1
      weight: 90
    - destination:
        host: app
        subset: v2
      weight: 10
```

Ohne Service Mesh: mehrere Deployments mit unterschiedlicher Replica-Anzahl unter demselben Service verwenden.

**Vorteile**: geringes Risiko, schrittweise Validierung
**Nachteile**: erfordert die Fähigkeit zum Traffic-Splitting

## Feature Flags {#feature-flags}

Code mit deaktivierten Features deployen. Features schrittweise nach Benutzersegment aktivieren.

- Deployment von Release entkoppeln
- Kill Switch für problematische Features
- Progressive Rollout pro Benutzersegment
- Keine zusätzliche Infrastruktur erforderlich

## Release-Checkliste {#release-checklist}

- **Kapazitätsplanung**: erwartete Last, kann die Infrastruktur sie bewältigen
- **Integration**: Load Balancer konfiguriert, Monitoring bereit
- **Fehlerbehandlung**: Bewertung der Auswirkungen pro Komponente
- **Rollback-Plan**: definiert und getestet
- **Kommunikation**: Benachrichtigung der Stakeholder, Status-Seiten

## Release und Error Budget {#release-and-error-budget}

Aus SRE-Perspektive:
- Verbleibendes Error Budget -> schneller deployen, mehr Risiken eingehen
- Error Budget aufgebraucht -> Releases einfrieren, Fokus auf Zuverlässigkeit
- Kleinere Änderungen = geringeres Risiko (kleinerer Blast Radius)
- Automatisierte Rollback-Mechanismen sind verpflichtend

## Cloud-Native-15-Factor-Methodik {#cloud-native-15-factor-methodology}

Erweiterung der 12-Factor-App für Cloud-native Services:

1. Ein Codebase pro Service
2. API First: Vertrag vor Implementierung
3. Explizite Abhängigkeiten (pom.xml, package.json)
4. Strikte Trennung von Design, Build, Release und Run
5. Externalisierte Konfiguration (Umgebungsvariablen, Config-Server)
6. Logs als Event-Streams (stdout)
7. Schneller Start, sauberes Herunterfahren (Disposability)
8. Backing Services als angehängte Ressourcen
9. Environment Parity (Dev ~ Staging ~ Prod)
10. Admin-Prozesse als einmalige Tasks
11. Port Binding zum Bereitstellen des Service
12. Zustandslose Prozesse (Share-Nothing)
13. Skalierung über das Prozessmodell (Concurrency)
14. Telemetrie (Health, Performance, Business-Metriken)
15. Authentifizierung/Autorisierung als First-Class-Anliegen

## Stolperfallen {#gotchas}

- Rolling Updates können während des Übergangs Traffic mit gemischten Versionen erzeugen: Abwärtskompatibilität sicherstellen
- Blue-Green erfordert eine Datenbank-Migrationsstrategie bei Schema-Änderungen
- Canary setzt gute Observability voraus, um Probleme bei kleinen Traffic-Anteilen zu erkennen
- Feature Flags sammeln technische Schulden an, wenn sie nach dem Rollout nicht aufgeräumt werden
- Config-Rollback ist genauso wichtig wie Code-Rollback

## Siehe auch {#see-also}

- [[sre-principles]] - Error Budgets als Treiber der Deployment-Geschwindigkeit
- [[kubernetes-workloads]] - Deployment-Strategien in K8s
- [[service-mesh-istio]] - Traffic-Splitting für Canary
- [[helm-package-manager]] - versionierte Releases und Rollbacks
- [[gitops-and-argocd]] - automatisierte Deployments
