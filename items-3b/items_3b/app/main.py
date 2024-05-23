from fastapi import FastAPI
from items_3b.app.routers import inventories_router, products_router
from items_3b.app.models.models import Base, engine
from ..settings.config import init_db

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(products_router.router, prefix="/api", tags=["Products"])
app.include_router(inventories_router.router, prefix="/api", tags=["Inventories"])

