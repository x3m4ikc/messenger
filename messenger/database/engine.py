from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

from config_reader import config

DB_USER = config.db_user.get_secret_value()
DB_NAME = config.db_name.get_secret_value()
DB_PASS = config.db_pass.get_secret_value()
DB_PORT = config.db_port.get_secret_value()
DB_HOST = config.db_host.get_secret_value()

engine = create_async_engine(
    url='postgresql+asyncpg://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME),
    echo=True
)

session_maker = async_sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)

metadata = MetaData()
Base = declarative_base()


async def get_db():
    async with session_maker() as session:
        yield session
