#!/bin/bash
uv run alembic revision --autogenerate -m "Initial migration"
uv run alembic upgrade head
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers ${BACKEND_WORKERS:-2}