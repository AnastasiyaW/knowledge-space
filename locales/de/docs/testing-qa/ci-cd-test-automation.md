---
title: "CI/CD für Testautomatisierung"
category: infrastructure
tags: [ci-cd, github-actions, jenkins, selenoid, docker, pipeline, scheduling, browser-testing]
level: 3
source_sha256: 4866924347d308b441424e44947cd8968ebc886f400156f8204a9c9d0fbce1a1
translation: machine
translated_at: '2026-10-24'
---
# CI/CD für Testautomatisierung {#cicd-for-test-automation}

Tests, die nur lokal laufen, nützen dem Team wenig. CI/CD automatisiert die Ausführung, erstellt Berichte und liefert Rückmeldung zu jeder Änderung. Jenkins (selbst gehostet, parametrisierte Builds), GitHub Actions (Cloud, YAML-Workflows) und Selenoid (Docker-Browser-Farm) bilden den Standard-Infrastruktur-Stack.

## Wichtige Fakten {#key-facts}

- **Jenkins**: selbst gehostet, parametrisierte Builds, Credentials-Store, Allure-Plugin integriert
- **GitHub Actions**: `secrets.NAME` für verschlüsselte Secrets, `vars.NAME` für Konfiguration, `if: always()` für Artefakte
- **Selenoid**: Docker-basierte Browser-Farm, leichtgewichtig im Vergleich zu Selenium Grid, integrierte Videoaufnahme und VNC
- Docker Compose für E2E: App + Selenoid + Test-Runner in einem isolierten Netzwerk
- `depends_on: condition: service_healthy` stellt sicher, dass die App bereit ist, bevor die Tests starten
- Nächtliche Läufe planen: Jenkins-Cron oder GH-Actions-Trigger `schedule`

## Muster {#patterns}

### GitHub-Actions-Workflow {#github-actions-workflow}

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

### Jenkins-Pipeline {#jenkins-pipeline}

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

### Selenoid (Docker-Browser-Farm) {#selenoid-docker-browser-farm}

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

### Docker Compose für E2E {#docker-compose-for-e2e}

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

### Android-Emulator in CI {#android-emulator-in-ci}

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

## Stolperfallen {#gotchas}

- `if: always()` beim Hochladen von Artefakten - ohne diese Angabe gehen Testergebnisse bei einem Fehlschlag verloren
- Der Credentials-Store von Jenkins ist sicherer als einfache Umgebungsvariablen - die Syntax `credentials('id')` verwenden
- Selenoid benötigt eine `browsers.json`-Konfiguration mit spezifischen Chrome-/Firefox-Image-Versionen
- Android-Emulator in CI: macOS-Runner verwenden (Hardwarebeschleunigung); Linux funktioniert, ist aber langsamer

## Siehe auch {#see-also}

- [[allure-reporting]] - Veröffentlichung von Berichten aus CI
- [[selenium-webdriver]] - Selenoid als Remote-WebDriver
- [[test-architecture]] - Docker- und Testinfrastruktur: Verantwortlichkeiten
- [[mobile-testing]] - Android-Emulator in GitHub Actions
