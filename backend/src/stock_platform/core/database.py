from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from redis.asyncio import Redis
from motor.motor_asyncio import AsyncIOMotorClient
from core.settings import settings
import asyncio

Base = declarative_base()

async_engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}",
    echo=settings.debug,
    pool_size=20,
    max_overflow=50,
)

AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True
)

mongo_client = AsyncIOMotorClient(settings.mongodb_url)
mongo_db = mongo_client[settings.mongodb_db]

_lock_initialized = False
_lock = None

def get_lock():
    global _lock_initialized, _lock
    if not _lock_initialized:
        _lock = asyncio.Lock()
        _lock_initialized = True
    return _lock

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_redis():
    yield redis_client

async def get_mongo():
    yield mongo_db

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def init_database():
    lock = get_lock()
    async with lock:
        await create_tables()