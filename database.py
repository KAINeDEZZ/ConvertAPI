from aioredis import create_redis_pool, Redis


database: Redis
pages_count = 0


async def init_database(ip: str, port: int):
    global database, pages_count

    database = await create_redis_pool(f'redis://{ip}:{port}', timeout=1)

    if type(database) == Exception:
        print('err')
        pass  # TODO

    while await database.keys('*'):
        pages_count += 1
        await database.select(database.db + 1)


async def close_database(redis_link):
    redis_link.close()
    await redis_link.wait_closed()


async def database_add_table(data: dict):
    try:
        global pages_count
        if pages_count != 0:
            await database.select(database.db + 1)
        pages_count += 1

        for key in data:
            await database.set(key, data[key])

    except Exception as ex:
        return ex

    return True


async def database_delete_table():
    try:
        await database.flushall()
    except Exception as ex:
        return ex

    if database.db != 0:
        global pages_count
        pages_count -= 1
        await database.select(database.db - 1)

    return True
