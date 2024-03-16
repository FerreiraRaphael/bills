import datetime
from typing import Optional
from pydantic import BaseModel
from api.bills.tags.model import Tag

class Bill(BaseModel):

    id: Optional[int]
    name: str
    value: int
    date: Optional[datetime.datetime]
    main_tag_id: Optional[int]
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    deleted_at: Optional[datetime.datetime]
    tags: Optional[list[Tag]]
    main_tag: Optional[Tag]
