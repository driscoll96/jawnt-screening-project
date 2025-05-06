import uuid
from app.db import SessionLocal, init_db
from app.models.employee import (
    Organization,
    OrganizationAdministrator,
    OrganizationEmployee,
    OrganizationEmployeeAccount,
    OrganizationEmployeeAccountDebitCard,
    OrganizationEmployeeAccountPayment,
    OrganizationEmployeeAccountDebitCardTransaction,
)

# Initialize tables
init_db()
db = SessionLocal()

# Create organization
org = Organization(uid=str(uuid.uuid4()), name="TestOrg")
db.add(org)
db.commit()
db.refresh(org)

# Create admin
admin = OrganizationAdministrator(organization_id=org.id)
db.add(admin)
db.commit()

# Define test employees
employees_data = [
    {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "merchant": "SEPTA"
    },
    {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@example.com",
        "merchant": "MARTA"
    }
]

for emp in employees_data:
    # Create employee
    employee = OrganizationEmployee(
        organization_id=org.id,
        first_name=emp["first_name"],
        last_name=emp["last_name"],
        email=emp["email"]
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)

    # Create account
    account = OrganizationEmployeeAccount(
        organization_id=org.id,
        account_id=str(uuid.uuid4()),
        balance_cents=10000
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    # Create debit card
    card = OrganizationEmployeeAccountDebitCard(
        organization_id=org.id,
        debit_card_id=str(uuid.uuid4())
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    # Add ACH payment
    payment = OrganizationEmployeeAccountPayment(
        type="ACH_DEBIT",
        external_account_id=999,
        internal_account_id=account.id,
        external_payment_id=str(uuid.uuid4()),
        amount_cents=5000
    )
    db.add(payment)

    # Add swipe transactions
    for amount in [2500, 1500]:
        txn = OrganizationEmployeeAccountDebitCardTransaction(
            debit_card_id=card.id,
            external_payment_id=str(uuid.uuid4()),
            merchant_name=emp["merchant"],
            amount_cents=amount
        )
        db.add(txn)

db.commit()
db.close()

print("✅ Seeded multiple employees, accounts, payments, and transactions!")