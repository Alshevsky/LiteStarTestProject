import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from users_app.database.base import Base
from users_app.database.config import DATABASE_URL


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def session(test_engine):
    """Create a test database session."""
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture
async def async_client():
    """Create an async HTTP client."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client
