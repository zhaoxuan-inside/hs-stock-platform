import asyncio
import uuid
from redis.asyncio import Redis
from core.database import redis_client
from datetime import timedelta


class DistributedLock:
    def __init__(self, redis: Redis, lock_name: str, expire: int = 30, timeout: int = 10):
        self.redis = redis
        self.lock_name = f"lock:{lock_name}"
        self.expire = expire
        self.timeout = timeout
        self.lock_value = None
        self._refresh_task = None
        self._refresh_interval = max(1, expire // 3)

    async def acquire(self) -> bool:
        deadline = asyncio.get_event_loop().time() + self.timeout
        self.lock_value = str(uuid.uuid4())

        while asyncio.get_event_loop().time() < deadline:
            result = await self.redis.set(
                self.lock_name,
                self.lock_value,
                ex=self.expire,
                nx=True
            )
            if result:
                await self._start_refresh()
                return True
            await asyncio.sleep(0.1)
        return False

    async def release(self):
        if self._refresh_task:
            self._refresh_task.cancel()
            self._refresh_task = None

        if self.lock_value:
            script = """
            if redis.call("get", KEYS[1]) == ARGV[1] then
                return redis.call("del", KEYS[1])
            else
                return 0
            end
            """
            await self.redis.eval(script, 1, self.lock_name, self.lock_value)
            self.lock_value = None

    async def _start_refresh(self):
        async def refresh():
            while True:
                await asyncio.sleep(self._refresh_interval)
                if self.lock_value:
                    await self.redis.set(
                        self.lock_name,
                        self.lock_value,
                        ex=self.expire,
                        xx=True
                    )
        self._refresh_task = asyncio.create_task(refresh())

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.release()


async def get_lock(lock_name: str, expire: int = 30, timeout: int = 10) -> DistributedLock:
    return DistributedLock(redis_client, lock_name, expire, timeout)


async def with_lock(lock_name: str, func, *args, expire: int = 30, timeout: int = 10, **kwargs):
    async with DistributedLock(redis_client, lock_name, expire, timeout):
        return await func(*args, **kwargs)