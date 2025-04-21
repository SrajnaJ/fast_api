import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_engine, get_db
from app.main import app

# client = TestClient(app)
@pytest.fixture(scope="session")
def test_engine():
    from app import models
    engine = get_engine(is_test=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        
@pytest.fixture
def test_client(test_engine):
    from app.database import get_db

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client

    # Clear overrides after test
    app.dependency_overrides.clear()

@pytest.fixture
def admin_credentials():
    return {"username": "admin", "password": "adminpass"}

@pytest.fixture
def create_user(test_client):
    def _create_user(username, email, password):
        response = test_client.post("/auth/signup", json={
            "username": username,
            "email": email,
            "password": password
        })
        return response
    return _create_user

@pytest.fixture
def create_admin(db_session):
    def _create_admin(username, email, password):
        from app.models import User
        from app.utils import hash_password

        existing_admin = db_session.query(User).filter(User.username == username).first()
        if existing_admin:
            db_session.delete(existing_admin)
            db_session.commit()

        hashed_password = hash_password(password)
        admin = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)
        return admin
    return _create_admin

@pytest.fixture
def get_token(test_client):
    def _get_token(username, password):
        response = test_client.post("/auth/login", data={
            "username": username,
            "password": password
        })
        assert response.status_code == 200, f"Login failed: {response.json()}"
        return response.json()["access_token"]
    return _get_token