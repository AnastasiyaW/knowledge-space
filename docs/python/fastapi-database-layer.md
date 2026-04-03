---
title: FastAPI Database Layer (SQLAlchemy + Alembic)
category: frameworks
tags: [python, fastapi, sqlalchemy, alembic, orm, database, dao, migrations]
---

# FastAPI Database Layer (SQLAlchemy + Alembic)

SQLAlchemy is the most popular Python ORM. In FastAPI, it's used with async drivers (asyncpg for PostgreSQL) and the DAO (Data Access Object) pattern for clean separation between routes and database operations. Alembic handles schema migrations.

## Key Facts

- SQLAlchemy 2.0 uses `select()` style queries (not legacy `session.query()`)
- Async requires async engine + AsyncSession + async driver (asyncpg, aiosqlite)
- `Mapped[type]` + `mapped_column()` is the modern model definition style
- N+1 problem: use `selectinload` (collections) or `joinedload` (single related) for eager loading
- Alembic autogenerates migrations from model changes
- DAO/Repository pattern abstracts CRUD into reusable class methods

## Patterns

### Engine and Session Setup
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

### Model Definition (SQLAlchemy 2.0)
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

### CRUD Operations
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

### DAO Pattern
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

### Eager Loading (Avoiding N+1)
```python
from sqlalchemy.orm import selectinload, joinedload

# selectinload - separate SELECT (good for collections)
query = select(Hotel).options(selectinload(Hotel.rooms))

# joinedload - JOIN in same query (good for single objects)
query = select(Room).options(joinedload(Room.hotel))
```

### Complex Queries (Subqueries, Joins)
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

### Alembic Migrations
```bash
alembic init migrations
# Configure alembic.ini with DB URL and env.py with Base.metadata

alembic revision --autogenerate -m "initial"  # generate from model changes
alembic upgrade head                           # apply migrations
alembic downgrade -1                           # rollback one step
alembic current                                # show current revision
```

### Unit of Work (Atomic Transactions)
```python
async with async_session() as session:
    async with session.begin():  # auto-commit or rollback
        session.add(user)
        session.add(booking)
        # Both saved atomically
```

## Gotchas

- `.scalars().all()` for single-model queries; `.all()` for multi-column/join queries
- `.scalars()` with multi-column queries silently drops all columns except the first
- Default lazy loading causes N+1 queries - always use `selectinload`/`joinedload`
- Import ALL models in `env.py` for Alembic autogenerate to detect them
- `expire_on_commit=False` prevents attribute access errors after commit in async

## See Also

- [[fastapi-fundamentals]] - routes, dependencies
- [[fastapi-pydantic-validation]] - ORM to Pydantic conversion
- [[async-programming]] - async SQLAlchemy sessions
- [[sql-databases/index]] - SQL fundamentals
