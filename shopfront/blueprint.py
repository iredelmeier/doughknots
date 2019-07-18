from typing import Any

import opentracing

from httpx import Blueprint
from httpx.response import abort, respond

from bakery import Kind

from .shopfront import NoopShopFront, ShopFront


def factory(name: str = __name__, shopfront: ShopFront = None) -> Blueprint:
    client = shopfront if shopfront else NoopShopFront()
    blueprint = Blueprint(name)

    @blueprint.post("/")
    async def order(req: Any) -> Any:
        body = req.json

        try:
            assert isinstance(body, dict)
        except AssertionError:
            abort(400)

        for k, v in body.items():
            try:
                Kind[k]
            except KeyError:
                abort(404)

            try:
                assert isinstance(v, int)
                assert v >= 0
            except AssertionError:
                abort(400)

        await client.order(body)

        res = respond(None, status=204)
        return res

    return blueprint
