import os
from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool
from alembic import context

from app.models.user import User
from app.models.chat_message import ChatMessage
from app.database import Base  # Import your SQLAlchemy Base

# Load environment variables
load_dotenv()

# Alembic configuration
config = context.config

# Read and apply logging configuration from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set in .env or is incorrectly configured!")

# Set SQLAlchemy URL in Alembic config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Add your model's MetaData object for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable here as well.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario, we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Determine if the script is running in offline mode or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
