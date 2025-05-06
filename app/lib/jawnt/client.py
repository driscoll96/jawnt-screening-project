import time
from enum import Enum
import uuid
from random import randint

class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class PaymentResponse:
    def __init__(self, payment_id, status, amount):
        self.payment_id = payment_id
        self.status = status
        self.amount = amount

def external_call(*args, amount, **kwargs) -> PaymentResponse:
    time.sleep(2)
    return PaymentResponse(
        payment_id=uuid.uuid4(),
        status=PaymentStatus.PENDING,
        amount=amount,
    )

def long_external_call():
    time.sleep(30)

def perform_ach_debit(internal_account_id, external_account_id, amount, idempotency_key):
    return external_call(internal_account_id, external_account_id, idempotency_key, amount=amount)

def perform_ach_credit(internal_account_id, external_account_id, amount, idempotency_key):
    return external_call(internal_account_id, external_account_id, idempotency_key, amount=amount)

def perform_swipe(debit_card_id, amount, idempotency_key):
    return external_call(debit_card_id, amount=amount, idempotency_key=idempotency_key)

def get_payment_status(payment_id):
    long_external_call()
    return PaymentStatus.SUCCESS if randint(1, 2) == 1 else PaymentStatus.FAILURE

def get_swipe_status(payment_id):
    long_external_call()
    return PaymentStatus.SUCCESS if randint(1, 2) == 1 else PaymentStatus.FAILURE