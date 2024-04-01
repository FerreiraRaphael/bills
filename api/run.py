import functools
from io import StringIO
from contextlib import asynccontextmanager
import yaml
from typing import Annotated
from fastapi import FastAPI, Request, Response, Depends
from libsql_client import create_client, Transaction
from api.bills._m.insert_bill import insert_bill
from api.bills._q.fetch_bills import fetch_bills
from api.bills.model import Bill
from api.env import get_env
# from dotenv import load_dotenv

# load_dotenv(override=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('DB connecting.',
      get_env("DB_URL"),
      # "Using Auth token db" if get_env("DB_AUTH") else ""
    )
    async with create_client(
        url=get_env("DB_URL"),
        auth_token=get_env("DB_AUTH")
    ) as db:
      print('To DB Connected.')
      app.state.db = db
      yield
      print('Closing DB Connection.')
      await db.close()

async def t(req: Request):
    try:
        t: Transaction = req.app.state.db.transaction()
        yield t
        await t.commit()
    except Exception as e:
        await t.rollback()
        raise e

DTransaction = Annotated[Transaction, Depends(t)]

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root(t: DTransaction):
    return await fetch_bills(t)


@app.post("/add_bills")
async def add_new_bill(
        t: DTransaction,
        bills: list[Bill]
    ):
    return await insert_bill(t, *bills)


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
