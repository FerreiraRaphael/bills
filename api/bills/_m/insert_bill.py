import os
from sqlite3 import Connection
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from api.bills.model import Bill
from api.bills.tags.model import Tag
from packages.sql_eng import JinjaSql
from datetime import datetime

sql_path = os.path.join(os.path.dirname(__file__))
file_loader = FileSystemLoader(sql_path)
env = Environment(loader=file_loader)
sql_eng = JinjaSql(env=env, param_style="qmark")


def insert_bill(con: Connection, *args: Bill):
    datetime_str_format = '%Y-%m-%dT%H:%M:%SZ'
    for bill in args:
        name, value, date = bill.name, bill.value, bill.date
        con.execute(f"""INSERT INTO bills (name, value, date) 
                    VALUES ('{name}', '{value}', '{date.strftime(datetime_str_format)}')
                    """)
