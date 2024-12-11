import logging
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.webscraper import WebScraperRequestBody, WebScraperSuccessResponse, WebScraperErrorResponse
from app.services.webscraper import WebScraperService, get_webscraper_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/webscraper",
    tags=["Webscraper"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/", response_model=WebScraperSuccessResponse)
def scrape_document(
    request: WebScraperRequestBody,
    service: WebScraperService = Depends(get_webscraper_service),
):
    try:
        document_id = service.scrape_and_store_content(request.document_url, request.title)
        return WebScraperSuccessResponse(
            status="Success",
            message="Document content successfully scraped and stored.",
            document_id=document_id,
        )
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"An error occurred while scraping the document: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=WebScraperErrorResponse(
                status="Error",
                message="Failed to scrape the document.",
                reason=str(e),
                error_code="SCRAPING_ERROR",
            ).model_dump(),
        )

@router.get("/{document_id}", response_model=WebScraperSuccessResponse)
def get_scraped_document(
    document_id: str,
    service: WebScraperService = Depends(get_webscraper_service),
):

    try:
        content_data = service.retrieve_scraped_content(document_id)

        return WebScraperSuccessResponse(
            status="Success",
            message="Document content successfully retrieved.",
            document_content=content_data,
        )
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"An error occurred while retrieving the document: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=WebScraperErrorResponse(
                status="Error",
                message="Failed to retrieve the document content.",
                reason=str(e),
                error_code="RETRIEVAL_ERROR",
            ).model_dump(),
        )
