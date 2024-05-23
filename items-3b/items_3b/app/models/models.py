import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
import random
import string

Base = declarative_base()
engine = create_engine("sqlite:///./test.db", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Product(Base):
    """Product Model.

    Args:
        id ([uuid]): ID
        sku ([string]): sku with format "####-###-####"
        name ([string]): product name
    """
    __tablename__ = "products"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sku = Column(String, unique=True)
    name = Column(String, unique=True)
    
    inventories = relationship("Inventory", back_populates="product")

class Inventory(Base):
    """Inventory Model.

    Args:
        id ([uuid]): ID
        product_id ([uuid]): Product ID
        stock ([integer]): product stock, default 100.
    """
    __tablename__ = "inventories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, ForeignKey("products.id"))
    stock = Column(Integer, default=100)
    
    product = relationship("Product", back_populates="inventories")
    