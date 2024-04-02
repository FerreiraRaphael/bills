import pytest_asyncio
from dotenv import load_dotenv
from libsql_client import Client

from api.env import get_env
from api.run import create_client

load_dotenv(dotenv_path=".env.test", override=True)


@pytest_asyncio.fixture(scope="session")
async def setup_client():
    async with create_client(
        auth_token=get_env("DB_AUTH"), url=get_env("DB_URL")
    ) as client:
        # call clean_db.sql here
        yield client
        await client.close()


@pytest_asyncio.fixture(scope="function")
async def t(setup_client: Client):
    t = setup_client.transaction()
    yield t
    await t.rollback()
