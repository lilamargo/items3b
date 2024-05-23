import re
import uuid
from pydantic import BaseModel, constr, validator

class ProductCreate(BaseModel):
    sku: constr(strip_whitespace=True) # type: ignore
    name: constr(strip_whitespace=True) # type: ignore
    
    @validator('sku')
    def validate_sku(cls, v):
        if not re.match(r'^\d{4}-\d{3}-\d{4}$', v):
            raise ValueError('SKU debe estar en el formato ####-###-####')
        return v
    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z0-9\s]+$', v):
            raise ValueError('El nombre no debe contener caracteres especiales')
        return v
    
class ProductResponse(BaseModel):
    id: uuid.UUID
    sku: str
    name: str

    class Config:
        orm_mode = True

class InventoryUpdate(BaseModel):
    stock: int
    
class InventoryResponse(BaseModel):
    id: str
    product_id: str
    stock: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int
