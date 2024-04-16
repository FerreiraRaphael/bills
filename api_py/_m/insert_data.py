from typing import Any, Callable, Dict, List, TypeVar

from libsql_client import Transaction

from api_py.models import TableModel

T = TypeVar("T", bound=TableModel)

TMapper = Callable[[T], Dict[str, Any]]


def treat_data(mapper: TMapper[T], *args: T):
    params_string = []
    model_objects_values = []
    for object in args:
        object = mapper(object)
        filtered_object = {k: v for k, v in object.items() if v is not None}
        model_columns = filtered_object.keys()
        params_string.extend([f'({", ".join(["?" for _ in model_columns])})'])
        model_objects_values.extend(filtered_object.values())
    return (model_columns, params_string, model_objects_values)


async def insert_data(
    t: Transaction, TableModel: T, mapper: TMapper[T], *args: T
) -> List[T]:
    sql_columns, params_string, model_objects_values = treat_data(mapper, *args)
    sql = f"""
                INSERT INTO {TableModel.__table_name__} ({", ".join(sql_columns)})
                VALUES {", ".join(params_string)}
                RETURNING *;
                """
    res = await t.execute(
        sql,
        model_objects_values,
    )
    return [TableModel(**(row.asdict())) for row in res.rows]
