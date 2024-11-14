from fastapi import APIRouter, Depends, HTTPException

from app.schemas.embedding import EmbeddingRequestBody, EmbeddingErrorResponse, EmbeddingSuccessResponse
from app.services.embedding import EmbeddingService, get_embedding_service

router = APIRouter(
    prefix="/api/v1/embedding",
    tags=["Embedding"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=EmbeddingSuccessResponse)
def createEmbeddings(
    request: EmbeddingRequestBody,
    service: EmbeddingService = Depends(get_embedding_service),
):
    if not request.text_content and not request.content_url:
        error_response = EmbeddingErrorResponse(
            status="Error",
            message="Embedding Failed.",
            reason="Either content url or text content must be provided.",
            error_code="400_BAD_REQUEST",
        )

        raise HTTPException(status_code=400, detail=error_response.dict())

    embedding = service.create_pdf_embedding(
        text_content=request.text_content, pdf_url=request.content_url
    )

    return embedding
