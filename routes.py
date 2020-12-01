from aiohttp.web import UrlDispatcher, get, post
from methods import METHODS


def create_routes(router: UrlDispatcher):
    for default_method in METHODS:
        adding_function = eval(f'router.add_{default_method.lower()}')
        for api_method in METHODS[default_method]:
            adding_function(path=api_method.path, handler=api_method.handler)
