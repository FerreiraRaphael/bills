from libsql_client import Transaction


async def check_tag(t: Transaction, name: str):
    res = await t.execute("SELECT * FROM tags WHERE name = ?;", [name])
    return len(res.rows) != 0
