from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# The engine manages the connection pool to PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Prints SQL queries in terminal when DEBUG=True
    pool_size=5,          # Keep 5 connections ready
    max_overflow=10,      # Allow up to 10 extra connections under load
)

# Session factory — creates new database sessions
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Base class for all our database table models
class Base(DeclarativeBase):
    pass


async def get_db_session() -> AsyncSession:
    """
    Creates a database session for a single request.
    Used as a FastAPI dependency.
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
