from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, List
import uuid


class LedgerError(Exception):
    pass


@dataclass(frozen=True)
class Transaction:
    id: str
    type: str  # "DEPOSIT" or "TRANSFER"
    amount: Decimal
    created_at: datetime
    from_account_id: Optional[str] = None
    to_account_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    flagged: bool = False  # simple fraud signal


@dataclass
class Account:
    id: str
    owner_name: str
    currency: str = "EUR"
    balance: Decimal = Decimal("0.00")


class Ledger:
    """
    In-memory transaction system (no database yet).
    Great for learning + easy to test.
    """
    def __init__(self) -> None:
        self.accounts: Dict[str, Account] = {}
        self.transactions: List[Transaction] = []
        self._idempotency_index: Dict[str, str] = {}  # key -> txn_id

    def create_account(self, owner_name: str, currency: str = "EUR") -> Account:
        acct = Account(id=str(uuid.uuid4()), owner_name=owner_name, currency=currency)
        self.accounts[acct.id] = acct
        return acct

    def get_account(self, account_id: str) -> Account:
        acct = self.accounts.get(account_id)
        if not acct:
            raise LedgerError("Account not found")
        return acct

    def deposit(self, account_id: str, amount: Decimal) -> Transaction:
        if amount <= 0:
            raise LedgerError("Deposit amount must be positive")

        acct = self.get_account(account_id)
        acct.balance += amount

        txn = Transaction(
            id=str(uuid.uuid4()),
            type="DEPOSIT",
            amount=amount,
            created_at=datetime.utcnow(),
            to_account_id=acct.id,
        )
        self.transactions.append(txn)
        return txn

    def transfer(self, from_id: str, to_id: str, amount: Decimal, idempotency_key: str) -> Transaction:
        if amount <= 0:
            raise LedgerError("Transfer amount must be positive")
        if from_id == to_id:
            raise LedgerError("Cannot transfer to the same account")

        # Idempotency: return the original txn if the same key is reused
        if idempotency_key in self._idempotency_index:
            original_id = self._idempotency_index[idempotency_key]
            for t in self.transactions:
                if t.id == original_id:
                    return t

        from_acct = self.get_account(from_id)
        to_acct = self.get_account(to_id)

        if from_acct.currency != to_acct.currency:
            raise LedgerError("Currency mismatch")
        if from_acct.balance < amount:
            raise LedgerError("Insufficient funds")

        # Apply balances
        from_acct.balance -= amount
        to_acct.balance += amount

        flagged = amount >= Decimal("10000.00")  # simple fraud flag rule

        txn = Transaction(
            id=str(uuid.uuid4()),
            type="TRANSFER",
            amount=amount,
            created_at=datetime.utcnow(),
            from_account_id=from_id,
            to_account_id=to_id,
            idempotency_key=idempotency_key,
            flagged=flagged,
        )
        self.transactions.append(txn)
        self._idempotency_index[idempotency_key] = txn.id
        return txn

    def account_history(self, account_id: str) -> List[Transaction]:
        # Returns all transactions involving this account
        return [
            t for t in self.transactions
            if t.from_account_id == account_id or t.to_account_id == account_id
        ]
