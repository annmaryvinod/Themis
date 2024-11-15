import logging

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.embedding import EmbeddingRequestBody, EmbeddingSuccessResponse
from app.services.embedding import EmbeddingService, get_embedding_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/embedding",
    tags=["Embedding"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=EmbeddingSuccessResponse)
def create_embeddings(
    request: EmbeddingRequestBody,
    service: EmbeddingService = Depends(get_embedding_service),
):
    try:
        document_id = service.create_pdf_embeddings(pdf_url=request.content_url)
        # TODO: Add support for text content
        return EmbeddingSuccessResponse(
            status="Success",
            message="Content successfully processed and embedding stored.",
            document_id=document_id,
        )
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"An error occurred while creating embeddings: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
