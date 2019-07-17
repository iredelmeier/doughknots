import asyncio
import uvloop
from signal import signal, SIGINT

import opentracing
from sanic import Sanic

import bakery
import bakery.blueprint
from httpx import Client
import shopfront
import shopfront.blueprint
import staffroom
from trace import Tracer
from trace.span import set_exporter
import unknotter
import unknotter.blueprint


def main() -> None:
    asyncio.set_event_loop(uvloop.new_event_loop())

    http_session = Client()
    bakery_client = bakery.HttpClient(
        "http://localhost:8000/bakery", client=http_session
    )

    bakery_service = bakery.Service()
    staff_room = staffroom.service.Service()
    shopfront_service = shopfront.service.Service(
        bakery=bakery_client, staff_room=staff_room
    )
    unknotter_service = unknotter.service.Service()

    exporter = unknotter.exporter.Exporter(unknotter=unknotter_service)

    set_exporter(exporter)

    tracer = Tracer()
    opentracing.set_global_tracer(tracer)

    bakery_blueprint = bakery.blueprint.factory(bakery=bakery_service)
    shopfront_blueprint = shopfront.blueprint.factory(shopfront=shopfront_service)
    shopfront_blueprint = shopfront.blueprint.factory(shopfront=shopfront_service)
    unknotter_blueprint = unknotter.blueprint.factory(unknotter=unknotter_service)

    app = Sanic()

    app.blueprint(bakery_blueprint, url_prefix="/bakery")
    app.blueprint(shopfront_blueprint, url_prefix="/shopfront")
    app.blueprint(unknotter_blueprint, url_prefix="/unknotter")

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
