from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from apps.orders.models import Order
from apps.items.models import Item
from apps.user.models import User
from database.base_models import Base
from settings.db_settings import DB_SETTINGS

user = DB_SETTINGS['USER']
password = DB_SETTINGS['PASSWORD']
host = DB_SETTINGS['HOST']
db_name = DB_SETTINGS['NAME']
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}"

async_engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
metadata = Base.metadata
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
