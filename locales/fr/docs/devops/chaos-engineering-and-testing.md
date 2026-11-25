---
title: "Ingénierie du chaos et tests de fiabilité"
category: concepts
tags: [devops, sre, chaos-engineering, testing, load-testing, resilience]
level: 3
source_sha256: e87b42779c733a99bb68a5f0a86859d5f484f3f473dced37d66ae4448341d48a
translation: machine
translated_at: '2026-10-24'
---
# Ingénierie du chaos et tests de fiabilité {#chaos-engineering-and-reliability-testing}

Les tests de fiabilité valident le comportement d'un système sous contrainte et en cas de défaillance. L'ingénierie du chaos injecte délibérément des défaillances afin de découvrir les faiblesses avant qu'elles ne provoquent des interruptions de service.

## Pyramide des tests d'infrastructure {#infrastructure-testing-pyramid}

1. **Validation de la configuration** (unitaire) - vérifications de syntaxe, validation de schéma
2. **Intégration d'infrastructure** - tests d'interaction entre services
3. **Niveau système** - validation de la pile complète
4. **Chaos** - injection de défaillances

## Types de tests de fiabilité {#reliability-testing-types}

| Type | Objectif | Outils |
|------|----------|--------|
| **Test de charge** | Charge attendue soutenue, vérification des SLO | k6, Locust, JMeter |
| **Test de stress** | Au-delà de la charge attendue, recherche du point de rupture | k6, Gatling |
| **Test d'endurance** | Durée prolongée, détection des fuites et de l'épuisement des ressources | k6, personnalisé |
| **Ingénierie du chaos** | Injection de défaillances, vérification de la résilience | Chaos Monkey, Litmus, Gremlin |

## Ingénierie du chaos {#chaos-engineering}

### Prérequis {#prerequisites}

1. Processus de gestion des incidents opérationnel
2. Culture d'apprentissage des erreurs (sans recherche de coupable)
3. Confiance au sein de l'organisation
4. Bonne observabilité et supervision

### Principes {#principles}

1. Définir l'état stable (valeurs normales des SLI)
2. Émettre l'hypothèse que l'état stable se maintient pendant l'expérience
3. Introduire des événements réalistes (arrêt d'un pod, partition réseau, disque plein)
4. Chercher à invalider l'hypothèse
5. Minimiser le rayon d'impact (commencer petit, disposer d'un interrupteur d'arrêt automatisé)

### Outils {#tools}

- **Chaos Monkey** (Netflix) - arrête aléatoirement des instances
- **Litmus** - chaos natif pour Kubernetes
- **Gremlin** - plateforme SaaS de chaos
- **PowerfulSeal** - injection de défaillances de pods et de nœuds K8s

## Exercices de type Game Day {#game-days}

Exercices de fiabilité planifiés, simulant de véritables incidents :

1. Définir le scénario et le périmètre
2. Prévenir les équipes concernées
3. Exécuter la défaillance simulée
4. Observer la réaction des équipes
5. Faire le bilan et documenter les enseignements

Cadence régulière (mensuelle ou trimestrielle). Ces exercices permettent de tester les runbooks, les alertes et la communication.

## Outils de test d'infrastructure {#infrastructure-testing-tools}

### InSpec (conformité) {#inspec-compliance}

```ruby
control 'sshd-8' do
  impact 0.6
  title 'Server: Configure the service port'
  describe sshd_config do
    its('Port') { should cmp 22 }
  end
end
```

### Testinfra (Python + Pytest) {#testinfra-python-pytest}

```python
def test_access(host):
    addr = host.addr("google.com")
    assert addr.is_resolvable
    assert addr.port(443).is_reachable
```

### Validation de la configuration {#configuration-validation}

```bash
nginx -t -c nginx.conf
terraform validate
ansible --check
kubectl apply --dry-run=client -f deploy.yml
yamllint file.yaml
python -m json.tool sample.json
```

## Patterns de résilience {#resilience-patterns}

### Circuit Breaker {#circuit-breaker}

Trois états : CLOSED (normal) -> OPEN (échec immédiat) -> HALF-OPEN (sonde de rétablissement).

```java
@CircuitBreaker(name = "service", fallbackMethod = "fallback")
public Response callService() { ... }
```

### Load Shedding {#load-shedding}

Rejeter les requêtes lorsque la capacité est atteinte. Renvoyer un 503. Mieux vaut servir 80 % des requêtes avec succès que 100 % lentement.

### Limitation de débit (Rate Limiting) {#rate-limiting}

- Par client (token bucket, fenêtre glissante)
- Globale (compteur distribué dans Redis)
- Adaptative (ajustement selon la charge courante)
- Propagation de la contre-pression (back-pressure)

### Dégradation gracieuse (Graceful Degradation) {#graceful-degradation}

- Renvoyer des données en cache ou périmées lorsque le backend est indisponible
- Désactiver les fonctionnalités non critiques sous charge
- Files d'attente prioritaires pour le traitement des requêtes

## Métriques de performance {#performance-metrics}

### APDEX (Application Performance Index) {#apdex-application-performance-index}

Indice standardisé de satisfaction des utilisateurs : Satisfait (<T), Tolérant (T-4T), Frustré (>4T).

Score = (Satisfaits + Tolérants/2) / Total. Valeurs comprises entre 0 et 1.

### Percentiles plutôt que moyennes {#percentiles-over-averages}

p50, p95, p99 pour la latence. Les moyennes masquent les valeurs aberrantes et la latence de queue.

## Pièges à éviter {#gotchas}

- Pratiquer l'ingénierie du chaos sans réponse aux incidents opérationnelle est irresponsable
- Un rayon d'impact trop large transforme l'expérience en interruption réelle
- Les tests de charge doivent inclure des données et des schémas d'accès réalistes
- Les tests d'endurance sont souvent omis, alors qu'ils détectent les fuites mémoire que les tests courts manquent
- `siege -c 50 -t 30s http://localhost:80` pour un test de charge rapide

## Voir aussi {#see-also}

- [[sre-principles]] - budgets d'erreur et objectifs de fiabilité
- [[sre-incident-management]] - réponse aux incidents éprouvée par le chaos
- [[monitoring-and-observability]] - détection de l'impact des expériences de chaos
- [[service-mesh-istio]] - circuit breaking, nouvelles tentatives et délais d'expiration
