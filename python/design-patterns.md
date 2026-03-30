---
title: Design Patterns in Python
category: patterns
tags: [python, design-patterns, singleton, factory, observer, strategy, repository, dependency-injection]
---

# Design Patterns in Python

Classical design patterns adapted to Python's dynamic nature. Many GoF patterns are simplified or unnecessary in Python thanks to first-class functions, duck typing, and built-in features. This entry covers the patterns most commonly used in Python backend development.

## Key Facts

- Python's first-class functions replace Strategy, Command, and Template Method patterns without classes
- Singleton is rarely needed -- module-level instances serve the same purpose
- Repository pattern separates data access from business logic; widely used with SQLAlchemy and FastAPI
- Factory pattern is useful for creating objects based on configuration or runtime conditions
- Observer pattern is implemented via callbacks, signals (blinker), or event systems
- Dependency injection in Python uses constructor injection and FastAPI's `Depends()`
- `functools.lru_cache` replaces manual Flyweight/Object Pool patterns
- See [[fastapi-dependency-injection]] for DI patterns, [[oop-inheritance-and-mro]] for ABC and Protocol

## Patterns

### Repository Pattern

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, id: int) -> T | None: ...

    @abstractmethod
    async def create(self, entity: T) -> T: ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 20) -> list[T]: ...

class SQLAlchemyUserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> User | None:
        return await self.session.get(User, id)

    async def create(self, entity: User) -> User:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def list(self, skip: int = 0, limit: int = 20) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
```

### Strategy Pattern (Pythonic -- Functions)

```python
from typing import Callable

# Strategy as functions -- no class hierarchy needed
def compress_gzip(data: bytes) -> bytes:
    import gzip
    return gzip.compress(data)

def compress_zstd(data: bytes) -> bytes:
    import zstandard
    return zstandard.ZstdCompressor().compress(data)

def compress_none(data: bytes) -> bytes:
    return data

# Strategy selection
STRATEGIES: dict[str, Callable[[bytes], bytes]] = {
    "gzip": compress_gzip,
    "zstd": compress_zstd,
    "none": compress_none,
}

def process_data(data: bytes, compression: str = "gzip") -> bytes:
    compress = STRATEGIES[compression]
    return compress(data)
```

### Factory Pattern

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> None: ...

class EmailNotification(Notification):
    def send(self, message: str, recipient: str) -> None:
        print(f"Email to {recipient}: {message}")

class SMSNotification(Notification):
    def send(self, message: str, recipient: str) -> None:
        print(f"SMS to {recipient}: {message}")

class PushNotification(Notification):
    def send(self, message: str, recipient: str) -> None:
        print(f"Push to {recipient}: {message}")

def create_notification(channel: str) -> Notification:
    """Factory function -- returns appropriate implementation."""
    factories: dict[str, type[Notification]] = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }
    cls = factories.get(channel)
    if not cls:
        raise ValueError(f"Unknown channel: {channel}")
    return cls()
```

### Singleton (Module-Level Instance)

```python
# Python way: module-level instance replaces Singleton class

# config.py
class _Settings:
    def __init__(self):
        self.debug = False
        self.database_url = ""

    def load_from_env(self):
        import os
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.database_url = os.getenv("DATABASE_URL", "")

settings = _Settings()  # module-level singleton
settings.load_from_env()

# Usage in other modules:
# from config import settings
# if settings.debug: ...
```

### Observer Pattern (Event System)

```python
from typing import Callable, Any
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable) -> None:
        self._subscribers[event].append(handler)

    def publish(self, event: str, **data: Any) -> None:
        for handler in self._subscribers[event]:
            handler(**data)

    def on(self, event: str):
        """Decorator for subscribing to events."""
        def decorator(func):
            self.subscribe(event, func)
            return func
        return decorator

bus = EventBus()

@bus.on("user.created")
def send_welcome_email(user_id: int, email: str, **_):
    print(f"Sending welcome email to {email}")

@bus.on("user.created")
def track_analytics(user_id: int, **_):
    print(f"Tracking user {user_id} creation")

bus.publish("user.created", user_id=1, email="alice@example.com")
```

### Unit of Work Pattern

```python
class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.orders = OrderRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

# Usage
async with UnitOfWork(SessionLocal) as uow:
    user = await uow.users.create(User(name="Alice"))
    order = await uow.orders.create(Order(user_id=user.id, total=99.99))
    # Both committed together, or both rolled back
```

## Gotchas

- **Over-engineering patterns**: Python's duck typing and first-class functions make many GoF patterns unnecessary. A dict of functions replaces Strategy; a module variable replaces Singleton; `@dataclass` replaces Builder for most cases
- **Repository + ORM antipattern**: wrapping every ORM call in a repository method can lead to a thin wrapper that adds complexity without value. Use repositories when you need to swap data sources or add business logic on top of queries
- **Observer memory leaks**: event bus holding references to handler functions prevents garbage collection of objects those functions close over. Use `weakref` for long-lived event systems
- **Factory return types**: type checkers struggle with factory functions returning different types. Use `@overload` or generic return types to maintain type safety
- **Singleton state in tests**: module-level singletons persist across tests. Use dependency injection (`Depends`) to override them in test environments

## See Also

- [Python Design Patterns](https://python-patterns.guide/)
- [Cosmic Python -- Architecture Patterns](https://www.cosmicpython.com/)
- [[fastapi-dependency-injection]] - DI as a pattern
- [[oop-inheritance-and-mro]] - ABC and Protocol for interfaces
