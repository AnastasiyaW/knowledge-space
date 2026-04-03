---
title: Apache Airflow
category: tools
tags: [data-engineering, airflow, orchestration, dag, scheduling, pipelines]
---

# Apache Airflow

Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Directed Acyclic Graphs (DAGs). It is the de facto standard for data pipeline orchestration.

## Architecture

| Component | Role |
|-----------|------|
| **Web Server** | HTTP interface, user UI (default port 8080) |
| **Scheduler** | Periodically checks registered DAGs against schedule, creates DAG Runs |
| **Worker** | Executes tasks from the queue |
| **Queue** | Tasks waiting for execution (Redis, RabbitMQ) |
| **Metastore** | Stores DAG definitions, run history, task states (PostgreSQL, MySQL) |

Scales horizontally by adding Workers and Web Servers.

## DAG Structure (Five Blocks)

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

## TaskFlow API (Airflow 2.0+)

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

**Advantages:** XCom handled automatically, dependencies inferred from call chain, per-task retry overrides.

## Schedule Options

| Method | Example | Use Case |
|--------|---------|----------|
| Cron | `"0 2 * * *"` | Fixed calendar-based |
| Presets | `@daily`, `@hourly`, `@weekly` | Common intervals |
| timedelta | `timedelta(hours=2)` | Fixed interval from last run |
| `@once` | Single execution | Manual triggers |
| `None` | No schedule | Manual only |

## Operators and Sensors

| Type | Examples |
|------|---------|
| **PythonOperator** | Run Python functions |
| **BashOperator** | Run shell commands |
| **DummyOperator** | DAG flow structuring, join points |
| **S3KeySensor** | Wait for file in S3 |
| **ExternalTaskSensor** | Wait for task in another DAG |
| **HttpSensor** | Wait for HTTP endpoint success |

## Trigger Rules

| Rule | Behavior |
|------|----------|
| `ALL_SUCCESS` | Default - all upstream succeeded |
| `ONE_SUCCESS` | At least one upstream succeeded |
| `ALL_FAILED` | All upstream failed |
| `ALL_DONE` | All upstream completed (any status) |

## XCom (Cross-Communication)

```python
def multiply(**context):
    value = context['task_instance'].xcom_pull(
        task_ids='load_task', key='return_value')
    return value * value  # auto-pushed to XCom

# TaskFlow API: XCom is implicit via function params/returns
```

## Key Parameters

- `catchup=True/False` - whether to backfill missed runs
- `max_active_runs` - limit concurrent DAG runs
- `execution_timeout` - kill task if too long
- `depends_on_past` - task waits for previous run's success
- `on_failure_callback` - alert function on failure

## Built-in Context Variables

- `ds` - execution date (YYYY-MM-DD string)
- `execution_date` - execution datetime object
- `dag` - DAG object
- `task_instance` / `ti` - current TaskInstance

## Gotchas
- `schedule_interval` defines interval between runs, not run time. `@daily` with `start_date=Jan 1` first runs on Jan 2
- `catchup=True` (default) will backfill all missed intervals - can flood the system
- `provide_context=True` required for XCom in classic API; TaskFlow handles automatically
- When upstream fails with `ALL_SUCCESS`, downstream shows "upstream_failed" (not "failed")
- DAG files go in configured `dags/` directory; deploy by pushing to Git

## See Also
- [[etl-elt-pipelines]] - pipeline design patterns
- [[apache-spark-core]] - common execution engine
- [[data-quality]] - validation in pipelines
