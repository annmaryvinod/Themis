import os

from fastapi import FastAPI

from app.config.settings import settings
from app.routers import embedding
from app.routers.retriever import retriever_router

# Set the environment variable
os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.HUGGINGFACEHUB_API_TOKEN


app = FastAPI(
    title="themis-api-service",
    description="LLM API service for themis",
    version="1.0.0",
)

app.include_router(embedding.router)
app.include_router(retriever_router, prefix="/api/retriever")

@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
