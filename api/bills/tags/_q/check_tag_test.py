import json
import unittest

from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from api.bills.tags._q.check_tag import check_tag
from api.run import create_con


def print_beautiful(*values: object, model: BaseModel | list[BaseModel]) -> None:
    return print(*values, json.dumps(model, default=pydantic_encoder, indent=2))


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = (
            create_con("db/test.sqlite")
            .executescript("""BEGIN;
                                                            INSERT INTO tags ("name")
                                                             VALUES ("tag1"), ("tag2");
                                                             """)
            .connection
        )

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()
        cls.con.close()

    def test_check_tag(self):
        assert check_tag(self.con, "tag1")
        assert check_tag(self.con, "tag2")
        assert not check_tag(self.con, "tag3")
        assert not check_tag(self.con, "tag4")
        self.con.execute("DELETE FROM tags WHERE id IS NOT NULL;")
        self.con.execute("DELETE FROM sqlite_sequence WHERE name='tags';")


if __name__ == "__main__":
    unittest.main()
