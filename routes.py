from aiohttp.web import UrlDispatcher, get, post
from methods import convert, database


def create_routes(router: UrlDispatcher):
    for default_method in METHODS:
        adding_function = eval(f'router.add_{default_method.lower()}')
        for api_method in METHODS[default_method]:
            adding_function(path=api_method.path, handler=api_method.handler)


class APIMethod:
    def __init__(self, path: str, handler):
        self.path = path
        self.handler = handler

    def get_router_format(self) -> dict:
        return {'path': self.path, 'handler': self.handler}


METHODS = {
    'GET': [
        APIMethod('/convert', convert)
    ],
    'POST': [
        APIMethod('/database', database)
    ]}
