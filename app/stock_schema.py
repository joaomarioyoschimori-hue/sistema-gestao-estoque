from pydantic import BaseModel, Field


class StockMovementCreate(BaseModel):
    movement_type: str
    quantity: int = Field(gt=0)