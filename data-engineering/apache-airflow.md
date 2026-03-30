---
title: Apache Airflow
category: concepts
tags: [airflow, dag, orchestration, scheduling, operators, etl, pipeline]
---

# Apache Airflow

Apache Airflow is a workflow orchestration platform for authoring, scheduling, and monitoring data pipelines. Pipelines are defined as Python code (DAGs), executed on a schedule, and monitored through a web UI.

## Key Facts

- **DAG (Directed Acyclic Graph)**: a collection of tasks with defined dependencies and execution order. No cycles allowed
- DAGs are Python files placed in the `dags/` directory (DagBag). Airflow scans this directory periodically
- **schedule_interval**: cron expression or preset (`@daily`, `@hourly`). Cron evaluated in the scheduler's timezone. Example: `0 0 * * 1-6` = Mon-Sat at midnight
- **execution_date / logical_date**: the date the DAG run represents (not when it actually runs). A `@daily` DAG with execution_date 2026-03-29 runs on 2026-03-30
- **Operators**: define individual tasks. Core types:
  - `PythonOperator`: runs a Python callable
  - `BashOperator`: runs a shell command
  - `PostgresOperator` / `MySqlOperator`: executes SQL
  - `BranchPythonOperator`: conditional branching based on return value
  - `ShortCircuitOperator`: stops downstream tasks if condition is False
- **Sensors**: wait for an external condition (file existence, partition availability, external DAG completion). `ExternalTaskSensor` waits for another DAG's task
- **XCom**: cross-communication between tasks. Tasks push/pull small values. Return value from PythonOperator auto-pushes to XCom
- **Connections**: stored credentials for external systems (databases, APIs). Managed via UI or CLI. Referenced by `conn_id` in hooks
- **Hooks**: interfaces to external systems (PostgresHook, S3Hook, HttpHook). Used inside operators/sensors
- **Trigger Rules**: control when a task runs based on upstream status. Default: `all_success`. Options: `all_failed`, `one_success`, `none_failed`, etc.

## Patterns

### DAG definition (three equivalent styles)

```python
# Style 1: context manager
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG('my_pipeline', schedule_interval='@daily',
         start_date=datetime(2026, 1, 1), catchup=False) as dag:

    extract = PythonOperator(task_id='extract', python_callable=extract_fn)
    transform = PythonOperator(task_id='transform', python_callable=transform_fn)
    load = PythonOperator(task_id='load', python_callable=load_fn)

    extract >> transform >> load

# Style 2: decorator (TaskFlow API, Airflow 2.x)
from airflow.decorators import dag, task

@dag(schedule_interval='@daily', start_date=datetime(2026, 1, 1), catchup=False)
def my_pipeline():
    @task
    def extract(): return data
    @task
    def transform(data): return result
    @task
    def load(result): ...

    load(transform(extract()))

my_pipeline()
```

### Using XCom and execution_date

```python
def get_article_for_today(**kwargs):
    # Get logical execution date, NOT current date
    ds = kwargs['ds']  # '2026-03-29' format
    day_of_week = datetime.strptime(ds, '%Y-%m-%d').weekday() + 1

    pg_hook = PostgresHook(postgres_conn_id='conn_greenplum')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(f'SELECT heading FROM articles WHERE id = {day_of_week}')
    result = cursor.fetchone()[0]

    return result  # auto-pushed to XCom

task = PythonOperator(
    task_id='get_article',
    python_callable=get_article_for_today,
    provide_context=True
)
```

### Jinja templating in operators

```python
BashOperator(
    task_id='echo_date',
    bash_command='echo "Processing {{ ds }}, prev: {{ prev_ds }}"'
)
```

## Gotchas

- `execution_date` is the **start of the interval**, not when the DAG actually runs. A daily DAG for 2026-03-29 runs at the end of that day (start of 2026-03-30). This is the #1 source of confusion
- `catchup=True` (default) triggers backfill runs for all missed intervals since `start_date`. Set `catchup=False` for pipelines that should only process current data
- XCom is for small values (metadata, file paths, row counts). Do NOT pass large DataFrames through XCom - write to storage and pass the path
- Noncron schedules (`schedule_interval='0 0 * * 1-6'`) create confusion with ExternalTaskSensors. Consider using BranchPythonOperator with standard `@daily` schedule instead
- DAG file is parsed by scheduler every 30s. Heavy imports or computation at module level slows the entire scheduler
- Custom operators should be packaged as Airflow plugins (placed in `plugins/` directory) for reusability

## See Also

- [[etl-and-elt]] - Airflow as ETL/ELT orchestrator
- [[apache-spark]] - Spark jobs triggered by Airflow
- [[data-quality]] - validation tasks in Airflow pipelines
- https://airflow.apache.org/docs/ - Apache Airflow documentation
