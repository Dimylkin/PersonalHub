from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from settings.base import get_settings


settings = get_settings()

engine = create_async_engine(
    settings.DB.URL,
    echo=settings.DB.ECHO,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise