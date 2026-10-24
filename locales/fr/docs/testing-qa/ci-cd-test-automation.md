---
title: "CI/CD pour l'automatisation des tests"
category: infrastructure
tags: [ci-cd, github-actions, jenkins, selenoid, docker, pipeline, scheduling, browser-testing]
level: 3
source_sha256: 4866924347d308b441424e44947cd8968ebc886f400156f8204a9c9d0fbce1a1
translation: machine
translated_at: '2026-10-24'
---
# CI/CD pour l'automatisation des tests {#cicd-for-test-automation}

Des tests exécutés uniquement en local ne servent à rien pour l'équipe. La CI/CD automatise l'exécution, produit des rapports et fournit un retour sur chaque modification. Jenkins (auto-hébergé, builds paramétrés), GitHub Actions (cloud, workflows YAML) et Selenoid (ferme de navigateurs Docker) forment la pile d'infrastructure standard.

## Points clés {#key-facts}

- **Jenkins** : auto-hébergé, builds paramétrés, magasin d'identifiants, plugin Allure intégré
- **GitHub Actions** : `secrets.NAME` pour les secrets chiffrés, `vars.NAME` pour la configuration, `if: always()` pour les artefacts
- **Selenoid** : ferme de navigateurs basée sur Docker, plus légère que Selenium Grid, vidéo et VNC intégrés
- Docker Compose pour les tests E2E : application + Selenoid + exécuteur de tests dans un réseau isolé
- `depends_on: condition: service_healthy` garantit que l'application est prête avant le démarrage des tests
- Planifier les exécutions nocturnes : cron Jenkins ou déclencheur `schedule` de GH Actions

## Modèles {#patterns}

### Workflow GitHub Actions {#github-actions-workflow}

```yaml
name: Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # nightly at 2 AM

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - name: Run tests
        env:
          FRONTEND_URL: ${{ vars.FRONTEND_URL }}
          TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
        run: pytest tests/ --alluredir=allure-results
      - uses: actions/upload-artifact@v4
        if: always()  # upload even on failure
        with:
          name: allure-results
          path: allure-results
```

### Pipeline Jenkins {#jenkins-pipeline}

```groovy
pipeline {
    agent any
    parameters {
        string(name: 'ENV', defaultValue: 'dev')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'])
    }
    stages {
        stage('Test') {
            steps {
                sh "pytest tests/ --browser=${params.BROWSER} --alluredir=allure-results"
            }
        }
        stage('Report') {
            steps {
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }
}
```

### Selenoid (ferme de navigateurs Docker) {#selenoid-docker-browser-farm}

```yaml
services:
  selenoid:
    image: aerokube/selenoid:latest
    ports: ["4444:4444"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./browsers.json:/etc/selenoid/browsers.json
```

```python
capabilities = {
    "browserName": "chrome",
    "selenoid:options": {"enableVNC": True, "enableVideo": True},
}
driver = webdriver.Remote(
    command_executor="http://selenoid:4444/wd/hub",
    desired_capabilities=capabilities,
)
```

### Docker Compose pour les tests E2E {#docker-compose-for-e2e}

```yaml
services:
  app:
    build: .
    ports: ["3000:3000"]
    healthcheck:
      test: curl -f http://localhost:3000/health
  selenoid:
    image: aerokube/selenoid:latest
    volumes: ["/var/run/docker.sock:/var/run/docker.sock"]
  tests:
    build: { context: ., dockerfile: e2e/Dockerfile }
    depends_on:
      app: { condition: service_healthy }
    environment:
      BASE_URL: http://app:3000
      SELENOID_URL: http://selenoid:4444/wd/hub
```

### Émulateur Android dans la CI {#android-emulator-in-ci}

```yaml
# macOS runner for hardware acceleration
runs-on: macos-latest
steps:
  - uses: reactivecircus/android-emulator-runner@v2
    with:
      api-level: 29
      arch: x86_64
      script: ./gradlew connectedAndroidTest
```

## Pièges {#gotchas}

- `if: always()` sur l'envoi des artefacts : sans cela, les résultats des tests sont perdus en cas d'échec
- Le magasin d'identifiants Jenkins est plus sécurisé que les variables d'environnement en clair : utilisez la syntaxe `credentials('id')`
- Selenoid nécessite un fichier de configuration `browsers.json` avec des versions d'images Chrome/Firefox précises
- Émulateur Android en CI : utilisez un runner macOS (accélération matérielle) ; Linux fonctionne mais est plus lent

## Voir aussi {#see-also}

- [[allure-reporting]] - publication des rapports depuis la CI
- [[selenium-webdriver]] - Selenoid comme WebDriver distant
- [[test-architecture]] - Docker et responsabilité de l'infrastructure de tests
- [[mobile-testing]] - émulateur Android dans GitHub Actions
