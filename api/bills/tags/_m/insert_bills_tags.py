from libsql_client import Transaction

from api._m.insert_data import insert_data
from api.bills.tags.model import BillTag


def map_bills_tags(insert_bills_tags: BillTag):
    return insert_bills_tags.dict()


def insert_bills_tags(t: Transaction, *bills_tags_ids: BillTag):
    return insert_data(t, BillTag, map_bills_tags, *bills_tags_ids)
