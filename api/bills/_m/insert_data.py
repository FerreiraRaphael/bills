from sqlite3 import Connection

from pydantic import BaseModel


def treat_data(mapper, *args: BaseModel):
    params_string = []
    model_objects_values = []
    for object in args:
        object = mapper(object)
        model_columns = object.keys()
        params_string.extend([f'({", ".join(["?" for _ in model_columns])})'])
        model_objects_values.extend(object.values())
    return (model_columns, params_string, model_objects_values)


def insert_data(con: Connection, table: str, mapper, *args: BaseModel):
    sql_columns, params_string, model_objects_values = treat_data(mapper, *args)
    return con.execute(
        f"""
                INSERT INTO {table} ({", ".join(sql_columns)})
                VALUES {", ".join(params_string)}
                RETURNING *;
                """,
        model_objects_values,
    )
