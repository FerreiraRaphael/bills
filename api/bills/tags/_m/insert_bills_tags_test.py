import unittest

from api.bills._m.insert_bill import insert_bill
from api.bills.model import Bill
from api.bills.tags._m.insert_bills_tags import insert_bills_tags
from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags.model import Tag
from api.run import create_con


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = create_con("db/test.sqlite").executescript("BEGIN;").connection

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()
        cls.con.close()

    def test_insert_bills_tags(self):
        date_sample = "2024-01-01T00:00:00Z"
        bill1 = Bill(id=1, name="bill1", value="9999", date=date_sample)
        tag1 = Tag(id=1, name="tag1")
        tag2 = Tag(id=2, name="tag2")
        tag3 = Tag(id=3, name="tag3")
        insert_bill(self.con, bill1)
        insert_tag(self.con, tag1, tag2, tag3)
        insert_bills_tags(self.con, 1, 1, 2, 3)
        bills_tags_list = self.con.execute(
            """SELECT bill_id, tag_id FROM bills_tags"""
        ).fetchall()
        assert len(bills_tags_list) == 3
        assert bills_tags_list[0] == {"bill_id": 1, "tag_id": 1}
        assert bills_tags_list[1] == {"bill_id": 1, "tag_id": 2}
        assert bills_tags_list[2] == {"bill_id": 1, "tag_id": 3}
        self.con.execute("DELETE FROM bills WHERE id IS NOT NULL;")
        self.con.execute("DELETE FROM tags WHERE id IS NOT NULL;")
        self.con.execute("DELETE FROM bills_tags WHERE bill_id IS NOT NULL;")
        self.con.execute("DELETE FROM sqlite_sequence WHERE name='bills';")
        self.con.execute("DELETE FROM sqlite_sequence WHERE name='tags';")
        self.con.execute("DELETE FROM sqlite_sequence WHERE name='bills_tags';")


if __name__ == "__main__":
    unittest.main()
