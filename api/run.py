import os
import sqlite3

from fastapi import FastAPI, Request

from api.bills._q.fetch_bills import fetch_bills


def create_con(db_path: str, trace_callback=None):
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    sqlite3.paramstyle = "qmark"
    con = sqlite3.connect(os.path.abspath(db_path))
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

@app.get("/ping")
async def ping():
    return "ping"
