from libsql_client import Transaction

from api.logger import RequestLogger


async def check_tag(t: Transaction, logger: RequestLogger, name: str):
    log = logger.getChild(__name__, __file__)
    try:
        log.debug(f"check_tag {name}")
        res = await t.execute("SELECT * FROM tags WHERE name = ?;", [name])
        log.debug(f"check_tag result {res.rows}")
        return len(res.rows) != 0
    except Exception as e:
        log.exception("failed in fetch bills", exc_info=e)
        raise e
