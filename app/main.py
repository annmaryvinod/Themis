from fastapi import FastAPI

from app.routers import embedding, item

app = FastAPI(
    title="LLM Project 1 API",
    description="An API for managing items.",
    version="1.0.0",
)

app.include_router(item.router)
app.include_router(embedding.router)


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
