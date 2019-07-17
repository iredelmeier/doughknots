# mypy: allow-untyped-defs
from typing import Any, Mapping

import sanic.blueprints


class Blueprint:
    def __init__(self, name: str) -> None:
        self.__blueprint = sanic.blueprints.Blueprint(name)

    @property
    def name(self) -> Any:
        return self.__blueprint.name

    def register(self, app: Any, options: Mapping[Any, Any] = None) -> None:
        self.__blueprint.register(app, options)

    def get(self, uri: str) -> Any:
        return self.__blueprint.get(uri)

    def post(self, uri: str) -> Any:
        return self.__blueprint.post(uri)

    def put(self, uri: str) -> Any:
        return self.__blueprint.put(uri)

    def delete(self, uri: str) -> Any:
        return self.__blueprint.delete(uri)
