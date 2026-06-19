import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не задан в переменных окружения")

# важно: лог для проверки (очень помогает на Railway)
print("DATABASE_URL loaded:", DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()