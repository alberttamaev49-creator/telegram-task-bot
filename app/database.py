import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не задан")

print("DATABASE_URL loaded:", DATABASE_URL)

# FIX: убираем sslmode (ломает SQLAlchemy async)
if "sslmode" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()