import logging

from psycopg2.pool import SimpleConnectionPool

from app.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    connection_pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=settings.DATABASE_URL,
    )
    logger.info("Database connection pool created successfully.")
except Exception as e:
    logger.error(f"Error creating database connection pool: {e}")


def get_connection():
    try:
        return connection_pool.getconn()
    except Exception as e:
        logger.error(f"Error getting connection from pool: {e}")
        raise


def put_connection(conn):
    try:
        connection_pool.putconn(conn)
    except Exception as e:
        logger.error(f"Error returning connection to pool: {e}")
        raise
