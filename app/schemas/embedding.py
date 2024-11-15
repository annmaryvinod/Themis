from typing import Optional

from pydantic import BaseModel, model_validator


class EmbeddingRequestBody(BaseModel):
    title: str
    content_url: Optional[str] = None
    text_content: Optional[str] = None

    @model_validator(mode="after")
    def check_content(self):
        if not self.content_url and not self.text_content:
            raise ValueError("Either content_url or text_content must be provided.")
        return self


class EmbeddingSuccessResponse(BaseModel):
    status: str
    message: str
    document_id: str
