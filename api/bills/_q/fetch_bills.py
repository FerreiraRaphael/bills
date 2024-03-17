import os
from sqlite3 import Connection
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from api.bills.model import Bill
from api.bills.tags.model import Tag
from packages.sql_eng import JinjaSql

sql_path = os.path.join(os.path.dirname(__file__))
file_loader = FileSystemLoader(sql_path)
env = Environment(loader=file_loader)
sql_eng = JinjaSql(env=env, param_style="qmark")


def render_cls_fields(cls):
    def wrapper(table_name: str = "tag", *table_cols: str):
        annotations = cls.__annotations__
        annotations_items = annotations.items()
        fields = None
        if len(table_cols) == 0:
            fields = [f"'{k}', {table_name}.{k}" for k, _ in annotations_items]
        else:
            fields = [f"'{k}', {table_name}.{k}" for k in table_cols if annotations[k]]
        return ", ".join(fields)

    return wrapper


class FetchBillsParams(BaseModel):
    join_tags: Optional[bool]
    join_main_tag: Optional[bool]


def fetch_bills(con: Connection, params: FetchBillsParams = None):
    dic = params.dict() if params else {}
    sql, params = sql_eng.prepare_query(
        "fetch_bills.sql", {**(dic), "render_tag": render_cls_fields(Tag)}
    )
    return [Bill.from_dict(row) for row in con.execute(sql, params).fetchall()]
