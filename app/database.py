from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_URL_ASYNC


engine = create_engine(SQLALCHEMY_DATABASE_URL)
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, autocommit=False, autoflush=False)

def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db_context():
    async with AsyncSessionLocal() as async_db:
        yield async_db
