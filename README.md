# Test project
## Запуск приложения:
### 1. Запустить контейнер с postgres:
```
docker compose up -d
```
### 2. (Опционально) Создать собственноручно виртуальную среду:
```
python3.12 -m venv .venv
source .venv/bin/activate
pip install poetry
```
### 2.1 Выполнить установку зависимостей:
```
poetry install --no-root
```
### 3. Выполнить миграции:
```
poetry run python scrips/run_alembic.py upgrade head
```
### 4. Выполнить запуск приложения:
```
uvicorn users_app.main:app
```

### 5. Для проверки работоспособности запустить тесты:
```
pytest tests/ -v
```
### 6. (Опционально) Заполнить базу мокнутыми данными:
```
python3 scripts/fill_db.py
```
## Пример создания миграций:
```
poetry run python scrips/run_alembic.py revision --autogenerate -m "create users table"
```