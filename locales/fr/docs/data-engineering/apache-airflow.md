---
title: "Apache Airflow"
category: tools
tags: [data-engineering, airflow, orchestration, dag, scheduling, pipelines]
level: 3
source_sha256: 9054b7420dedfff36ae886b22bc8291ecd6bd5e8e33e224177482a2e77d656bd
translation: machine
translated_at: '2026-10-24'
---
# Apache Airflow {#apache-airflow}

Apache Airflow est une plateforme open source permettant de concevoir, planifier et superviser des workflows sous forme de graphes orientés acycliques (DAG). C'est le standard de facto pour l'orchestration de pipelines de données.

## Architecture {#architecture}

| Composant | Rôle |
|-----------|------|
| **Serveur web** | Interface HTTP, interface utilisateur (port par défaut 8080) |
| **Scheduler** | Vérifie périodiquement les DAG enregistrés par rapport à leur planification et crée les DAG Runs |
| **Worker** | Exécute les tâches de la file d'attente |
| **File d'attente** | Tâches en attente d'exécution (Redis, RabbitMQ) |
| **Metastore** | Stocke les définitions de DAG, l'historique des exécutions et les états des tâches (PostgreSQL, MySQL) |

Passe à l'échelle horizontalement en ajoutant des Workers et des serveurs web.

## Structure d'un DAG (cinq blocs) {#dag-structure-five-blocks}

```python
# 1. IMPORTS
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# 2. TASK FUNCTIONS
def extract(): pass
def transform(): pass
def load(): pass

# 3. DEFAULT ARGS + DAG
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
}

dag = DAG('etl_pipeline', default_args=default_args,
          schedule_interval='0 12 * * *', catchup=False)

# 4. TASK INITIALIZATION
t1 = PythonOperator(task_id='extract', python_callable=extract, dag=dag)
t2 = PythonOperator(task_id='transform', python_callable=transform, dag=dag)
t3 = PythonOperator(task_id='load', python_callable=load, dag=dag)

# 5. DEPENDENCIES
t1 >> t2 >> t3
```

## TaskFlow API (Airflow 2.0+) {#taskflow-api-airflow-20}

```python
from airflow.decorators import dag, task

@dag(schedule_interval='@daily', start_date=days_ago(1), catchup=False)
def etl_pipeline():
    @task(retries=3)
    def extract():
        return requests.get(URL).content

    @task()
    def transform(raw_data):
        return pd.read_csv(StringIO(raw_data)).to_csv(index=False)

    @task()
    def load(data):
        print(f"Loading {len(data)} bytes")

    raw = extract()
    table = transform(raw)
    load(table)

etl_pipeline()
```

**Avantages :** XCom géré automatiquement, dépendances déduites de la chaîne d'appels, surcharges de retry par tâche.

## Options de planification {#schedule-options}

| Méthode | Exemple | Cas d'usage |
|---------|---------|-------------|
| Cron | `"0 2 * * *"` | Basé sur un calendrier fixe |
| Préréglages | `@daily`, `@hourly`, `@weekly` | Intervalles courants |
| timedelta | `timedelta(hours=2)` | Intervalle fixe depuis la dernière exécution |
| `@once` | Exécution unique | Déclenchements manuels |
| `None` | Aucune planification | Manuel uniquement |

## Opérateurs et sensors {#operators-and-sensors}

| Type | Exemples |
|------|----------|
| **PythonOperator** | Exécute des fonctions Python |
| **BashOperator** | Exécute des commandes shell |
| **DummyOperator** | Structuration du flux du DAG, points de jonction |
| **S3KeySensor** | Attend un fichier dans S3 |
| **ExternalTaskSensor** | Attend une tâche d'un autre DAG |
| **HttpSensor** | Attend le succès d'un point de terminaison HTTP |

## Règles de déclenchement {#trigger-rules}

| Règle | Comportement |
|-------|--------------|
| `ALL_SUCCESS` | Par défaut - toutes les tâches amont ont réussi |
| `ONE_SUCCESS` | Au moins une tâche amont a réussi |
| `ALL_FAILED` | Toutes les tâches amont ont échoué |
| `ALL_DONE` | Toutes les tâches amont sont terminées (quel que soit leur statut) |

## XCom (communication croisée) {#xcom-cross-communication}

```python
def multiply(**context):
    value = context['task_instance'].xcom_pull(
        task_ids='load_task', key='return_value')
    return value * value  # auto-pushed to XCom

# TaskFlow API: XCom is implicit via function params/returns
```

## Paramètres clés {#key-parameters}

- `catchup=True/False` - pour rattraper (backfill) les exécutions manquées
- `max_active_runs` - limite le nombre de DAG runs simultanés
- `execution_timeout` - arrête la tâche si elle dure trop longtemps
- `depends_on_past` - la tâche attend le succès de l'exécution précédente
- `on_failure_callback` - fonction d'alerte en cas d'échec

## Variables de contexte intégrées {#built-in-context-variables}

- `ds` - date d'exécution (chaîne YYYY-MM-DD)
- `execution_date` - objet datetime de l'exécution
- `dag` - objet DAG
- `task_instance` / `ti` - TaskInstance courante

## Pièges courants {#gotchas}
- `schedule_interval` définit l'intervalle entre les exécutions, pas l'heure d'exécution. Un `@daily` avec `start_date=Jan 1` s'exécute pour la première fois le 2 janvier
- `catchup=True` (par défaut) rattrapera tous les intervalles manqués - peut surcharger le système
- `provide_context=True` est requis pour XCom dans l'API classique ; TaskFlow le gère automatiquement
- Lorsqu'une tâche amont échoue avec `ALL_SUCCESS`, la tâche aval affiche "upstream_failed" (et non "failed")
- Les fichiers DAG se placent dans le répertoire `dags/` configuré ; déploiement par push vers Git

## Voir aussi {#see-also}
- [[etl-elt-pipelines]] - patrons de conception de pipelines
- [[apache-spark-core]] - moteur d'exécution courant
- [[data-quality]] - validation dans les pipelines
