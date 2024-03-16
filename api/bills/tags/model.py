import datetime
from typing import Optional
from pydantic import BaseModel


class Tag(BaseModel):

    id: Optional[int]
    name: str
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    deleted_at: Optional[datetime.datetime]
