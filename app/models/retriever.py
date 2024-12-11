from sqlalchemy import create_engine, text
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import numpy as np
import os
import uuid
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


class RetrieverModel:
    def __init__(self):
        model_name = "EleutherAI/gpt-neo-1.3B"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def get_embedding(self, text: str):
        
        try:
            tokens = self.tokenizer(
                text, return_tensors="pt", padding=True, truncation=True
            )
            with torch.no_grad():
                outputs = self.model(**tokens)
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            logger.info(f"Generated embedding for text: {text}")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def query_database(self, query_embedding, top_k=5):
       
        try:
            query = """
            SELECT document_id, chunk, 1 - (embedding <=> :query_embedding) AS similarity
            FROM embeddings
            ORDER BY similarity DESC
            LIMIT :top_k
            """
            with engine.connect() as conn:
                results = conn.execute(
                    text(query),
                    {"query_embedding": query_embedding.tolist(), "top_k": top_k},
                )
                return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error querying database: {e}")
            raise

    def store_query_history(self, user_id: str, query: str, embedding: list):
        
        try:
            query_history_query = """
            INSERT INTO query_history (user_id, query, embedding)
            VALUES (:user_id, :query, :embedding)
            """
            with engine.connect() as conn:
                conn.execute(
                    text(query_history_query),
                    {"user_id": user_id, "query": query, "embedding": embedding.tolist()},
                )
            logger.info(f"Stored query in history for user: {user_id}")
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
