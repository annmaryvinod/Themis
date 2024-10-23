from fastapi import FastAPI

from app.routers import item

app = FastAPI(
    title="LLM Project 1 API",
    description="An API for managing items.",
    version="1.0.0",
)

app.include_router(item.router)


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
