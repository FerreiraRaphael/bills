import unittest

from api.bills._m.insert_bill import insert_bill
from api.bills._q.fetch_bills import fetch_bills
from api.bills.model import Bill
from libsql_client import dbapi2
class TestStringMethods(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()

    def test_insert_single(self):
      self.con: dbapi2.ConnectionTypes = self.con
      with self.con as con:
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
        self.con: dbapi2.ConnectionTypes = self.con
        with self.con as con:
            date_sample = "2024-01-01T00:00:00Z"
            bill1 = Bill(id=1, name="multi1", value="9999", date=date_sample)
            bill2 = Bill(id=2, name="multi2", value="9999", date=date_sample)
            bill3 = Bill(id=3, name="multi3", value="9999", date=date_sample)
            insert_bill(con, bill1, bill2, bill3)

            bill_list = fetch_bills(con)
            assert len(bill_list) == 3
            assert bill_list[0].name == bill1.name
            assert bill_list[1].name == bill2.name
            assert bill_list[1].value == bill2.value
            assert bill_list[2].value == bill3.value
            assert bill_list[0].id == bill1.id
            assert bill_list[2].id == bill3.id
            con.rollback()

    def test_insert_return(self):
        self.con: dbapi2.ConnectionTypes = self.con
        with self.con as con:
            date_sample = "2024-01-01T00:00:00Z"
            bill1 = Bill(id=1, name="multi1", value="9999", date=date_sample)
            bill2 = Bill(id=2, name="multi2", value="9999", date=date_sample)
            bill3 = Bill(id=3, name="multi3", value="9999", date=date_sample)
            res1, res2, res3 = insert_bill(con, bill1, bill2, bill3)
            assert res1.name == bill1.name
            assert res2.name == bill2.name
            assert res3.name == bill3.name
            assert res1.created_at is not None
            assert res1.updated_at is not None
            assert res1.deleted_at is None
            con.rollback()

    def test_insert_one_return(self):
        self.con: dbapi2.ConnectionTypes = self.con
        with self.con as con:
            date_sample = "2024-01-01T00:00:00Z"
            bill1 = Bill(id=1, name="multi1", value="9999", date=date_sample)
            [res1] = insert_bill(con, bill1)
            assert res1.name == bill1.name
            assert res1.created_at is not None
            assert res1.updated_at is not None
            assert res1.deleted_at is None
            con.rollback()

if __name__ == "__main__":
    unittest.main()
