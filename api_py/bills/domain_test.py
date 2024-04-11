from datetime import datetime

import aiofiles
from libsql_client import Transaction

from api_py.bills._q.fetch_bills import FetchBillsParams, fetch_bills
from api_py.bills.domain import create_new_bills_from_csv
from api_py.logger import RequestLogger

csv_path = "api/bills/domain_test.csv"


async def test_create_new_bills_from_csv(t: Transaction, log: RequestLogger):
    async with aiofiles.open(csv_path, "r") as file:
        data = await file.read()
        await create_new_bills_from_csv(t, log, data)
        bill_list = await fetch_bills(
            t, log, FetchBillsParams(join_main_tag=True, join_tags=True)
        )
        assert len(bill_list) == 56
        assert bill_list[0].name == "Pag*Bacuribebidas"
        assert bill_list[0].id == 1
        assert bill_list[0].value == 4350
        assert (
            datetime.strftime(bill_list[0].date, "%Y-%m-%dT%H:%M:%SZ")
            == "2024-02-24T00:00:00Z"
        )
        assert len(bill_list[0].tags) == 1
        assert bill_list[0].tags[0].name == "Meus gastos"
        assert bill_list[0].tags[0].id == 1
        assert bill_list[0].main_tag.name == "Meus gastos"
        assert bill_list[0].main_tag.id == 1

        assert bill_list[35].name == "Amazon Prime Canais"
        assert bill_list[35].id == 36
        assert bill_list[35].value == 995
        assert (
            datetime.strftime(bill_list[35].date, "%Y-%m-%dT%H:%M:%SZ")
            == "2024-03-02T00:00:00Z"
        )
        assert len(bill_list[35].tags) == 2
        assert bill_list[35].tags[0].name == "fixo"
        assert bill_list[35].tags[0].id == 4
        assert bill_list[35].tags[1].name == "assinatura"
        assert bill_list[35].tags[1].id == 5
        assert bill_list[35].main_tag.name == "fixo"
        assert bill_list[35].main_tag.id == 4


async def test_decimal_in_create_new_bills(t: Transaction, log: RequestLogger):
    data = """"name","tags","number","date","main_tag","time"
               bill1,tag1,5.1,2024-02-25,main_tag,00:00
               bill2,tag1,2.2,2024-02-25,main_tag,00:00
               bill3,tag1,4.1,2024-02-25,main_tag,00:00
               bill4,tag1,13.84,2024-02-25,main_tag,00:00
               bill5,tag1,3.3,2024-02-25,main_tag,00:00
               bill6,tag1,0.11,2024-02-25,main_tag,00:00
               bill7,tag1,1000.01,2024-02-25,main_tag,00:00"""

    await create_new_bills_from_csv(t, log, data)
    bill_list = await fetch_bills(t, log)
    print(bill_list[0].name)
    assert bill_list[0].value == 510
    assert bill_list[1].value == 220
    assert bill_list[2].value == 410
    assert bill_list[3].value == 1384
    assert bill_list[4].value == 330
    assert bill_list[5].value == 11
    assert bill_list[6].value == 100001
