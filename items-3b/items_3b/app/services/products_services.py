
from fastapi import HTTPException
from uuid import uuid4
from items_3b.app.models.models import Product
from items_3b.app.schemas.products_schema import ProductCreate, ProductResponse
from sqlalchemy.orm import Session
from typing import List

class ProductServices:
    """Product service class."""
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate):
        """Create product service.

        Args:
            product (ProductCreate): schema

        Returns:
            [JSON]: ProductResponse schema
        """
        try:
            
            db_product = Product(sku=product.sku, name=product.name)
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Hubo un error al crear un producto. {e}")
        return db_product
    
    def get_products(self, id: str = None, name: str = None, sku: str = None, skip: int = 0, limit: int = 10) -> List[ProductResponse]:
        """Get products service.

        Args:
            id (str, optional): Defaults to None.
            name (str, optional): Defaults to None.
            sku (str, optional): Defaults to None.
            skip (int, optional): Defaults to 0.
            limit (int, optional): Defaults to 10.

        Returns:
            List[ProductResponse]: schema
        """
        
        query = self.db.query(Product)

        if id:
            query = query.filter(Product.id == id)
        if name:
            query = query.filter(Product.name == name)
        if sku:
            query = query.filter(Product.sku == sku)

        products = query.offset(skip).limit(limit).all()
        return [ProductResponse(id=str(product.id), sku=product.sku, name=product.name) for product in products]