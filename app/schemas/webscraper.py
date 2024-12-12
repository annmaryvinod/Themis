from typing import Optional, List, Dict
from pydantic import BaseModel, model_validator

class WebScraperRequestBody(BaseModel):
    title: str
    document_url: str = None

    @model_validator(mode="after")
    def validate_document_url(self):
        if not self.document_url:
            raise ValueError("The document_url must be provided.")
        return self

class WebScraperSuccessResponse(BaseModel):
    status: str = "Success"
    message: str
    document_content: str  # Ensure this is defined as required
    extracted_metadata: Optional[List[Dict[str, str]]] = None


class WebScraperErrorResponse(BaseModel):
    status: str = "Error"
    message: str
    reason: Optional[str] = None
    error_code: Optional[str] = None
