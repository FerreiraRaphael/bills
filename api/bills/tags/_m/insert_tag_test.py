from libsql_client import Transaction

from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags._q.check_tag import check_tag
from api.bills.tags.model import Tag


async def test_insert_tag_single(t: Transaction):
    await insert_tag(t, Tag(name="tag1"))
    await insert_tag(t, Tag(name="tag2"))
    assert await check_tag(t, "tag1")
    assert await check_tag(t, "tag2")
    assert not await check_tag(t, "tag3")
    assert not await check_tag(t, "tag4")


async def test_insert_tag_multi(t: Transaction):
    await insert_tag(t, Tag(name="tag1"), Tag(name="tag2"))
    assert await check_tag(t, "tag1")
    assert await check_tag(t, "tag2")
    assert not await check_tag(t, "tag3")
    assert not await check_tag(t, "tag4")


async def test_insert_return(t: Transaction):
    [tag1, tag2] = await insert_tag(t, Tag(name="tag1"), Tag(name="tag2"))
    assert tag1.created_at is not None
    assert tag1.updated_at is not None
    assert tag1.deleted_at is None
    assert tag2.created_at is not None
    assert tag2.updated_at is not None
    assert tag2.deleted_at is None
