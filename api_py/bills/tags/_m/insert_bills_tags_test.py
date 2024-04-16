from libsql_client import Transaction

from api_py.bills._m.insert_bill import insert_bill
from api_py.bills._q.fetch_bills import FetchBillsParams, fetch_bills
from api_py.bills.model import Bill
from api_py.bills.tags._m.insert_bills_tags import insert_bills_tags
from api_py.bills.tags._m.insert_tag import insert_tag
from api_py.bills.tags.model import BillTag, Tag
from api_py.logger import RequestLogger


async def test_insert_bills_tags(t: Transaction, log: RequestLogger):
    date_sample = "2024-01-01T00:00:00Z"
    bill1 = Bill(id=1, name="bill1", value="9999", date=date_sample)
    tag1 = Tag(id=1, name="tag1")
    tag2 = Tag(id=2, name="tag2")
    tag3 = Tag(id=3, name="tag3")
    await insert_bill(t, log, bill1)
    await insert_tag(t, log, tag1, tag2, tag3)
    await insert_bills_tags(
        t,
        log,
        BillTag(bill_id=1, tag_id=1),
        BillTag(bill_id=1, tag_id=2),
        BillTag(bill_id=1, tag_id=3),
    )
    bill_list = await fetch_bills(t, log, FetchBillsParams(join_tags=True))
    assert len(bill_list) == 1
    assert len(bill_list[0].tags) == 3
    assert bill_list[0].tags[0].name == "tag1"
    assert bill_list[0].tags[1].name == "tag2"
    assert bill_list[0].tags[2].name == "tag3"
