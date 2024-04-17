from libsql_client import Transaction

from api.bills.tags.model import Tag
from api.logger import RequestLogger


async def check_tag(t: Transaction, logger: RequestLogger, name: str):
    log = logger.getChild(__name__, __file__)
    try:
        log.debug(f"check_tag {name}")
        result = await t.execute("SELECT * FROM tags WHERE name = ?;", [name])
        log.debug(f"check_tag result {result.rows}")
        return [Tag(**(row.asdict())) for row in result.rows]
    except Exception as e:
        log.exception("failed in fetch bills", exc_info=e)
        raise e
