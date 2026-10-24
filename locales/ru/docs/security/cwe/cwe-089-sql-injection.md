---
description: "CWE-89: SQL-инъекция — недоверенные данные изменяют структуру запроса. Неочевидные векторы: сырые запросы ORM, динамические идентификаторы, пути LIKE/JSON, резолверы GraphQL."
date: 2026-04-16
tags: [security, cwe, sql-injection, web, owasp, database]
level: Advanced
source_sha256: 9f10a2aef0ce2313b763035d7277f7c3f8fa8080795163a34686416341ee8e66
translation: machine
translated_at: '2026-10-24'
---
# CWE-89: SQL-инъекция {#cwe-89-sql-injection}

**Место в CWE Top 25:** 3 (2024). OWASP A03:2021.
**Диапазон последствий:** обход аутентификации, полная выгрузка БД, RCE через `xp_cmdshell`/`COPY TO PROGRAM`/UDF.

---

## Функциональная семантика {#functional-semantics}

SQL — язык, в котором данные являются кодом: парсер не может отличить задуманную структуру запроса от внедрённой. Уязвимость возникает на границе, где строка с SQL формируется конкатенацией или интерполяцией недоверенных данных. Парсер БД обрабатывает результирующую строку как единый запрос; внедрённые токены изменяют дерево разбора, а не только значения данных.

**Каноническое изменение дерева разбора:**

```sql
-- Intended: SELECT * FROM users WHERE name = '<input>'
-- Input: ' OR '1'='1
-- Result:  SELECT * FROM users WHERE name = '' OR '1'='1'
--                                               ^^^^^^^^^^ injected predicate, always true
```

Ключевое различие: параметризованные запросы передают значение *после* разбора, поэтому дерево разбора фиксировано, а внедрённые SQL-токены трактуются как литеральные строковые данные.

---

## Неочевидные векторы инъекции {#non-obvious-injection-vectors}

### 1. «Запасные выходы» ORM: сырые запросы {#1-orm-escape-hatch-raw-queries}

```python
# VULNERABLE: Django ORM raw() with f-string
def search_users(request):
    username = request.GET['q']
    users = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")
    # Equivalent to classic injection; ORM provides zero protection here
```

```python
# FIXED: parameterized raw query
def search_users(request):
    username = request.GET['q']
    users = User.objects.raw(
        "SELECT * FROM auth_user WHERE username = %s",
        [username]
    )
```

**Функции сырых запросов ORM, обходящие параметризацию (все требуют ручной проверки):**
- Django: `Model.objects.raw()`, `connection.cursor().execute()` с интерполяцией, `extra(where=)`, `RawSQL()`
- SQLAlchemy: `text()` с `.format()` или f-строками, `engine.execute(string % values)`
- ActiveRecord: `where("name = '#{params[:name]}'")`
- Hibernate: `session.createNativeQuery(hql_string)` с конкатенацией строк
- GORM: `db.Raw("... " + userInput)`

### 2. Динамические имена таблиц и столбцов {#2-dynamic-table-and-column-names}

Параметризация применяется только к *значениям*, но не к идентификаторам (именам таблиц, столбцов, полям ORDER BY). В стандартном SQL идентификаторы параметризовать нельзя.

```python
# VULNERABLE: dynamic ORDER BY column
def get_sorted_data(request):
    col = request.GET.get('sort', 'name')
    query = f"SELECT * FROM products ORDER BY {col}"  # injection via sort=1; DROP TABLE products--
    return db.execute(query)
```

```python
# FIXED: allowlist identifiers
ALLOWED_SORT_COLUMNS = {'name', 'price', 'created_at'}

def get_sorted_data(request):
    col = request.GET.get('sort', 'name')
    if col not in ALLOWED_SORT_COLUMNS:
        col = 'name'
    query = f"SELECT * FROM products ORDER BY {col}"  # col is now validated
    return db.execute(query)
```

**Примечание:** экранирование идентификаторов кавычками (обратными или двойными) НЕ предотвращает инъекцию — злоумышленник может закрыть кавычку. Единственно безопасный подход для идентификаторов — allowlist.

### 3. Инъекция через шаблоны LIKE {#3-like-pattern-injection}

```javascript
// VULNERABLE: Node.js with pg - LIKE wildcard injection
async function searchProducts(req, res) {
    const term = req.query.term;
    // Attacker sends: term = %  → returns all rows
    // Attacker sends: term = \%anything\%  → escaping manipulation
    const result = await pool.query(
        `SELECT * FROM products WHERE name LIKE '%${term}%'`
    );
}
```

Даже при параметризации метасимволы LIKE (`%`, `_`) в *значении* приводят к DoS (полное сканирование таблицы) или неожиданным результатам. Это две отдельные проблемы:

