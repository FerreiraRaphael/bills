import os
from sqlite3 import Connection

from jinja2 import Environment, FileSystemLoader

from api.bills._m.insert_bill import insert_data
from api.bills.tags.model import Tag
from packages.sql_eng import JinjaSql

sql_path = os.path.join(os.path.dirname(__file__))
file_loader = FileSystemLoader(sql_path)
env = Environment(loader=file_loader)
sql_eng = JinjaSql(env=env, param_style="qmark")


def map_tag(tag: Tag):
    dict = tag.dict()
    return dict


def insert_tag(con: Connection, *args: Tag):
    return insert_data(con, "tags", map_tag, *args)
