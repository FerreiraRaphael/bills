import json
import unittest

from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from api.bills._q.fetch_bills import FetchBillsParams, fetch_bills, render_cls_fields
from api.bills.tags.model import Tag
from api.bills.model import Bill
from api.run import create_con


def print_beautiful(*values: object, model: BaseModel | list[BaseModel]) -> None:
    return print(*values, json.dumps(model, default=pydantic_encoder, indent=2))


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = (
            create_con("db/test.sqlite")
            .executescript("BEGIN;")
            .connection
        )

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()
        cls.con.close()

    def test_insert(self):

        insert_bill(Bill(name='name', value='9999',date='2024-01-01T00:00:00Z'))
        insert_bill(Bill(name='name2', value='9999',date='2024-01-01T00:00:00Z'))
        insert_bill(Bill(name='name3', value='9999',date='2024-01-01T00:00:00Z'))

        bill_list = fetch_bills(self.con)
        assert len(bill_list) == 3
        assert bill_list[0].name == "name"
        assert bill_list[1].name == "name2"
        assert bill_list[2].name == "name3"

if __name__ == "__main__":
    unittest.main()
