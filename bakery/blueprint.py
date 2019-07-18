from typing import Any

import opentracing

from exceptions import ServiceUnavailableError
from httpx import Blueprint
from httpx.response import abort, respond

from .bakery import Bakery, NoopBakery
from .kind import Kind


def factory(name: str = __name__, bakery: Bakery = None) -> Blueprint:
    client = bakery if bakery else NoopBakery()
    blueprint = Blueprint(name)

    @blueprint.post("/<kind>")
    async def bake(req: Any, kind: str) -> Any:
        body = req.json

        try:
            k = Kind[kind]
        except KeyError:
            abort(404)

        try:
            amount = body

            assert isinstance(amount, int)
            assert amount >= 0
        except AssertionError:
            abort(400)

        await client.bake(k, amount)

        res = respond(None, status=204)
        return res

    @blueprint.delete("/<kind>")
    async def take(req: Any, kind: str) -> Any:
        req["span"].operation_name = "/bakery/<kind>"
        args = req.args

        try:
            k = Kind[kind]
        except KeyError:
            abort(404)

        try:
            amount = int(args["amount"][0])

            assert isinstance(amount, int)
            assert amount >= 0
        except (KeyError, ValueError, AssertionError):
            abort(400)

        try:
            await client.take(k, amount)
        except ServiceUnavailableError:
            abort(503)

        return respond(None, status=204)

    @blueprint.get("/")
    async def inventory(req: Any) -> Any:
        inventory = await client.inventory()
        return respond(inventory)

    return blueprint
