import asyncio
from typing import Optional

from app.schemas.item import ItemRead


class ItemService:
    async def get_item(self, item_id: int) -> Optional[ItemRead]:
        await asyncio.sleep(0.1)
        return ItemRead(id=item_id, name="hello world")


async def get_item_service() -> ItemService:
    return ItemService()
