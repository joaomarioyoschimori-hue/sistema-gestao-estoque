from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    code: str = Field(min_length=1)
    description: str = ""
    purchase_price: float = Field(ge=0)
    sale_price: float = Field(ge=0)
    quantity: int = Field(ge=0)