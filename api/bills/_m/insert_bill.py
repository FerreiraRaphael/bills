from sqlite3 import Connection

from pydantic import BaseModel
from pydash import omit

from api.bills.model import Bill


def map_bill(bill: Bill):
    dict = bill.dict()
    datetime_str_format = "%Y-%m-%dT%H:%M:%SZ"
    dict["date"] = dict["date"].strftime(datetime_str_format)
    return omit(dict, *Bill.__join_fields__)


def treat_data(mapper, *args: BaseModel):
    params_string = []
    model_objects_values = []
    for object in args:
        object = mapper(object)
        model_columns = object.keys()
        params_string.extend([f'({", ".join(["?" for _ in model_columns])})'])
        model_objects_values.extend(object.values())
    return (model_columns, params_string, model_objects_values)


def insert_data(con: Connection, table: str, mapper, *args: BaseModel):
    sql_columns, params_string, model_objects_values = treat_data(mapper, *args)
    return con.execute(
        f"""
                INSERT INTO {table} ({", ".join(sql_columns)})
                VALUES {", ".join(params_string)}
                """,
        model_objects_values,
    )


def insert_bill(con: Connection, *args: Bill):
    return insert_data(con, "bills", map_bill, *args)
