from aiohttp.web import Application, run_app
from routes import create_routes
from database import init_database
import asyncio


def init_api():
    application = Application()
    create_routes(application.router)

    application.on_startup.append(lambda tmp: init_database('localhost', 6379))
    # loop = asyncio.get_event_loop()
    # loop.create_task(init_database('))
    # database_init_task.add_done_callback(lambda coro_result: set_database(coro_result.result()))

    return application


if __name__ == '__main__':
    app = init_api()
    run_app(app)
