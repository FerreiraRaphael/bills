import unittest

from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags._q.check_tag import check_tag
from api.bills.tags.model import Tag
from api.run import create_con


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = create_con("db/test.sqlite")

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_insert_tag_single(self):
        con = self.con.cursor().connection
        insert_tag(con, Tag(name="tag1"))
        insert_tag(con, Tag(name="tag2"))
        assert check_tag(con, "tag1")
        assert check_tag(con, "tag2")
        assert not check_tag(con, "tag3")
        assert not check_tag(con, "tag4")
        con.rollback()

    def test_insert_tag_multi(self):
        con = self.con.cursor().connection
        insert_tag(con, Tag(name="tag1"), Tag(name="tag2"))
        assert check_tag(con, "tag1")
        assert check_tag(con, "tag2")
        assert not check_tag(con, "tag3")
        assert not check_tag(con, "tag4")
        con.rollback()


if __name__ == "__main__":
    unittest.main()
