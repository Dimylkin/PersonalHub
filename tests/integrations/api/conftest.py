import os
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.parse import urlparse

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from docker.errors import DockerException
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer

from app.application import get_app
from database.postgres.tables.board import BoardDB
from database.postgres.tables.column import ColumnDB
from database.postgres.tables.task import TaskDB
from database.postgres.session import get_session
from settings.base import AppSettings, DBSettings, Settings


def get_test_settings(async_url: str) -> Settings:
    parsed = urlparse(async_url)

    settings = object.__new__(Settings)

    settings.APP = AppSettings(
        APP_NAME="personalhub-test",
        HOST="127.0.0.1",
        APP_PORT=8000,
    )

    settings.DB = DBSettings(
        DB_HOST=parsed.hostname or "localhost",
        DB_PORT=parsed.port or 5432,
        DB_USER=parsed.username or "test",
        DB_PASSWORD=parsed.password or "test",
        DB_NAME=parsed.path.lstrip("/"),
    )

    return settings


@pytest.fixture(autouse=True)
def mock_settings(async_url: str):
    test_settings = get_test_settings(async_url)

    with (
        patch("settings.base.get_settings", return_value=test_settings),
    ):
        yield


_DOCKER_SOCKET_CANDIDATES = [
    Path.home() / ".docker" / "run" / "docker.sock",
    Path("/var/run/docker.sock"),
    Path("/run/docker.sock"),
]

_POSTGRES_IMAGE = os.getenv("POSTGRES_IMAGE", "postgres:16")


def resolve_docker_host() -> None:
    if os.environ.get("DOCKER_HOST"):
        return

    for candidate in _DOCKER_SOCKET_CANDIDATES:
        if candidate.exists():
            os.environ["DOCKER_HOST"] = f"unix://{candidate}"
            os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")
            return


@pytest.fixture(scope="session")
def container() -> Generator[PostgresContainer, Any]:
    resolve_docker_host()

    try:
        postgres = PostgresContainer(
            image=_POSTGRES_IMAGE,
            username="test",
            password="test",
            dbname="test",
        )
        postgres.start()

        yield postgres

        postgres.stop()
    except DockerException as exc:
        pytest.fail(f"Docker недоступен: {exc}")


@pytest.fixture(scope="session")
def sync_url(container: PostgresContainer) -> str:
    return container.get_connection_url()


@pytest.fixture(scope="session")
def async_url(sync_url: str) -> str:
    return (
        sync_url
        .replace("postgresql+psycopg2://", "postgresql+asyncpg://")
        .replace("postgresql+psycopg://", "postgresql+asyncpg://")
        .replace("postgresql://", "postgresql+asyncpg://")
    )


@pytest.fixture(scope="session")
def apply_migrations(sync_url: str):
    project_root = Path(__file__).resolve().parents[3]

    alembic_ini_path = project_root / "alembic.ini"
    migrations_path = project_root / "src" / "database" / "postgres" / "migrations"

    cfg = Config(str(alembic_ini_path))
    cfg.set_main_option("script_location", str(migrations_path))
    cfg.set_main_option(
        "sqlalchemy.url",
        sync_url
        .replace("postgresql+asyncpg://", "postgresql+psycopg://")
        .replace("postgresql+psycopg2://", "postgresql+psycopg://")
        .replace("postgresql://", "postgresql+psycopg://"),
    )

    command.upgrade(cfg, "head")

    yield


@pytest.fixture(scope="session")
def engine(
    async_url: str,
    apply_migrations,
) -> Generator[AsyncEngine, Any]:
    engine = create_async_engine(
        async_url,
        echo=False,
        poolclass=NullPool,
    )

    yield engine


@pytest.fixture(scope="session")
def session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture(scope="function")
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with session_factory() as test_session:
        yield test_session


@pytest_asyncio.fixture(scope="function")
async def clean_db(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[None]:
    async with session_factory() as session:
        await session.execute(delete(TaskDB))
        await session.execute(delete(ColumnDB))
        await session.execute(delete(BoardDB))
        await session.commit()

    yield

    async with session_factory() as session:
        await session.execute(delete(TaskDB))
        await session.execute(delete(ColumnDB))
        await session.execute(delete(BoardDB))
        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def client(
    clean_db: None,
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncClient]:
    app = get_app()

    async def override_get_session() -> AsyncGenerator[AsyncSession]:
        async with session_factory() as test_session:
            try:
                yield test_session
                await test_session.commit()
            except Exception:
                await test_session.rollback()
                raise

    app.dependency_overrides[get_session] = override_get_session

    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as test_client:
            yield test_client

    app.dependency_overrides.clear()
