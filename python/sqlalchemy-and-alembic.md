---
title: SQLAlchemy and Alembic
category: concepts
tags: [python, sqlalchemy, alembic, orm, database, migrations, async, postgresql]
---

# SQLAlchemy and Alembic

**SQLAlchemy** is Python's SQL toolkit and ORM. SQLAlchemy 2.0 introduced a new declarative syntax with `mapped_column()`, native async support, and strict typing. **Alembic** is the migration tool for SQLAlchemy, managing database schema versioning through Python migration scripts.

## Key Facts

- SQLAlchemy 2.0 style: `DeclarativeBase`, `Mapped[type]`, `mapped_column()` replace legacy `Column()` and `declarative_base()`
- `create_async_engine()` + `async_sessionmaker()` for async database access (requires `asyncpg` or `aiosqlite`)
- Relationships: `relationship()` with `back_populates` for bidirectional; lazy loading modes: `select`, `joined`, `subquery`, `selectin`
- `select()` constructs queries; `session.execute(stmt)` runs them; `.scalars()` extracts ORM objects
- Alembic `alembic init` creates migration environment; `alembic revision --autogenerate` detects model changes
- `alembic upgrade head` applies all pending migrations; `alembic downgrade -1` reverts one step
- Connection pooling: `pool_size`, `max_overflow`, `pool_recycle` control connection lifecycle
- See [[fastapi-dependency-injection]] for session-per-request pattern, [[dataclasses-and-pydantic]] for model serialization

## Patterns

### SQLAlchemy 2.0 Model Definition

```python
from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    orders: Mapped[list["Order"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r})"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    total: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="orders")
```

### Async Engine and Session

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/mydb"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=False,  # True for SQL logging
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Usage in FastAPI dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Query Patterns (2.0 Style)

```python
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

# Basic select
stmt = select(User).where(User.email == "alice@example.com")
result = await session.execute(stmt)
user = result.scalar_one_or_none()

# Filter with multiple conditions
stmt = (
    select(User)
    .where(and_(User.is_active == True, User.name.ilike("%alice%")))
    .order_by(User.created_at.desc())
    .limit(10)
    .offset(0)
)
users = (await session.execute(stmt)).scalars().all()

# Eager loading relationships
stmt = (
    select(User)
    .where(User.id == user_id)
    .options(selectinload(User.orders))
)
user = (await session.execute(stmt)).scalar_one()
# user.orders is already loaded -- no extra query

# Aggregations
stmt = select(func.count(User.id)).where(User.is_active == True)
count = (await session.execute(stmt)).scalar()
```

### CRUD Operations

```python
# Create
user = User(name="Alice", email="alice@example.com")
session.add(user)
await session.flush()  # assigns user.id without committing

# Update
user.name = "Alice Updated"
await session.flush()

# Bulk update
stmt = (
    update(User)
    .where(User.is_active == False)
    .values(deleted_at=func.now())
)
await session.execute(stmt)

# Delete
await session.delete(user)
await session.flush()
```

### Alembic Setup and Usage

```bash
# Initialize Alembic
alembic init alembic

# Generate migration from model changes
alembic revision --autogenerate -m "add users table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

```python
# alembic/env.py -- async configuration
from app.models import Base

target_metadata = Base.metadata

# Migration file example
def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

def downgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
```

## Gotchas

- **Lazy loading in async**: default lazy loading (`select`) triggers a sync query which fails in async sessions with `MissingGreenlet`. Always use eager loading (`selectinload`, `joinedload`) or set `lazy="selectin"` on relationships
- **`expire_on_commit=False`**: without this, accessed attributes raise `DetachedInstanceError` after commit. Set on `sessionmaker` for FastAPI response serialization
- **Alembic autogenerate misses**: autogenerate does not detect column type changes (e.g., `String(50)` -> `String(100)`), table renames, or custom constraints. Review generated migrations manually
- **N+1 query problem**: accessing `user.orders` for each user in a list triggers one query per user. Use `selectinload(User.orders)` to batch-load in a single query
- **Connection pool exhaustion**: forgetting to close sessions (missing `yield` in FastAPI dependency) leaks connections. The pool eventually blocks, causing request timeouts

## See Also

- [SQLAlchemy 2.0 docs](https://docs.sqlalchemy.org/en/20/)
- [Alembic docs](https://alembic.sqlalchemy.org/)
- [[fastapi-dependency-injection]] - session-per-request pattern
- [[dataclasses-and-pydantic]] - Pydantic models for response serialization
