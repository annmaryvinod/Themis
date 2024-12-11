from psycopg2.extras import Json
from app.store.database import get_connection, put_connection
import logging

logger = logging.getLogger(__name__)

class WebScrapedContent:
    @staticmethod
    def store_scraped_content(document_id: str, title: str, url: str, content: str, metadata: dict):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO webscraper_contents (document_id, title, url, content, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (document_id, title, url, content, Json(metadata))
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Error storing scraped content: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                put_connection(conn)

    @staticmethod
    def get_scraped_content(document_id: str):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT title, url, content, metadata
                    FROM webscraper_contents
                    WHERE document_id = %s
                    """,
                    (document_id,)
                )
                result = cursor.fetchone()
                if result:
                    return {
                        "title": result[0],
                        "url": result[1],
                        "content": result[2],
                        "metadata": result[3]
                    }
                return None
        except Exception as e:
            logger.error(f"Error retrieving scraped content: {e}")
            raise
        finally:
            if conn:
                put_connection(conn)

