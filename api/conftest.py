import pytest_asyncio
from libsql_client import Client

from api.run import create_client


@pytest_asyncio.fixture(scope="session")
async def setup_client():
    async with create_client("file:db/test.sqlite") as client:
        yield client
        await client.close()


@pytest_asyncio.fixture(scope="function")
async def t(setup_client: Client):
    t = setup_client.transaction()
    yield t
    await t.rollback()
