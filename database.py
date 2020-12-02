from aioredis import create_redis_pool, Redis


database: Redis


async def init_database(ip: str, port: int):
    global database
    database = await create_redis_pool(f'redis://{ip}:{port}', timeout=1)

    if type(database) == Exception:
        pass  # TODO


async def close_database(redis_link):
    redis_link.close()
    await redis_link.wait_closed()


async def set_table(data: dict):
    try:
        print(data)
        for key in data:

            await database.set(key, data[key])

    except Exception as ex:
        return ex

    return True


async def get_table():
    try:
        for key in await database.keys('*'):
            print(await database.get(key))

    except Exception as ex:
        return ex

    return True

