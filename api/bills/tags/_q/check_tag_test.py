import pytest_asyncio
from libsql_client import Client, Transaction

from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags._q.check_tag import check_tag
from api.bills.tags.model import Tag
from api.logger import RequestLogger


@pytest_asyncio.fixture(scope="module")
async def t(setup_client: Client, log: RequestLogger):
    t = setup_client.transaction()
    await insert_tag(t, log, Tag(name="tag1"), Tag(name="tag2"))
    yield t
    await t.rollback()


async def test_check_tag(t: Transaction, log: RequestLogger):
    assert await check_tag(t, log, "tag1")
    assert await check_tag(t, log, "tag2")
    assert not await check_tag(t, log, "tag3")
    assert not await check_tag(t, log, "tag4")
