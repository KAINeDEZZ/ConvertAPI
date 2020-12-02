from aiohttp.web import Response, Request
from course_parser import parse_table
from database import database_add_table, database_delete_table, database_get_keys
import exceptions
import json


async def convert(request: Request) -> Response:
    params = dict(request.query)

    params_status = await check_args(params, ('from', 'to', 'amount'))
    if params_status:
        return Response(**params_status.convert_to_json())

    data = await database_get_keys((params['from'], params['to']))
    for key in data:
        if key == 'RUR':
            data[key] = 1

        if data[key] is None:
            return Response(**exceptions.InvalidArgumentException(
                '[from, to]', 'one of the parameters is set incorrectly or data is missing').convert_to_json())

        data[key] = float(data[key])

    if not params['amount'].isdigit():
        return Response(**exceptions.InvalidArgumentException('amount', 'the value must be numeric').convert_to_json())

    return Response(body=json.dumps(
        {'response': data[params['from']] * int(params['amount']) / data[params['to']]}))


async def database(request: Request) -> Response:
    params = dict(request.query)

    params_status = await check_args(params, ('merge',))
    if params_status:
        return Response(**params_status.convert_to_json())

    if params['merge'] == '1':
        return await create_new_table()

    elif params['merge'] == '0':
        return await delete_table()

    else:
        return Response(**exceptions.InvalidArgumentException('merge', 'it can be only: [0, 1]').convert_to_json())


async def check_args(actual_args: dict, need_args: tuple) -> None or exceptions.ArgumentsNotFoundException:
    not_found_args = need_args - actual_args.keys()
    if not_found_args:
        return exceptions.ArgumentsNotFoundException(list(not_found_args))


async def create_new_table() -> Response:
    data = await parse_table()
    if issubclass(type(data), Exception):
        return Response(**data.convert_to_json())

    status = await database_add_table(data)
    if status:
        return Response(**status.convert_to_json())

    return Response(status=202)


async def delete_table() -> Response:
    status = await database_delete_table()
    if status:
        return Response(**status.convert_to_json())
    else:
        return Response(status=202)
