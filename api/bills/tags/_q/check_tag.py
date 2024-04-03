from libsql_client import Transaction


async def check_tag(t: Transaction, name: str):
    res = await t.execute("SELECT id FROM tags WHERE name = ?;", [name])
    return [row.asdict() for row in res.rows]
