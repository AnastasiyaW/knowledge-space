---
title: CI/CD for Test Automation
category: infrastructure
tags: [ci-cd, github-actions, jenkins, selenoid, docker, pipeline, scheduling, browser-testing]
---

# CI/CD for Test Automation

Tests running only locally are useless for the team. CI/CD automates execution, produces reports, and provides feedback on every change. Jenkins (self-hosted, parameterized builds), GitHub Actions (cloud, YAML workflows), and Selenoid (Docker browser farm) form the standard infrastructure stack.

## Key Facts

- **Jenkins**: self-hosted, parameterized builds, credentials store, Allure plugin built-in
- **GitHub Actions**: `secrets.NAME` for encrypted secrets, `vars.NAME` for config, `if: always()` for artifacts
- **Selenoid**: Docker-based browser farm, lightweight vs Selenium Grid, built-in video/VNC
- Docker Compose for E2E: app + Selenoid + test runner in isolated network
- `depends_on: condition: service_healthy` ensures app is ready before tests start
- Schedule nightly runs: Jenkins cron or GH Actions `schedule` trigger

## Patterns

### GitHub Actions Workflow

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

### Jenkins Pipeline

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

### Selenoid (Docker Browser Farm)

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

### Docker Compose for E2E

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

### Android Emulator in CI

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

## Gotchas

- `if: always()` on artifact upload - without it, test results are lost on failure
- Jenkins credentials store is more secure than plain env vars - use `credentials('id')` syntax
- Selenoid needs `browsers.json` config with specific Chrome/Firefox image versions
- Android emulator on CI: use macOS runner (hardware acceleration); Linux works but slower

## See Also

- [[allure-reporting]] - publishing reports from CI
- [[selenium-webdriver]] - Selenoid as remote WebDriver
- [[test-architecture]] - Docker + test infrastructure ownership
- [[mobile-testing]] - Android emulator in GitHub Actions
