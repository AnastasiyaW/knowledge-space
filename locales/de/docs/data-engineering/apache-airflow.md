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

Apache Airflow ist eine Open-Source-Plattform zum Erstellen, Scheduling und Überwachen von Workflows als gerichtete azyklische Graphen (Directed Acyclic Graphs, DAGs). Sie ist der De-facto-Standard für die Orchestrierung von Datenpipelines.

## Architektur {#architecture}

| Komponente | Rolle |
|-----------|------|
| **Web Server** | HTTP-Schnittstelle, Benutzeroberfläche (Standardport 8080) |
| **Scheduler** | Prüft registrierte DAGs periodisch anhand des Zeitplans und erstellt DAG Runs |
| **Worker** | Führt Tasks aus der Queue aus |
| **Queue** | Auf Ausführung wartende Tasks (Redis, RabbitMQ) |
| **Metastore** | Speichert DAG-Definitionen, Lauf-Historie und Task-Zustände (PostgreSQL, MySQL) |

Skaliert horizontal durch Hinzufügen von Workern und Web Servern.

## DAG-Struktur (fünf Blöcke) {#dag-structure-five-blocks}

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

**Vorteile:** XCom wird automatisch verwaltet, Abhängigkeiten werden aus der Aufrufkette abgeleitet, Retry-Einstellungen können pro Task überschrieben werden.

## Scheduling-Optionen {#schedule-options}

| Methode | Beispiel | Anwendungsfall |
|--------|---------|----------|
| Cron | `"0 2 * * *"` | Feste kalenderbasierte Ausführung |
| Presets | `@daily`, `@hourly`, `@weekly` | Gängige Intervalle |
| timedelta | `timedelta(hours=2)` | Festes Intervall ab dem letzten Lauf |
| `@once` | Einmalige Ausführung | Manuelle Trigger |
| `None` | Kein Zeitplan | Nur manuell |

## Operatoren und Sensoren {#operators-and-sensors}

| Typ | Beispiele |
|------|---------|
| **PythonOperator** | Führt Python-Funktionen aus |
| **BashOperator** | Führt Shell-Befehle aus |
| **DummyOperator** | Strukturiert den DAG-Ablauf, dient als Join-Punkt |
| **S3KeySensor** | Wartet auf eine Datei in S3 |
| **ExternalTaskSensor** | Wartet auf einen Task in einem anderen DAG |
| **HttpSensor** | Wartet auf eine erfolgreiche HTTP-Antwort eines Endpunkts |

## Trigger-Regeln {#trigger-rules}

| Regel | Verhalten |
|------|----------|
| `ALL_SUCCESS` | Standard – alle vorgelagerten Tasks waren erfolgreich |
| `ONE_SUCCESS` | Mindestens ein vorgelagerter Task war erfolgreich |
| `ALL_FAILED` | Alle vorgelagerten Tasks sind fehlgeschlagen |
| `ALL_DONE` | Alle vorgelagerten Tasks sind abgeschlossen (unabhängig vom Status) |

## XCom (Cross-Communication) {#xcom-cross-communication}

```python
def multiply(**context):
    value = context['task_instance'].xcom_pull(
        task_ids='load_task', key='return_value')
    return value * value  # auto-pushed to XCom

# TaskFlow API: XCom is implicit via function params/returns
```

## Wichtige Parameter {#key-parameters}

- `catchup=True/False` – ob verpasste Läufe nachgeholt (Backfill) werden sollen
- `max_active_runs` – begrenzt die Anzahl gleichzeitiger DAG-Läufe
- `execution_timeout` – beendet den Task, wenn er zu lange läuft
- `depends_on_past` – Task wartet auf den Erfolg des vorherigen Laufs
- `on_failure_callback` – Alarmfunktion bei Fehlschlag

## Integrierte Kontextvariablen {#built-in-context-variables}

- `ds` – Ausführungsdatum (String im Format YYYY-MM-DD)
- `execution_date` – Ausführungsdatum und -zeit als datetime-Objekt
- `dag` – DAG-Objekt
- `task_instance` / `ti` – aktuelle TaskInstance

## Stolpersteine {#gotchas}
- `schedule_interval` legt das Intervall zwischen den Läufen fest, nicht die Laufzeit. `@daily` mit `start_date=Jan 1` läuft erstmals am 2. Januar
- `catchup=True` (Standard) holt alle verpassten Intervalle nach und kann das System überlasten
- `provide_context=True` ist in der klassischen API für XCom erforderlich; die TaskFlow API übernimmt dies automatisch
- Schlägt ein vorgelagerter Task bei `ALL_SUCCESS` fehl, zeigt der nachgelagerte Task „upstream_failed“ an (nicht „failed“)
- DAG-Dateien gehören in das konfigurierte Verzeichnis `dags/`; das Deployment erfolgt per Push nach Git

## Siehe auch {#see-also}
- [[etl-elt-pipelines]] – Entwurfsmuster für Pipelines
- [[apache-spark-core]] – gängige Ausführungsengine
- [[data-quality]] – Validierung in Pipelines
