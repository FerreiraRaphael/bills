import functools
import sqlite3
from io import StringIO

import yaml
from fastapi import FastAPI, Request, Response

from api.bills._m.insert_bill import insert_bill
from api.bills._q.fetch_bills import fetch_bills
from api.bills.model import Bill


def create_con(db_path: str, trace_callback=None):
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    sqlite3.paramstyle = "qmark"
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    con.set_trace_callback(trace_callback)
    return con


con = create_con("db/dev.sqlite")

app = FastAPI()


@app.middleware("http")
def add_stuff(request: Request, call_next):
    request.stuff = "go"
    return call_next(request)


@app.get("/")
async def root(request: Request):
    return fetch_bills(con)


@app.post("/add_bills")
async def add_new_bill(request: Request, bills: list[Bill]):
    return insert_bill(con, *bills)

@app.get("/ping")
async def ping():
    return "pingg"


@app.get("/openapi.yaml", include_in_schema=False)
@functools.lru_cache
def read_openapi_yaml() -> Response:
    openapi_json = app.openapi()
    yaml_s = StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type="text/yaml")
