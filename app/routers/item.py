from fastapi import APIRouter, Depends, HTTPException

from app.schemas.item import ItemRead
from app.services.item import ItemService, get_item_service

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/{item_id}", response_model=ItemRead)
async def read_item(
    item_id: int, service: ItemService = Depends(get_item_service)
) -> ItemRead:
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
