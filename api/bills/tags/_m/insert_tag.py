from sqlite3 import Connection

from api._m.insert_data import insert_data
from api.bills.tags.model import Tag


def map_tag(tag: Tag):
    dict = tag.dict()
    return dict


def insert_tag(con: Connection, *args: Tag):
    return insert_data(con, Tag, map_tag, *args)
