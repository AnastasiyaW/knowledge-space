---
title: CI/CD for Test Automation
category: infrastructure
tags: [ci-cd, github-actions, gitlab-ci, pipeline, workflow, continuous-integration]
---
# CI/CD for Test Automation

Automated test execution in CI/CD pipelines - GitHub Actions, GitLab CI, Jenkins - run tests on every commit.

## Key Facts

- CI (Continuous Integration): automatically run tests on each push/PR
- CD (Continuous Delivery/Deployment): automatically deploy after tests pass
- GitHub Actions: `.github/workflows/*.yml` - most popular for open-source
- GitLab CI: `.gitlab-ci.yml` - integrated with GitLab repos
- Jenkins, CircleCI, TeamCity - other CI platforms, similar concepts
- Key concepts: workflow/pipeline, job, step, trigger, artifact, secret
- Tests should run on every push to feature branches and on PR merge to main
- [[allure-reporting]] reports published as CI artifacts or to GitHub Pages
- Parallel test execution (`pytest -n auto`) speeds up CI runs
- Environment variables and secrets for configuration (base URLs, tokens)

## Patterns

```yaml
# .github/workflows/tests.yml - GitHub Actions
name: Run Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:  # manual trigger

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --alluredir=allure-results -n auto
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}
          API_TOKEN: ${{ secrets.API_TOKEN }}

      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results
          path: allure-results

  # Publish Allure to GitHub Pages
  report:
    needs: test
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Checkout gh-pages
        uses: actions/checkout@v4
        with:
          ref: gh-pages
          path: gh-pages

      - name: Download results
        uses: actions/download-artifact@v4
        with:
          name: allure-results
          path: allure-results

      - name: Generate Allure report
        uses: simple-elf/allure-report-action@v1.7
        with:
          allure_results: allure-results
          allure_history: gh-pages/allure-history

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: allure-history
```

```yaml
# .gitlab-ci.yml - GitLab CI
stages:
  - test
  - report

api-tests:
  stage: test
  image: python:3.12-slim
  script:
    - pip install -r requirements.txt
    - pytest tests/api/ --alluredir=allure-results -n auto
  artifacts:
    paths:
      - allure-results
    when: always
  variables:
    BASE_URL: $STAGING_URL
```

```python
# requirements.txt for CI
pytest>=7.0
pytest-xdist>=3.0
allure-pytest>=2.13
requests>=2.31
playwright>=1.40

# Freeze exact versions for reproducibility
# pip freeze > requirements.txt
```

## Gotchas

- **Symptom**: Playwright tests fail in CI with "no browsers installed" - **Cause**: need `playwright install` step - **Fix**: add `playwright install --with-deps chromium` to CI pipeline
- **Symptom**: GitHub Pages deploy fails with 403 - **Cause**: workflow permissions not set - **Fix**: enable "Read and write permissions" in repo Settings > Actions > General
- **Symptom**: tests pass locally, fail in CI - **Cause**: headless mode not enabled, display not available - **Fix**: run browsers in headless mode, use Xvfb for Selenium, or use Playwright (headless by default)
- **Symptom**: secrets not available in forked PRs - **Cause**: GitHub security restriction - **Fix**: use environment-based approach or skip tests requiring secrets on forks
- Always use `if: always()` for artifact upload - otherwise artifacts are lost on test failure
- Pin dependency versions in `requirements.txt` for reproducible CI builds

## See Also

- [[allure-reporting]] - generating and publishing test reports
- [[pytest-plugins-and-parallel]] - xdist for parallel CI execution
- [[test-project-structure]] - organizing project for CI
- [GitHub Actions docs](https://docs.github.com/en/actions)
- [GitLab CI docs](https://docs.gitlab.com/ee/ci/)
