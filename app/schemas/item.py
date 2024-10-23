from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="An item name")


class ItemRead(ItemBase):
    id: int
    name: str

    class Config:
        from_attributes = True
