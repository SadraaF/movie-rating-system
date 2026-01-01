from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Checks connections for liveness
    echo=False,  # Set to True to see generated SQL statements
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)