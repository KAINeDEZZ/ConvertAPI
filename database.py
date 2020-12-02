from aioredis import create_redis_pool, Redis
import exceptions


database: Redis


async def init_database(ip: str, port: int):
    global database

    database = await create_redis_pool(f'redis://{ip}:{port}', timeout=1)

    if type(database) == Exception:
        print(database)
        exit()

    while await database.keys('*'):
        await database.select(database.db + 1)

    if database.db != 0:
        await database.select(database.db - 1)


async def database_add_table(data: dict) -> None or exceptions.AtypicalException:
    try:
        if await database.keys('*'):
            await database.select(database.db + 1)

        for key in data:
            await database.set(key, data[key])

    except Exception as exception:
        return exceptions.AtypicalException(exception, 'database')


async def database_delete_table() -> None or exceptions.AtypicalException:
    try:
        await database.flushdb()
    except Exception as exception:
        return exceptions.AtypicalException(exception, 'database')

    if database.db != 0:
        await database.select(database.db - 1)


async def database_get_keys(keys: tuple) -> dict or exceptions.AtypicalException:
    try:
        data = {}
        for key in keys:
            data[key] = await database.get(key)
        return data

    except Exception as exception:
        return exceptions.AtypicalException(exception, 'database')
