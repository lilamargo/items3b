from fastapi import HTTPException
from uuid import uuid4
from fastapi import APIRouter, Depends, Query
from items_3b.app.services.products_services import ProductServices
from sqlalchemy.orm import Session
from items_3b.app.models.models import Product, engine, get_db
from items_3b.app.schemas.products_schema import ProductCreate, ProductResponse

router = APIRouter()



@router.post("/products", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create product endpoint.

    Args:
        product (ProductCreate): Schema
        db (Session, optional):  Defaults to Depends(get_db).

    Returns:
        [JSON]: ProductResponse schema.
    """
    try:
        product_services = ProductServices(db)
        return product_services.create_product(product)
    except:
        raise HTTPException(status_code=400, detail=f"Hubo un error al crear un producto.")

@router.get(
    "/products",
    name="get-products",
    response_model=list[ProductResponse],
    responses={404: {"description": "producto no encontrado"}},
)
def get_products(
    db: Session = Depends(get_db),
    id: str = Query(None),
    name: str = Query(None),
    sku: str = Query(None),
    skip: int = 0,
    limit: int = 10,
):
    """Get products endpoint.

    Args:
        db (Session, optional): Defaults to Depends(get_db).
        id (str, optional): Defaults to Query(None).
        name (str, optional): Defaults to Query(None).
        sku (str, optional): Defaults to Query(None).
        skip (int, optional): Defaults to 0.
        limit (int, optional): Defaults to 10.

    Raises:
        HTTPException: product not found.

    Returns:
        [JSON]: dict
    """
    try:
        product_services = ProductServices(db)
        return product_services.get_products(id, name, sku, skip, limit)
    except:
        raise HTTPException(status_code=400, detail=f"Hubo un error al obtener un producto.")