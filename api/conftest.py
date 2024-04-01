import pytest_asyncio
from libsql_client import Client

# from api.env import get_env
from api.run import create_client

# from dotenv import load_dotenv

# load_dotenv(dotenv_path=".env.test", override=True)

# print('envenvenv', url=get_env("DB_URL"))

@pytest_asyncio.fixture(scope="session")
async def setup_client():
    async with create_client(
        # url=get_env("DB_URL"),
        # auth_token=get_env("DB_AUTH")
        url="file:db/test.sqlite"
    ) as client:
        # client.batch()
        yield client
        await client.close()


@pytest_asyncio.fixture(scope="function")
async def t(setup_client: Client):
    t = setup_client.transaction()
    yield t
    await t.rollback()
