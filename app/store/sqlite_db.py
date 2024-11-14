import logging
import psycopg2
from psycopg2.extensions import connection as Connection, cursor as Cursor
from app.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_sql_db() -> Connection:
    """Initialize the SQL database connection and cursor.

    Returns:
        DbDict: A dictionary containing the database connection and cursor.

    Raises:
        psycopg2.DatabaseError: If there is an issue connecting to the database.
    """
    logger.info("Initializing SQL database...")

    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DATABASE_URL,
    )

    return conn


try:
    conn = init_sql_db()
    logger.info("SQL database initialized successfully.")
except psycopg2.DatabaseError as e:
    logger.error(f"Failed to initialize SQL database: {e}")
    # Handle the exception as needed, possibly re-raise or exit the program
