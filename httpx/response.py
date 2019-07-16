from typing import Any, Mapping

import sanic.response


def respond(body: Any, status: int = 200, headers: Mapping[str, str] = None) -> Any:
    return sanic.response.json(body, status=status, headers=headers)
