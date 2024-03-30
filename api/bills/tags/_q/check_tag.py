from sqlite3 import Connection


def check_tag(con: Connection, name: str):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tags WHERE name = ?;", [name])
    return cursor.fetchone() is not None
