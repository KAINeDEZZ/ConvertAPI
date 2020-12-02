from aiohttp.web import Response, Request
from course_parser import get_table


database_class = None


def set_database(database_link):
    global database_class

    if type(database_link) == Exception:
        #  TODO
        pass
    else:
        database_class = database_link


async def convert(request: Request):
    return Response()  # TODO


async def database(request: Request):
    return Response()  # TODO
