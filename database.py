from aioredis import create_redis_pool, Redis


async def init_database(ip: str, port: int) -> Redis:
    redis = await create_redis_pool(f'redis://{ip}:{port}', timeout=1)
    return redis


async def close_database(redis_link):
    redis_link.close()
    await redis_link.wait_closed()
