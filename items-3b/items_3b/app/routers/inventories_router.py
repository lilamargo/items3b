from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends, Query
from items_3b.app.schemas.orders_schema import OrderCreate
from items_3b.app.services.inventories_services import InventoryServices
from sqlalchemy.orm import Session
from items_3b.app.models.models import  get_db
from items_3b.app.schemas.inventories_schema import  InventoryResponse, InventoryUpdate


router = APIRouter()

@router.patch("/inventories/product/{product_id}", response_model=InventoryUpdate)
def update_inventory(product_id: str, inventory_update: InventoryUpdate, db: Session = Depends(get_db)):
    """Update inventory endpoint.

    Args:
        product_id (str): [description]
        inventory_update (InventoryUpdate): schema validator
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        [JSON]: inventory data.
    """
    try:
        inventory_services = InventoryServices(db)
        return inventory_services.update_inventory(product_id, inventory_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hubo un error al agregar stock al inventario. {e}")

@router.get(
    "/inventories",
    name="get-inventories",
    response_model=List[InventoryResponse],
    responses={404: {"description": "Inventario no encontrado"}},
)
def get_inventories(
    db: Session = Depends(get_db),
    id: str = Query(None),
    product_id: str = Query(None),
    skip: int = 0,
    limit: int = 10,
):
    """Get inventories endpoint.

    Args:
        db (Session, optional):  Defaults to Depends(get_db).
        id (str, optional):  Defaults to Query(None).
        product_id (str, optional):  Defaults to Query(None).
        skip (int, optional):  Defaults to 0.
        limit (int, optional): Defaults to 10.
    Returns:
        [JSON]: InventoryResponse schema
    """
    try:
        inventory_services = InventoryServices(db)
        return inventory_services.get_inventories(id, product_id, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hubo un error al obtener el inventario. {e}")

@router.post("/orders", response_model=OrderCreate)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create Order endpoint

    Args:
        order (OrderCreate): Schema
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        [JSON]: OrderResponse schema.
    """
    try:
        inventory_services = InventoryServices(db)
        return inventory_services.create_order(order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hubo un error al crear una orden. {e}")