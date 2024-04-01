import os
from typing import Literal

ENV_VARS = Literal["DB_AUTH", "DB_URL"]


def get_env(var: ENV_VARS):
    return os.getenv(var)
