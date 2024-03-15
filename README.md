# commands

### migrate
```shell
alembic revision --autogenerate -m "Create a baseline migrations"
```
```shell
alembic upgrade head
```
```shell
uvicorn api.run:app --reload
```

