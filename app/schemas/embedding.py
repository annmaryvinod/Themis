from typing import Optional
from pydantic import BaseModel


class EmbeddingRequestBody(BaseModel):
    title: str
    content_url : Optional[str] = None
    text_content : Optional[str] = None

class EmbeddingErrorResponse(BaseModel):
    status : str
    message : str
    reason : str
    error_code : str

class EmbeddingSuccessResponse(BaseModel):
    status : str
    message : str
    embedding_id : str