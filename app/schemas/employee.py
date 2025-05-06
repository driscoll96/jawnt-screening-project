from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    organization_id: int

class EmployeeUpdate(BaseModel):
    first_name: str
    last_name: str

class ACHDebit(BaseModel):
    internal_account_id: int
    external_account_id: int
    amount_cents: int

class Swipe(BaseModel):
    debit_card_id: str
    amount_cents: int