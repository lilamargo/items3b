from typing import List
from uuid import  uuid4
import logging
from items_3b.app.models.models import Inventory, Product
from items_3b.app.schemas.inventories_schema import InventoryResponse, InventoryUpdate
from items_3b.app.schemas.orders_schema import OrderCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException


log = logging.getLogger(__name__)

class InventoryServices:
    """Inventory class services."""
    def __init__(self, db: Session):
        self.db = db

    def update_inventory(self, product_id: str, inventory_update: InventoryUpdate):
        """Update inventory service.

        Args:
            product_id (str): [description]
            inventory_update (InventoryUpdate): [description]

        Raises:
            HTTPException: Error al crear un inventario.

        Returns:
            [JSON]: InventoryResponse schema
        """
        try:
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product_id).first()
            if not inventory:
                inventory = Inventory(product_id=product_id, stock=100)
                self.db.add(inventory)
            inventory.stock += inventory_update.stock
            self.db.commit()
            self.db.refresh(inventory)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Hubo un error al actualizar el inventario: {e}")
        return InventoryResponse(id=str(inventory.id), product_id=inventory.product_id, stock=inventory.stock)

    def get_inventories(self, id: str = None, product_id: str = None, skip: int = 0, limit: int = 10) -> List[InventoryResponse]:
        """Get inventories service.

        Args:
            id (str, optional): Defaults to None.
            product_id (str, optional): Defaults to None.
            skip (int, optional): Defaults to 0.
            limit (int, optional): Defaults to 10.

        Returns:
            List[InventoryResponse]
        """
        query = self.db.query(Inventory)

        if id:
            query = query.filter(Inventory.id == id)
        if product_id:
            query = query.filter(Inventory.product_id == product_id)


        inventories = query.offset(skip).limit(limit).all()
        return [InventoryResponse(id=str(product.id), product_id=product.product_id, stock=product.stock) for product in inventories]
    
    def create_order(self, order: OrderCreate):
        """Create order service.

        Args:
            order (OrderCreate): schema

        Returns:
            [JSON]: OrderResponse schema
        """
        inventory = self.db.query(Inventory).filter(Inventory.product_id == str(order.product_id)).first()
        if not inventory:
            raise HTTPException(status_code=400, detail="Producto no encontrado en el inventario")
        if inventory.stock <= 10:
            log.warning(f"⚠️   WARNING: Quedan {inventory.stock} unidades en el inventario. ⚠️ ")
        if inventory.stock < order.quantity:
            raise HTTPException(status_code=400, detail="No hay suficiente stock")
        inventory.stock -= order.quantity
        self.db.commit()
        return order

