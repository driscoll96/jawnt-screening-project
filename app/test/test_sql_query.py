import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.db import Base, get_db

# Setup in-memory SQLite DB for testing
engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
Base.metadata.create_all(engine)

@pytest.fixture(scope="module")
def db_session():
    with Session(engine) as session:
        # Insert test data
        session.execute(text("""
            INSERT INTO organization_employee_account_debit_card_transaction (debit_card_id, external_payment_id, merchant_name, amount_cents)
            VALUES 
            (1, 101, 'SEPTA', 500),
            (1, 102, 'MARTA', 500),
            (1, 103, 'MARTA', 1000),
            (1, 104, 'SEPTA', 250);
        """))
        session.commit()
        yield session

def test_aggregate_debit_card_transactions(db_session):
    result = db_session.execute(text("""
        SELECT
            merchant_name,
            SUM(amount_cents) / 100.0 AS total_amount_usd
        FROM
            organization_employee_account_debit_card_transaction
        GROUP BY
            merchant_name
        ORDER BY
            total_amount_usd DESC;
    """)).fetchall()

    assert result == [
        ('MARTA', 15.0),
        ('SEPTA', 7.5)
    ]