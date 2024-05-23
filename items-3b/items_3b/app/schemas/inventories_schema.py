from typing import Optional
import uuid
from pydantic import BaseModel



class InventoryUpdate(BaseModel):
    stock: int
    
class InventoryResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    product_id: str
    stock: int

    class Config:
        orm_mode = True
