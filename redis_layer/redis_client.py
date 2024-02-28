# import redis
from redis.asyncio import Redis, from_url

from settings.redis_settings import REDIS_SETTINGS

redis_client: Redis = None


async def init_redis_pool():
    global redis_client
    redis_client = from_url(
        REDIS_SETTINGS['URL'],
        encoding="utf-8",
        decode_responses=True,
        # password=REDIS_SETTINGS['PASSWORD'],
    )


async def test():
    global redis_client
    await redis_client.set("TEST_KEY", "TEST_VALUE")
    print(await redis_client.get("TEST_KEY"))
