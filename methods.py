from aiohttp.web import Response, Request


async def convert(request: Request):
    return Response(text='0')  # TODO


async def database(request: Request):
    return Response(text='0')  # TODO


class APIMethod:
    def __init__(self, path: str, handler):
        self.path = path
        self.handler = handler

    def get_router_format(self):
        return {'path': self.path, 'handler': self.handler}


METHODS = {
    'GET': [
        APIMethod('/convert', convert)
    ],
    'POST': [
        APIMethod('/database', database)
    ]}
