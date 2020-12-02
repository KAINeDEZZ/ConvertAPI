from aiohttp.web import Response, Request
from course_parser import parse_table
from database import database_add_table, database_delete_table


async def convert(request: Request) -> Response:
    return Response()  # TODO


async def database(request: Request) -> Response:
    merge = request.query.get('merge')
    if merge == '1':
        return await create_new_table()

    elif merge == '0':
        return await delete_table()

    else:
        return Response()  # TODO


async def create_new_table() -> Response:
    data = await parse_table()
    if issubclass(type(data), Exception):
        return Response(text=data.__str__())

    status = await database_add_table(data)
    if issubclass(type(status), Exception):
        return Response(text=status.__str__())

    return Response(text='Таблица курса обновленна')


async def delete_table():
    status = await database_delete_table()
    if issubclass(type(status), Exception):
        return Response(text=status.__str__())
    else:
        return Response(text='Лист удалён')
