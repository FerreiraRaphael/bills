import json
import unittest

from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from api.bills._m.insert_bill import insert_bill
from api.bills._m.update_bills import update_bills
from api.bills._q.fetch_bills import FetchBillsParams, fetch_bills, render_cls_fields
from api.bills.model import Bill
from api.bills.tags._m.insert_bills_tags import InsertBillsTagsInput, insert_bills_tags
from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags.model import Tag
from api.run import create_con


def print_beautiful(*values: object, model: BaseModel | list[BaseModel]) -> None:
    return print(*values, json.dumps(model, default=pydantic_encoder, indent=2))


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = (
            create_con("db/test.sqlite")
            .executescript("""   
BEGIN;   
DELETE FROM BILLS_TAGS;
DELETE FROM BILLS;
DELETE FROM TAGS;
                    """)
            .connection
        )
        date_sample = "2024-01-01T00:00:00Z"
        bill1 = Bill(id=1, name="name", value=9999, date=date_sample)
        bill2 = Bill(id=2, name="name2", value=9999, date=date_sample)
        tag1 = Tag(id=1, name="name")
        tag2 = Tag(id=2, name="name2")
        tag3 = Tag(id=3, name="name3")
        bills_tags1 = InsertBillsTagsInput(bill_id=1, tag_id=2)
        bills_tags2 = InsertBillsTagsInput(bill_id=1, tag_id=1)
        insert_bill(cls.con, bill1, bill2)
        insert_tag(cls.con, tag1, tag2, tag3)
        insert_bills_tags(cls.con, bills_tags1, bills_tags2)
        update_bills(cls.con, 3, 1)

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()
        cls.con.close()

    def test_output_join(self):
        bill_list = fetch_bills(
            self.con, FetchBillsParams(join_main_tag=True, join_tags=True)
        )
        assert len(bill_list) == 2
        assert bill_list[0].name == "name"
        assert bill_list[1].name == "name2"
        assert len(bill_list[0].tags) == 2
        assert len(bill_list[1].tags) == 0
        assert bill_list[0].tags[0].name == "name"
        assert bill_list[0].tags[1].name == "name2"
        assert bill_list[0].main_tag.name == "name3"

    def test_output_no_join(self):
        bill_list = fetch_bills(self.con)
        assert len(bill_list) == 2
        assert bill_list[0].tags is None
        assert bill_list[1].tags is None

    def test_render_tags(self):
        assert render_cls_fields(Tag)("tag", "name") == "'name', tag.name"


if __name__ == "__main__":
    unittest.main()


"""
INSERT INTO bills (id, name, value, date)
    VALUES
        (1, 'name', 9999, '2024-01-01T00:00:00Z'),
        (2, 'name2', 9999, '2024-01-01T00:00:00Z');

INSERT INTO tags (id, name) VALUES (1, 'name'), (2, 'name2'), (3, 'name3');

INSERT INTO bills_tags (bill_id, tag_id) VALUES (1, 2), (1, 1);

UPDATE bills SET main_tag_id = 3 WHERE id=1;
"""
