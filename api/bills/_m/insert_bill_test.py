import json
import unittest

from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from api.bills._m.insert_bill import insert_bill
from api.bills._q.fetch_bills import fetch_bills
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

    def test_insert_single(self):
        date_sample = "2024-01-01T00:00:00Z"
        insert_bill(self.con, Bill(name="single1", value="9999", date=date_sample))
        insert_bill(self.con, Bill(name="single2", value="9999", date=date_sample))
        insert_bill(self.con, Bill(name="single3", value="9999", date=date_sample))

        bill_list = fetch_bills(self.con)
        assert len(bill_list) == 3
        assert bill_list[0].name == "single1"
        assert bill_list[1].name == "single2"
        assert bill_list[1].value == 9999
        assert bill_list[2].value == 9999
        assert bill_list[0].id == 1
        assert bill_list[2].id == 3
        self.con.execute("DELETE FROM bills WHERE id IS NOT NULL;")
        self.con.execute("DELETE FROM sqlite_sequence WHERE name='bills';")

    def test_insert_multiple(self):
        date_sample = "2024-01-01T00:00:00Z"
        bill1 = Bill(name="multi1", value="9999", date=date_sample)
        bill2 = Bill(name="multi2", value="9999", date=date_sample)
        bill3 = Bill(name="multi3", value="9999", date=date_sample)
        insert_bill(self.con, bill1, bill2, bill3)

        bill_list = fetch_bills(self.con)
        assert len(bill_list) == 3
        assert bill_list[0].name == "multi1"
        assert bill_list[1].name == "multi2"
        assert bill_list[1].value == 9999
        assert bill_list[2].value == 9999
        assert bill_list[0].id == 1
        assert bill_list[2].id == 3
        self.con.execute("DELETE FROM bills WHERE id IS NOT NULL;")
        self.con.execute("DELETE FROM sqlite_sequence WHERE name='bills';")


if __name__ == "__main__":
    unittest.main()
