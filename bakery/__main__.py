import asyncio
import uvloop
from signal import signal, SIGINT

from sanic import Sanic

from . import blueprint


def main() -> None:
    app = Sanic()

    app.blueprint(blueprint.factory())

    asyncio.set_event_loop(uvloop.new_event_loop())

    server = app.create_server(host="127.0.0.1", port=8000, return_asyncio_server=True)

    loop = asyncio.get_event_loop()
    _ = asyncio.create_task(server)
    signal(SIGINT, lambda s, f: loop.stop())

    try:
        loop.run_forever()
    except Exception:
        loop.stop()


if __name__ == "__main__":
    main()
