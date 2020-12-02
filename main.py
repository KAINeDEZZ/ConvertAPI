from aiohttp.web import Application, run_app
from routes import create_routes
from database import init_database
from methods import set_database
import asyncio


def init_api():
    application = Application()
    create_routes(application.router)

    loop = asyncio.get_event_loop()
    database_init_task = loop.create_task(init_database('localhost', 63279))
    database_init_task.add_done_callback(lambda coro_result: set_database(coro_result.result()))

    return application


if __name__ == '__main__':
    app = init_api()
    run_app(app)
