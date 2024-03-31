import pytest_asyncio
from libsql_client import Client, Transaction

from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags._q.check_tag import check_tag
from api.bills.tags.model import Tag


@pytest_asyncio.fixture(scope="module")
async def t(setup_client: Client):
    t = setup_client.transaction()
    await insert_tag(t, Tag(name="tag1"), Tag(name="tag2"))
    yield t
    await t.rollback()


async def test_check_tag(t: Transaction):
    assert await check_tag(t, "tag1")
    assert await check_tag(t, "tag2")
    assert not await check_tag(t, "tag3")
    assert not await check_tag(t, "tag4")
