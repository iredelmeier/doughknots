from typing import Any

from sanic.exceptions import InvalidUsage, NotFound, ServiceUnavailable
from sanic.response import json

from httpx import Blueprint

from .bakery import Bakery
from .exceptions import InsufficientDoughknots
from .kind import Kind
from .service import Service


def factory(name: str = __name__, bakery: Bakery = None) -> Blueprint:
    client = bakery if bakery else Service()
    blueprint = Blueprint(name)

    @blueprint.post("/<kind>")
    async def bake(req: Any, kind: str) -> Any:
        body = req.json

        try:
            k = Kind[kind]
        except KeyError:
            raise NotFound("Not found")

        try:
            amount = body

            assert isinstance(amount, int)
            assert amount >= 0
        except Exception:
            raise InvalidUsage("Invalid usage")

        await client.bake(k, amount)

        return json(None)

    @blueprint.delete("/<kind>")
    async def take(req: Any, kind: str) -> Any:
        body = req.args

        try:
            k = Kind[kind]
        except KeyError:
            raise NotFound("Not found")

        try:
            amount = int(body.get("amount", [1][0]))

            assert isinstance(amount, int)
            assert amount >= 0
        except Exception:
            raise InvalidUsage("Invalid usage")

        try:
            await client.take(k, amount)
        except InsufficientDoughknots:
            raise ServiceUnavailable("Service unavailable")

        return json(None)

    @blueprint.get("/")
    async def get(req: Any) -> Any:
        inventory = await client.inventory()
        return json(inventory)

    return blueprint
