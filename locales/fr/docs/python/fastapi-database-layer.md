---
title: "Couche d'accès aux données FastAPI (SQLAlchemy + Alembic)"
category: frameworks
tags: [python, fastapi, sqlalchemy, alembic, orm, database, dao, migrations]
level: 2
source_sha256: b039464c843bcfbb657ae16a56ca9883377baf9840668b11f8feb737d5e27270
translation: machine
translated_at: '2026-10-24'
---
# Couche d'accès aux données FastAPI (SQLAlchemy + Alembic) {#fastapi-database-layer-sqlalchemy-alembic}

SQLAlchemy est l'ORM Python le plus populaire. Dans FastAPI, il s'utilise avec des pilotes asynchrones (asyncpg pour PostgreSQL) et le patron DAO (Data Access Object) pour séparer proprement les routes des opérations de base de données. Alembic gère les migrations de schéma.

## Points clés {#key-facts}

- SQLAlchemy 2.0 utilise le style de requêtes `select()` (et non l'ancien `session.query()`)
- L'asynchrone nécessite un moteur asynchrone, une `AsyncSession` et un pilote asynchrone (asyncpg, aiosqlite)
- `Mapped[type]` + `mapped_column()` est le style moderne de définition des modèles
- Problème N+1 : utiliser `selectinload` (collections) ou `joinedload` (relation unique) pour le chargement anticipé (eager loading)
- Alembic génère automatiquement les migrations à partir des modifications des modèles
- Le patron DAO/Repository regroupe les opérations CRUD dans des méthodes de classe réutilisables

## Modèles {#patterns}

### Configuration du moteur et de la session {#engine-and-session-setup}
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/mydb"
)
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass
```

### Définition des modèles (SQLAlchemy 2.0) {#model-definition-sqlalchemy-20}
```python
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(200))
    stars: Mapped[int]
    rooms: Mapped[list["Room"]] = relationship(back_populates="hotel")

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    price: Mapped[int]
    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
```

### Opérations CRUD {#crud-operations}
```python
from sqlalchemy import select, update, delete, func

# Read
async with async_session() as session:
    query = select(Hotel).where(Hotel.location.ilike(f"%{location}%"))
    result = await session.execute(query)
    hotels = result.scalars().all()

# Create
async with async_session() as session:
    hotel = Hotel(name="Grand", location="Moscow", stars=5)
    session.add(hotel)
    await session.commit()

# Update
async with async_session() as session:
    query = update(Hotel).where(Hotel.id == id).values(stars=4)
    await session.execute(query)
    await session.commit()

# Delete
async with async_session() as session:
    query = delete(Hotel).filter_by(id=hotel_id)
    await session.execute(query)
    await session.commit()
```

### Patron DAO {#dao-pattern}
```python
class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, id):
        async with async_session() as session:
            query = select(cls.model).where(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        async with async_session() as session:
            instance = cls.model(**values)
            session.add(instance)
            await session.commit()
            return instance

class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def search_by_location(cls, location):
        async with async_session() as session:
            query = select(Hotel).where(Hotel.location.ilike(f"%{location}%"))
            result = await session.execute(query)
            return result.scalars().all()
```

### Chargement anticipé (éviter le N+1) {#eager-loading-avoiding-n1}
```python
from sqlalchemy.orm import selectinload, joinedload

# selectinload - separate SELECT (good for collections)
query = select(Hotel).options(selectinload(Hotel.rooms))

# joinedload - JOIN in same query (good for single objects)
query = select(Room).options(joinedload(Room.hotel))
```

### Requêtes complexes (sous-requêtes, jointures) {#complex-queries-subqueries-joins}
```python
booked = (
    select(Booking.room_id, func.count().label("booked"))
    .where(and_(Booking.date_from < date_to, Booking.date_to > date_from))
    .group_by(Booking.room_id)
    .subquery()
)

query = (
    select(Room, (Room.quantity - func.coalesce(booked.c.booked, 0)).label("rooms_left"))
    .outerjoin(booked, Room.id == booked.c.room_id)
    .where(Room.hotel_id == hotel_id)
)
```

### Migrations Alembic {#alembic-migrations}
```bash
alembic init migrations
# Configure alembic.ini with DB URL and env.py with Base.metadata

alembic revision --autogenerate -m "initial"  # generate from model changes
alembic upgrade head                           # apply migrations
alembic downgrade -1                           # rollback one step
alembic current                                # show current revision
```

### Unit of Work (transactions atomiques) {#unit-of-work-atomic-transactions}
```python
async with async_session() as session:
    async with session.begin():  # auto-commit or rollback
        session.add(user)
        session.add(booking)
        # Both saved atomically
```

## Pièges courants {#gotchas}

- `.scalars().all()` pour les requêtes sur un seul modèle ; `.all()` pour les requêtes sur plusieurs colonnes ou avec jointures
- `.scalars()` avec des requêtes multi-colonnes supprime silencieusement toutes les colonnes sauf la première
- Le chargement paresseux par défaut provoque des requêtes N+1 : utiliser systématiquement `selectinload`/`joinedload`
- Importer TOUS les modèles dans `env.py` pour qu'Alembic autogenerate les détecte
- `expire_on_commit=False` évite les erreurs d'accès aux attributs après un commit en mode asynchrone

## Voir aussi {#see-also}

- [[fastapi-fundamentals]] - routes, dépendances
- [[fastapi-pydantic-validation]] - conversion ORM vers Pydantic
- [[async-programming]] - sessions SQLAlchemy asynchrones
- [[sql-databases/index]] - fondamentaux SQL
