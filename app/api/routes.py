from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.employee import OrganizationEmployeeAccountPayment, OrganizationEmployeeAccountDebitCardTransaction
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, ACHDebit, Swipe
from ..services.employee import (
    create_employee_with_assets,
    update_employee,
    delete_employee,
    create_ach_debit_payment,
    swipe_debit_card
)

router = APIRouter()

@router.post("/employees")
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee_with_assets(db, payload)

@router.patch("/employees/{employee_id}")
def update_employee_route(
        employee_id: int,
        payload: EmployeeUpdate,
        db: Session = Depends(get_db)
):
    return update_employee(db, employee_id, payload)

@router.delete("/employees/{employee_id}")
def delete_employee_route(employee_id: int, db: Session = Depends(get_db)):
    return delete_employee(db, employee_id)

@router.post("/payments/ach-debit")
def create_ach_debit(payload: ACHDebit, db: Session = Depends(get_db)):
    return create_ach_debit_payment(db, payload)

@router.post("/transactions/swipe")
def swipe_card(payload: Swipe, db: Session = Depends(get_db)):
    return swipe_debit_card(db, payload)

@router.get("/payments")
def list_payments(db: Session = Depends(get_db)):
    return db.query(OrganizationEmployeeAccountPayment).all()

@router.get("/transactions")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(OrganizationEmployeeAccountDebitCardTransaction).all()
