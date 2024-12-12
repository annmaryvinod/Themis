import uuid
from typing import Dict, List
import logging
from app.models.webscraper import WebScrapedContent
from app.schemas.webscraper import WebScraperSuccessResponse
from app.utils.web_scraper import scrape_web_content

logger = logging.getLogger(__name__)

# Function to sanitize strings by removing invalid characters like null bytes
def sanitize_string(input_string: str) -> str:
    return input_string.replace('\x00', '').strip()

class WebScraperService:
    def scrape_and_store_content(self, url: str, title: str) -> WebScraperSuccessResponse:
        if not url:
            raise ValueError("No URL provided.")
        
        logger.info(f"Scraping content from URL: {url}")
        scraped_content = scrape_web_content(url)
        
        if not scraped_content or "content" not in scraped_content:
            raise ValueError(f"No content found at the provided URL: {url}")

        document_id = str(uuid.uuid4())

        sanitized_url = sanitize_string(url)
        sanitized_title = sanitize_string(title)
        sanitized_content = sanitize_string(scraped_content["content"])
        
        metadata = scraped_content.get("metadata", {})
        metadata_list = [metadata] if isinstance(metadata, dict) else (metadata if isinstance(metadata, list) else [])

        WebScrapedContent.store_scraped_content(
            document_id=document_id,
            title=sanitized_title,
            url=sanitized_url,
            content=sanitized_content,
            metadata=metadata_list,
        )

        logger.info(f"Content successfully stored with document ID: {document_id}")
        
        return WebScraperSuccessResponse(
            status="Success",
            message="Content successfully scraped and stored.",
            document_content=sanitized_content,  # Ensure this field is populated
            extracted_metadata=metadata_list,  # Include metadata if needed
        )


async def get_webscraper_service() -> WebScraperService:
    return WebScraperService()