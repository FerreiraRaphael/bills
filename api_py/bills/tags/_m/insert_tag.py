from libsql_client import Transaction

from api_py._m.insert_data import insert_data
from api_py.bills.tags.model import Tag
from api_py.logger import RequestLogger


def map_tag(tag: Tag):
    dict = tag.dict()
    return dict


async def insert_tag(t: Transaction, logger: RequestLogger, *args: Tag):
    log = logger.getChild(__name__, __file__)
    try:
        log.debug(f"insert_tag {list(map(lambda x: x.json(), args))}")
        result = await insert_data(t, Tag, map_tag, *args)
        log.debug(f"insert_tag result {list(map(lambda x: x.json(), result))}")
        return result
    except Exception as e:
        log.exception("failed in insert_tag", exc_info=e)
        raise e