```javascript
// FIXED: parameterize the whole pattern, escape LIKE metacharacters in value
async function searchProducts(req, res) {
    const term = req.query.term
        .replace(/\\/g, '\\\\')
        .replace(/%/g, '\\%')
        .replace(/_/g, '\\_');
    const result = await pool.query(
        'SELECT * FROM products WHERE name LIKE $1 ESCAPE \'\\\'',
        [`%${term}%`]
    );
}
```

### 4. Инъекция в путь JSON/JSONB в PostgreSQL {#4-postgresql-jsonjsonb-path-injection}

```python
# VULNERABLE: jsonb path in raw query
def filter_by_attr(conn, attr_name, value):
    query = f"SELECT * FROM items WHERE data->>'{attr_name}' = %s"
    # attr_name injection: ' OR 1=1 --  breaks out of jsonb operator context
    conn.execute(query, (value,))
```

```python
# FIXED: allowlist attr_name
ALLOWED_ATTRS = {'color', 'size', 'brand'}

def filter_by_attr(conn, attr_name, value):
    if attr_name not in ALLOWED_ATTRS:
        raise ValueError("Invalid attribute")
    query = f"SELECT * FROM items WHERE data->>{attr_name!r} = %s"
    conn.execute(query, (value,))
```

### 5. Резолверы GraphQL, формирующие сырые запросы {#5-graphql-resolvers-building-raw-queries}

```javascript
// VULNERABLE: GraphQL resolver constructing SQL
const resolvers = {
    Query: {
        user: async (_, { filter }) => {
            // filter = { field: "name", value: "alice' OR '1'='1" }
            const sql = `SELECT * FROM users WHERE ${filter.field} = '${filter.value}'`;
            return db.query(sql);
        }
    }
};
```

```javascript
// FIXED: parameterize and validate field name
const ALLOWED_FIELDS = new Set(['name', 'email', 'role']);

const resolvers = {
    Query: {
        user: async (_, { filter }) => {
            if (!ALLOWED_FIELDS.has(filter.field)) throw new Error('Invalid field');
            const sql = `SELECT * FROM users WHERE ${filter.field} = $1`;
            return db.query(sql, [filter.value]);
        }
    }
};
```

### 6. Инъекция второго порядка {#6-second-order-injection}

Данные сохранены корректно (с параметризацией), но позже извлечены и встроены в новый запрос без экранирования.

```sql
-- Registration: username 'admin'--  stored safely in DB
INSERT INTO users (username) VALUES ($1)  -- parameterized, safe

-- Password change: username retrieved from session, embedded into new query
SELECT * FROM users WHERE username = 'admin'--' AND password = 'x'
-- The -- comments out the password check
```

**Обнаружение:** проследите все пути, по которым данные, хранящиеся в БД, читаются и затем используются при формировании запроса. Параметризация на этапе записи не защищает путь «чтение → использование».

---

## Условия срабатывания {#trigger-conditions}

| Вектор | Условие срабатывания |
|--------|---------------------|
| Параметр запроса/тело HTTP | Пользовательский ввод напрямую попадает в запрос |
| Заголовок HTTP (User-Agent, Referer) | Записывается в БД через сырой INSERT |
| Cookie/значение сессии | Извлекается и используется в запросе |
| Поле JSON-тела | Извлечённое поле используется в динамическом SQL |
| Загрузка файла (имя файла) | Имя файла сохраняется или запрашивается без параметризации |
| Ответ внешнего API | Сохраняется, затем используется для инъекции второго порядка |
| `variables` в GraphQL | Любое поле передаётся в динамический SQL |

---

## Эвристики обнаружения {#detection-heuristics}

**Трассировка: вход HTTP → формирование запроса**

1. Определите все источники HTTP-входа: `request.GET`, `request.POST`, `request.headers`, cookies, сегменты пути URL, поля JSON-тела.
2. Проследите каждое значение через стек вызовов.
3. Отметьте любую точку, где значение (или его производное) конкатенируется или интерполируется в строку, передаваемую функции выполнения запроса к БД.
4. Отдельно проверьте: `cursor.execute(string)`, `raw()`, `text()`, вызовы f-строк/`.format()` в слое БД, оператор `+` над строками в функциях с именами `query`, `search`, `filter`, `find`, `fetch`.

**Шаблоны кода с высокой сигнальностью:**

```python
# Python - flag any of these patterns
f"SELECT ... {user_var}"
"SELECT ... " + user_var
"SELECT ... %s" % user_var   # % formatting - NOT parameterized (different from %s as placeholder)
cursor.execute("SELECT ... '" + val + "'")
```

```javascript
// JavaScript - flag these
`SELECT ... ${userVal}`
"SELECT ... " + userVal
db.query("SELECT ... '" + val + "'")
```

