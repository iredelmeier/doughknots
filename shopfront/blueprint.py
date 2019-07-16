from typing import Any

from sanic.exceptions import InvalidUsage, NotFound
from sanic.response import json

from httpx import Blueprint

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
            raise InvalidUsage("Invalid usage")

        for k, v in body.items():
            try:
                Kind[k]
            except KeyError:
                raise NotFound("Not found")

            try:
                assert isinstance(v, int)
                assert v >= 0
            except AssertionError:
                raise InvalidUsage("Invalid usage")

        await client.order(body)

        return json(None)

    return blueprint
