from typing import List

from app.store.database import get_connection, put_connection


class Embedding:
    def __init__(self, document_id: str, text: str, embedding: List[float]):
        self.document_id = document_id
        self.text = text
        self.embedding = embedding

    @staticmethod
    def store_embeddings(
        document_id: str, text_chunks: List[str], embeddings: List[List[float]]
    ):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                for chunk, embedding in zip(text_chunks, embeddings):
                    cur.execute(
                        """
                        INSERT INTO embeddings (document_id, chunk, embedding)
                        VALUES (%s, %s, %s)
                        """,
                        (document_id, chunk, embedding),
                    )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            put_connection(conn)
