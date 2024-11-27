import contextlib
from typing import Any, AsyncIterator

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.utils import create_engine_url


class Base(DeclarativeBase):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}


# Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
class DatabaseSessionManager:
    def __init__(
        self, async_host: str, sync_host: str, engine_kwargs: dict[str, Any] = {}
    ):
        self._async_engine = create_async_engine(async_host, **engine_kwargs)
        self._sync_engine = create_engine(sync_host, **engine_kwargs)  # sync engine is used only for db migration

        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._async_engine, expire_on_commit=False
        )

    async def close(self):
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._async_engine.dispose()

        self._async_engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._async_engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


session_manager = DatabaseSessionManager(
    create_engine_url(settings, async_driver=True),
    create_engine_url(settings, async_driver=False),
    {"echo": settings.echo_sql},
)


async def get_db_session():
    async with session_manager.session() as session:
        yield session
