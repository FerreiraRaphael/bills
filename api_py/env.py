import os
from typing import Literal

ENV_VARS = Literal["DB_AUTH", "DB_URL", "CLERK_FRONTEND_API_URL", "CLERK_API_URL", "CLERK_SECRET_KEY"]


def get_env(var: ENV_VARS):
    return os.getenv(var)
