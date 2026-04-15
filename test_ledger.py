from decimal import Decimal
import pytest
from main import Ledger, LedgerError

def test_deposit_increases_balance():
    ledger = Ledger()
    a = ledger.create_account("A")
    ledger.deposit(a.id, Decimal("50.00"))
    assert ledger.get_account(a.id).balance == Decimal("50.00")

def test_transfer_moves_money():
    ledger = Ledger()
    a = ledger.create_account("A")
    b = ledger.create_account("B")
    ledger.deposit(a.id, Decimal("100.00"))
    ledger.transfer(a.id, b.id, Decimal("25.00"), idempotency_key="k-12345678")
    assert ledger.get_account(a.id).balance == Decimal("75.00")
    assert ledger.get_account(b.id).balance == Decimal("25.00")

def test_insufficient_funds_raises():
    ledger = Ledger()
    a = ledger.create_account("A")
    b = ledger.create_account("B")
    with pytest.raises(LedgerError):
        ledger.transfer(a.id, b.id, Decimal("1.00"), idempotency_key="k-abcdefgh")

def test_idempotency_returns_same_transaction():
    ledger = Ledger()
    a = ledger.create_account("A")
    b = ledger.create_account("B")
    ledger.deposit(a.id, Decimal("100.00"))

    t1 = ledger.transfer(a.id, b.id, Decimal("10.00"), idempotency_key="idem-12345678")
    t2 = ledger.transfer(a.id, b.id, Decimal("10.00"), idempotency_key="idem-12345678")

    assert t1.id == t2.id
    # balances should only change once
    assert ledger.get_account(a.id).balance == Decimal("90.00")
    assert ledger.get_account(b.id).balance == Decimal("10.00")

def test_cannot_transfer_to_self():
    ledger = Ledger()
    a = ledger.create_account("A")
    ledger.deposit(a.id, Decimal("10.00"))
    with pytest.raises(LedgerError):
        ledger.transfer(a.id, a.id, Decimal("1.00"), idempotency_key="k-self1234")

def test_currency_mismatch_raises():
    ledger = Ledger()
    a = ledger.create_account("A", currency="EUR")
    b = ledger.create_account("B", currency="USD")
    ledger.deposit(a.id, Decimal("10.00"))
    with pytest.raises(LedgerError):
        ledger.transfer(a.id, b.id, Decimal("1.00"), idempotency_key="k-cur12345")
