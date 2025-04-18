
## Запуск миграций:
```
poetry run python run_alembic.py revision --autogenerate -m "create users table"
poetry run python run_alembic.py upgrade head
```