from sqlite3 import Connection


def fetch_id(con: Connection, table: str, *sql_columns: str):
    placeholders = ", ".join(["?"] * len(sql_columns))
    cursor = con.cursor()
    cursor.execute(
        f"""SELECT id FROM {table} WHERE name IN ({placeholders});""", sql_columns
    )
    id_values = cursor.fetchall()
    cursor.close()
    return id_values


def insert_bills_tags(con: Connection, bill_id: int, *tags_id: int):
    params_string = [", ".join(["(?, ?)" for _ in tags_id])]
    values_list = []
    for tag_id in tags_id:
        values_list.append(bill_id)
        values_list.append(tag_id)

    return con.execute(
        f"""
                INSERT INTO bills_tags (bill_id, tag_id)
                VALUES{", ".join(params_string)}
                """,
        tuple(values_list),
    )
