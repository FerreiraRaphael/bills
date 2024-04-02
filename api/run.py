import functools
from contextlib import asynccontextmanager
from io import StringIO
from typing import Annotated, List

import aiofiles
import yaml
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from libsql_client import Transaction, create_client
from pydantic import BaseModel
from pydash import uniq

from api.bills._m.insert_bill import insert_bill
from api.bills._q.fetch_bills import fetch_bills
from api.bills.model import Bill
from api.env import get_env
from api.logger import RequestLogger, create_logger, create_request_logger

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
        if not t.closed:
            await t.commit()
    except Exception as e:
        await t.rollback()
        raise e


async def log(req: Request):
    yield await create_request_logger(req.app.state.logger, req.url.path)


DTransaction = Annotated[Transaction, Depends(t)]
DLogger = Annotated[RequestLogger, Depends(log)]

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(t: DTransaction, logger: DLogger):
    log = logger.getChild(__name__, __file__)
    try:
        log.info("router fetch_bills")
        return await fetch_bills(t, log)
    except Exception as e:
        log.exception("router fetch_bills fail", exc_info=e)
        await t.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": (f"An unhandled exception occurred: {e!r}.")},
        )


@app.post("/add_bills")
async def add_new_bill(t: DTransaction, logger: DLogger, bills: list[Bill]):
    log = logger.getChild(__name__, __file__)
    try:
        log.info(f"router add_new_bill")
        return await insert_bill(t, log, *bills)
    except Exception as e:
        log.exception("router add_new_bill fail", exc_info=e)
        await t.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": (f"An unhandled exception occurred: {e!r}.")},
        )


@app.get("/ping")
async def ping():
    return "pingg"


class LoggerInput(BaseModel):
    logs: List[str]
    append = True


@app.post("/logger", response_class=PlainTextResponse)
async def post_logger(input: LoggerInput):
    if input.append:
        lines = input.logs
        async with aiofiles.open("logs.txt", mode="r") as file:
            text = await file.read()
            lines.extend(text.split("\n"))
        unique_lines = uniq(lines)
        async with aiofiles.open("logs.txt", mode="w") as file:
            await file.write("\n".join(unique_lines))
    else:
        async with aiofiles.open("logs.txt", mode="w") as file:
            await file.writelines(input.logs)
    async with aiofiles.open("logs.txt", mode="r") as file:
        return await file.read()


@app.get("/logger", response_class=PlainTextResponse)
async def get_logger():
    async with aiofiles.open("logs.txt", mode="r") as file:
        return await file.read()


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
        content={"message": (f"An unhandled exception occurred: {exc!r}.")},
    )
