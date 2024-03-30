from sqlite3 import Connection

from pydash import omit

from api._m.insert_data import insert_data
from api.bills.model import Bill


def map_bill(bill: Bill):
    dict = bill.dict()
    datetime_str_format = "%Y-%m-%dT%H:%M:%SZ"
    dict["date"] = dict["date"].strftime(datetime_str_format)
    return omit(dict, *Bill.__join_fields__)


def insert_bill(con: Connection, *args: Bill):
    return insert_data(con, Bill, map_bill, *args)
