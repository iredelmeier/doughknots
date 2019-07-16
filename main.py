import asyncio
import uvloop
from signal import signal, SIGINT

from sanic import Sanic

import bakery
import bakery.blueprint
from httpx import Client
import shopfront
import shopfront.blueprint


def main() -> None:
    http_session = Client()
    bakery_client = bakery.HttpClient("http://localhost:8000", client=http_session)

    bakery_service = bakery.Service()
    shopfront_service = shopfront.service.Service(bakery=bakery_client)

    bakery_blueprint = bakery.blueprint.factory(bakery=bakery_service)
    shopfront_blueprint = shopfront.blueprint.factory(shopfront=shopfront_service)

    app = Sanic()

    app.blueprint(bakery_blueprint)
    app.blueprint(shopfront_blueprint)

    asyncio.set_event_loop(uvloop.new_event_loop())

    server = app.create_server(
        host="127.0.0.1", port=8000, return_asyncio_server=True, debug=True
    )

    _ = asyncio.ensure_future(server)
    loop = asyncio.get_event_loop()
    signal(SIGINT, lambda s, f: loop.stop())

    try:
        loop.run_forever()
    except Exception:
        loop.stop()


if __name__ == "__main__":
    main()
