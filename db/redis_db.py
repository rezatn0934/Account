import redis.asyncio as aioredis

from core.config import settings


async def get_redis_client():
    redis = await aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', encoding='utf-8', db=2,
                                    decode_response=True)
    return redis
