from fastapi import FastAPI, Request
import sqlite3
import os

print(os.path.abspath("../db/dev.sqlite"))

con = sqlite3.connect(os.path.abspath("db/dev.sqlite"))
con.row_factory = sqlite3.Row

app = FastAPI()

@app.middleware("http")
def add_stuff(request: Request, call_next):
    request.stuff = "go"
    print("in mid", request)
    return call_next(request)

@app.get("/")
async def root(request: Request):
    sql = """
      SELECT
        b.id,
        b.name,
        b.value,
        b.date,
        b.main_tag_id,
        t.id as id_name,
        t.name as tag_name,
        mt.name as main_tag_name
      FROM
        bills AS b
        left JOIN bills_tags AS bt ON bt.bill_id == b.id
        left JOIN tags AS t ON bt.tag_id == t.id
        left JOIN tags AS mt ON b.main_tag_id == mt.id
      WHERE b.deleted_at is null;
      """
    res = [dict(zip(('id', 'name', 'value'), row)) for row in con.execute(sql).fetchall()]

    print(res)
    return res
