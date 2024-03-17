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

migrations

```shell
sqitch add bills -n 'Creates table to track our bills.'
```

test

```shell
python -m unittest discover -p '*_test.py'
```
