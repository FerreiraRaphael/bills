from libsql_client import Transaction
from pydash import omit

from api._m.insert_data import insert_data
from api.bills.model import Bill
from api.logger import RequestLogger


def map_bill(bill: Bill):
    dict = bill.dict()
    datetime_str_format = "%Y-%m-%dT%H:%M:%SZ"
    dict["date"] = dict["date"].strftime(datetime_str_format)
    return omit(dict, *Bill.__join_fields__)


async def insert_bill(t: Transaction, logger: RequestLogger, *args: Bill):
    log = logger.getChild(__name__, __file__)
    try:
        log.debug(f"insert_bill")
        result = await insert_data(t, Bill, map_bill, *args)
        log.debug(f"insert_bill result")
        return result
    except Exception as e:
        log.exception("failed in insert_bill", exc_info=e)
        raise e
