---
title: "Django REST Framework et modèles de l'ORM"
category: concepts
tags: [python, django, drf, rest-api, orm, serializers]
level: 3
source_sha256: eaac09ce17fa260632df116fcca09b6670761f21a4b923e14fe462d1f0dd8386
translation: machine
translated_at: '2026-10-24'
---
# Django REST Framework et modèles de l'ORM {#django-rest-framework-and-orm-patterns}

Modèles de sérialiseurs Django REST Framework, gestion des relations, validation et techniques avancées de l'ORM, notamment les objets Q/F, les annotations et l'optimisation des requêtes.

## Points clés {#key-facts}

- DRF propose 5 approches de sérialisation des relations : PrimaryKey, String, Slug, Hyperlinked, Nested
- Validation au niveau des champs : méthode `validate_<fieldname>(self, value)`
- Validation au niveau de l'objet : `validate(self, data)` pour les contrôles inter-champs
- `select_related` (JOIN) pour ForeignKey/OneToOne ; `prefetch_related` (requête séparée) pour ManyToMany
- Les objets `F()` référencent les valeurs des champs dans les requêtes sans charger les données en Python
- Les objets `Q()` permettent des clauses WHERE complexes avec les opérateurs OR et NOT

## Modèles {#patterns}

### Types de champs de relation des sérialiseurs {#serializer-related-field-types}

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

**Guide de sélection** :
- PrimaryKey : le plus efficace, transfert de données minimal
- StringRelated : affichage uniquement, peu utile pour les écritures
- Slug : identifiant lisible par un humain, sans requêtes supplémentaires
- Hyperlinked : API de style HATEOAS
- Nested : données complètes dans une seule réponse, risque de requêtes N+1

### Validation {#validation}

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

### Modèles avancés de l'ORM Django {#django-orm-advanced-patterns}

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

## Pièges courants {#gotchas}

- Les sérialiseurs imbriqués peuvent générer des requêtes N+1 : utilisez toujours `select_related`/`prefetch_related` dans le queryset de la vue
- `write_only=True` dans `extra_kwargs` empêche le champ d'apparaître dans la réponse
- `validate_<field>` s'exécute après les validateurs au niveau des champs ; `validate()` s'exécute en dernier
- Les opérations `F()` s'exécutent dans la base de données, et non en Python : vous ne pouvez pas utiliser de fonctions Python avec elles
- `select_related` suit les ForeignKey dans le sens direct ; `prefetch_related` fonctionne pour les relations inverses et les M2M

## Voir aussi {#see-also}

- [[web-scraping]] - collecte de données alimentant les modèles Django
- [[stdlib-patterns]] - modèles de traitement de données en Python
- [[sql-databases/advanced-patterns]] - équivalent SQL brut des opérations de l'ORM
