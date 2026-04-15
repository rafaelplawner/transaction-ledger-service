# transaction-ledger-service
A Python transaction ledger system handling balances, transactions, and idempotent operations.

A lightweight in-memory transaction ledger system built in Python. This project simulates basic financial operations such as deposits and transfers while ensuring data consistency and idempotent transaction handling.

Features

Create and manage accounts
Process deposits and transfers
Prevent duplicate transactions using idempotency keys
Basic fraud flagging support
Simple and testable in-memory design
Unit tests included


Project Structure
.
├── main.py
├── demo.py
├── test_ledger.py

How to Run

Run the main program:
python main.py

Run the demo:
python demo.py

Run tests (if using pytest):
pytest

Design Overview

The system is built around three main components:

Transaction: Immutable record of an operation (deposit or transfer)
Account: Represents a user account with balance tracking
Ledger: Core engine that processes transactions and enforces rules

Key design decisions:
Uses Python dataclasses for structured data modeling
Ensures idempotency to prevent duplicate transaction processing
Uses an in-memory design for simplicity and ease of testing

Example Usage:
ledger = Ledger()

ledger.create_account("A1", "Alice")
ledger.create_account("A2", "Bob")

ledger.deposit("A1", Decimal("100.00"))
ledger.transfer("A1", "A2", Decimal("25.00"))

Tech Stack
Python 3
Standard Library (dataclasses, decimal, datetime)
pytest (for testing)
Future Improvements
Add persistent storage (database integration)
Build a REST API (Flask or FastAPI)
Improve concurrency handling
Extend fraud detection logic

Author
Rafael Plawner
McGill University – Honours Cognitive Science (Computer Science focus)

Purpose
This project was built to strengthen backend development fundamentals, including state management, edge case handling, and writing testable, maintainable code.
