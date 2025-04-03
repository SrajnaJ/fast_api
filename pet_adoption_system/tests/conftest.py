import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

# Replace with your MySQL test database credentials
TEST_DATABASE_URL = "mysql+pymysql://root:Abcd%401234@localhost/pet_adoption_db"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override function
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply dependency override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_db():
    """Fixture to set up and tear down the test database"""
    Base.metadata.create_all(bind=engine)  # Create tables
    yield  # Run the tests
    Base.metadata.drop_all(bind=engine)  # Clean up after tests

@pytest.fixture(scope="module")
def client():
    """Test client for FastAPI"""
    return TestClient(app)

@pytest.fixture
def admin_token(client):
    """Fixture to get an admin authentication token"""
    response = client.post("/auth/login", data={"username": "admin@example.com", "password": "adminpass"})
    assert response.status_code == 200, f"Login failed: {response.json()}"
    return response.json().get("access_token")
