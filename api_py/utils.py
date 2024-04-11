import json
from typing import Union

from pydantic import BaseModel
from pydantic.json import pydantic_encoder


def print_beautiful(*values: object, model: Union[BaseModel, list[BaseModel]]) -> None:
    return print(*values, json.dumps(model, default=pydantic_encoder, indent=2))
