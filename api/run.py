import asyncio
import functools
from contextlib import asynccontextmanager
from io import StringIO
from typing import Annotated, Optional, List, Any, Tuple
import uuid
import time
import sys
from fastapi.responses import JSONResponse
from starlette.routing import Match
import fnmatch

import yaml
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, Response
from libsql_client import Transaction, create_client

from api.bills._m.insert_bill import insert_bill
from api.bills._q.fetch_bills import fetch_bills
from api.bills.model import Bill
from api.bills.t import anotherFunc
from api.env import get_env

from api.logger import create_logger, RequestLogger, create_request_logger

load_dotenv(override=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = create_logger()

    print(
        "DB connecting.",
        get_env("DB_URL"),
        "Using Auth token db" if get_env("DB_AUTH") else "",
    )
    async with create_client(
        url=get_env("DB_URL"), auth_token=get_env("DB_AUTH")
    ) as db:
        print("To DB Connected.")
        app.state.db = db
        yield
        print("Closing DB Connection.")
        await db.close()


async def t(req: Request):
    try:
        t: Transaction = req.app.state.db.transaction()
        yield t
        await t.commit()
    except Exception as e:
        await t.rollback()
        raise e

def l(req: Request):
    yield create_request_logger(req)

DTransaction = Annotated[Transaction, Depends(t)]
DLogger = Annotated[RequestLogger, Depends(l)]

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(t: DTransaction, logger: DLogger):
    l = logger.getChild(__name__, __file__)
    try:

        l.info('router fetch_bills')
        return await fetch_bills(t, l)
    except Exception as e:
        l.exception('router fetch_bills fail', exc_info=e)
        return JSONResponse(
        status_code=500,
        content={
            "message": (
                f"An unhandled exception occurred: {e!r}."
            )
          },
        )


@app.post("/add_bills")
async def add_new_bill(t: DTransaction, bills: list[Bill]):
    return await insert_bill(t, *bills)


@app.get("/ping")
async def ping(l: DLogger):
    return "pingg"


@app.get("/openapi.yaml", include_in_schema=False)
@functools.lru_cache
def read_openapi_yaml() -> Response:
    openapi_json = app.openapi()
    yaml_s = StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type="text/yaml")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": (
                f"An unhandled exception occurred: {exc!r}."
            )
        },
    )
