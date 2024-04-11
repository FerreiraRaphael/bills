from typing import Tuple

from pydantic import BaseModel


class TableModel(BaseModel):
    __table_name__: str
    __join_fields__: Tuple[str]
