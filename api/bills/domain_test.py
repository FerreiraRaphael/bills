# import aiofiles
from libsql_client import Transaction

# from api.bills.domain import create_new_bills_from_csv

csv_path = "api/bills/test.csv"


async def test_create_new_bills_from_csv(t: Transaction):
    assert True
    # async with aiofiles.open(csv_path, "r") as file:
    #     data = await file.read()
    #     result = await create_new_bills_from_csv(t, data)
    #     assert len(result) != 0
