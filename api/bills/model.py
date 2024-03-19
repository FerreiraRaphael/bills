import datetime
import json
from typing import Optional, Type, TypeVar

from pydantic import BaseModel, validator

from api.bills.tags.model import Tag

T = TypeVar("T", bound="Bill")


class Bill(BaseModel):
    id: Optional[int]
    name: str
    value: int
    date: Optional[datetime.datetime]
    main_tag_id: Optional[int]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]
    tags: Optional[list[Tag]]
    main_tag: Optional[Tag]

    @validator("created_at", "updated_at", "deleted_at", pre=True)
    @classmethod
    def transform_datetime(cls, raw: str | datetime.datetime) -> datetime.datetime:
        if isinstance(raw, str):
            return datetime.datetime.fromisoformat(raw)
        return raw

    @validator("tags", "main_tag", pre=True)
    @classmethod
    def transform_tags(cls, raw: str | Tag | list[Tag] | None) -> Tag | list[Tag]:
        if not raw or isinstance(raw, (Tag, list)):
            return raw
        value = json.loads(raw)
        if isinstance(value, list):
            return [Tag.from_dict(row) for row in value]
        return Tag.from_dict(value)

    @classmethod
    def from_dict(cls: Type[T], dic: dict) -> T:
        return cls(**{k: v for k, v in dic.items()})
