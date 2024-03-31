from libsql_client import Transaction

from api._m.insert_data import insert_data
from api.bills.tags.model import Tag


def map_tag(tag: Tag):
    dict = tag.dict()
    return dict


async def insert_tag(t: Transaction, *args: Tag):
    return await insert_data(t, Tag, map_tag, *args)
