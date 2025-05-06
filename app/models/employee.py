from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    uid = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

class OrganizationAdministrator(Base):
    __tablename__ = "organization_administrator"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)

class OrganizationEmployee(Base):
    __tablename__ = "organization_employee"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

class OrganizationEmployeeAccount(Base):
    __tablename__ = "organization_employee_account"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    account_id = Column(String, nullable=False)
    balance_cents = Column(Integer, nullable=False)

class OrganizationEmployeeAccountDebitCard(Base):
    __tablename__ = "organization_employee_account_debit_card"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    debit_card_id = Column(String, nullable=False)

class OrganizationEmployeeAccountPayment(Base):
    __tablename__ = "organization_employee_account_payment"
    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)
    external_account_id = Column(Integer, nullable=False)
    internal_account_id = Column(Integer, ForeignKey("organization_employee_account.id"), nullable=False)
    external_payment_id = Column(String, nullable=False)
    amount_cents = Column(Integer, nullable=False)

class OrganizationEmployeeAccountDebitCardTransaction(Base):
    __tablename__ = "organization_employee_account_debit_card_transaction"
    id = Column(Integer, primary_key=True)
    debit_card_id = Column(Integer, ForeignKey("organization_employee_account_debit_card.id"), nullable=False)
    external_payment_id = Column(Integer, nullable=False)
    merchant_name = Column(String(255), nullable=False)
    amount_cents = Column(Integer, nullable=False)

