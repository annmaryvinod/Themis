import logging
import os
import sys
from typing import List, Optional

import psycopg2

from app.config.settings import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        conn = psycopg2.connect(dsn=settings.DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise


def run_migration(conn, file_path: str, direction: str) -> None:
    try:
        with conn.cursor() as cursor:
            with open(file_path, "r") as f:
                content = f.read()

            if direction == "up":
                sql_section = content.split("-- +migrate Up")[1].split(
                    "-- +migrate Down"
                )[0]
            elif direction == "down":
                sql_section = content.split("-- +migrate Down")[1]
            else:
                raise ValueError("Direction must be 'up' or 'down'")

            statements = [
                stmt.strip() for stmt in sql_section.strip().split(";") if stmt.strip()
            ]
            for statement in statements:
                cursor.execute(statement)

            conn.commit()
            logger.info(
                f"Successfully executed migration: {os.path.basename(file_path)}"
            )
    except (IOError, IndexError) as e:
        conn.rollback()
        logger.error(f"Error reading or parsing migration file {file_path}: {e}")
        raise
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Database error while executing migration {file_path}: {e}")
        raise


def find_migrations_dir(custom_path: Optional[str] = None) -> str:
    if custom_path and os.path.isdir(custom_path):
        return custom_path

    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    location = os.path.join(app_dir, "migrations")

    if os.path.isdir(location):
        return location

    raise FileNotFoundError(
        """Could not find 'migrations' directory.
        Please specify the path using the --migrations-dir argument."""
    )


def get_migration_files(migrations_dir: str, direction: str) -> List[str]:
    migration_files = sorted(
        [f for f in os.listdir(migrations_dir) if f.endswith(".sql")]
    )
    if direction == "down":
        migration_files.reverse()
    return migration_files


def migrate(direction: str, migrations_dir: Optional[str] = None) -> None:
    try:
        conn = get_db_connection()

        migrations_dir = find_migrations_dir(migrations_dir)
        logger.info(f"Using migrations directory: {migrations_dir}")

        migration_files = get_migration_files(migrations_dir, direction)

        for file in migration_files:
            logger.info(f"Running migration: {file}")
            run_migration(conn, os.path.join(migrations_dir, file), direction)

        logger.info(f"Successfully completed all {direction} migrations.")
    except (FileNotFoundError, ValueError, psycopg2.Error) as e:
        logger.error(f"Migration failed: {e}")
        raise
    finally:
        if "conn" in locals():
            conn.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run database migrations")
    parser.add_argument("direction", choices=["up", "down"], help="Migration direction")
    parser.add_argument("--migrations-dir", help="Path to migrations directory")
    args = parser.parse_args()

    try:
        migrate(args.direction, args.migrations_dir)
    except Exception as e:
        logger.error(f"An error occurred during migration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
