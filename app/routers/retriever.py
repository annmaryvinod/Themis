from fastapi import APIRouter, HTTPException, Request, Depends
from app.schemas.retriever import QueryRequest, QueryHistoryRequest
from app.services.retriever import RetrieverService

retriever_router = APIRouter()

@retriever_router.post("/retrieve", tags=["Retriever"])
async def retrieve(request: QueryRequest):
   
    retriever_service = RetrieverService()
    results = retriever_service.retrieve(query=request.query, user_id=request.user_id)
    return {"results": results}

@retriever_router.post("/retrieve_with_history", tags=["Retriever"])
async def retrieve_with_history(request: QueryHistoryRequest):
    
    retriever_service = RetrieverService()
    results = retriever_service.retrieve_with_history(
        query=request.query, history=request.history, user_id=request.user_id
    )
    return {"results": results}
