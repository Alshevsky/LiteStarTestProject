import logging
from contextlib import asynccontextmanager
from typing import Coroutine

from litestar import Litestar
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from users_app.database.base import Base

logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/users_db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def create_db_and_tables(app: Litestar):
    logger.info("Creating tables and engine")
    if getattr(app.state, "engine", None) is None:
        app.state.engine = engine
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    logger.info("Tables created")
    try:
        yield
    finally:
        await engine.dispose()


async def get_session() -> AsyncSession:
    async with Session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            await session.close()


def session_connection(method: Coroutine):
    async def wrapper(*args, **kwargs):
        async with Session.begin() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
