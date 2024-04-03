<<<<<<< Updated upstream
# import aiofiles
from libsql_client import Transaction

# from api.bills.domain import create_new_bills_from_csv
=======
from datetime import datetime
import aiofiles
from libsql_client import Transaction

from api.bills._q.fetch_bills import FetchBillsParams, fetch_bills
from api.bills.domain import create_new_bills_from_csv
>>>>>>> Stashed changes

csv_path = "api/bills/test.csv"


async def test_create_new_bills_from_csv(t: Transaction):
<<<<<<< Updated upstream
    assert True
    # async with aiofiles.open(csv_path, "r") as file:
    #     data = await file.read()
    #     result = await create_new_bills_from_csv(t, data)
    #     assert len(result) != 0
=======
    async with aiofiles.open(csv_path, "r") as file:
        data = await file.read()
        await create_new_bills_from_csv(t, data)
        bill_list = await fetch_bills(t, FetchBillsParams(join_main_tag=True, join_tags=True))
        assert len(bill_list) == 1
        assert bill_list[0].name == "Uber* Trip"
        assert bill_list[0].id == 1
        assert bill_list[0].value == 2216
        assert datetime.strftime(bill_list[0].date, "%Y-%m-%dT%H:%M:%SZ") == "2024-02-26T00:00:00Z"
        assert len(bill_list[0].tags) == 2
        assert bill_list[0].tags[0].name == "Meus gastos"
        assert bill_list[0].tags[0].id == 1
        assert bill_list[0].tags[1].name == "uber"
        assert bill_list[0].tags[1].id == 2
        assert bill_list[0].main_tag.name == "Meus gastos"
        assert bill_list[0].main_tag.id == 1

>>>>>>> Stashed changes
