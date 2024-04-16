import functools
import os
from contextlib import asynccontextmanager
from io import StringIO
from typing import Annotated, List

import aiofiles
import aiohttp
import yaml
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, Response, APIRouter
from fastapi.responses import JSONResponse, PlainTextResponse
from libsql_client import Transaction, create_client
from pydantic import BaseModel
from pydash import uniq
from libsql_client import Client
from api_py.bills._m.insert_bill import insert_bill
from api_py.bills._q.fetch_bills import fetch_bills
from api_py.bills.model import Bill
from api_py.env import get_env
from api_py.logger import RequestLogger, create_logger, create_request_logger

load_dotenv(override=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('No lifespan')
    app.state.logger = create_logger()

    print(
        "DB connecting.",
        get_env("DB_URL"),
        "Using Auth token db" if get_env("DB_AUTH") else "",
    )
    try:
        async with create_client(
            url=get_env("DB_URL"), auth_token=get_env("DB_AUTH")
        ) as db:
          print("To DB Connected.")
          app.state.db = db
          yield
          print("Closing DB Connection.")
          await db.close()
    except Exception as e:
        print('error when trying to connect db', e)
        raise e

async def create_db(app: FastAPI):
    print('created db if not exists')
    print(
        "DB connecting.",
        get_env("DB_URL"),
        "Using Auth token db" if get_env("DB_AUTH") else "",
    )
    try:
        async with create_client(
            url=get_env("DB_URL"), auth_token=get_env("DB_AUTH")
        ) as db:
          print("To DB Connected.")
          app.state.db = db
          return db
    except Exception as e:
        print('error when trying to connect db', e)
        raise e

async def db():
    print('created db if not exists')
    print(
        "DB connecting.",
        get_env("DB_URL"),
        "Using Auth token db" if get_env("DB_AUTH") else "",
    )
    try:
        async with create_client(
            url=get_env("DB_URL"), auth_token=get_env("DB_AUTH")
        ) as db:
          print("To DB Connected.")
          yield db
    except Exception as e:
        print('error when trying to connect db', e)
        raise e
    finally:
      print('finally')
      await db.close()
      print('finally2')

DB = Annotated[Client, Depends(db)]

async def t(req: Request, db: DB):
    # print('Chegando na transaction, da erro aqui')
    # if req.app.state.db is None:
    #   print('Sem db criando um')
    #   await create_db(req.app)
    transaction: Transaction = db.transaction()
    try:
        yield transaction
        if not transaction.closed:
            await transaction.commit()
    except Exception as e:
        await transaction.rollback()
        raise e


async def http():
    async with aiohttp.ClientSession() as session:
        yield session
        await session.close()


async def log(req: Request):
    print('Criando o logger request')
    logger = create_logger()
    yield await create_request_logger(logger, req.url.path)


DTransaction = Annotated[Transaction, Depends(t)]
DLogger = Annotated[RequestLogger, Depends(log)]
DHttp = Annotated[RequestLogger, Depends(http)]
router = APIRouter()

@router.get("/api")
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


@router.post("/api/add_bills")
async def add_new_bill(t: DTransaction, logger: DLogger, bills: list[Bill]):
    log = logger.getChild(__name__, __file__)
    try:
        log.info(f"router add_new_bill {list(map(lambda x: x.json(), bills))}")
        return await insert_bill(t, log, *bills)
    except Exception as e:
        log.exception("router add_new_bill fail", exc_info=e)
        await t.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": (f"An unhandled exception occurred: {e!r}.")},
        )


@router.get("/api/ping")
async def ping():
    return "pingg"


class LoggerInput(BaseModel):
    logs: List[str]
    append = True


@router.post("/api/logger", response_class=PlainTextResponse)
async def post_logger(input: LoggerInput):
    # if input.append:
    lines = input.logs
    logs_path = "logs.txt"
    async with aiofiles.open(logs_path, mode="a", newline="\n") as file:
        if input.append and os.path.exists(logs_path):
            text = await file.read()
            lines.extend(text.split("\n"))
        unique_lines = uniq(lines)
        await file.write("\n".join(unique_lines))
        return await file.read()


@router.get("/api/logger", response_class=PlainTextResponse)
async def get_logger():
    async with aiofiles.open("logs.txt", mode="r") as file:
        return await file.read()


def create_api():
  print('Criando o app')
  app = FastAPI()
  app.include_router(router)

  # @app.on_event("startup")
  # async def startup_event():
  #     print('No lifespan')
  #     app.state.logger = create_logger()

  #     print(
  #         "DB connecting.",
  #         get_env("DB_URL"),
  #         "Using Auth token db" if get_env("DB_AUTH") else "",
  #     )
  #     try:
  #         async with create_client(
  #             url=get_env("DB_URL"), auth_token=get_env("DB_AUTH")
  #         ) as db:
  #           print("To DB Connected.")
  #           app.state.db = db
  #     except Exception as e:
  #         print('error when trying to connect db', e)
  #         raise e

  @app.get("/api/openapi.yaml", include_in_schema=False)
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

  return app
