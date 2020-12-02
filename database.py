from aioredis import create_redis_pool, Redis


database: Redis


async def init_database(ip: str, port: int):
    global database

    database = await create_redis_pool(f'redis://{ip}:{port}', timeout=1)

    if type(database) == Exception:
        print('err')
        pass  # TODO

    while await database.keys('*'):
        await database.select(database.db + 1)

    if database.db != 0:
        await database.select(database.db - 1)


async def close_database(redis_link):
    redis_link.close()
    await redis_link.wait_closed()


async def database_add_table(data: dict):
    try:
        if await database.keys('*'):
            await database.select(database.db + 1)

        for key in data:
            await database.set(key, data[key])

    except Exception as ex:
        return ex

    return True


async def database_delete_table():
    try:
        await database.flushdb()
    except Exception as ex:
        return ex

    if database.db != 0:
        await database.select(database.db - 1)

    return True


async def database_get_keys(keys):
    try:
        data = {}
        for key in keys:
            data[key] = await database.get(key)
        return data

    except Exception as ex:
        return ex
