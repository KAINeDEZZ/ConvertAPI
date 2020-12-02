from aiohttp.web import Response, Request
from course_parser import parse_table
from database import set_table, get_table
import exceptions


async def convert(request: Request):
    await get_table()
    return Response()  # TODO


async def database(request: Request):
    merge = request.query.get('merge')
    if merge == '1':
        return await update_table()

    elif merge == 0:
        pass

    else:
        return Response()  # TODO


async def update_table() -> Response:
    data = await parse_table()
    if issubclass(type(data), Exception):
        return Response(text=data.__str__())

    print(data)
    status = await set_table(data)
    if status is not True:
        return Response(text=status.__str__())

    return Response(text='Таблица курса обновленна')
