import unittest
from sqlite3 import Connection

from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags._q.check_tag import check_tag
from api.bills.tags.model import Tag


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con: Connection = cls.con
        insert_tag(cls.con, Tag(name="tag1"), Tag(name="tag2"))

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()

    def test_check_tag(self):
        assert check_tag(self.con, "tag1")
        assert check_tag(self.con, "tag2")
        assert not check_tag(self.con, "tag3")
        assert not check_tag(self.con, "tag4")


if __name__ == "__main__":
    unittest.main()
