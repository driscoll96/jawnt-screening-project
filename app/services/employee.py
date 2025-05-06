import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..lib.jawnt import queue
from ..lib.jawnt.client import perform_ach_debit, perform_swipe
from ..models.employee import (
    OrganizationEmployee,
    OrganizationEmployeeAccount,
    OrganizationEmployeeAccountDebitCard,
    OrganizationEmployeeAccountPayment,
    OrganizationEmployeeAccountDebitCardTransaction
)
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, ACHDebit, Swipe
from ..lib.jawnt.queue import message_queue

def create_employee_with_assets(db: Session, payload: EmployeeCreate):
    employee = OrganizationEmployee(
        organization_id=payload.organization_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)

    account = OrganizationEmployeeAccount(
        organization_id=payload.organization_id,
        account_id=str(uuid.uuid4()),
        balance_cents=0
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    card = OrganizationEmployeeAccountDebitCard(
        organization_id=payload.organization_id,
        debit_card_id=str(uuid.uuid4())
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    return {
        "employee_id": employee.id,
        "account_id": account.account_id,
        "debit_card_id": card.debit_card_id
    }

def update_employee(db: Session, employee_id: int, payload: EmployeeUpdate):
    employee = db.get(OrganizationEmployee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.first_name = payload.first_name
    employee.last_name = payload.last_name
    db.commit()
    return {"status": "updated"}

def delete_employee(db: Session, employee_id: int):
    employee = db.get(OrganizationEmployee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"status": "deleted"}

def create_ach_debit_payment(db: Session, payload: ACHDebit):
    response = perform_ach_debit(
        internal_account_id=payload.internal_account_id,
        external_account_id=payload.external_account_id,
        amount=payload.amount_cents,
        idempotency_key=str(uuid.uuid4())
    )

    payment = OrganizationEmployeeAccountPayment(
        type="ACH_DEBIT",
        external_account_id=payload.external_account_id,
        internal_account_id=payload.internal_account_id,
        external_payment_id=str(response.payment_id),
        amount_cents=payload.amount_cents
    )
    db.add(payment)
    db.commit()

    message_queue.publish({
        "type": "ACH_DEBIT",
        "payment_id": str(response.payment_id),
        "amount": payload.amount_cents
    })

    return {"payment_id": str(response.payment_id), "status": response.status.value}

def swipe_debit_card(db: Session, payload: Swipe):
    card = db.query(OrganizationEmployeeAccountDebitCard).filter_by(debit_card_id=payload.debit_card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    response = perform_swipe(
        debit_card_id=payload.debit_card_id,
        amount=payload.amount_cents,
        idempotency_key=str(uuid.uuid4())
    )

    transaction = OrganizationEmployeeAccountDebitCardTransaction(
        debit_card_id=card.id,
        external_payment_id=str(response.payment_id),
        merchant_name="Test Merchant",  # Placeholder
        amount_cents=payload.amount_cents
    )
    db.add(transaction)
    db.commit()

    message_queue.publish({
        "type": "SWIPE",
        "transaction_id": str(response.payment_id),
        "amount": payload.amount_cents
    })

    return {"transaction_id": str(response.payment_id), "status": response.status.value}
