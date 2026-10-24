---
title: "Testarchitektur"
category: methodology
tags: [test-strategy, test-pyramid, project-structure, conftest, test-types, coverage, logging, security]
level: 3
source_sha256: 4f13f494b4f8422ca809aea508318ad5019552e67c1623f527d0f4ea12e031e5
translation: machine
translated_at: '2026-10-24'
---
# Testarchitektur {#test-architecture}

Testautomatisierungsprojekte sind Softwareprojekte - sie benötigen dieselben Engineering-Praktiken: Versionskontrolle, Code-Review, Abhängigkeitsverwaltung, CI/CD. Die Architektur umfasst die Projektstruktur (conftest-Hierarchie, Client-Klassen, Modelle), die Teststrategie (Pyramide, Testarten, Abdeckung) sowie betriebliche Aspekte (Logging, Maskierung von Geheimnissen, Metriken).

## Kernfakten {#key-facts}

- **Testpyramide**: viele Unit-Tests (schnell), weniger Integrationstests, am wenigsten E2E-Tests (langsam, teuer)
- Projektstruktur: `tests/api/`, `tests/ui/`, `clients/`, `models/` - getrennte Zuständigkeiten
- Lösung für das Anwachsen der `conftest.py`: Die Liste `pytest_plugins` importiert Fixtures aus separaten Modulen
- Maskierung sensibler Daten: eigene Logging-Filter und Vorsicht bei `pytest -l` (showlocals)
- Testisolation: Jeder Test bereitet seine eigenen Daten vor, prüft sie unabhängig und räumt danach auf
- Zu verfolgende Metriken: Ausführungszeit, Stabilität (Bestehensquote), Verfügbarkeit der Infrastruktur, Dauer der Feedback-Schleife

## Muster {#patterns}

### Projektstruktur {#project-structure}

```python
tests/
  conftest.py              # global fixtures + pytest_plugins
  api/
    conftest.py            # API-specific fixtures
    users/
      test_create_user.py
    spend/
      test_spending.py
  ui/
    conftest.py            # browser fixtures
    test_login.py
  clients/
    spend_client.py        # HTTP client classes
    db_client.py
  models/
    user.py                # Pydantic response models
    spend.py
  fixtures/
    user_fixtures.py       # extracted from conftest via plugins
    auth_fixtures.py
```

### Testpyramide und Testarten {#test-pyramid-and-types}

| Ebene | Geschwindigkeit | Kosten | Beispiele |
|-------|-----------------|--------|-----------|
| Unit | Schnell (ms) | Niedrig | Reine Funktionen, Validatoren |
| Integration | Mittel (s) | Mittel | API-Aufrufe, DB-Abfragen |
| E2E / UI | Langsam (10s+) | Hoch | Vollständige Benutzerabläufe mit Browser |

- **Smoke-Tests**: kritische Pfade, werden zuerst ausgeführt (Login, zentrale CRUD-Operationen)
- **Regressionstests**: vollständige Suite, werden nachts oder pro PR ausgeführt
- **Contract-Tests**: Validierung des API-Schemas zwischen Services

### Maskierung sensibler Daten {#sensitive-data-masking}

```python
import logging, re

class SensitiveDataFilter(logging.Filter):
    PATTERNS = [
        (re.compile(r'(password["\s:=]+)[^\s,}"]+', re.I), r'\1***'),
        (re.compile(r'(token["\s:=]+)[^\s,}"]+', re.I), r'\1***'),
        (re.compile(r'(Bearer\s+)\S+', re.I), r'\1***')]

    def filter(self, record):
        msg = record.getMessage()
        for pattern, replacement in self.PATTERNS:
            msg = pattern.sub(replacement, msg)
        record.msg = msg
        record.args = ()
        return True

logging.getLogger().addFilter(SensitiveDataFilter())
```

### Umgebungsverwaltung {#environment-management}

```ini
# .env.sample (committed)
FRONTEND_URL=http://localhost:3000
TEST_USERNAME=
TEST_PASSWORD=

# .env (gitignored, actual values)
```

Umgebungen wechseln: `.env.prod`, `.env.staging` sowie eine eigene pytest-Option (`--env=prod`) oder CI-Umgebungsvariablen.

### Abhängigkeitsverwaltung {#dependency-management}

```bash
# Simple: venv + pip
python -m venv .venv && pip install -r requirements.txt

# Teams: Poetry (deterministic builds via lockfile)
poetry init && poetry add pytest requests
```

## Fallstricke {#gotchas}

- Pro Verzeichnis nur eine `conftest.py` - für die verzeichnisübergreifende Nutzung von Fixtures `pytest_plugins` verwenden
- Tests, die von Nebeneffekten anderer Tests abhängen, sind fragil; Isolation erzwingen
- `pytest -l` zeigt bei Fehlern lokale Variablen - Tokens und Passwörter erscheinen dann in den CI-Logs
- Abdeckung ist ein Richtwert, kein Ziel: ca. 85 % sind praktikabel, 100 % bringen abnehmenden Nutzen

## Siehe auch {#see-also}

- [[pytest-fundamentals]] - Fixtures, Parametrisierung, Hooks
- [[allure-reporting]] - Testberichte als Kommunikationsmittel im Team
- [[ci-cd-test-automation]] - Ausführung von Tests in CI-Pipelines
- [[api-testing-tools]] - HTTP-Client-Klassen und Validierung von Antworten
