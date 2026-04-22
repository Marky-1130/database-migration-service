from logging.config import fileConfig

from typing import Any
from sqlalchemy import engine_from_config, create_engine, text
from sqlalchemy import pool
from sqlalchemy.exc import SQLAlchemyError

from alembic import context
from config import settings
from db_models import Base

def create_db_if_not_exists():

    db_name = settings.DB_NAME
    db_base_url = settings.create_db_base_url()
    db_url = settings.create_db_url()

    print("Database Settings Values")
    print("---------------------------------------")
    print(f"Database Name: {db_name}")
    print(f"Base DB URL: {db_base_url}")
    print(f"DB URL: {db_url}")
    print("---------------------------------------")

    conn = None

    try:
        base_engine = create_engine(db_base_url)

        with base_engine.connect() as conn:
            if settings.RESET_DB:
                conn.execute(text(f"DROP DATABASE IF EXISTS `{db_name}`;"))

            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;"))

        db_engine = create_engine(db_url)
        with db_engine.connect() as conn:
            #TODO: Update how to handle versions
            conn.execute(text("TRUNCATE TABLE alembic_version;"))

    except SQLAlchemyError as exc:
        print(f"An error occurred: {exc}")
        raise exc
    
    finally: 
        if base_engine:
            base_engine.dispose()
        if db_engine:
            db_engine.dispose()

#Call the function for database creation/setup
create_db_if_not_exists()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
# Set the SQLAlchemy URL for Alembic configurations
config.set_main_option("sqlalchemy.url", settings.create_db_url())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
