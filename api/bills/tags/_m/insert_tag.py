from sqlite3 import Connection

from api.bills._m.insert_data import insert_data
from api.bills.tags.model import Tag


def map_tag(tag: Tag):
    dict = tag.dict()
    return dict


def insert_tag(con: Connection, *args: Tag):
    return insert_data(con, "tags", map_tag, *args)
