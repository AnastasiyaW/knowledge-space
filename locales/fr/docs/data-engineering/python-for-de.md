---
title: "Python pour l'ingénierie des données"
category: reference
tags: [data-engineering, python, pandas, database-access, functional-programming]
level: 3
source_sha256: 4d1bdc748fc551027259704d276f5d3de7c138f54e834ecf9346d2e118387ccb
translation: machine
translated_at: '2026-10-24'
---
# Python pour l'ingénierie des données {#python-for-data-engineering}

Python est le langage de script principal pour l'ingénierie des données. Cette entrée couvre les patterns propres au DE : l'accès aux bases de données, la gestion des fichiers, la programmation fonctionnelle pour les transformations de données, et Pandas pour la manipulation de données.

## Accès aux bases de données {#database-access}

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

**Utilisez toujours des requêtes paramétrées** (placeholders `%s`) - jamais de f-strings. Cela prévient les injections SQL.

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

## Essentiels Pandas {#pandas-essentials}

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

## Patterns de programmation fonctionnelle {#functional-programming-patterns}

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

## Opérations sur les fichiers {#file-operations}

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

## Tests {#testing}

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

## Pièges Python courants {#key-python-gotchas}
- Arguments par défaut mutables : `def f(x=[])` partage la liste entre les appels. Utilisez `None`
- `is` vérifie l'identité, `==` vérifie l'égalité
- GIL : utilisez `multiprocessing` pour le parallélisme lié au CPU
- Les générateurs sont économes en mémoire pour les grands jeux de données

## Voir aussi {#see-also}
- [[pyspark-dataframe-api]] - traitement de données distribué
- [[etl-elt-pipelines]] - Python dans le contexte ETL
- [[apache-airflow]] - orchestration basée sur Python
