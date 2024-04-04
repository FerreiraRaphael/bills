from datetime import datetime

import aiofiles
from libsql_client import Transaction
import pytest

from api.bills._q.fetch_bills import FetchBillsParams, fetch_bills
from api.bills.domain import create_new_bills_from_csv
from api.logger import RequestLogger

csv_path = "api/bills/test.csv"

@pytest.mark.skip(reason="no way of currently testing this")
async def test_create_new_bills_from_csv(t: Transaction, log: RequestLogger):
    async with aiofiles.open(csv_path, "r") as file:
        data = await file.read()
        await create_new_bills_from_csv(t, log, data)
        bill_list = await fetch_bills(
            t, log, FetchBillsParams(join_main_tag=True, join_tags=True)
        )
        assert len(bill_list) == 1
        assert bill_list[0].name == "Uber* Trip"
        assert bill_list[0].id == 1
        assert bill_list[0].value == 2216
        assert (
            datetime.strftime(bill_list[0].date, "%Y-%m-%dT%H:%M:%SZ")
            == "2024-02-26T00:00:00Z"
        )
        assert len(bill_list[0].tags) == 2
        assert bill_list[0].tags[0].name == "Meus gastos"
        assert bill_list[0].tags[0].id == 1
        assert bill_list[0].tags[1].name == "uber"
        assert bill_list[0].tags[1].id == 2
        assert bill_list[0].main_tag.name == "Meus gastos"
        assert bill_list[0].main_tag.id == 1
