#!bin/bash
uv run alembic check || uv run alembic revision --autogenerate -m "Initial migration"
uv run alembic upgrade head
