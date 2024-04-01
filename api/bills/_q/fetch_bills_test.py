import pytest_asyncio
from libsql_client import Client, Transaction

from api.bills._m.insert_bill import insert_bill
from api.bills._m.update_bills import update_main_tag
from api.bills._q.fetch_bills import FetchBillsParams, fetch_bills, render_cls_fields
from api.bills.model import Bill
from api.bills.tags._m.insert_bills_tags import insert_bills_tags
from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags.model import BillTag, Tag


@pytest_asyncio.fixture(scope="module")
async def t(setup_client: Client):
    t = setup_client.transaction()
    date_sample = "2024-01-01T00:00:00Z"
    await insert_bill(
        t,
        Bill(id=1, name="name", value=9999, date=date_sample),
        Bill(id=2, name="name2", value=9999, date=date_sample),
    )
    await insert_tag(
        t,
        Tag(id=1, name="name"),
        Tag(id=2, name="name2"),
        Tag(id=3, name="name3"),
    )
    await insert_bills_tags(
        t, BillTag(bill_id=1, tag_id=2), BillTag(bill_id=1, tag_id=1)
    )
    await update_main_tag(t, 3, 1)
    yield t
    await t.rollback()


async def test_output_join(t: Transaction):
    bill_list = await fetch_bills(
        t, FetchBillsParams(join_main_tag=True, join_tags=True)
    )
    assert len(bill_list) == 2
    assert bill_list[0].name == "name"
    assert bill_list[1].name == "name2"
    assert len(bill_list[0].tags) == 2
    assert len(bill_list[1].tags) == 0
    assert bill_list[0].tags[0].name == "name"
    assert bill_list[0].tags[1].name == "name2"
    assert bill_list[0].main_tag.name == "name3"


async def test_output_no_join(t: Transaction):
    bill_list = await fetch_bills(t)
    assert len(bill_list) == 2
    assert bill_list[0].tags is None
    assert bill_list[1].tags is None


def test_render_tags():
    assert render_cls_fields(Tag)("tag", "name") == "'name', tag.name"
