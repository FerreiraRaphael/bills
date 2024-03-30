from os import path

import pytest

from api.run import create_con


@pytest.fixture(scope="class", autouse=True)
def setup_con(request):
    con = create_con("file:db/test.sqlite")
    script_dir = path.dirname(path.abspath(__file__))
    sql_path = path.join(script_dir, "../db/clean_db.sql")
    with open(sql_path) as sql:
        con.executescript(sql.read())
    request.cls.con = con
    yield con
    con.close()
