import uuid

from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        schema_extra = {
            "example": {
                "title": "Smartphone",
                "description": "A brand new smartphone with a 6-inch display.",
                "price": 499.99,
            }
        }


class ProductResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True
