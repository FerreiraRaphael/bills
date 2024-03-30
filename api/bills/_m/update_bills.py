from sqlite3 import Connection

from pydantic import BaseModel


class UpdateBillsInput(BaseModel):
    bill_id: int
    main_tag_id: int


def update_main_tag(con: Connection, main_tag_id: int, bill_id: int):
    con.execute("UPDATE bills SET main_tag_id = ? WHERE id = ?", [main_tag_id, bill_id])
