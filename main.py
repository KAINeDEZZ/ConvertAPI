from aiohttp.web import Application, run_app
from routes import create_routes
from database import init_database


def init_api() -> Application:
    application = Application()
    create_routes(application.router)

    application.on_startup.append(lambda tmp: init_database('localhost', 6379))
    return application


if __name__ == '__main__':
    app = init_api()
    run_app(app)
