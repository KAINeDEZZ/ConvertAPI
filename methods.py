from aiohttp.web import Response, Request
from course_parser import parse_table
from database import database_add_table, database_delete_table, database_get_keys


async def convert(request: Request) -> Response:
    params = dict(request.query)
    if list(params.keys()) != ['from', 'to', 'amount']:
        return Response(text='Неверные параметры')

    data = await database_get_keys((params['from'], params['to']))
    for key in data:
        if key == 'RUR':
            data[key] = 1

        if data[key] is None:
            return Response(text='Один из параметров задан неправильно или отсутствуют данные')

        data[key] = float(data[key])

    return Response(text=str(data[params['from']] * int(params['amount']) / data[params['to']]))


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
