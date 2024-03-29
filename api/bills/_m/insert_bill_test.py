import unittest

from api.bills._m.insert_bill import insert_bill
from api.bills._q.fetch_bills import fetch_bills
from api.bills.model import Bill
from api.run import create_con


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = create_con("db/test.sqlite")

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()
        cls.con.close()

    def test_insert_single(self):
        con = self.con.cursor().connection
        date_sample = "2024-01-01T00:00:00Z"
        insert_bill(
            con, Bill(id=1, name="single1", value="9999", date=date_sample)
        )
        insert_bill(
            con, Bill(id=2, name="single2", value="9999", date=date_sample)
        )
        insert_bill(
            con, Bill(id=3, name="single3", value="9999", date=date_sample)
        )

        bill_list = fetch_bills(con)
        assert len(bill_list) == 3
        assert bill_list[0].name == "single1"
        assert bill_list[1].name == "single2"
        assert bill_list[1].value == 9999
        assert bill_list[2].value == 9999
        assert bill_list[0].id == 1
        assert bill_list[2].id == 3
        con.rollback()

    def test_insert_multiple(self):
        con = self.con.cursor().connection
        date_sample = "2024-01-01T00:00:00Z"
        bill1 = Bill(id=1, name="multi1", value="9999", date=date_sample)
        bill2 = Bill(id=2, name="multi2", value="9999", date=date_sample)
        bill3 = Bill(id=3, name="multi3", value="9999", date=date_sample)
        insert_bill(con, bill1, bill2, bill3)

        bill_list = fetch_bills(con)
        assert len(bill_list) == 3
        assert bill_list[0].name == "multi1"
        assert bill_list[1].name == "multi2"
        assert bill_list[1].value == 9999
        assert bill_list[2].value == 9999
        assert bill_list[0].id == 1
        assert bill_list[2].id == 3
        con.rollback()


if __name__ == "__main__":
    unittest.main()
