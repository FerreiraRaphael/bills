import json

from pydantic import BaseModel
from pydantic.json import pydantic_encoder


def print_beautiful(*values: object, model: BaseModel | list[BaseModel]) -> None:
    return print(*values, json.dumps(model, default=pydantic_encoder, indent=2))
