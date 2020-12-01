from aiohttp.web import Application, run_app
from routes import create_routes


def init_api():
    application = Application()
    create_routes(application.router)

    return application


if __name__ == '__main__':
    app = init_api()
    run_app(app)
