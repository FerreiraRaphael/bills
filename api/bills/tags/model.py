import datetime
from typing import Optional, Type, TypeVar

from pydantic import validator

from api.models import TableModel

T = TypeVar("T", bound="Tag")


class Tag(TableModel):
    __table_name__ = 'tags'
    id: Optional[int]
    name: str
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    deleted_at: Optional[datetime.datetime]

    @validator("created_at", "updated_at", "deleted_at", pre=True)
    @classmethod
    def transform(cls, raw: str | datetime.datetime) -> datetime.datetime:
        if isinstance(raw, str):
            return datetime.datetime.fromisoformat(raw)
        return raw

    @classmethod
    def from_dict(cls: Type[T], dic: dict) -> T:
        return cls(**{k: v for k, v in dic.items()})


class BillTag(TableModel):
  __table_name__ = 'bills_tags'
  bill_id: int
  tag_id: int
