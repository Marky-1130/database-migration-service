# create alembic folder if it doesn't exist
mkdir -p alembic/versions

echo "Running Alembic migrations..."
python3 -m alembic revision --autogenerate -m "migration_init"
python3 -m alembic upgrade head
rm -rf alembic/versions/*