from libsql_client import Transaction
from pydantic import BaseModel


class UpdateBillsInput(BaseModel):
    bill_id: int
    main_tag_id: int


async def update_main_tag(t: Transaction, main_tag_id: int, bill_id: int):
    return await t.execute(
        "UPDATE bills SET main_tag_id = ? WHERE id = ?", [main_tag_id, bill_id]
    )
