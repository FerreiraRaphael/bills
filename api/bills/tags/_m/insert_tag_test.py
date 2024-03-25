import json
import unittest

from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags._q.check_tag import check_tag
from api.bills.tags.model import Tag
from api.run import create_con


def print_beautiful(*values: object, model: BaseModel | list[BaseModel]) -> None:
    return print(*values, json.dumps(model, default=pydantic_encoder, indent=2))


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = create_con("db/test.sqlite").executescript("BEGIN;").connection

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()
        cls.con.close()

    def test_insert_tag_single(self):
        insert_tag(self.con, Tag(name="tag1"))
        insert_tag(self.con, Tag(name="tag2"))
        assert check_tag(self.con, "tag1")
        assert check_tag(self.con, "tag2")
        assert not check_tag(self.con, "tag3")
        assert not check_tag(self.con, "tag4")
        self.con.execute("DELETE FROM tags WHERE id IS NOT NULL;")
        self.con.execute("DELETE FROM sqlite_sequence WHERE name='tags';")

    def test_insert_tag_multi(self):
        insert_tag(self.con, Tag(name="tag1"), Tag(name="tag2"))
        assert check_tag(self.con, "tag1")
        assert check_tag(self.con, "tag2")
        assert not check_tag(self.con, "tag3")
        assert not check_tag(self.con, "tag4")
        self.con.execute("DELETE FROM tags WHERE id IS NOT NULL;")
        self.con.execute("DELETE FROM sqlite_sequence WHERE name='tags';")


if __name__ == "__main__":
    unittest.main()
