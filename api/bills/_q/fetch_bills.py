import os
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from libsql_client import Transaction
from pydantic import BaseModel

from api.bills.model import Bill
from api.bills.tags.model import Tag
from api.models import TableModel
from packages.sql_eng import JinjaSql

sql_path = os.path.join(os.path.dirname(__file__))
file_loader = FileSystemLoader(sql_path)
env = Environment(loader=file_loader)
sql_eng = JinjaSql(env=env, param_style="qmark")


def render_cls_fields(cls: TableModel):
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


async def fetch_bills(con: Transaction, params: FetchBillsParams = None):
    dic = params.dict() if params else {}
    sql, params = sql_eng.prepare_query(
        "fetch_bills.sql", {**(dic), "render_tag": render_cls_fields(Tag)}
    )
    result = await con.execute(sql, params)
    return [Bill(**(row.asdict())) for row in result.rows]
