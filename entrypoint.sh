set -x
cd fast_flat

alembic upgrade head
uvicorn main:app --host 0.0.0.0 --reload --port 8000
