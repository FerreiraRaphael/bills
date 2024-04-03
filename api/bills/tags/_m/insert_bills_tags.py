from libsql_client import Transaction

from api._m.insert_data import insert_data
from api.bills.tags.model import BillTag
from api.logger import RequestLogger


def map_bills_tags(insert_bills_tags: BillTag):
    return insert_bills_tags.dict()


async def insert_bills_tags(
    t: Transaction, logger: RequestLogger, *bills_tags_ids: BillTag
):
    log = logger.getChild(__name__, __file__)
    try:
        log.debug(f"insert_bills_tags {list(map(lambda x: x.json(), bills_tags_ids))}")
        result = await insert_data(t, BillTag, map_bills_tags, *bills_tags_ids)
        log.debug(f"insert_bills_tags result {list(map(lambda x: x.json(), result))}")
        return result
    except Exception as e:
        log.exception("failed in insert_bills_tags", exc_info=e)
        raise e
