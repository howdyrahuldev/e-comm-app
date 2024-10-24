import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the src directory to the system path
# sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
from e_comm_app.app.config import get_db
from e_comm_app.app.main import app
from e_comm_app.app.orm.e_comm_orm import Base, Product

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_products.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Dependency override for using test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestProductAPI(unittest.TestCase):

    def setUp(self):
        """Set up the test database before each test"""
        Base.metadata.create_all(bind=engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        """Tear down the test database after each test"""
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    # Test GET /products (List all products)
    def test_get_products(self):
        response = client.get("/v1/products")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    # Test GET /products/{id} (Get product by ID)
    def test_get_product_by_id(self):
        # Add a product to the database
        new_product = Product(
            title="Test Product", description="Test Description", price=100
        )
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)

        response = client.get(f"/v1/products/{new_product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Test Product")

    # Test POST /products (Create a new product)
    def test_create_product(self):
        product_data = {
            "title": "New Product",
            "description": "New Product Description",
            "price": 50,
        }
        response = client.post("/v1/products", json=product_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "New Product")

    # Test PUT /products/{id} (Update a product)
    def test_update_product(self):
        # Add a product to the database
        new_product = Product(
            title="Old Product", description="Old Description", price=50
        )
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)

        updated_data = {
            "title": "Updated Product",
            "description": "Updated Description",
            "price": 75,
        }
        response = client.put(f"/v1/products/{new_product.id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Product")

    # Test DELETE /products/{id} (Delete a product)
    def test_delete_product(self):
        # Add a product to the database
        new_product = Product(
            title="Delete Product", description="Delete Description", price=30
        )
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)

        response = client.delete(f"v1/products/{new_product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Product deleted successfully")
