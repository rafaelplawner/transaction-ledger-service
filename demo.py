from decimal import Decimal
from main import Ledger

ledger = Ledger()

a = ledger.create_account("Rafael")
b = ledger.create_account("Soraya")

ledger.deposit(a.id, Decimal("100.00"))

t1 = ledger.transfer(a.id, b.id, Decimal("25.00"), idempotency_key="pay-12345678")
t2 = ledger.transfer(a.id, b.id, Decimal("25.00"), idempotency_key="pay-12345678")  # same key -> same txn

print("A balance:", ledger.get_account(a.id).balance)
print("B balance:", ledger.get_account(b.id).balance)
print("Txn1 == Txn2?", t1.id == t2.id)
print("A history:", len(ledger.account_history(a.id)))
