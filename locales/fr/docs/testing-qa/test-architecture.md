---
title: "Architecture de tests"
category: methodology
tags: [test-strategy, test-pyramid, project-structure, conftest, test-types, coverage, logging, security]
level: 3
source_sha256: 4f13f494b4f8422ca809aea508318ad5019552e67c1623f527d0f4ea12e031e5
translation: machine
translated_at: '2026-10-24'
---
# Architecture de tests {#test-architecture}

Les projets d'automatisation de tests sont des projets logiciels à part entière : ils requièrent les mêmes pratiques d'ingénierie : gestion de versions, revue de code, gestion des dépendances, CI/CD. L'architecture couvre la structure du projet (hiérarchie des conftest, classes clientes, modèles), la stratégie de test (pyramide, types, couverture) et les aspects opérationnels (journalisation, masquage des secrets, métriques).

## Points clés {#key-facts}

- **Pyramide de tests** : beaucoup de tests unitaires (rapides), moins de tests d'intégration, encore moins de tests E2E (lents, coûteux)
- Structure du projet : `tests/api/`, `tests/ui/`, `clients/`, `models/` - séparer les responsabilités
- Solution au gonflement de `conftest.py` : la liste `pytest_plugins` importe les fixtures depuis des modules séparés
- Masquage des données sensibles : filtres de journalisation personnalisés et précaution avec `pytest -l` (showlocals)
- Isolation des tests : chaque test prépare ses propres données, vérifie son résultat de manière indépendante et nettoie après lui
- Métriques à suivre : durée d'exécution, stabilité (taux de réussite), disponibilité de l'infrastructure, délai de la boucle de rétroaction

## Patrons {#patterns}

### Structure du projet {#project-structure}

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

### Pyramide de tests et types {#test-pyramid-and-types}

| Niveau | Vitesse | Coût | Exemples |
|-------|-------|------|----------|
| Unitaire | Rapide (ms) | Faible | Fonctions pures, validateurs |
| Intégration | Moyenne (s) | Moyen | Appels API, requêtes BDD |
| E2E / UI | Lente (10 s et plus) | Élevé | Parcours utilisateur complets avec navigateur |

- **Tests de fumée** : chemins critiques, exécutés en premier (connexion, CRUD principal)
- **Tests de non-régression** : suite complète, exécutée chaque nuit ou à chaque pull request
- **Tests de contrat** : validation du schéma d'API entre services

### Masquage des données sensibles {#sensitive-data-masking}

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

### Gestion des environnements {#environment-management}

```ini
# .env.sample (committed)
FRONTEND_URL=http://localhost:3000
TEST_USERNAME=
TEST_PASSWORD=

# .env (gitignored, actual values)
```

Pour changer d'environnement : `.env.prod`, `.env.staging` + une option pytest personnalisée (`--env=prod`) ou des variables d'environnement CI.

### Gestion des dépendances {#dependency-management}

```bash
# Simple: venv + pip
python -m venv .venv && pip install -r requirements.txt

# Teams: Poetry (deterministic builds via lockfile)
poetry init && poetry add pytest requests
```

## Pièges à éviter {#gotchas}

- Un seul `conftest.py` par répertoire : utiliser `pytest_plugins` pour partager des fixtures entre répertoires
- Les tests qui dépendent des effets de bord d'autres tests sont fragiles : imposer l'isolation
- `pytest -l` expose les variables locales en cas d'échec : jetons et mots de passe deviennent visibles dans les journaux CI
- La couverture est un indicateur, non un objectif : environ 85 % est réaliste, 100 % présente des rendements décroissants

## Voir aussi {#see-also}

- [[pytest-fundamentals]] - fixtures, parametrize, hooks
- [[allure-reporting]] - rapports de tests comme outil de communication d'équipe
- [[ci-cd-test-automation]] - exécution des tests dans les pipelines CI
- [[api-testing-tools]] - classes clientes HTTP et validation des réponses
