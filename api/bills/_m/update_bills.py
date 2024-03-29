from sqlite3 import Connection

from pydantic import BaseModel


class UpdateBillsInput(BaseModel):
    bill_id: int
    main_tag_id: int


def update_bills(con: Connection, main_tag_id: int, bill_id: int):
    con.execute(
        f"""UPDATE bills SET main_tag_id = {main_tag_id} WHERE id = {bill_id}"""
    )
