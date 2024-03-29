# commands

### migrate
```shell
atlas migrate apply --env test
atlas migrate apply --env local
```

```shell
atlas migrate diff migration_name \
  --to file://db/schema.sql \
  --dev-url "sqlite://dev?mode=memory" \
  --format '{{ sql . "  " }}'

atlas migrate down --env local  --dev-url "sqlite://dev?mode=memory"
```

test
```shell
pytest
```

linter
```shell
ruff check --fix --select 'I,E,F,UP,B,SIM'
```

format
```shell
ruff format --check
ruff format
```
