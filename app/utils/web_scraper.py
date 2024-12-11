import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict

logger = logging.getLogger(__name__)


def scrape_web_content(url: str) -> Dict[str, str]:
    try:
        logger.info(f"Attempting to scrape content from URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.get_text(strip=True)
        metadata = {
            "title": soup.title.string if soup.title else "",
            "meta_description": (
                soup.find("meta", attrs={"name": "description"})["content"]
                if soup.find("meta", attrs={"name": "description"})
                else ""
            ),
        }
        return {"content": content, "metadata": metadata}

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for URL: {url}. Error: {e}")
        raise ValueError(f"Failed to fetch content from URL: {url}") from e

    except Exception as e:
        logger.error(f"An unexpected error occurred while scraping the URL: {e}")
        raise ValueError(f"Error occurred while scraping URL: {url}") from e
