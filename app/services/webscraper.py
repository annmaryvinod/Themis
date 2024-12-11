import uuid
from typing import Dict
import logging

from app.models.webscraper import WebScrapedContent
from app.utils.web_scraper import scrape_web_content

logger = logging.getLogger(__name__)

class WebScraperService:
    def scrape_and_store_content(self, url: str, title: str) -> str:
        if not url:
            raise ValueError("No URL provided.")
        
        logger.info(f"Scraping content from URL: {url}")
        scraped_content = scrape_web_content(url)
        
        if not scraped_content:
            raise ValueError(f"No content found at the provided URL: {url}")
        
        document_id = str(uuid.uuid4())

        WebScrapedContent.store_scraped_content(
            document_id=document_id,
            title=title,
            url=url,
            content=scraped_content["content"],
            metadata=scraped_content.get("metadata", {}),
        )

        logger.info(f"Content successfully stored with document ID: {document_id}")
        return document_id

    def retrieve_scraped_content(self, document_id: str) -> Dict[str, str]:
        logger.info(f"Retrieving content for document ID: {document_id}")
        content_data = WebScrapedContent.get_scraped_content(document_id)
        
        if not content_data:
            raise ValueError(f"No content found for document ID: {document_id}")
        
        logger.info(f"Content successfully retrieved for document ID: {document_id}")
        return content_data


async def get_webscraper_service() -> WebScraperService:
    return WebScraperService()
