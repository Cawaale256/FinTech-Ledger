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

It directly aligns with your 30‑Day Backend Study Plan and prepares you for micro1 backend interviews.

## Overview
The FinTech Ledger is a simplified wallet + transfer system.
Users can:

Create a wallet

Transfer money between wallets

View transaction history

The system guarantees transactional integrity, idempotent writes, and secure access control.

## Architecture
Tech Stack
FastAPI — API framework

PostgreSQL — relational database

SQLAlchemy — ORM

Alembic — migrations

Pydantic — request/response validation

JWT Authentication — ownership checks

Redis (optional) — idempotency cache


## Project structure
fintech-ledger/
│
├── app/
│   ├── api/
│   │   ├── accounts.py
│   │   ├── transfers.py
│   │   └── transactions.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   ├── db/
│   │   ├── session.py
│   │   ├── models.py
│   │   └── migrations/
│   │
│   ├── schemas/
│   │   ├── accounts.py
│   │   ├── transfers.py
│   │   └── transactions.py
│   │
│   └── services/
│       ├── idempotency.py
│       └── ledger.py
│
└── README.md
