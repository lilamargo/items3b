import uuid
from pydantic import BaseModel


class OrderCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int
