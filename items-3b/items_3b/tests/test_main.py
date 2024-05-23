import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from items_3b.app.main import app 

from items_3b.app.models.models import Base, Inventory, get_db, Product 
from items_3b.app.schemas.products_schema import ProductCreate 

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestProductEndpoints(unittest.TestCase):

    def setUp(self):
        self.db = TestingSessionLocal()

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_create_product_success(self):
        product_data = {
            "sku": "4225-776-3234",
            "name": "Test"
        }
        response = client.post("/api/products", json=product_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sku"], product_data["sku"])
        self.assertEqual(response.json()["name"], product_data["name"])

    def test_create_product_failure(self):
        product_data = {
            "sku": "FailSKU123",
            "name": "Repetido"
        }
        response = client.post("/products", json=product_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())

    def test_get_products_success(self):
        product_data = {
            "sku": "4225-776-3234",
            "name": "Test"
        }
        client.post("/api/products", json=product_data)

        response = client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_get_products_with_filters(self):
        products = [
            {"sku": "4225-111-3234", "name": "Test Product 1"},
            {"sku": "1234-776-8887", "name": "Test Product 2"}
        ]
        for product_data in products:
            client.post("/api/products", json=product_data)

        response = client.get("/api/products", params={"sku": "4225-111-3234"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["sku"], "4225-111-3234")

    def test_get_products_failure(self):
        response = client.get("/api/products", params={"sku": "non-existent"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        

class TestInventoryEndpoints(unittest.TestCase):

    def setUp(self):
        self.db = TestingSessionLocal()

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_update_inventory_success(self):
        product_id = "0277fb0d-849c-484c-a42e-3198ae228f7c"
        inventory_update_data = {"stock": 50}
        response = client.patch(f"/api/inventories/product/{product_id}", json=inventory_update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["stock"], 150)

    def test_update_inventory_failure(self):
        product_id = "non-existent"
        inventory_update_data = {"stock": 50}
        response = client.patch(f"/api/inventories/product/{product_id}", json=inventory_update_data)
        self.assertEqual(response.status_code, 200)

    def test_get_inventories_success(self):
        inventories = [
            {"product_id": "4225-111-3234", "stock": 50},
            {"product_id": "6547-123-3234", "stock": 100}
        ]
        for inventory_data in inventories:
            self.db.add(Inventory(**inventory_data))
        self.db.commit()

        response = client.get("/api/inventories")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_get_inventories_with_filters(self):
        inventories = [
            {"product_id": "4225-111-3234", "stock": 50},
            {"product_id": "1234-222-3234", "stock": 100}
        ]
        for inventory_data in inventories:
            self.db.add(Inventory(**inventory_data))
        self.db.commit()

        response = client.get("/api/inventories", params={"product_id": "4225-111-3234"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["product_id"], "4225-111-3234")

    def test_get_inventories_failure(self):
        response = client.get("/api/inventories", params={"product_id": "non-existent"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_create_order_success(self):
        inventory = Inventory(product_id="0277fb0d-849c-484c-a42e-3198ae228f7c", stock=50)
        self.db.add(inventory)
        self.db.commit()

        order_data = {"product_id": "0277fb0d-849c-484c-a42e-3198ae228f7c", "quantity": 10}
        response = client.post("/api/orders", json=order_data)
        self.assertEqual(response.status_code, 200)

    def test_create_order_insufficient_stock(self):
        inventory = Inventory(product_id="0277fb0d-1234-484c-a42e-3198ae228f7c", stock=0)
        self.db.add(inventory)
        self.db.commit()

        order_data = {"product_id": "0277fb0d-1234-484c-a42e-3198ae228f7c", "quantity": 106}
        response = client.post("/api/orders", json=order_data)
        self.assertEqual(response.status_code, 500)

if __name__ == "__main__":
    unittest.main()
