import unittest
import json
from pydantic import BaseModel
from pydantic.json import pydantic_encoder
from api.run import create_con
from api.bills.tags.model import Tag
from api.bills._q.fetch_bills import fetch_bills, FetchBillsParams, render_cls_fields

def print_beautiful(
  *values: object,
  model: BaseModel | list[BaseModel]
) -> None:
  return print(
    *values,
    json.dumps(
      model,
      default=pydantic_encoder,
      indent=2
    )
  )

class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = create_con("db/test.sqlite").executescript("""
BEGIN;
DELETE FROM BILLS_TAGS;
DELETE FROM BILLS;
DELETE FROM TAGS;
INSERT INTO bills (id, name, value, date)
    VALUES
        (1, 'name', 9999, '2024-01-01T00:00:00Z'),
        (2, 'name2', 9999, '2024-01-01T00:00:00Z');

INSERT INTO tags (id, name) VALUES (1, 'name'), (2, 'name2'), (3, 'name3');

INSERT INTO bills_tags (bill_id, tag_id) VALUES (1, 2), (1, 1);

UPDATE bills SET main_tag_id = 3 WHERE id=1;
                    """).connection

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()
        cls.con.close()

    def test_output_join(self):
        bill_list = fetch_bills(self.con, FetchBillsParams(
          join_main_tag=True,
          join_tags=True
        ))
        assert len(bill_list) == 2
        assert bill_list[0].name == 'name'
        assert bill_list[1].name == 'name2'
        assert len(bill_list[0].tags)==2
        assert len(bill_list[1].tags)==0
        assert bill_list[0].tags[0].name == 'name'
        assert bill_list[0].tags[1].name == 'name2'
        assert bill_list[0].main_tag.name == 'name3'

    def test_output_no_join(self):
        bill_list = fetch_bills(self.con)
        assert len(bill_list) == 2
        assert bill_list[0].tags == None
        assert bill_list[1].tags == None

    def test_render_tags(self):
        assert render_cls_fields(Tag)("tag", "name") == "'name', tag.name"

if __name__ == '__main__':
    unittest.main()
