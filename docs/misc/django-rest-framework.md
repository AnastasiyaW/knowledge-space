---
title: Django REST Framework and ORM Patterns
category: concepts
tags: [misc, python, django, drf, rest-api, orm, serializers]
---

# Django REST Framework and ORM Patterns

Django REST Framework serializer patterns, relationship handling, validation, and advanced ORM techniques including Q/F objects, annotations, and query optimization.

## Key Facts

- DRF offers 5 relationship serialization approaches: PrimaryKey, String, Slug, Hyperlinked, Nested
- Field-level validation: `validate_<fieldname>(self, value)` method
- Object-level validation: `validate(self, data)` for cross-field checks
- `select_related` (JOIN) for ForeignKey/OneToOne; `prefetch_related` (separate query) for ManyToMany
- `F()` objects reference field values in queries without loading data to Python
- `Q()` objects enable complex WHERE clauses with OR, NOT operators

## Patterns

### Serializer Related Field Types

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

**Selection guide**:
- PrimaryKey: most efficient, minimal data transfer
- StringRelated: display-only, not useful for writes
- Slug: human-readable identifier without extra requests
- Hyperlinked: HATEOAS-style APIs
- Nested: complete data in one response, risk of N+1 queries

### Validation

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

### Django ORM Advanced Patterns

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

## Gotchas

- Nested serializers can cause N+1 queries - always use `select_related`/`prefetch_related` in view queryset
- `write_only=True` in `extra_kwargs` prevents field from appearing in response
- `validate_<field>` runs after field-level validators; `validate()` runs last
- `F()` operations happen in the database, not Python - you cannot use Python functions with them
- `select_related` follows ForeignKey forward; `prefetch_related` works for reverse relations and M2M

## See Also

- [[python-web-scraping]] - data collection that feeds into Django models
- [[python-stdlib-patterns]] - Python data processing patterns
- [[sql-advanced-patterns]] - raw SQL equivalent of ORM operations
