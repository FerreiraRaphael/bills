from sqlite3 import Connection

from pydantic import BaseModel

from api.bills._m.insert_data import insert_data


class InsertBillsTagsInput(BaseModel):
    bill_id: int
    tag_id: int


def map_bills_tags(insert_bills_tags: InsertBillsTagsInput):
    return insert_bills_tags.dict()


def insert_bills_tags(con: Connection, *bills_tags_ids: InsertBillsTagsInput):
    return insert_data(con, "bills_tags", map_bills_tags, *bills_tags_ids)
