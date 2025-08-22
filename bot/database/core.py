from bot.configs.configs import db_configs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(url=db_configs.DATABASE_URL.get_secret_value())

SessionLocal = async_sessionmaker(engine, class_=AsyncSession)