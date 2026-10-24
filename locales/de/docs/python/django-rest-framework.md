---
title: "Django REST Framework und ORM-Muster"
category: concepts
tags: [python, django, drf, rest-api, orm, serializers]
level: 3
source_sha256: eaac09ce17fa260632df116fcca09b6670761f21a4b923e14fe462d1f0dd8386
translation: machine
translated_at: '2026-10-24'
---
# Django REST Framework und ORM-Muster {#django-rest-framework-and-orm-patterns}

Serializer-Muster für Django REST Framework, Beziehungsbehandlung, Validierung sowie fortgeschrittene ORM-Techniken einschließlich Q/F-Objekten, Annotationen und Abfrageoptimierung.

## Wichtige Fakten {#key-facts}

- DRF bietet 5 Ansätze zur Serialisierung von Beziehungen: PrimaryKey, String, Slug, Hyperlinked, Nested
- Feldbezogene Validierung: `validate_<fieldname>(self, value)`-Methode
- Objektbezogene Validierung: `validate(self, data)` für feldübergreifende Prüfungen
- `select_related` (JOIN) für ForeignKey/OneToOne; `prefetch_related` (separate Abfrage) für ManyToMany
- `F()`-Objekte referenzieren Feldwerte in Abfragen, ohne Daten in Python zu laden
- `Q()`-Objekte ermöglichen komplexe WHERE-Klauseln mit OR- und NOT-Operatoren

## Muster {#patterns}

### Typen serialisierter Beziehungsfelder {#serializer-related-field-types}

```python
class BookSerializer(serializers.Serializer):
    # 1. PrimaryKeyRelatedField - FK integer
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    # {"author": 42}

    # 2. StringRelatedField - calls __str__()
    author = serializers.StringRelatedField()
    # {"author": "Ernest Hemingway"}

    # 3. SlugRelatedField - specific field
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # {"author": "e.hemingway"}

    # 4. HyperlinkedRelatedField - URL
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )
    # {"author": "http://api.example.com/authors/42/"}

    # 5. Nested serializer - full object
    author = AuthorSerializer(read_only=True)
    # {"author": {"id": 42, "name": "Ernest Hemingway", ...}}
```

**Auswahlhilfe**:
- PrimaryKey: am effizientesten, minimale Datenübertragung
- StringRelated: nur zur Anzeige, für Schreiboperationen nicht geeignet
- Slug: menschenlesbarer Bezeichner ohne zusätzliche Anfragen
- Hyperlinked: APIs im HATEOAS-Stil
- Nested: vollständige Daten in einer Antwort, Risiko von N+1-Abfragen

### Validierung {#validation}

```python
class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}
```

### Fortgeschrittene Muster des Django ORM {#django-orm-advanced-patterns}

```python
from django.db.models import Q, F, Count, Avg, Sum, Prefetch

# Q objects for complex WHERE
Employee.objects.filter(
    Q(department='Engineering') | Q(salary__gt=100000)
)
Employee.objects.filter(~Q(department='HR'))  # NOT

# F objects - field references without Python loading
Employee.objects.filter(salary__gt=F('min_salary') * 2)
Employee.objects.update(salary=F('salary') * 1.1)  # 10% raise for all

# Annotations
Employee.objects.annotate(
    bonus=F('salary') * 0.1,
    team_size=Count('department__employees')
)

# select_related (JOIN, ForeignKey/OneToOne)
Order.objects.select_related('customer', 'customer__address')

# prefetch_related (separate query, ManyToMany/reverse FK)
Author.objects.prefetch_related(
    Prefetch('books', queryset=Book.objects.filter(published=True))
)

# Aggregations
result = Order.objects.aggregate(
    total=Sum('amount'),
    average=Avg('amount'),
    count=Count('id')
)
```

## Fallstricke {#gotchas}

- Verschachtelte Serializer können N+1-Abfragen verursachen – verwenden Sie im View-Queryset immer `select_related`/`prefetch_related`
- `write_only=True` in `extra_kwargs` verhindert, dass das Feld in der Antwort erscheint
- `validate_<field>` läuft nach den feldbezogenen Validatoren; `validate()` läuft zuletzt
- `F()`-Operationen werden in der Datenbank ausgeführt, nicht in Python – Python-Funktionen können damit nicht verwendet werden
- `select_related` folgt ForeignKey vorwärts; `prefetch_related` funktioniert für Rückwärtsbeziehungen und M2M

## Siehe auch {#see-also}

- [[web-scraping]] – Datensammlung, die in Django-Modelle einfließt
- [[stdlib-patterns]] – Muster zur Datenverarbeitung in Python
- [[sql-databases/advanced-patterns]] – SQL-Entsprechung der ORM-Operationen
