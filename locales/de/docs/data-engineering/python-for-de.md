---
title: "Python für Data Engineering"
category: reference
tags: [data-engineering, python, pandas, database-access, functional-programming]
level: 3
source_sha256: 4d1bdc748fc551027259704d276f5d3de7c138f54e834ecf9346d2e118387ccb
translation: machine
translated_at: '2026-10-24'
---
# Python für Data Engineering {#python-for-data-engineering}

Python ist die primäre Skriptsprache für Data Engineering. Dieser Eintrag behandelt DE-spezifische Muster: Datenbankzugriff, Dateiverarbeitung, funktionale Programmierung für Datentransformationen und Pandas für die Datenmanipulation.

## Datenbankzugriff {#database-access}

### psycopg2 (PostgreSQL) {#psycopg2-postgresql}

```python
import psycopg2

conn = psycopg2.connect(host="localhost", port=5432,
                         dbname="mydb", user="user", password="pass")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE age > %s", (25,))
rows = cursor.fetchall()
conn.commit()
cursor.close(); conn.close()
```

**Immer parametrisierte Abfragen verwenden** (`%s`-Platzhalter) - niemals f-Strings. Verhindert SQL-Injection.

### SQLAlchemy {#sqlalchemy}

```python
from sqlalchemy import create_engine, text
engine = create_engine("postgresql://user:pass@localhost:5432/mydb")

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))

# Pandas integration
df = pd.read_sql("SELECT * FROM users", engine)
df.to_sql("users_backup", engine, if_exists="replace", index=False)
```

### ClickHouse {#clickhouse}

```python
from clickhouse_driver import Client
client = Client(host="localhost", port=9000)
result = client.execute("SELECT * FROM events LIMIT 10")
```

## Pandas-Grundlagen {#pandas-essentials}

```python
import pandas as pd

# I/O
df = pd.read_csv("data.csv"); df = pd.read_parquet("data.parquet")
df.to_csv("out.csv", index=False); df.to_parquet("out.parquet")

# Explore
df.shape; df.dtypes; df.info(); df.describe(); df.head()

# Filter
df[df["age"] > 25]
df[(df["age"] > 25) & (df["city"] == "NYC")]

# Transform
df["salary_k"] = df["salary"] / 1000
df["category"] = df["amount"].apply(lambda x: "high" if x > 100 else "low")
df.dropna(subset=["name"]); df.fillna(0)
df["date"] = pd.to_datetime(df["date"])

# Aggregate
df.groupby("dept").agg(avg_sal=("salary", "mean"), count=("id", "count"))
pd.merge(df1, df2, on="id", how="left")
```

## Muster der funktionalen Programmierung {#functional-programming-patterns}

```python
# map, filter, reduce
list(map(lambda x: x**2, [1, 2, 3]))
list(filter(lambda x: x > 0, [-1, 0, 2]))
from functools import reduce
reduce(lambda acc, x: acc + x, [1, 2, 3, 4])

# Decorators (common in ETL)
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper
```

## Dateioperationen {#file-operations}

```python
# JSON
import json
with open("data.json") as f: data = json.load(f)
with open("out.json", "w") as f: json.dump(data, f, indent=2)

# CSV
import csv
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader: print(row["name"])

# YAML
import yaml
with open("config.yaml") as f: config = yaml.safe_load(f)
```

## Testen {#testing}

```python
# pytest
def test_transform():
    assert transform([1, 2, 3]) == [2, 4, 6]

@pytest.fixture
def sample_data():
    return pd.DataFrame({"a": [1, 2], "b": [3, 4]})

def test_sum(sample_data):
    assert sample_data["a"].sum() == 3
```

## Wichtige Python-Fallstricke {#key-python-gotchas}
- Veränderliche Standardargumente: `def f(x=[])` teilt die Liste über alle Aufrufe hinweg. Stattdessen `None` verwenden
- `is` prüft die Identität, `==` prüft die Gleichheit
- GIL: für CPU-gebundene Parallelität `multiprocessing` verwenden
- Generatoren sind speichereffizient für große Datenmengen

## Siehe auch {#see-also}
- [[pyspark-dataframe-api]] - verteilte Datenverarbeitung
- [[etl-elt-pipelines]] - Python im ETL-Kontext
- [[apache-airflow]] - Python-basierte Orchestrierung