```java
// Java - flag these
"SELECT * FROM t WHERE x = '" + input + "'"
stmt.execute(String.format("SELECT ... %s", input))
```

**Специфичные для ORM «запасные выходы», которые стоит искать:**

```bash
# grep patterns for common ORMs
grep -rn "\.raw(" --include="*.py"
grep -rn "RawSQL(" --include="*.py"
grep -rn "extra(where" --include="*.py"
grep -rn "createNativeQuery" --include="*.java"
grep -rn "\.where(\".*#\{" --include="*.rb"    # Ruby string interpolation in ActiveRecord where
grep -rn "db\.Raw(" --include="*.go"
```

---

## Затронутые экосистемы {#affected-ecosystems}

| Экосистема | API параметризации | Частый «запасной выход» |
|-----------|-------------------|------------------------|
| Python/Django | плейсхолдеры `%s` в `execute()` | `raw()`, `extra()`, `RawSQL()` |
| Python/SQLAlchemy | `bindparam()`, `:name` в `text()` | `text()` с `.format()` |
| Node.js/pg | плейсхолдеры `$1`/`$2` | Template literals |
| Node.js/mysql2 | плейсхолдеры `?` | Template literals |
| Java/JDBC | `?` в `PreparedStatement` | `Statement.execute(string)` |
| PHP/PDO | `?` или `:name` | `query()` с конкатенацией |
| Ruby/ActiveRecord | `?` или условия-хэши | Интерполяция строк в `where()` |
| Go/database/sql | `?` или `$1` | `db.Exec(string)` с `+` |
| .NET/ADO.NET | `@param` в `SqlParameter` | `SqlCommand` с конкатенацией строк |

---

## Серьёзность в зависимости от СУБД {#database-specific-severity}

| БД | Эскалация помимо доступа к данным |
|----|----------------------------------|
| MSSQL | `xp_cmdshell` → выполнение команд ОС (при роли sysadmin) |
| PostgreSQL | `COPY TO PROGRAM` → выполнение команд ОС (при роли superuser) |
| MySQL | `INTO OUTFILE` → запись файлов в корень веб-сервера; загрузка UDF |
| SQLite | Чтение файлов через `ATTACH DATABASE`; эскалация ограничена |
| Oracle | `DBMS_SCHEDULER` → команды ОС (при роли DBA) |

---

## Шаблоны исправления {#fixing-patterns}

| Шаблон | Примечания |
|--------|-----------|
| Параметризованные запросы | Основная защита. Работает для всех типов значений. |
| Хранимые процедуры | Эффективны, если сама процедура использует параметризацию внутри |
| Allowlist для идентификаторов | Обязателен для таблиц/столбцов/ORDER BY; параметризации недостаточно |
| ORM с безопасным API запросов | Безопасны по умолчанию; проверяйте все аналоги `raw()` |
| WAF (Web Application Firewall) | Только эшелонированная защита; обходится, не является основным средством контроля |
| Принцип наименьших привилегий для учётной записи БД | Ограничивает радиус поражения; не предотвращает инъекцию |
| Подавление сообщений об ошибках | Затрудняет слепую инъекцию и перебор; не является исправлением |

---

## Особенности — признаки ложных срабатываний {#gotchas-false-positive-indicators}

- **Константные строки запроса без интерполяции:** `db.execute("SELECT 1")` — пользовательские данные не участвуют.
- **Целочисленные параметры, приведённые к типу до запроса:** `id = int(request.GET['id'])`, затем `f"WHERE id = {id}"` — приведение к целому исключает строковую инъекцию. Всё равно является запашком кода; предпочтительна параметризация.
- **Функции экранирования, применённые корректно:** `pg_escape_string()`, `mysql_real_escape_string()` в узких контекстах — технически безопасны для строковых значений, но не защищают идентификаторы и уязвимы, если набор символов изменяем. Не рекомендуются, но сами по себе не являются находкой.
- **Методы построителя запросов ORM (не сырые):** `User.objects.filter(name=value)` — параметризуется ORM; не является находкой. Только `.raw()` и `.extra()` являются запасными выходами.
- **Тестовый код и фикстуры:** жёстко заданные запросы в тестовых файлах с литералами вроде `'test_user'` — не являются находкой.

---

## См. также {#see-also}

- CWE-564: Hibernate Injection — вариант SQL-инъекции, специфичный для ORM
- CWE-943: Improper Neutralization — родительский класс для NoSQL-инъекций (MongoDB `$where` и т. п.)
- CWE-116: Encoding/Escaping — механизм защиты; смягчение через экранирование
- [[sql-injection-deep-dive]] — существующая статья базы знаний с более глубокими шаблонами эксплуатации
