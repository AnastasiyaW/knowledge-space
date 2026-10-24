---
title: "FastAPI-Datenbankschicht (SQLAlchemy + Alembic)"
category: frameworks
tags: [python, fastapi, sqlalchemy, alembic, orm, database, dao, migrations]
level: 2
source_sha256: b039464c843bcfbb657ae16a56ca9883377baf9840668b11f8feb737d5e27270
translation: machine
translated_at: '2026-10-24'
---
# FastAPI-Datenbankschicht (SQLAlchemy + Alembic) {#fastapi-database-layer-sqlalchemy-alembic}

SQLAlchemy ist der populärste Python-ORM. In FastAPI wird er mit asynchronen Treibern (asyncpg für PostgreSQL) und dem DAO-Muster (Data Access Object) verwendet, um Routen und Datenbankoperationen sauber zu trennen. Alembic übernimmt die Schema-Migrationen.

## Wichtige Fakten {#key-facts}

- SQLAlchemy 2.0 verwendet `select()`-Abfragen (nicht das veraltete `session.query()`)
- Async erfordert eine asynchrone Engine, `AsyncSession` und einen asynchronen Treiber (asyncpg, aiosqlite)
- `Mapped[type]` + `mapped_column()` ist der moderne Stil zur Modelldefinition
- N+1-Problem: `selectinload` (Collections) oder `joinedload` (einzelne Relation) für Eager Loading verwenden
- Alembic erzeugt Migrationen automatisch aus Änderungen an den Modellen
- Das DAO-/Repository-Muster kapselt CRUD in wiederverwendbare Klassenmethoden

## Muster {#patterns}

### Engine- und Session-Setup {#engine-and-session-setup}
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

### Modelldefinition (SQLAlchemy 2.0) {#model-definition-sqlalchemy-20}
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

### CRUD-Operationen {#crud-operations}
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

### DAO-Muster {#dao-pattern}
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

### Eager Loading (Vermeidung von N+1) {#eager-loading-avoiding-n1}
```python
from sqlalchemy.orm import selectinload, joinedload

# selectinload - separate SELECT (good for collections)
query = select(Hotel).options(selectinload(Hotel.rooms))

# joinedload - JOIN in same query (good for single objects)
query = select(Room).options(joinedload(Room.hotel))
```

### Komplexe Abfragen (Subqueries, Joins) {#complex-queries-subqueries-joins}
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

### Alembic-Migrationen {#alembic-migrations}
```bash
alembic init migrations
# Configure alembic.ini with DB URL and env.py with Base.metadata

alembic revision --autogenerate -m "initial"  # generate from model changes
alembic upgrade head                           # apply migrations
alembic downgrade -1                           # rollback one step
alembic current                                # show current revision
```

### Unit of Work (atomare Transaktionen) {#unit-of-work-atomic-transactions}
```python
async with async_session() as session:
    async with session.begin():  # auto-commit or rollback
        session.add(user)
        session.add(booking)
        # Both saved atomically
```

## Fallstricke {#gotchas}

- `.scalars().all()` für Abfragen auf einzelne Modelle; `.all()` für Abfragen mit mehreren Spalten oder Joins
- `.scalars()` bei Abfragen mit mehreren Spalten verwirft stillschweigend alle Spalten außer der ersten
- Standardmäßiges Lazy Loading verursacht N+1-Abfragen – immer `selectinload`/`joinedload` verwenden
- Alle Modelle in `env.py` importieren, damit Alembic Autogenerate sie erkennt
- `expire_on_commit=False` verhindert Attributzugriffsfehler nach einem Commit im async-Betrieb

## Siehe auch {#see-also}

- [[fastapi-fundamentals]] - Routen, Dependencies
- [[fastapi-pydantic-validation]] - Konvertierung von ORM zu Pydantic
- [[async-programming]] - asynchrone SQLAlchemy-Sessions
- [[sql-databases/index]] - SQL-Grundlagen
