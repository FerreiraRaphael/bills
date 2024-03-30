from sqlite3 import Connection

from api._m.insert_data import insert_data
from api.bills.tags.model import BillTag


def map_bills_tags(insert_bills_tags: BillTag):
    return insert_bills_tags.dict()


def insert_bills_tags(con: Connection, *bills_tags_ids: BillTag):
    return insert_data(con, BillTag, map_bills_tags, *bills_tags_ids)
