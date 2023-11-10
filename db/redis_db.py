import redis.asyncio as aioredis

from config.config import settings

redis_auth = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', encoding='utf-8',
                               db=settings.REDIS_AUTH_DATABASE, decode_responses=True)

redis_token = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', encoding='utf-8',
                                db=settings.REDIS_TOKEN_DATABASE, decode_responses=True)


def get_redis_auth_client():

    """
    The get_redis_auth_client function returns a redis client object that is connected to the Redis server.
        The function uses the REDIS_AUTH_HOST and REDIS_AUTH_PORT environment variables to connect to the Redis server.

    :return: The redis_auth variable
    :doc-author: Trelent
    """
    return redis_auth


def get_redis_token_client():

    """
    The get_redis_token_client function returns a redis client object that is connected to the Redis server.
        This function is used by other functions in this module to connect to the Redis server.

    :return: The redis_token variable
    :doc-author: Trelent
    """
    return redis_token
