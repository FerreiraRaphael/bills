from libsql_client import Transaction

from api.bills._m.insert_bill import insert_bill
from api.bills._q.fetch_bills import fetch_bills
from api.bills.model import Bill

date_sample = "2024-01-01T00:00:00Z"


async def test_insert_one_return(t: Transaction):
    bill1 = Bill(id=1, name="multi1", value="9999", date=date_sample)
    [res1] = await insert_bill(t, bill1)
    assert res1.name == bill1.name
    assert res1.created_at is not None
    assert res1.updated_at is not None
    assert res1.deleted_at is None


async def test_insert_single(t: Transaction):
    await insert_bill(t, Bill(id=1, name="single1", value="9999", date=date_sample))
    await insert_bill(t, Bill(id=2, name="single2", value="9999", date=date_sample))
    await insert_bill(t, Bill(id=3, name="single3", value="9999", date=date_sample))
    bill_list = await fetch_bills(t)
    assert len(bill_list) == 3
    assert bill_list[0].name == "single1"
    assert bill_list[1].name == "single2"
    assert bill_list[1].value == 9999
    assert bill_list[2].value == 9999
    assert bill_list[0].id == 1
    assert bill_list[2].id == 3


async def test_insert_multiple(t: Transaction):
    bill1 = Bill(id=1, name="multi1", value="9999", date=date_sample)
    bill2 = Bill(id=2, name="multi2", value="9999", date=date_sample)
    bill3 = Bill(id=3, name="multi3", value="9999", date=date_sample)
    await insert_bill(t, bill1, bill2, bill3)
    bill_list = await fetch_bills(t)
    assert len(bill_list) == 3
    assert bill_list[0].name == bill1.name
    assert bill_list[1].name == bill2.name
    assert bill_list[1].value == bill2.value
    assert bill_list[2].value == bill3.value
    assert bill_list[0].id == bill1.id
    assert bill_list[2].id == bill3.id


async def test_insert_return(t: Transaction):
    bill1 = Bill(id=1, name="multi1", value="9999", date=date_sample)
    bill2 = Bill(id=2, name="multi2", value="9999", date=date_sample)
    bill3 = Bill(id=3, name="multi3", value="9999", date=date_sample)
    res1, res2, res3 = await insert_bill(t, bill1, bill2, bill3)
    assert res1.name == bill1.name
    assert res2.name == bill2.name
    assert res3.name == bill3.name
    assert res1.created_at is not None
    assert res1.updated_at is not None
    assert res1.deleted_at is None
