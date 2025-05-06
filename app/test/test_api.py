from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import create_app
from app.db import get_db
from app.models.employee import Base, Organization
import tempfile
import os

# Use a temporary file-based SQLite DB to persist across requests
db_file = tempfile.NamedTemporaryFile(delete=False)
TEST_DATABASE_URL = f"sqlite:///{db_file.name}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency that also initializes schema + seed
def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        if not db.query(Organization).first():
            db.add(Organization(uid="test-org", name="Test Org"))
            db.commit()
        yield db
    finally:
        db.close()

# Create app and override deps
test_app = create_app()
test_app.dependency_overrides[get_db] = override_get_db
client = TestClient(test_app)

def test_create_employee():
    response = client.post("/api/employees", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "organization_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert "employee_id" in data
    assert "account_id" in data
    assert "debit_card_id" in data

def test_update_employee():
    create_resp = client.post("/api/employees", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "organization_id": 1
    })
    assert create_resp.status_code == 200
    emp_id = create_resp.json()["employee_id"]

    response = client.patch(f"/api/employees/{emp_id}", json={
        "first_name": "Janet",
        "last_name": "Dough"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "updated"

def test_ach_debit():
    create_resp = client.post("/api/employees", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "organization_id": 1
    })
    assert create_resp.status_code == 200
    account_id = 1  # Since it always starts from 1 for the test DB

    response = client.post("/api/payments/ach-debit", json={
        "internal_account_id": account_id,
        "external_account_id": 999,
        "amount_cents": 5000
    })
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"

def test_swipe_card():
    create_resp = client.post("/api/employees", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "organization_id": 1
    })
    assert create_resp.status_code == 200
    card_id = create_resp.json()["debit_card_id"]

    response = client.post("/api/transactions/swipe", json={
        "debit_card_id": card_id,
        "amount_cents": 1200
    })
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"

def test_delete_employee():
    create_resp = client.post("/api/employees", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "organization_id": 1
    })
    assert create_resp.status_code == 200
    emp_id = create_resp.json()["employee_id"]

    response = client.delete(f"/api/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

# Clean up the temporary DB file after tests
def teardown_module(module):
    os.unlink(db_file.name)