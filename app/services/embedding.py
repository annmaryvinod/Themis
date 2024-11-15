import uuid
from typing import List

from langchain_huggingface import HuggingFaceEmbeddings

from app.models.embedding import Embedding
from app.utils.pdf_extractor import extract_text_from_pdf
from app.utils.text_splitter import split_text_into_chunks


class EmbeddingService:
    def create_pdf_embeddings(self, pdf_url: str) -> str:
        if pdf_url:
            text_content = extract_text_from_pdf(pdf_url)
        if not text_content:
            raise ValueError("No text content provided.")

        text_chunks = split_text_into_chunks(text_content)
        embeddings = self._generate_embeddings(text_chunks)

        embedding_id = str(uuid.uuid4())
        Embedding.store_embeddings(embedding_id, text_chunks, embeddings)

        return embedding_id

    def _generate_embeddings(self, text_chunks: List[str]) -> List[List[float]]:
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        embeddings = embedding_model.embed_documents(text_chunks)
        return embeddings


async def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
