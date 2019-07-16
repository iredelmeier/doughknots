from sanic.blueprints import Blueprint
from sanic.response import json


def factory(name=__name__,):
    blueprint = Blueprint(name)

    @blueprint.post("/order")
    async def order(request):
        return json({"hello": "world"})

    return blueprint
