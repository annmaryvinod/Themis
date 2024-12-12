from sentence_transformers import SentenceTransformer
import logging
import numpy as np
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from app.store.database import get_connection, put_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetrieverModel:
    def __init__(self):
        
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def get_embedding(self, text: str):
        try:
            
            embedding = self.model.encode(text)
            logger.info(f"Generated embedding for text: {text}")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def query_database(self, query_embedding, top_k=5):
        try:
            query = """
            SELECT document_id, chunk, 1 - (embedding <=> %s) AS similarity
            FROM embeddings
            ORDER BY similarity DESC
            LIMIT %s
            """
            conn = get_connection()
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, (query_embedding.tolist(), top_k))
                    results = cursor.fetchall()
                    return results
            finally:
                put_connection(conn)
        except Exception as e:
            logger.error(f"Error querying database: {e}")
            raise

    def store_query_history(self, user_id: str, query: str, embedding: list):
        try:
            query_history_query = """
            INSERT INTO query_history (user_id, query, embedding)
            VALUES (%s, %s, %s)
            """
            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        query_history_query, (user_id, query, embedding.tolist())
                    )
                    conn.commit()
                    logger.info(f"Stored query in history for user: {user_id}")
            finally:
                put_connection(conn)
        except Exception as e:
            logger.error(f"Error storing query history: {e}")
            raise

    def retrieve(self, query: str, user_id: str):
        embedding = self.get_embedding(query)
        self.store_query_history(user_id, query, embedding)
        return self.query_database(embedding)

    def retrieve_with_history(self, query: str, history: list, user_id: str):
        context = " ".join([entry["text"] for entry in history]) + " " + query
        embedding = self.get_embedding(context)
        self.store_query_history(user_id, query, embedding)
        return self.query_database(embedding)
