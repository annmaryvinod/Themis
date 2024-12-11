from pydantic import BaseModel
from typing import List, Dict


class QueryRequest(BaseModel):
   
    query: str
    user_id: str


class QueryHistoryRequest(BaseModel):
   
    query: str
    history: List[Dict[str, str]]
    user_id: str


class RetrievedDocument(BaseModel):
    
    document_id: str
    chunk: str
    similarity_score: float


class RetrieveResponse(BaseModel):
   
    results: List[RetrievedDocument]


class ErrorResponse(BaseModel):
   
    detail: str
