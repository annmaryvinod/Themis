import os
from typing import Union
import uuid
from fastapi import HTTPException
from app.config.settings import settings
from app.schemas.embedding import EmbeddingErrorResponse, EmbeddingSuccessResponse

from app.utils.pdf_extractor import extractTextFromPDF
from app.utils.text_splitter import splitTextIntoChunks

from app.store.sqlite_db import conn

from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    def create_pdf_embedding(
        self, text_content: str, pdf_url: str
    ) ->  Union[EmbeddingSuccessResponse, EmbeddingErrorResponse]:
        if pdf_url:
            text_content = extractTextFromPDF(pdf_url)
        else:
            text_content = text_content

        text_chunks = splitTextIntoChunks(text_content)
        embeddings = self.__generateEmbeddings(text_chunks)

        try:
            embedding_id = str(uuid.uuid4())
            stored_id = self.__storeEmbeddingsInDB(embedding_id, text_chunks, embeddings)
            success_response = EmbeddingSuccessResponse(
                status="Success",
                message="Content successfully processed and embedding stored.",
                embedding_id=stored_id,
            )

            return success_response

        except Exception as e:
            error_response = EmbeddingErrorResponse(
                status="Error",
                message="Embedding Failed",
                reason=str(e),
                error_code="500_INTERNAL_ERROR",
            )

            raise HTTPException(status_code=500, detail=error_response.dict())

    def __generateEmbeddings(self, text_chunks):
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.HUGGINGFACEHUB_API_TOKEN

        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        embeddings = embedding_model.embed_documents(text_chunks)
        return embeddings

    def __storeEmbeddingsInDB(self, document_id, text_chunks, embeddings):
        cur = conn.cursor()

        for text, embedding in zip(text_chunks, embeddings):
            cur.execute(
                """
                INSERT INTO embeddings (document_id,text, embedding)
                VALUES (%s, %s,%s)
            """,
                (document_id, text, embedding),
            )
        conn.commit()
        print("Embeddings stored in PostgreSQL successfully.")

        return document_id


async def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()