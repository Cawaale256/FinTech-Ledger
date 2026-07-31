# FinTech Ledger / Payment API 

A minimal, production‑grade financial ledger built with Python, FastAPI, and PostgreSQL.
This project is intentionally designed to train real backend engineering skills including:

Idempotency keys

Atomic database transactions

Ownership & authorization checks

Error payload design

Pagination foundations

Secure logging

Zero‑downtime migration patterns

## Overview
The FinTech Ledger is a simplified wallet + transfer system.
Users can:
- Create a wallet
- Transfer money between wallets
- View transaction history

The system guarantees transactional integrity, idempotent writes, and secure access control.

## Architecture

<img width="1215" height="743" alt="image" src="https://github.com/user-attachments/assets/70adf7b5-1440-4f1b-89a4-426c4f5e5b6d" />


Tech Stack:
- FastAPI — API framework
- PostgreSQL — relational database
- SQLAlchemy — ORM
- Alembic — migrations
- Pydantic — request/response validation
- JWT Authentication — ownership checks
- Redis (optional) — idempotency cache
