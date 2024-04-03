from libsql_client import Transaction
from pydantic import BaseModel

from api.logger import RequestLogger


class UpdateBillsInput(BaseModel):
    bill_id: int
    main_tag_id: int


async def update_main_tag(t: Transaction, logger: RequestLogger, main_tag_id: int, bill_id: int):
    log = logger.getChild(__name__, __file__)
    try:
        log.debug(f"update_main_tag {{ 'main_tag_id': main_tag_id, 'bill_id': bill_id  }}")
        # dic = params.dict() if params else {}
        result = await t.execute(
            "UPDATE bills SET main_tag_id = ? WHERE id = ?", [main_tag_id, bill_id]
        )
        log.debug(f"update_main_tag result {result.rows}")
        return None
    except Exception as e:
        log.exception("failed in update_main_tag", exc_info=e)
        raise e
